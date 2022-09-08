#IMPORT PACKAGES
import os
from matplotlib.contour import ContourLabeler
import pandas as pd
import numpy as np
import math
import itertools

cwd = os.getcwd()+'\\'
print(cwd)

# Controlla che la workin directory in cui ti trovi sia quella in cui sono contenuti i file che devi importare
# se non fosse così devi cambiarla specificando il percorso:
# per esempio se hai creato una cartella sul desktop sarà "C:\\Users\\you_user\\\OneDrive - Eli Lilly and Company\\cartella"
# che dovrai sostituire a quello che c' è ora:

if cwd != 'C:\\Users\\l029700\\Downloads\\OneDrive_1_8-30-2022\\rep_task_kin':
    os.chdir('C:\\Users\\l029700\\Downloads\\OneDrive_1_8-30-2022\\rep_task_kin')
    cwd = os.getcwd()+'\\'

#questa è una variabile di numerazione. Non cambiarla.
var=1

# Table structures.
# Per questa tabella devi avere le seguenti colonne:
# FQ;
# FCLTY;
# OWNER;
# TABLE_NAME;
# COLUMN_NAME;
# DATA_TYPE;
# DATA_LENGTH;
# DATA_PRECISION;
# DATA_SCALE;
# COLUMN_ID

# E' importante che siano in questo ordine.
# Queste informazioni per esempio nel caso di Oracle le ottieni andando sul sorgente e facendo un select * dalla tabella all_tab_columns.

# Prenditi tutte le tabelle che sono di interesse.


df_full = pd.read_csv('Darwin_table_structure.csv',delimiter=";")


# Table count
# Per questa tabella devi avere le seguenti colonne:
# 1) Nel caso tu stia facendo su più siti:

# TABLE_NAME;
# COUNT_sito1;
# Count_sito2;
# Count_sito3;
# ...
# OWNER

# Altrimenti se lavori su un solo sito:

# TABLE_NAME;
# COUNT;
# OWNER

# Anche in questo caso è importante l'ordine.


df_count = pd.read_csv("DARWIN_count.csv",delimiter=";")


# In questo caso si eliminano le tabelle che ci interessano importare ma che hanno la count = 0 
# Devi mettere in questa lista quindi tutte le tabelle di interesse e che non presentano un count = 0:


included_table_fields = ['ANALYSIS_DETAILS',
'APPLICATION_PROPERTY',
'AUD_DETAIL',
'AUD_EVENT',
'AUD_EVENT_TYPE',
'BULLETIN',
'BULLETIN_SCOPE',
'CALC_FUNCTION',
'CHAMBER_STORAGE_LOCATION',
'CHART',
'CHART_GALLERY',
'CHART_GRID_COLUMNS',
'CHART_GROUPING_DATA',
'CHART_RESULT_DATA',
'COMMAND',
'COMMAND_PARAMETER',
'COMPLIANCE',
'COMPLIANCE_LEVEL_DETAILS',
'COMPONENT_DATA_TRANSFORM',
'COMPONENT_LIST',
'COMPONENT_SET_TYPE',
'COMPONENT_SUMMARY_CALC',
'CONTACT',
'CUSTOMER',
'EM_LOCATION',
'EM_PROGRAM',
'EM_PROGRAM_CHILDREN',
'ENTITY_DEFINITION_PAGE',
'ENTITY_DOCUMENTS',
'ENTITY_SPECIFICATION',
'ENTITY_SPEC_LEVEL',
'ENTITY_SPEC_LIMIT',
'ENTITY_SPEC_TEST_LIMIT',
'ENTITY_UPGRADE',
'EVENT_SCRIPT',
'FOLDER',
'GLOBAL_GROUP',
'GROUPS',
'HANDLING_PRECAUTION',
'ICON',
'INSPECTION_DETAIL',
'INSPECTION_TEST',
'JOB_HEADER',
'JOB_HEADER_GLOBAL_GROUP',
'LABEL_GENERIC_PROPETY',
'LABEL_TARGET_DEFINITIONS',
'LABEL_TEMPLATE',
'LIFECYCLE_SAMPLE_STATUS',
'LIFE_CYCLE_GENERAL',
'LIFE_CYCLE_HISTORY',
'LIFE_CYCLE_MASTER',
'LIFE_CYCLE_STAGE',
'LIFE_CYCLE_TRIG_EVENT_SCRIPT',
'LLY_COA_DATA_SET_VERSION',
'LLY_COA_FACILITY_ADDRESS',
'LLY_COA_FACILITY_TYPE',
'LLY_GHS_ENTRY',
'LLY_MTRL_ACLRTD_CC',
'LLY_SMARTLAB_SBMSN_ERR',
'LLY_SMARTLAB_WCMAP',
'LLY_SMARTLAB_WCMAP_CHILD',
'LOCATION',
'LOOKUP',
'LOOKUP_HEADER',
'LOOKUP_RELATION',
'LOT_DETAILS',
'LOT_DETAILS_GLOBAL_GROUP',
'LOT_DETAILS_SAMPLING_PLAN',
'LOT_DETAILS_SPEC',
'LOT_DETAILS_TEST_GROUP',
'MATERIAL',
'MATERIAL_GLOBAL_GROUP',
'MATERIAL_PACKAGING',
'MENU_REPORT_ENTITY',
'M_ENTITY_DEFINITION',
'M_ENTITY_DEFINITION_FILTER',
'M_ENTITY_DEFINITION_PROPERTY',
'M_ENTITY_GENERIC_PROPERTY',
'M_ENTITY_RELATIONSHIP',
'M_ENTITY_RELATIONSHIP_FIELDS',
'M_LOCALE',
'OBJECT_SEQ',
'OFFLINE_SCHEDULE_ITEM',
'PACKAGE_COMPONENT',
'PACKAGING',
'PACKAGING_COMPONENT',
'PASSWORD_PROFILE',
'PRIVILEGE',
'PRODUCT_MARKET_SITE',
'PRODUCT_REGIMEN_TYPE',
'QUERY',
'QUERY_CONDITION',
'QUERY_CONDITION_VALUE',
'QUERY_GROUPBY',
'QUERY_RESULT',
'QUERY_SORT',
'RELEASE_STATUS',
'REPORT_ARGUMENT',
'REPORT_DEFINITION',
'REPORT_TEMPLATE',
'RESULT',
'RESULT_AUDIT_HISTORY',
'RESULT_DATA_TRANSFORM',
'ROLE',
'ROLE_PRIVILEGE',
'SAMPLE',
'SAMPLE_GLOBAL_GROUP',
'SAMPLE_TEST_ALLOCATION',
'SAMPLING_PLAN',
'SAMPLING_PLAN_GLOBAL_GROUP',
'SAMPLING_PLAN_STAGE',
'SAMP_TMPL_HEADER',
'SCHEDULED_ITEM',
'SCHEDULED_ITEM_TYPE',
'SCHEDULEITEM_PARAMETER',
'SKD_TRIG_EVENT_SCRIPT',
'SPEC',
'SPEC_CONTROL',
'SPEC_CONTROL_TEST_ENTRY',
'SPEC_GLOBAL_GROUP',
'SPEC_LIMIT_ENTRY',
'SPEC_PACKAGING',
'SPEC_TEST',
'STB_CHAMBER_CONDITION',
'STB_PACKAGE_ORIENTATION',
'STB_PACKAGING',
'STB_STD',
'STB_STD_ORIENT_CHILD',
'STB_STD_TP_CC',
'STB_STD_TP_CC_PACK',
'STB_STD_TP_CC_PACK_ORIENT',
'STB_STT',
'STB_STUDY',
'STB_STUDY_HISTORY',
'STB_TIMEPOINT',
'STORAGE_CONDITION',
'STORAGE_REPORT_VARIABLE',
'TEMPLATE_FIELDS',
'TEST',
'TIME_ZONES',
'TRAINING_RECORDS_CONFIG',
'TREE_LIST',
'TREE_LIST_HIERARCHY',
'TREE_LIST_ITEM',
'UNIT',
'USERS',
'USER_DEFAULT_GROUPS',
'USER_GROUP',
'USER_INTERFACE',
'USER_PRIVILEGE',
'USER_ROLE',
'VERSIONED_ANALYSIS',
'VERSIONED_COMPONENT',
'VERSIONED_COMPONENT_LIMIT',
'VERSION_ANALYSIS_GLOBAL_GROUP',
'IMI_ERROR',
'IMI_INTF',
'IMI_TRANSA',
'IMI_TRANSA_LOB',
'IMS_LOV_VALUE',
'LLY_BNDRY_VAL_EXTRCTN_RUL_CNFG'
]

#questi sono i datatype che si stanno escludendo al momento
excluded_datatype_fields=['RAW','BLOB']

#si prendono solo le tabelle che ci interessano e i datatype che ci interessano
df_temp = df_full.query("TABLE_NAME in @included_table_fields")
df = df_temp.query("DATA_TYPE not in @excluded_datatype_fields")

#si crea un dataframe con tutte le colonne che si escludono a causa del datatype, con relativa tabella
#e si gruppano per facility code, in modo da non avere duplicati in caso di più siti.
df_scart = df_temp.query("DATA_TYPE in @excluded_datatype_fields").groupby('FCLTY')


# Qui si settano i nomi 
# vedere sui file txt presenti dove andrà il nome che si setta. Si capisce abbastanza bene perchè per esempio 
# <<system_UPPER>> sarà sostituito da come definisci appunto la variabile system_UPPER

system_name = 'DARWIN'
system_UPPER = 'DARWIN'
system_prefix_l = 'darwin'
system='darwin'


if len(df_scart)>0:
    fclty = list(df_scart.groups.keys())
else:
    fclty = list(df['FCLTY'].unique())
siti = ['Kinsale']

#Apertura file di testo che verrano utilizzati: 

rep_task_header = open(cwd + 'rep_task_header.txt')  # apro il file txt nel cwd
rep_task_header = list(rep_task_header)  # creo una lista
rep_task_2 = open(cwd + 'rep_task_2.txt')
rep_task_2 = list(rep_task_2)
end_rep=open(cwd + 'end_rep.txt')
end_rep = list(end_rep)
final = open(cwd + 'final.txt')
final = list(final)


conto=0
len_sottogruppo_per_sito = {}
for i in siti:
    len_sottogruppo_per_sito[i]=0

def template(lista_viste=[],lista_particular_datatype=[],select=0,viste=False,particular_datatype=False,first=True):
    """
    Nel caso non si abbiano datatype particolari o viste da gestire con particolari rep task non inserire nessun parametro.
    Nel caso invece si abbiano particolari datatype o viste da gestire le situazioni possibili sono le seguenti:

    Ipotizziamo che ci siano due viste 'VISTA1' e 'VISTA2' e i datatype particolari che si vogliono in un rep task a parte siano
    'CLOB' e 'NCLOB' e in un altra parte 'VARCHAR': la var lista_particular_datatype sarà così lista_particular_datatype=[['CLOB','NCLOB'],['VARCHAR']]

    1) template(lista_viste=['VISTA1','VISTA2'],lista_particular_datatype=[['CLOB','NCLOB'],['VARCHAR']],viste=False,particular_datatype=False,first=True)

    In questo caso otterremo i rep task senza considerare tabelle con particolari datatype e le viste più la parte iniziale (rep_task_header.txt)

    2) template(lista_viste=['VISTA1','VISTA2'],lista_particular_datatype=[['CLOB','NCLOB'],['VARCHAR']],viste=True,particular_datatype=False,first=False)

    In questo caso si otterrà il rep task solamente relativo alle viste senza la parte inziale (rep_task_header.txt)

    3) template(lista_viste=['VISTA],lista_particular_datatype=[['CLOB','NCLOB'],['VARCHAR']], select=0,viste=False,particular_datatype=True,first=False)

    In questo caso si otterrà il rep task solamente relativo alle tabelle che hanno particular datatype CLOB e NCLOB (i primi nella lista di liste
    senza la parte inziale (rep_task_header.txt)

    4) template(lista_viste=['VISTA],lista_particular_datatype=[['CLOB','NCLOB'],['VARCHAR']], select=1,viste=False,particular_datatype=True,first=False)

    In questo caso si otterrà il rep task solamente relativo alle tabelle che hanno particular datatype VARCHAR (il secondo lista di liste ) 
    senza la parte inziale (rep_task_header.txt)

    in generale quindi basterà mettere select uguale alla posizione del rep task che vogliamo creare (conteggio python parte da zero)
    """
    print(lista_viste)
    if particular_datatype:
        print('c')
        lista_particular_datatype = lista_particular_datatype[select]
        table_particular = df_full.query("DATA_TYPE in @lista_particular_datatype")['TABLE_NAME']
        data= df_count.query("TABLE_NAME in @table_particular")
    elif viste:
        print('b)')
        data = df_count.query("TABLE_NAME in @lista_viste")
    else:
        print('a')
        lista_particular_datatype = list(itertools.chain(*lista_particular_datatype))
        table_particular = df_full.query("DATA_TYPE in @lista_particular_datatype")['TABLE_NAME']
        data = df_count.query("TABLE_NAME not in @table_particular")
        data = data.query("TABLE_NAME not in @lista_viste")
    dict = {}
    for i,j in zip(data.columns[1:],siti):
        dict['df_' + j] = data[['TABLE_NAME',i,'OWNER']]
    A = 'Outputs:\n'
    with open('rep_' + system +'_'+ str(var) +'.yml', 'w') as rep_file:
        if first:
            rep_file.write('#--Start CloudFormation template\n')
            for line in rep_task_header:
                rep_file.write(line.replace('<<system_name>>', system_name))
        for k, j, site, facility_code in zip(dict, data.columns[1:-1], siti, fclty):
            dict[k] = dict[k].sort_values(j)

            # si creano poi i sottogruppi secondo la regola che in ogni rep task non ci possano
            # essere più di 49 tabelle e più di 10mln di record
            sg = []
            num = 0
            count = 0
            gruppo = 0
            for i in range(len(dict[k])):
                num+=1
                count += dict[k].iloc[i, 1]
                if count < 10000000 and num <= 49:
                    sg.append(gruppo)
                else:
                    gruppo+=1
                    sg.append(gruppo)
                    count= dict[k].iloc[i, 1]
                    num=1
            dict[k].loc[:, 'SOTTOGRUPPO'] = sg

            # si fa quindi una group by per sottogruppo
            s = dict[k].groupby('SOTTOGRUPPO')
            for i, j in zip(s.groups.keys(), range(len(s.groups.keys()))):
                table = s.get_group(i)  # avrai per ogni sottogroppo di ogni sito
                rep_file.write('\n')
                for line in rep_task_2:
                #in questo caso se si ha un vista andrà cambiato il expEdbMqDiaDmsTargetEndpoint perchè si potrò fare solo in full 
                # senza CDC. Ricorda di verificare anche nella shared dove è mappato
                    if viste:
                        rep_file.write(line.replace('<<A>>', 'A' + str(j +len_sottogruppo_per_sito[site]+ 1)).replace('<<system_prefix_l>>',
                                                                                   system_prefix_l).replace(
                        '<<system_name>>', system_name).replace('<<system_UPPER>>', system_UPPER).replace(
                        '-<<site>>', '-' + site.lower()).replace('<<site>>', site).replace('<<part>>','View'))
                    else:
                        rep_file.write(line.replace('<<A>>', 'A' + str(j +len_sottogruppo_per_sito[site]+ 1)).replace('<<system_prefix_l>>',
                                                                                   system_prefix_l).replace(
                        '<<system_name>>', system_name).replace('<<system_UPPER>>', system_UPPER).replace(
                        '-<<site>>', '-' + site.lower()).replace('<<site>>', site).replace('<<part>>',''))
                colonne_scartate = 0
                # questa ci serve per aggiornarla dopo nel caso la tabella sia in df_scart
                for i, j , OWNER in zip(table['TABLE_NAME'], range(len(table)),table['OWNER']):
                    if i != table.iloc[-1, 0]:
                        if len(df_scart)>0:# se è l'ultimo non devo mettere la virgola in fondo
                            if i not in df_scart.get_group(facility_code)['TABLE_NAME'].values:  # se la tabella ha una colonna che non importiamo a causa del datatype occorrerà fare transformation
                                rep_file.write(" " * 10 + "{\"rule-type\":\"selection\",\"rule-id\":\"" + str(
                                    j + colonne_scartate + 1) + "\",\"rule-action\":\"include\",\"rule-name\":\""
                                               + str(
                                    j + colonne_scartate + 1) + "\",\"object-locator\":{\"schema-name\":\"" + OWNER + "\",\"table-name\":\"" + i +"\"}}," '\n')
                            else:
                                rep_file.write(" " * 10 + "{\"rule-type\":\"selection\",\"rule-id\":\"" + str(
                                    j + colonne_scartate + 1) + "\",\"rule-action\":\"include\",\"rule-name\":\""
                                               + str(
                                    j + colonne_scartate + 1) + "\",\"object-locator\":{\"schema-name\":\"" + OWNER + "\",\"table-name\":\"" + i+"\"}}," '\n')
                                for h, m in zip(
                                        df_scart.get_group(facility_code)[df_scart.get_group(facility_code)['TABLE_NAME'] == i][
                                            'COLUMN_NAME'], range(1,len(df_scart.get_group(facility_code)[
                                                                          df_scart.get_group(facility_code)[
                                                                              'TABLE_NAME'] == i][
                                                                          'COLUMN_NAME'])+1)):
                                    rep_file.write(
                                        " " * 10 + "{\"rule-type\":\"transformation\",\"rule-id\":\"" +
                                        str(j +colonne_scartate +m + 1) + "\",\"rule-action\":\"remove-column\",\"rule-name\":\""
                                        + str(
                                            j + colonne_scartate + m + 1) + "\",\"rule-target\":\"column\",\"object-locator\":{\"schema-name\":\"" + OWNER + "\",\"table-name\":\"" + i +
                                        "\",\"column-name\":\"" + h +"\"}}," '\n')
                                colonne_scartate += m
                        else:
                            rep_file.write(" " * 10 + "{\"rule-type\":\"selection\",\"rule-id\":\"" + str(
                                j + colonne_scartate + 1) + "\",\"rule-action\":\"include\",\"rule-name\":\""
                                    + str(
                                j + colonne_scartate + 1) + "\",\"object-locator\":{\"schema-name\":\"" + OWNER + "\",\"table-name\":\"" + i + "\"}}," '\n')

                    else:
                        if len(df_scart) > 0:
                            if i not in df_scart.get_group(facility_code)[
                                'TABLE_NAME'].values:  # se la tabella ha una colonna che non importiamo a causa del datatype occorrerà fare transformation
                                rep_file.write(" " * 10 + "{\"rule-type\":\"selection\",\"rule-id\":\"" + str(
                                    j + colonne_scartate + 1) + "\",\"rule-action\":\"include\",\"rule-name\":\""
                                               + str(
                                    j + colonne_scartate + 1) + "\",\"object-locator\":{\"schema-name\":\"" + OWNER + "\",\"table-name\":\"" + i + "\"}}" '\n')
                            else:
                                rep_file.write(" " * 10 + "{\"rule-type\":\"selection\",\"rule-id\":\"" + str(
                                    j + colonne_scartate + 1) + "\",\"rule-action\":\"include\",\"rule-name\":\""
                                               + str(
                                    j + colonne_scartate + 1) + "\",\"object-locator\":{\"schema-name\":\"" + OWNER + "\",\"table-name\":\"" + i + "\"}}," '\n')
                                for h, m in zip(
                                        df_scart.get_group(facility_code)[df_scart.get_group(facility_code)['TABLE_NAME'] == i][
                                            'COLUMN_NAME'], range(1,len(df_scart.get_group(facility_code)[
                                                                          df_scart.get_group(facility_code)[
                                                                              'TABLE_NAME'] == i][
                                                                          'COLUMN_NAME'])+1)):
                                    if h != df_scart.get_group(facility_code)[
                                        df_scart.get_group(facility_code)['TABLE_NAME'] == i][
                                        'COLUMN_NAME'].iloc[-1]:  # diverso dall'ultimo
                                        rep_file.write(
                                            " " * 10 + "{\"rule-type\":\"transformation\",\"rule-id\":\"" +
                                            str(j +colonne_scartate+m+ 1) + "\",\"rule-action\":\"remove-column\",\"rule-name\":\""
                                            + str(
                                                j +colonne_scartate+m+ 1) + "\",\"rule-target\":\"column\",\"object-locator\":{\"schema-name\":\"" + OWNER + "\",\"table-name\":\"" + i +
                                            "\",\"column-name\":\"" + h + "\"}}" '\n')
                                    else:
                                        rep_file.write(
                                            " " * 10 + "{\"rule-type\":\"transformation\",\"rule-id\":\"" +
                                            str(j + colonne_scartate+ m + 1) + "\",\"rule-action\":\"remove-column\",\"rule-name\":\""
                                            + str(
                                                j + colonne_scartate + m + 1) + "\",\"rule-target\":\"column\",\"object-locator\":{\"schema-name\":\"" + OWNER + "\",\"table-name\":\"" + i +
                                            "\",\"column-name\":\"" + h + "\"}}," '\n')

                                colonne_scartate += m
                        else:
                            rep_file.write(" " * 10 + "{\"rule-type\":\"selection\",\"rule-id\":\"" + str(
                                j + colonne_scartate + 1) + "\",\"rule-action\":\"include\",\"rule-name\":\""
                                    + str(
                                j + colonne_scartate + 1) + "\",\"object-locator\":{\"schema-name\":\"" + OWNER + "\",\"table-name\":\"" + i + "\"}}" '\n')

                rep_file.write(" " * 10 + "]\n")
                rep_file.write(" " * 10 + "}\'\n")
                for line in end_rep:
                    rep_file.write(line)
                rep_file.write("\n")
                rep_file.write('\n')
                # si vanno ad attaccare in fondo gli output
                # rep_file.write('Outputs:\n')
            
            for k in range(len(s.groups.keys())):
                for line in final:
                    A += line.replace('<<system_UPPER>>', system_UPPER).replace('<<site>>',site).replace('<<A>>','A' + str(k+len_sottogruppo_per_sito[site] + 1))
                A+='\n'
            len_sottogruppo_per_sito[site]+=len(s.groups.keys())
        rep_file.write(
            '##---#---#---#---#---#---#---#----OUTPUTS---#---#---#---#---#---#---#---#---#---#---#\n')
        rep_file.write(A)
        #print(conto)





# basta quindi richiamare la funzione come spiegato.
# IMPORTANTE: ogni volta che si rigira la funzione con parametri diversi assicurarsi di aumentare la var di 1 altrimenti il file 
# che genererà si chiamerà esattamente come il precedente

template(lista_particular_datatype=['CLOB','NCLOB'],particular_datatype=False,first=True)
var+=1
template(lista_particular_datatype=['CLOB','NCLOB'],particular_datatype=True,first=False)
