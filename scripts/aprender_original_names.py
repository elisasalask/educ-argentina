"""Reshape aggregated subjects into original score-variable columns.

Called after build_aprender_panel.py. No student microdata are modified.
"""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'outputs/aprender-panel-2026-11-12'
data = json.loads((OUT/'tables.json').read_text())
if 'variable_puntaje' not in data['panel_provincial'][0]:
    data = json.loads((OUT/'tables_long.json').read_text())
else:
    (OUT/'tables_long.json').write_text(json.dumps(data,ensure_ascii=False))

score_names = ['lpuntaje','mpuntaje','cnpuntaje','cspuntaje','TEL','TEM','TEN','TEC']
performance_names = ['ldesemp','mdesemp','cndesemp','csdesemp','cdesemp']

def reshape(rows):
    grouped = {}
    for r in rows:
        key = tuple(r[k] for k in ['provincia_codigo','anio','nivel','grado','sector','operativo'])
        if key not in grouped:
            orig_sector = r['sector'] if r['anio']==2022 and r['nivel']=='Secundaria' else {'Estatal':'1','Privado':'2','Sin clasificar':'3'}[r['sector']]
            grouped[key] = dict(provincia=r['provincia'],anio=r['anio'],nivel=r['nivel'],grado=r['grado'],
                sector=orig_sector,sector_etiqueta=r['sector'],operativo=r['operativo'],
                cod_provincia=r['provincia_codigo'] if r['anio']<=2019 and r['provincia_codigo']!='AR' else None,
                jurisdiccion=r['provincia_codigo'] if r['anio']>=2021 else None,
                registros_grupo=r['registros_grupo'],provincia_codigo=r['provincia_codigo'],
                archivo_fuente=r['archivo_fuente'],advertencia=r['advertencia'])
        g=grouped[key]
        assert g['registros_grupo']==r['registros_grupo']
        sc,wt,perf=r['variable_puntaje'],r['variable_ponderador'],r['variable_desempeno']
        g[sc]=r['puntaje_promedio']
        g[f'n_{sc}']=r['estudiantes_puntaje']
        g[f'n_escuelas_{sc}']=r['escuelas_puntaje']
        g[f'suma_{wt}_puntaje']=r['suma_ponderadores_puntaje']
        g[f'suma_{sc}_por_{wt}']=r['suma_puntaje_ponderado']
        g[f'n_{perf}']=r['estudiantes_desempeno']
        g[f'suma_{wt}_desempeno']=r['suma_ponderadores_desempeno']
        for k in range(6):
            g[f'{perf}_{k}_prop']=r[f'proporcion_codigo_{k}']
    frame=pd.DataFrame(grouped.values())
    # Original score names first; derived fields keep explicit aggregate prefixes.
    first=['provincia','anio','nivel','grado','sector','sector_etiqueta','operativo','cod_provincia','jurisdiccion']
    present_scores=[c for c in score_names if c in frame]
    rest=[c for c in frame if c not in first+present_scores]
    frame=frame[first+present_scores+rest].sort_values(['anio','nivel','grado','provincia_codigo','sector'])
    return frame

for name in ['panel_provincial','muestra_nacional_2019','sector_sin_clasificar']:
    frame=reshape(data[name])
    frame.to_csv(OUT/f'{name}.csv',index=False,encoding='utf-8-sig',float_format='%.12g')
    frame.to_csv(ROOT/'data/processed'/f'aprender_{name}.csv',index=False,encoding='utf-8-sig',float_format='%.12g')
    data[name]=json.loads(frame.to_json(orient='records',force_ascii=False))
(OUT/'tables.json').write_text(json.dumps(data,ensure_ascii=False,allow_nan=False))
print('Original variable names:',len(data['panel_provincial']),'provincial rows')
