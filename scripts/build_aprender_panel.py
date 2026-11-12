"""Build student-weighted province/sector aggregates from all supplied Aprender CSVs.

Run from any directory with Python, pandas and numpy. Raw inputs are read only.
"""
from pathlib import Path
import json
import math
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs' / 'aprender-panel-2026-11-12'
OUT.mkdir(parents=True, exist_ok=True)
PROVINCES = dict(zip('02 06 10 14 18 22 26 30 34 38 42 46 50 54 58 62 66 70 74 78 82 86 90 94'.split(),
    ['Ciudad de Buenos Aires','Buenos Aires','Catamarca','Córdoba','Corrientes','Chaco','Chubut','Entre Ríos','Formosa','Jujuy','La Pampa','La Rioja','Mendoza','Misiones','Neuquén','Río Negro','Salta','San Juan','San Luis','Santa Cruz','Santa Fe','Santiago del Estero','Tucumán','Tierra del Fuego']))
SECTORS = {'1':'Estatal','2':'Privado','Estatal':'Estatal','Privado':'Privado'}
METHOD_URL = 'https://www.argentina.gob.ar/sites/default/files/documento_metodologico_aprender_4.pdf'

def numeric(s):
    # Spaces are missing values in 2025. Decimal commas are preserved in raw files.
    return pd.to_numeric(s.str.strip().str.replace(',', '.', regex=False), errors='coerce')

def weighted(x, w):
    return float(np.dot(x, w) / w.sum()) if len(x) and w.sum() > 0 else None

panel, national, exceptions, coverage, checks = [], [], [], [], []
for path in sorted((ROOT/'data/raw/aprender').glob('*/*Estudiantes*.csv')):
    year = int(path.parent.name)
    parts = path.stem.split('_')
    grade = next(x for x in ['2_3grado','3grado','5_6grado','6grado'] if x in path.stem)
    grade_label = {'2_3grado':'2.º/3.º año','3grado':'3.º grado','5_6grado':'5.º/6.º año','6grado':'6.º grado'}[grade]
    level = 'Primaria' if 'Primaria' in parts else 'Secundaria'
    design = parts[-1]
    headers = pd.read_csv(path, sep=';', nrows=0).columns.tolist()
    province_col = next((c for c in ['jurisdiccion','cod_provincia'] if c in headers), None)
    subjects = []
    for name, scores, weights, perf in [
        ('Lengua', ['lpuntaje','TEL'], ['lpondera','ponderL'], 'ldesemp'),
        ('Matemática', ['mpuntaje','TEM'], ['mpondera','ponderM'], 'mdesemp'),
        ('Ciencias Naturales', ['cnpuntaje','TEN'], ['cnpondera'], 'cndesemp'),
        ('Ciencias Sociales', ['cspuntaje'], ['cspondera'], 'csdesemp'),
        ('Educación Ciudadana', ['TEC'], ['cpondera'], 'cdesemp')]:
        sc = next((c for c in scores if c in headers), None)
        wt = next((c for c in weights if c in headers), None)
        if sc and wt and perf in headers:
            subjects.append((name, sc, wt, perf))
    assert subjects, path
    ids = [c for c in ['ID','seccion','idseccion','claveseccion','idalumno'] if c in headers]
    cols = list(dict.fromkeys(ids + ['sector'] + ([province_col] if province_col else []) + [c for _,s,w,d in subjects for c in [s,w,d]]))
    df = pd.read_csv(path, sep=';', usecols=cols, dtype=str, keep_default_na=False)
    for c in cols:
        df[c] = df[c].str.strip()
    duplicates = int(df.duplicated(ids).sum())
    assert duplicates == 0, f'Duplicate student key in {path.name}: {duplicates}'
    df['sector_clean'] = df['sector'].map(SECTORS).fillna('Sin clasificar')
    if province_col:
        df['province_code'] = df[province_col].str.zfill(2)
        assert df['province_code'].isin(PROVINCES).all(), path
    else:
        # Do not infer province from section prefixes: 2019 sample is not provincial.
        assert year == 2019 and design == 'Muestral', path
        df['province_code'] = 'AR'
    normalized_cols = {c: numeric(df[c]) for _,s,w,d in subjects for c in [s,w,d]}
    counts = df.groupby(['province_code','sector_clean']).size()
    unknown = int((df.sector_clean == 'Sin clasificar').sum())
    coverage.append(dict(anio=year,nivel=level,grado=grade_label,operativo=design,registros=len(df),escuelas=df.ID.nunique(),
        provincias_observadas=df.province_code.nunique() if province_col else None,sector_sin_clasificar=unknown,
        materias=', '.join(x[0] for x in subjects),archivo=path.name,
        alcance='País y sector; no representativa por provincia' if not province_col else ('Censal' if design == 'Censal' else 'Muestra; dominio provincia-sector requiere validar precisión')))
    for subject, sc, wt, perf in subjects:
        x, w, d = (normalized_cols[c] for c in [sc,wt,perf])
        assert np.isfinite(x.dropna()).all() and np.isfinite(w.dropna()).all()
        assert (w.dropna() > 0).all(), (path, wt)
        literacy = year == 2024 and grade == '3grado'
        valid_codes = list(range(6)) if literacy else [1,2,3,4]
        assert d.dropna().isin(valid_codes).all(), (path, perf)
        valid_score = x.notna() & w.gt(0)
        valid_level = d.isin(valid_codes) & w.gt(0)
        groups = [(code,sector) for code in (PROVINCES if province_col else ['AR']) for sector in ['Estatal','Privado']]
        groups += [(code,'Sin clasificar') for code in sorted(df.province_code.unique()) if (code,'Sin clasificar') in counts.index]
        rows_this = []
        for code, sector in groups:
            mask = df.province_code.eq(code) & df.sector_clean.eq(sector)
            ms, md = mask & valid_score, mask & valid_level
            n = int(mask.sum())
            xs, ws = x[ms].to_numpy(), w[ms].to_numpy()
            sum_w = float(ws.sum())
            sum_wx = float(np.dot(xs,ws))
            ld = float(w[md].sum())
            note = []
            if n == 0: note.append('Sin registros en la base suministrada')
            if design == 'Muestral': note.append('Sin errores estándar: no evaluar significación ni hacer rankings')
            if literacy: note.append('Alfabetización: escala y seis niveles propios; no comparar directamente con 2016')
            if sector == 'Sin clasificar': note.append('Código sector original fuera de 1/2; no reasignado')
            if province_col is None: note.append('Representatividad país y sector; excluida del panel provincial')
            rec = dict(provincia_codigo=code,provincia=PROVINCES.get(code,'Argentina'),anio=year,nivel=level,grado=grade_label,
                sector=sector,materia='Lectura' if literacy else subject,operativo=design,
                puntaje_promedio=weighted(xs,ws),registros_grupo=n,
                estudiantes_puntaje=int(ms.sum()),escuelas_puntaje=int(df.loc[ms,'ID'].nunique()),
                suma_ponderadores_puntaje=sum_w,suma_puntaje_ponderado=sum_wx,
                estudiantes_desempeno=int(md.sum()),escuelas_desempeno=int(df.loc[md,'ID'].nunique()),
                suma_ponderadores_desempeno=ld,
                esquema_desempeno='Alfabetización 0–5' if literacy else 'Cuatro niveles 1–4',
                **{f'proporcion_codigo_{k}':float(w[md & d.eq(k)].sum()/ld) if k in valid_codes and ld else None for k in range(6)},
                variable_puntaje=sc,variable_ponderador=wt,variable_desempeno=perf,
                comparabilidad_temporal='Requiere revisar anclaje por grado, materia y edición',
                advertencia='; '.join(note),archivo_fuente=path.name)
            assert (rec['puntaje_promedio'] is None) == (sum_w == 0)
            if sum_w: assert xs.min()-1e-9 <= rec['puntaje_promedio'] <= xs.max()+1e-9
            if ld: assert abs(sum(rec[f'proporcion_codigo_{k}'] or 0 for k in valid_codes)-1) < 1e-10
            rows_this.append(rec)
            if sector == 'Sin clasificar': exceptions.append(rec)
            elif province_col: panel.append(rec)
            else: national.append(rec)
        # Direct source totals versus totals across all output groups, including exceptions.
        assert sum(r['registros_grupo'] for r in rows_this) == len(df)
        assert sum(r['estudiantes_puntaje'] for r in rows_this) == int(valid_score.sum())
        assert math.isclose(sum(r['suma_ponderadores_puntaje'] for r in rows_this), float(w[valid_score].sum()), rel_tol=1e-12)
        assert math.isclose(sum(r['suma_puntaje_ponderado'] for r in rows_this), float(np.dot(x[valid_score],w[valid_score])), rel_tol=1e-12)
        checks.append(dict(archivo=path.name,materia=subject,registros=len(df),claves_duplicadas=duplicates,
            puntajes_validos=int(valid_score.sum()),desempenos_validos=int(valid_level.sum()),
            desempeno_sin_puntaje=int((valid_level & ~valid_score).sum()),
            puntaje_sin_desempeno=int((valid_score & ~valid_level).sum()),
            puntaje_sin_ponderador=int((x.notna() & ~w.gt(0)).sum()),
            media_nacional_incluye_sector_sin_clasificar=weighted(x[valid_score].to_numpy(),w[valid_score].to_numpy()),
            reconciliacion='Conteos, sumas ponderadas y proporciones verificados'))
    print(f'{year} {grade_label} {design}: {len(df):,} records, {len(subjects)} subjects', flush=True)

tables = {'panel_provincial':panel,'muestra_nacional_2019':national,'sector_sin_clasificar':exceptions,'cobertura':coverage,'validacion':checks}
for name, rows in tables.items():
    frame = pd.DataFrame(rows)
    if 'puntaje_promedio' in frame:
        assert not frame.duplicated(['provincia_codigo','anio','nivel','grado','sector','materia','operativo']).any()
        frame = frame.sort_values(['anio','nivel','grado','materia','provincia_codigo','sector'])
    frame.to_csv(OUT/f'{name}.csv',index=False,encoding='utf-8-sig',float_format='%.12g')
    frame.to_csv(ROOT/'data/processed'/f'aprender_{name}.csv',index=False,encoding='utf-8-sig',float_format='%.12g')
    tables[name] = json.loads(frame.to_json(orient='records',force_ascii=False))
(OUT/'tables.json').write_text(json.dumps(tables,ensure_ascii=False,allow_nan=False),encoding='utf-8')
print(json.dumps({name:len(rows) for name,rows in tables.items()}))
import runpy
runpy.run_path(str(ROOT/'scripts/aprender_original_names.py'))
