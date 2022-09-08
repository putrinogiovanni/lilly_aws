'''
Inserire nelle due liste le tabelle prese da GMDM e CAVEAU (Athena)
'''
GMDM=[
'AAPROT',
'AAVALUE',
'AAVARS',
'AAVARSBOPDATA',
'AAVARSRECIPEPARAMS',
'AAVARSSUBST',
'AAVS',
'AAVTS',
'AAVTSKANTE',
'AG2CHARGE',
'AGOUTBATCH',
'AKTION',
'ANWENDER',
'ANWENDER2ARBPL',
'ANWENDER2DOMAIN',
'ANWENDER2PROPRIETOR',
'ANWENDER2ROLLE',
'ANWENDERZONE',
'ANWENDQUALIFIKATION',
]

CAVEAU=[
'AAVALUE',
'AAVARS',
'AAVARSBOPDATA',
'AAVARSSUBST',
'AAVS',
'AAVTS',
'AAVTSKANTE',
'AG2CHARGE',
'AGOUTBATCH',
'AKTION',
'ANWENDER',
'ANWENDERZONE',
'ANWENDQUALIFIKATION',
'APLANKANTE',
'APLANKNOTEN',
'VERKETTUNG',
'VISUMDYN',
'VISUMSTAMM',
'VSKANTE',
'VSKNOTEN',
'VSKOPF',
'VTS',
'VVGRAPH',
'VVGRAPHKOPF',
'VVHISTORIE',
'VVREFERENZ',
'VVSTAMM',
'VVSTAMMGRAPH',
'VVZUSTAND',
'WAAGE',
'WAAGENTESTTERMIN',
'WAAGENTESTTYP',
'WOCHENPLAN',
'XMLEXPORTUCATTRIBUTE',
'XMLEXPORTUSECASE',
'ZBILANZ'
]


OOS = [] # questa è una lista vuota che verrà riempita con le tabelle Out Of Scope (nel caso ci fossero)

'''
Loop che prende le tabelle che sono presenti in GMDM ma che non sono state integrate su CAVEAU
'''
for i,j in enumerate(GMDM):
    if j not in CAVEAU:
        OOS.append(j)

''' Questo serve semplicemente a stampare ogni tabella in OOS '''
for i,j in enumerate(OOS):
    print(j)

print(len(OOS)) # Quante tabelle sono Out Of Scope