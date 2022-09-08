import os
import pandas as pd
import numpy as np
import math

#Settaggio parametri
#vedere i file txt per capire dove va cosa

system = 'DARWIN'
system_l = 'darwin'
key = 'darwin_laboratory_system'
siti = ['Suzhou']
syte_l = list((map(lambda x: x.lower(), siti)))

#system = 'PA'
#system_l = 'pa'
#key = 'pa_audit_process_automation_system'
#siti = ['Sesto']
#syte_l = list((map(lambda x: x.lower(), siti)))


#versione
var = '1'

#METTERE I FILE CHE SI USANO NELLO STESSO CWD DOVE SI STA LAVORANDO
#QUINDI SE SE CI CREA UNA CARTELLINA SUL DESKTOP 'C:\\Users\\Desktop\\Shared
#qua dentro vanno salvati tutti i txt e i file che vengono usati nello script
#di seguito quindi al posto di 'C:\\Users\\l025434\\PycharmProjects\\CAVEAU\\Shared\\'
#sarà da inserire 'C:\\Users\\Desktop\\Shared\\'

cwd = os.getcwd()+'\\'

if cwd != 'C:\\Users\\l025434\\OneDrive - Eli Lilly and Company\\Documents\\CAVEAU\\Generator\\Shared\\':
    os.chdir('C:\\Users\\l025434\\OneDrive - Eli Lilly and Company\\Documents\\CAVEAU\\Generator\\Shared\\')
    cwd = os.getcwd()+'\\'

print(cwd)

#leggo file

s_header = open(cwd + 'first.txt')  # apro il file txt nel cwd
s_header = list(s_header)
s_2 = open(cwd + 'second.txt')  # apro il file txt nel cwd
s_2 = list(s_2)
s_2_view = open(cwd + 'second_viste.txt')  # apro il file txt nel cwd
s_2_view = list(s_2_view)
s_3 = open(cwd + 'third.txt')  # apro il file txt nel cwd
s_3 = list(s_3)
s_4 = open(cwd + 'four.txt')  # apro il file txt nel cwd
s_4 = list(s_4)
s_4 = open(cwd + 'four.txt')  # apro il file txt nel cwd
s_4 = list(s_4)
s_5 = open(cwd + 'five.txt')  # apro il file txt nel cwd
s_5 = list(s_5)
s_5_view = open(cwd + 'five_view.txt')  # apro il file txt nel cwd
s_5_view = list(s_5_view)
s_6 = open(cwd + 'six.txt')  # apro il file txt nel cwd
s_6 = list(s_6)
s_7 = open(cwd + 'seven.txt')  # apro il file txt nel cwd
s_7 = list(s_7)
s_7_view = open(cwd + 'seven_view.txt')  # apro il file txt nel cwd
s_7_view = list(s_7_view)
final = open(cwd + 'final.txt')  # apro il file txt nel cwd
final = list(final)

#sezioni presenti nella shared

sezioni = ['SECRET MANAGER GROUPS','DMS','EVENT BRIDGE TRIGGER']

view = False
viste_siti =['Sesto','Fegersheim','IndyIpm','Suzhou']

#scrittura file yml shared_system_versione.yml pubblicato nella cartella settata

with open('shared_' + system.lower() +'_'+ var +'.yml', 'w') as shr_file:
    for line in s_header:
        shr_file.write(line.replace('<<system>>', system))
    if view:
        for site in siti:
            if site in viste_siti:
                for line in s_2_view:
                    shr_file.write(line.replace('<<system_l>>',system.lower()).replace('<<site_l>>',site.lower()))
                shr_file.write('\n')
    else:
        for site in siti:
            for line in s_2:
                shr_file.write(line.replace('<<system_l>>',system.lower()).replace('<<site_l>>',site.lower()))
            shr_file.write('\n')
    #for line in s_3:
    #    shr_file.write(line)
    #shr_file.write('\n')
    for sez in sezioni:
        shr_file.write('#############################'+ sez +'#################################################\n')
        if sez == 'SECRET MANAGER GROUPS':
            for site in siti:
                for line in s_4:
                    shr_file.write(line.replace('<<system>>', system).replace('<<site>>',site).replace('<<system_l>>',system.lower()).replace('<<site_l>>',site.lower()))
                shr_file.write('\n')
                shr_file.write('\n')
        elif sez == 'DMS':
            for site in siti:
                if view:
                    if site in viste_siti:
                        for line in s_5_view:
                            shr_file.write(
                                line.replace('<<system>>', system).replace('<<site>>', site).replace('<<system_l>>',
                                                                                                     system.lower()).
                                replace('<<site_l>>', site.lower()).replace('<<key>>', key))
                        shr_file.write('\n')
                        shr_file.write('\n')
                else:
                    for line in s_5:
                        shr_file.write(line.replace('<<system>>', system).replace('<<site>>',site).replace('<<system_l>>',system.lower()).
                                       replace('<<site_l>>',site.lower()).replace('<<key>>',key))
                    shr_file.write('\n')
                    shr_file.write('\n')
        elif sez == 'EVENT BRIDGE TRIGGER':
            for line in s_6:
                shr_file.write(line.replace('<<system>>', system).replace('<<key>>',key))
            shr_file.write('\n')
            shr_file.write('\n')
    shr_file.write('############################################################################\n')
    shr_file.write('\n')
    shr_file.write('Outputs:\n')
    for site in siti:
        if view:
            if site in viste_siti:
                for line in s_7_view:
                    shr_file.write(line.replace('<<system>>', system).replace('<<site>>', site))
                shr_file.write('\n')
        else:
            for line in s_7:
                shr_file.write(line.replace('<<system>>', system).replace('<<site>>', site))
            shr_file.write('\n')
    for line in final:
        shr_file.write(line.replace('<<system>>', system))





