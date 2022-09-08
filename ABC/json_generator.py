import os
import pandas as pd
import numpy as np
import math

#SETTA IL PERCORSO CORRETTO. iN QUESTO CASO I FILE TXT
#E IL FILE PYTHON SI TROVANO NEL PERCORSO C:\\Users\\l025434\\PycharmProjects\\CAVEAU\\ABC\\
#SPECIFICA IL PERCORSO NECESSARIO, DOVE POI TI SI SALVERà OUTPUT
cwd = os.getcwd()+'\\'

if cwd != 'C:\\Users\\l025434\\PycharmProjects\\CAVEAU\\ABC\\':
    os.chdir('C:\\Users\\l025434\\PycharmProjects\\CAVEAU\\ABC')
    cwd = os.getcwd()+'\\'

print(cwd)

#!!!!! N.B QUESTO SCRIPT VA BENE SE E SOLO SE IL SISTEMA NON è PRESENTE
# NEL FILE JSON CHE SI DOVRà AGGIORNARE.
# ( PER QA SI HA IN s3://lly-edp-codeconfig-us-east-2-qa/edb-core/aads-edb-core-abc-backend/config/qa.json) !!!!


df = pd.read_csv('Mappatura ARN_QA.csv',delimiter=";")

template = open(cwd + 'template.txt')  # apro il file txt nel cwd
template = list(template)

systems = 'MAXIMO, PMX, TRW1000, TRW138'

with open(systems+'ABC_QA.json', 'w') as json:
    for i in range(len(df)):
        for line in template:
            json.write(line.replace('<<NAME>>',df.iloc[i,-2]).replace('<<ARN>>',df.iloc[i,-1]))
        if i != len(df) - 1:
            json.write('},\n')
        else:
            json.write('}')
