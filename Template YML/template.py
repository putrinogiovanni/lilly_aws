import os
import pandas as pd
import numpy as np
import math

# Questo è il percorso in cui si sta lavorando
cwd = os.getcwd()+'\\'

#METTERE I FILE CHE SI USANO NELLO STESSO CWD DOVE SI STA LAVORANDO
#QUINDI SE SE CI CREA UNA CARTELLINA SUL DESKTOP 'C:\\Users\\Desktop\\Template YML
#qua dentro vanno salvati tutti i txt e i file che vengono usati nello script.
#Nel mio caso io ho tutto su questo percorso 'C:\\Users\\l025434\\PycharmProjects\\CAVEAU\\Template YML\\'.
#Nel caso di una cartella sul Desktop sarà da inserire 'C:\\Users\\Desktop\\Template YML\\'
if cwd != 'C:\\Users\\l025434\\PycharmProjects\\CAVEAU\\Template YML\\':
    os.chdir('C:\\Users\\l025434\\PycharmProjects\\CAVEAU\\Template YML')
    cwd = os.getcwd()+'\\'

print(cwd)

#versione. Setta una variabile per definire la versione
var = '1'

# --------------Import data from .csv file-----------#

# leggo i file da

# SELECT * from
# GMDM_STG_DEV.GMDM_STG_L2.TBSTGIPC_STRUCTURE_ALL_INST

#e salvo in csv in PA_table_structures.csv con sep = ,
#In generale se non si è in possesso di una tabella simile con tutto dentro occorerà sempre produrre
#una tabella con le seguenti colonne:
#"FQ","FCLTY","OWNER","TABLE_NAME","COLUMN_NAME","DATA_TYPE","DATA_LENGTH","DATA_PRECISION","DATA_SCALE","NULLABLE","COLUMN_ID"
#Le colonne FQ, FCLTY, NULLABLE e COLUMN_ID possono essere lasciate vuote.

#N.b se il file csv che hai prodotto ha come separatore "," lascia così altrimenti devi mettere:
#pd.read_csv('GIPC_table_structures.csv',delimiter=';') per esempio (caso in cui si abbia come del ;


df_full = pd.read_csv('GIPC_table_structures.csv')

# si mette in UPPERCASE tutti i datatype per poter poi fare la join con il dizionario DatatypeDict.csv
df_full['DATA_TYPE']= df_full['DATA_TYPE'].apply(lambda x:x.upper())

#In questa lista vanno inserite tutte le tabelle che si vogliono integrare

included_table_fields = ['IPC_BATCH'
,'IPC_DIMCARP_CALIBRATIONS'
,'IPC_DIMCARP_LIMITS'
,'IPC_DIMCARP_SAMPLES'
,'IPC_DIMCARP_SAMPLINGS'
,'IPC_DIMCARP_STATS'
,'IPC_DIMCARP_TLU_CALIBRATIONS'
,'IPC_ESIGNS'
,'IPC_EVENTS'
,'IPC_STATS_VIEW'
,'IPC_UPG_CALIBRATIONS'
,'IPC_UPG_LIMITS'
,'IPC_UPG_SAMPLES'
,'IPC_UPG_SAMPLINGS'
,'IPC_UPG_STATS'
,'IPC_ZWICK_FTL_LIMITS'
,'IPC_ZWICK_FTL_SAMPLES'
,'IPC_ZWICK_FTL_SAMPLINGS'
,'IPC_ZWICK_FTL_STATS'
,'IPC_ZWICK_PGF_LIMITS'
,'IPC_ZWICK_PGF_SAMPLES'
,'IPC_ZWICK_PGF_SAMPLINGS'
,'IPC_ZWICK_PGF_STATS'
]

#vanno settati i datatype che dovranno essere esclusi: per ora 'RAW' e 'BLOB'
excluded_datatype_fields=['RAW','BLOB']

#si filtra il dataframe tenendo solamente le tabelle e i datatype che ci interessano
df_temp = df_full.query("TABLE_NAME in @included_table_fields")
df = df_temp.query("DATA_TYPE not in @excluded_datatype_fields")

#nel caso in cui si abbiano per esempio più siti e si è presa direttamenete tutta l'estrazione avremmo
#possibili tabelle presenti in più siti e quindi ripetizioni.ù
#Si vanno a prendere tutte le tabelle una sola volta
df = df.loc[:,'TABLE_NAME':].drop_duplicates(subset=['TABLE_NAME','COLUMN_NAME'])

#si mette il nome della tabella in UPPERCASe per naming convention
df['TABLE_NAME'] = df['TABLE_NAME'].apply(lambda x:x.upper())



#-------------- Dizionario Datatype ---------------------#
#Bisogna andare ad aprire e leggere il dizionario Datatype e vedere se le mappature sono giuste
#e sufficienti per il sistema che stiamo integrando.
#Nel caso mancasse qualcosa integrare in csv, sempre mettendo il valore sotto la colonna DATA_TYPE in UPPERCASE

#leggo dizionario datatype
df_conv = pd.read_csv("DatatypeDict.csv", delimiter=";")

# faccio una join tra df e df_conv
df = df.join(df_conv.set_index('DATA_TYPE'), on='DATA_TYPE')


#--------------Conversione datatype-------------------#

double_id = np.where((df['DATA_TYPE']=='NUMBER') & (df['DATA_SCALE'].isnull()) & (df['DATA_PRECISION'].isnull()))[0]
decimal_id= np.where((df['DATA_TYPE']=='NUMBER') & (df['DATA_SCALE'].notnull()))[0]


for i in decimal_id:
    df.iloc[i,-1]='decimal('+str(int(df.iloc[i,4]))+','+str(int(df.iloc[i,5]))+')'

for j in double_id:
    df.iloc[j, -1] = 'double'

#si ordina il dataframe per nome tabella . Questa è un'operazione necessaria
df = df.sort_values(by=['TABLE_NAME'])

# converto df in una stringa
df = df.astype(str)

#--------------formattazione per ogni sorgente---------#

#GIPC
df_col = len(df.columns) - 1
df_row = len(df.index) - 1
system_name = 'global_ipc_book'
system_prefix_l = 'gipc'
system_prefix_U = 'GIPC'
system_prefix_U_location = '${pMainKeyNameGIPC}'
chiave = 'pMainKeyNameGIPC'
system='gipc'


# df_col = len(df.columns) - 1  # stampo il numero di colonne meno uno, perché? la len parte da 1
# df_row = len(df.index) - 1
# system_name = 'syncade_lifecycle_services'
# system_prefix_l = 'syncade'
# system_prefix_U = 'SYNCADE'
# system_prefix_U_location = '${pMainKeyNameSyncade}'
# chiave = 'pMainKeyNameSyncade'
# system='syncade'

########################### FILE YML RAW #######################################################

# --------------Raw Template Files-------------------#
raw_cf_header = open(cwd + 'raw_cf_header.txt')  # apro il file txt nel cwd
raw_cf_header = list(raw_cf_header)  # creo una lista
raw_table_header = open(cwd + 'raw_table_header.txt')
raw_table_header = list(raw_table_header)
raw_table_partition = open(cwd + 'raw_table_partition.txt')
raw_table_partition = list(raw_table_partition)
count = 1

# --------------Generates Raw .yml file--------------#

size=0
with open('raw_' + system +'_'+ str(var) +'.yml', 'w') as raw_file:
    raw_file.write('#--Start CloudFormation template\n')
    for line in raw_cf_header:  # estraggo step by step gli elementi della lista
        raw_file.write(line.replace('<<chiave>>',chiave))  # scrivo sul template gli elementi estratti e metto la chiave
    raw_file.write('\n')
    for i in range(0, df_row):  # itero ciclo sul numero di righe
        # Extract table name from .csv file
        table_name = df.iloc[i+1, 0] #nome tabella
        table_name_lc = table_name.lower()
        # Remove '_' from table name
        table_name_nu = table_name.replace('_', '').replace('$', '')
        if i ==0:
            raw_file.write('#--Start of table #' + str(count) + '\n')
            for line in raw_table_header:
                raw_file.write(
                    line.replace('<<TABLE_NAME>>', table_name).replace('<<TABLE_NAME_NU>>', table_name_nu).replace(
                        '<<TABLE_NAME_LC>>', table_name_lc).replace('<<TABLE_NAME_NU>>', table_name_nu).replace(
                        '<<SYSTEM_NAME>>', system_name).replace('<<SYSTEM_PREFIX_U>>', system_prefix_U).replace(
                        '<<system_prefix_U_location>>', system_prefix_U_location).replace(
                        '<<SYSTEM_PREFIX_L>>', system_prefix_l))
            raw_file.write('\n')
            raw_file.write(" "*14 + '- Name: ' + df.iloc[i, 1] + '\n') #nome colonna della tabella su cui si itera
            raw_file.write(" "*16 + 'Type: ' + df.iloc[i, -1].lower() + '\n') #newdatype
        elif i != df_row-1 and i > 0 and df.iloc[i, 0] == df.iloc[i + 1, 0]: #se non è l'ultimo e nella riga dopo c'è ancora la stessa tabella
            raw_file.write(" "*14+ '- Name: ' + df.iloc[i, 1] + '\n')
            raw_file.write(" "*16 + 'Type: ' + df.iloc[i, -1].lower() + '\n')

        elif i != df_row-1 and i > 0 and df.iloc[i, 0] != df.iloc[i + 1, 0]: #se non è l'ultimo ma nella riga dopo c'è una tabella diversa
            raw_file.write(" "*14 + '- Name: ' + df.iloc[i, 1] + '\n') #nome colonna
            raw_file.write(" "*16 + 'Type: ' + df.iloc[i, -1].lower() + '\n') #newdatype
            for line in raw_table_partition:
                raw_file.write(line)
            raw_file.write('\n#--End of table #' + str(count) + '\n\n')
            count += 1
            raw_file.write('#--Start of table #' + str(count) + '\n')
            for line in raw_table_header:
                raw_file.write(
                    line.replace('<<TABLE_NAME>>', table_name).replace('<<TABLE_NAME_LC>>', table_name_lc).replace(
                        '<<TABLE_NAME_NU>>', table_name_nu).replace('<<SYSTEM_NAME>>', system_name).replace(
                        '<<SYSTEM_PREFIX_U>>', system_prefix_U).replace(
                        '<<system_prefix_U_location>>', system_prefix_U_location).replace('<<SYSTEM_PREFIX_L>>', system_prefix_l))
            raw_file.write('\n')

        elif i == df_row-1: # se è l'ultimo
            raw_file.write(" "*14 + '- Name: ' + df.iloc[i, 1] + '\n') #nome colonna
            raw_file.write(" "*16 + 'Type: ' + df.iloc[i, -1].lower() + '\n') #newdatype
            raw_file.write(" "*14 + '- Name: ' + df.iloc[i+1, 1] + '\n') #nome colonna ultima
            raw_file.write(" "*16 + 'Type: ' + df.iloc[i+1, -1].lower() + '\n') ##newdatype ultimo
            for line in raw_table_partition:
                raw_file.write(line)
            raw_file.write('\n#--End of table #' + str(count) + '\n\n')
    raw_file.write('#--End of Raw CloudFormation template for ' + system_name + '\n\n')



###################################################################################################
########################### FILE YML REFINE #######################################################

# # --------------Refine Template Files----------------#
ref_cf_header = open(cwd + 'ref_cf_header.txt')
ref_cf_header = list(ref_cf_header)
ref_table_header = open(cwd + 'ref_table_header.txt')
ref_table_header = list(ref_table_header)
ref_table_partition = open(cwd + 'ref_table_partition.txt')
ref_table_partition = list(ref_table_partition)
count = 1

# --------------Generates Refine .yml file-----------#

with open('ref_' + system +'_'+ str(var) + '.yml', 'w') as ref_file:  # apro il template ref_file in modalità scrittura
    ref_file.write('#--Start CloudFormation template\n')
    for line in ref_cf_header:
        ref_file.write(line.replace('<<chiave>>', chiave))
    ref_file.write('\n')

    for i in range(0, df_row):
        # Extract table name from .csv file
        table_name = df.iloc[i+1, 0]
        # Make the string lower case
        table_name_lc = table_name.lower()
        # Remove '_' from table name
        table_name_nu = table_name.replace('_', '').replace('$', '')

        if i == 0:
            ref_file.write('#--Start of table #' + str(count) + '\n')
            for line in ref_table_header:
                ref_file.write(
                        line.replace('<<TABLE_NAME>>',table_name).replace('<<TABLE_NAME_NU>>', table_name_nu).replace(
                        '<<TABLE_NAME_LC>>', table_name_lc).replace('<<TABLE_NAME_NU>>', table_name_nu).replace(
                        '<<SYSTEM_NAME>>', system_name).replace('<<SYSTEM_PREFIX_U>>', system_prefix_U).replace(
                        '<<SYSTEM_PREFIX_L>>', system_prefix_l).replace(
                        '<<system_prefix_U_location>>', system_prefix_U_location))
            ref_file.write('\n')
            ref_file.write(" "*12 + '- Name: ' + df.iloc[i, 1] + '\n')
            ref_file.write(" "*14 + 'Type: ' + df.iloc[i, -1].lower() + '\n')

        #il ragionamento è lo stesso della raw, solo ora che si aggiunge all'inizio campi tecnici diversi
        #definiti nella ref_table_header.txt
        elif i != df_row-1 and i > 0 and df.iloc[i, 0] == df.iloc[i + 1, 0]:
            ref_file.write(" "*12 + '- Name: ' + df.iloc[i, 1] + '\n')
            ref_file.write(" "*14 + 'Type: ' + df.iloc[i, -1].lower() + '\n')

        elif i != df_row-1 and i > 0 and df.iloc[i, 0] != df.iloc[i + 1, 0]:
            ref_file.write(" "*12 + '- Name: ' + df.iloc[i, 1] + '\n')
            ref_file.write(" "*14 + 'Type: ' + df.iloc[i, -1].lower() + '\n')

            for line in ref_table_partition:
                ref_file.write(line)
            ref_file.write('\n#--End of table #' + str(count) + '\n\n')
            count += 1
            ref_file.write('#--Start of table #' + str(count) + '\n')
            for line in ref_table_header:
                ref_file.write(
                    line.replace('<<TABLE_NAME>>', table_name).replace('<<TABLE_NAME_NU>>', table_name_nu).replace(
                        '<<TABLE_NAME_LC>>', table_name_lc).replace('<<TABLE_NAME_NU>>', table_name_nu).replace(
                        '<<SYSTEM_NAME>>', system_name).replace('<<SYSTEM_PREFIX_U>>', system_prefix_U).replace(
                        '<<SYSTEM_PREFIX_L>>', system_prefix_l).replace(
                        '<<system_prefix_U_location>>', system_prefix_U_location))
            ref_file.write('\n')

        elif i == df_row-1:
            ref_file.write(" "*12 + '- Name: ' + df.iloc[i, 1] + '\n')
            ref_file.write(" "*14 + 'Type: ' + df.iloc[i, -1].lower() + '\n')
            ref_file.write(" "*12 + '- Name: ' + df.iloc[i+1, 1] + '\n')
            ref_file.write(" "*14 + 'Type: ' + df.iloc[i+1, -1].lower() + '\n')
            for line in ref_table_partition:
                ref_file.write(line)
            ref_file.write('\n#--End of table #' + str(count) + '\n\n')

    ref_file.write('#--End of Ref CloudFormation template for ' + system_name + '\n\n')

###################################################################################################