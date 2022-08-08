#import functions
from docx import Document
from datetime import *
import re as r
import os
import glob
import xlwt


def get_raw_tables_data (wordDoc):
    #this function get the data from the table without any adjust

    raw_data = []

    for table in wordDoc.tables:
        for row in table.rows:
            for cell in row.cells:
                raw_data.append(str(cell.text))

    raw_data = list(filter(None, raw_data))
    #print (raw_data)
    return (raw_data)

def get_tables_data (wordDoc):
    # get_tables_data extract data from the document's tables

    raw_data = []
    data = []

    for table in wordDoc.tables:
        for row in table.rows:
            for cell in row.cells:
                raw_data.append(str(cell.text))

    #print (raw_data)

    for i in range (len(raw_data)):

        if 'NOME DO PACIENTE:' in raw_data[i]:
            temp_data = raw_data[i] + raw_data[i+1]

        elif 'CONDIÇÃO DO INGRESSO:' in raw_data[i]:
            temp_data = raw_data[i] + raw_data[i+1]
            
        elif 'CONDIÇÃO DO EGRESSO:' in raw_data[i]:
            temp_data = raw_data[i] + raw_data[i+1]

        elif 'DN:' in raw_data[i]:
            temp_data = raw_data[i].replace('.', '/')

        elif 'DATA DO INGRESSO:' in raw_data[i]:
            temp_data = raw_data[i].replace('.', '/')

        elif 'DATA DA ALTA:' in raw_data[i]:
            temp_data = raw_data[i].replace('.', '/')
        
        elif 'DESLOCAMENTO:' in raw_data[i]:
            temp_data = 'DESLOCAMENTO: MANAUS'

        else:
            temp_data = raw_data[i]

        temp_data = temp_data.replace("\n", ' ').replace('  ',' ').replace('\t',' ')
        
        if ':' in temp_data:
            data.append(temp_data)

    #for i in data:
    #    print(i)
    #print(data)
    
    return (data)

def get_text (wordDoc):
    #get_text extract data from Document's texts

    fullText = []
    for para in wordDoc.paragraphs:
        fullText.append(para.text)
    new_fullText = list(filter(None, fullText))
    #return '\n'.join(new_fullText)
    #print (new_fullText)
    return (new_fullText)

def lowercase_text (fullText):
    #this function convert the text to lowercase and change latin caracters
    
    lc_fullText = []
    for i in fullText:
        lc_fullText.append(i.lower().replace('ç', 'c').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ã', 'a').replace('ê', 'e'))
        
    #print(lc_fullText)
    return (lc_fullText)

def lowercase_table (tables_data):
    #this function convert the tables content to lowercase and change latin caracters

    lc_tablesdata = []
    for i in tables_data:
        lc_tablesdata.append(i.lower().replace('ç', 'c').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ã', 'a').replace('ê', 'e'))
        
    #print(lc_tablesdata)
    return (lc_tablesdata)

def get_year (fullText):
    #get the year of the document

    new_text = lowercase_text(fullText)

    label = 'ANO: '

    for i in new_text:
        if 'manaus' in i[:10]:
            temp_year = i
            year = r.search(r"\d{4}", temp_year).group(0)
            return (label + year)

        #elif i[0].isdigit():
        #    temp_year = i
        #    year = r.search(r"\d{4}", temp_year).group(0)
        #    return (label + year)

    for i in range (len(new_text)):
        j = new_text[i].replace(' ', '')
        if 'manaus' in j[:10]:
            temp_year = j
            year = r.search(r"\d{4}", temp_year).group(0)
            return (label + year)

def get_month (fullText):
    #get the month of the document

    fullText = lowercase_text(fullText)

    month = 'MÊS: '
    for i in fullText:
        if 'manaus' in i:
            temp_month = i
            if 'janeiro' in temp_month:
                month = month + '01'
                return month
            elif 'fevereiro' in temp_month:
                month = month + '02'
                return month
            elif 'marco' in temp_month:
                month = month + '03'
                return month
            elif 'abril' in temp_month:
                month = month + '04'
                return month
            elif 'maio' in temp_month:
                month = month + '05'
                return month
            elif 'junho' in temp_month:
                month = month + '06'
                return month
            elif 'julho' in temp_month:
                month = month + '07'
                return month
            elif 'agosto' in temp_month:
                month = month + '08'
                return month
            elif 'setembro' in temp_month:
                month = month + '09'
                return month
            elif 'outubro' in temp_month:
                month = month + '10'
                return month
            elif 'novembro' in temp_month:
                month = month + '11'
                return month
            elif 'dezembro' in temp_month:
                month = month + '12'
                return month

def get_gender ():
    #this function insert a new collum in the sheet

    gender = 'SEXO: '
    return gender

def get_age (tables_data):
    #get age between birth and document date

    age_data = 'VIDADE: '

    for i in tables_data:
        if 'DN:' in i:
            born_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            if (len(born_temp)) == 0:
                indices = [i for i, s in enumerate(tables_data) if 'DN:' in s]
                tables_data.insert(indices[0]+10, age_data)
                return (tables_data)
            else:    
                born = convert_year(born_temp)
                born = datetime.strptime(born, "%d/%m/%Y").date()
        if 'DATA DO INGRESSO:' in i:
            today_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            today = convert_year(today_temp)
            today = datetime.strptime(today, "%d/%m/%Y").date()

    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    
    age_data = age_data + str(age)
    
    #indices = [i for i, s in enumerate(tables_data) if 'DN:' in s]
    #tables_data.insert(indices[0]+10, age_data)

    tables_data.append(age_data)

    return (tables_data)

def get_entrydate (tables_data, text_data):
    #this function get the correct entrydate

    #print(tables_data)
    #print(lowercase_text(text_data))

    new_text = (lowercase_text(text_data))

    new_entry = 'DATA DO INGRESSO: '

    for i in range (len(tables_data)):
        if 'DATA DO INGRESSO:' in tables_data[i]:
            start_temp = str(r.findall(r':(.*)', tables_data[i])).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            if (len(start_temp)) == 0:
                for j in new_text:
                    if j[0].isdigit():
                        #new_entry = new_entry + j[:10]
                        #new_entry = new_entry.replace('.','/')
                        entry = r.findall(r"\d{2}[./]\d{2}[./]\d{4}", j[:10])
                        if not entry:
                            entry = r.findall(r"\d{2}[./]\d{2}[./]\d{2}", j[:8])
                        new_entry = new_entry + entry[0]
                        new_entry = new_entry.replace('.','/')
                        tables_data[i] = new_entry
                        return (tables_data)

    return (tables_data)

def get_time (tables_data):
    #get time in hospital

    time_data = 'TEMPO NA CASAI: '

    for i in tables_data:
        if 'DATA DO INGRESSO:' in i:
            start_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            init = convert_year(start_temp)
            init = datetime.strptime(init, "%d/%m/%Y").date()
        if 'DATA DA ALTA:' in i:
            end_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            if not end_temp:
                indices = [i for i, s in enumerate(tables_data) if 'DATA DA ALTA:' in s]
                tables_data.insert(indices[0]+1, time_data)
                return (tables_data)
            finish = convert_year(end_temp)
            finish = datetime.strptime(finish, "%d/%m/%Y").date()

    time = finish - init

    time_data = time_data + str(time.days)
    
    indices = [i for i, s in enumerate(tables_data) if 'DATA DA ALTA:' in s]
    tables_data.insert(indices[0]+1, time_data)

    return (tables_data)

def get_destination(tables_data):
    #get destination from-to

    for i in tables_data:
        if 'DESLOCAMENTO' in i:
            origin = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
        if 'PARA' in i:
            destiny = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
    destination_data = 'DESLOCAMENTO: '
    destination_data = destination_data + origin + '-' + destiny
    
    indices = [i for i, s in enumerate(tables_data) if 'PARA:' in s]
    tables_data.insert(indices[0]+1, destination_data)

    return (tables_data)

def convert_year(date):
    #this function convert year in format YY to YYYY

    #date = date.replace('.', '/')

    #date_temp = str(r.findall(r'/(.{2}$)', date)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
    date = date.replace(' ', '').replace(';','/').replace('.', '/')
    date_temp = date.split('/')[-1]
    date_temp = int(date_temp)
    if (len(str(date_temp))) <= 2:
        if date_temp < 10:
            complete = '200'
            date_temp = str(date_temp)
            date_new = complete + date_temp
        elif date_temp < 23:
            complete = '20'
            date_temp = str(date_temp)
            date_new = complete + date_temp
        else:
            complete = '19'
            date_temp = str(date_temp)
            date_new = complete + date_temp

        date = date[:-2] + date_new
        return (date)
    return (date)

def get_companion(tables_data):
    #This function return if the pacient have companion

    companion = 'ACOMPANHANTE: '
    for i in tables_data:
        if 'ACOMPANHANT' in i:
            lc_i = i.lower()
            companion_temp = str(r.findall(r':(.*)', lc_i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            if 'acompanhante' in companion_temp:
                #companion = companion + "N"
                companion = companion + "2"
                return companion
            elif len(companion_temp) >= 5:
                #companion = companion + "S"
                companion = companion + "1"
                return companion
            elif not companion_temp:
                #companion = companion + "N"
                companion = companion + "2"
                return companion        
            else:
                #companion = companion + "N"
                companion = companion + "2"
                return companion

def get_neglecteddiseases (tables_data, text_data):
    #this function search neglected diseases in document

    neglecteddiseases = [
        'malaria',
        'doença de Chagas',
        'leishmaniose',
        'tuberculose',
        'dengue',
        'hanseniase',
        'esquistossomose',
        'oncocercose',
        'filariose',
        'tracoma',
        'helmintos',
        'nematoides de solo'
    ]

    new_text = lowercase_text(text_data)

    new_table = lowercase_table(tables_data)

    neglected = 'DOENÇA NEGLIGENCIADA: '

    for j in neglecteddiseases:
        for i in new_text:
            if j in i:
                #neglected = neglected + 'S'
                neglected = neglected + '1'
                return (neglected)
        for i in new_table:
            if j in i:
                #neglected = neglected + 'S'
                neglected = neglected + '1'
                return (neglected)
    
    #neglected = neglected + 'N'
    neglected = neglected + '2'
    return (neglected)

def get_neglecteddiseases_reason (tables_data, text_data):
    #this function search neglected diseases in document

    dict = {
        'malaria' : 'MALÁRIA',
        'doença de chagas' : 'DOENÇA DE CHAGAS',
        'leishmaniose' : 'LEISHMANIOSE',
        'tuberculose' : 'TUBERCULOSE',
        'dengue' : 'DENGUE',
        'hanseniase' : 'HANSENÍASE',
        'esquistossomose' : 'ESQUISTOSSOMOSE',
        'oncocercose' : 'ONCOCERCOSE',
        'filariose' : 'FILARIOSE',
        'tracoma' : 'TRACOMA',
        'helmintos' : 'HELMINTOS',
        'nematoides de solo' : 'NEMATÓIDES DE SOLO'
    }

    new_table = lowercase_table(tables_data)

    new_text = lowercase_text(text_data)

    #print(new_table)

    neglected_reason = 'MOTIVO NEGLIGENCIADA: '

    for i in new_table:
        for j in dict:
            if j in i:
                if neglected_reason.find(str(dict[j])) == -1 :
                    neglected_reason = neglected_reason + str(dict[j]) + '; '
    for i in new_text:
        for j in dict:
            if j in i:
                if neglected_reason.find(str(dict[j])) == -1 :
                    neglected_reason = neglected_reason + str(dict[j]) + '; '

    return neglected_reason

def get_conditionsensitive (dict, tables_data, text_data):
    #this function search disease sensitive to primary condition
    
    new_text = lowercase_text(text_data)

    new_table = lowercase_table(tables_data)

    conditionsensitive = 'DOENÇA SENSÍVEL À CONDIÇÃO PRIMÁRIA: '

    for i in new_table:
        for j in dict:
            if j in i:
                #conditionsensitive = conditionsensitive + 'S'
                conditionsensitive = conditionsensitive + '1'
                return (conditionsensitive)
    for i in new_text:
        for j in dict:
            if j in i:
                #conditionsensitive = conditionsensitive + 'S'
                conditionsensitive = conditionsensitive + '1'
                return (conditionsensitive)
    
    #conditionsensitive = conditionsensitive + 'N'
    conditionsensitive = conditionsensitive + '2'
    return (conditionsensitive)

def get_conditionsensitive_reason (dict, tables_data, text_data):

    new_table = lowercase_table(tables_data)

    new_text = lowercase_text(text_data)

    #print(new_table)

    conditionsensitive_reason = 'MOTIVO DOENÇA DE CONDIÇÃO PRIMÁRIA: '

    for i in new_table:
        for j in dict:
            if j in i:
                if conditionsensitive_reason.find(str(dict[j])) == -1 :
                    conditionsensitive_reason = conditionsensitive_reason + str(dict[j]) + '; '
    for i in new_text:
        for j in dict:
            if j in i:
                if conditionsensitive_reason.find(str(dict[j])) == -1 :
                    conditionsensitive_reason = conditionsensitive_reason + str(dict[j]) + '; '

    return conditionsensitive_reason

def get_giveup(text_data):
    #this function return if pacient give up or not

    giveup = 'DESISTÊNCIA: '

    lc_text = lowercase_text(text_data)

    for i in lc_text:
        if 'desist' in i:
            #giveup = giveup + "S"
            giveup = giveup + "1"
            return giveup

    #giveup = giveup + "N"
    giveup = giveup + "2"
    return giveup

def get_giveup_reason(text_data):
    #this function return the reason if the pacient had give up

    giveup_reason = 'MOTIVO DESIST: '

    lc_text = lowercase_text(text_data)

    for i in range (len(lc_text)):
        if 'desist' in lc_text[i]:
            giveup_reason = giveup_reason + str(text_data[i])
            return giveup_reason

    return giveup_reason

def get_internment(text_data):
    #this function return if pacient were internment or not

    internment = 'INTERNAÇÃO HOSPITALAR: '
    
    lc_text = lowercase_text(text_data)

    for i in lc_text:
        if 'interna' in i:
            #internment = internment + "S"
            internment = internment + "1"
            return internment

    #internment = internment + "N"
    internment = internment + "2"
    return internment

def get_referencedunit (dict, tables_data, text_data):
    #this function get all referenced units in document

    new_table = lowercase_table(tables_data)

    new_text = lowercase_text(text_data)

    #print(new_table)

    referencedunit = 'UNIDADE REFERENCIADA: '

    for i in new_table:
        for j in dict:
            if j in i:
                if ' ' in j:
                    if referencedunit.find(str(dict[j])) == -1 :
                        referencedunit = referencedunit + str(dict[j]) + '; '
                else:
                    new_list = i.replace('.', '').replace(',', '').split(' ')
                    for i in new_list:
                        if i in j and len(i) == len(j):
                            if referencedunit.find(str(dict[j])) == -1 :
                                referencedunit = referencedunit + str(dict[j]) + '; '
    for i in new_text:
        for j in dict:
            if j in i:
                if ' ' in j:
                    if referencedunit.find(str(dict[j])) == -1 :
                        referencedunit = referencedunit + str(dict[j]) + '; '
                else:
                    new_list = i.replace('.', '').replace(',', '').split(' ')
                    for i in new_list:
                        if i in j and len(i) == len(j):
                            if referencedunit.find(str(dict[j])) == -1 :
                                referencedunit = referencedunit + str(dict[j]) + '; '


    return referencedunit

def get_provdischarge (text_data):
    #this functions return if pacient had a provisional discharge

    provdischarge = 'ALTA PROVISÓRIA: '

    new_text = lowercase_text(text_data)

    for i in new_text:
        if 'paciente de alta provisoria para seu municipio de origem' in i:
            #provdischarge = provdischarge + "S"
            provdischarge = provdischarge + "1"
            return provdischarge
        if 'paciente segue de alta provisoria para seu municipio de origem' in i:
            #provdischarge = provdischarge + "S"
            provdischarge = provdischarge + "1"
            return provdischarge

    #provdischarge = provdischarge + "N"
    provdischarge = provdischarge + "2"
    return provdischarge

def get_problemsolved (tables_data):
    #this function return if the problem were solved

    problemsolved = 'PROBLEMA RESOLVIDO: '
    for i in tables_data:
        if 'ALTA PROVISÓRIA: N' in i:
            for i in tables_data:
                if 'DESISTÊNCIA: S' in i:
                    #problemsolved = problemsolved + 'N'
                    problemsolved = problemsolved + '2'
                if 'DESISTÊNCIA: N' in i:
                    #problemsolved = problemsolved + 'S'
                    problemsolved = problemsolved + '1'
        if 'ALTA PROVISÓRIA: S' in i:
            #problemsolved = problemsolved + 'N'
            problemsolved = problemsolved + '2'
        
    indices = [i for i, s in enumerate(tables_data) if 'ALTA PROVISÓRIA:' in s]
    tables_data.insert(indices[0]+1, problemsolved)

    return (tables_data)

def get_conditition (text_data):
    #this function return the pacient situation
    
    pacientcond = 'SITUAÇÃO DO PACIENTE: '

    #print(text_data)

    cont = []

    for i in text_data:
        if 'PENDENCIAS EM FILA DE ESPERA NO SISREG' in i:
            indice_1 = [i for i, s in enumerate(text_data) if 'PENDENCIAS EM FILA DE ESPERA NO SISREG' in s]
            cont.append(indice_1[0])
        if 'RONOGRAMA DE RETORNO CONSULTA/EXAME/CIRURGIA' in i:
            indice_2 = [i for i, s in enumerate(text_data) if 'CRONOGRAMA DE RETORNO CONSULTA/EXAME/CIRURGIA' in s]
            cont.append(indice_2[0])
        if 'TERAPIA MEDICAMENTOSA' in i:
            indice_3 = [i for i, s in enumerate(text_data) if 'TERAPIA MEDICAMENTOSA' in s]
            cont.append(indice_3[0])
        if 'CONSULTAS/EXAME/CIRURGIA' in i:
            indice_4 = [i for i, s in enumerate(text_data) if 'CONSULTAS/EXAME/CIRURGIA' in s]
            cont.append(indice_4[0])
        if 'REGISTRO DE INTERVENÇÕES' in i:
            indice_5 = [i for i, s in enumerate(text_data) if 'REGISTRO DE INTERVENÇÕES' in s]
            cont.append(indice_5[0])

    if (len(cont)) == 0:
        for i in text_data:
            if 'OBS:' in i:
                indice_extra = [i for i, s in enumerate(text_data) if 'OBS:' in s]
                cont.append(indice_extra[0]-1)

        if (len(cont)) == 0:
            for i in text_data:
                if 'RELATÓRIO DE CONTRA' in i:
                    indice_extra = [i for i, s in enumerate(text_data) if 'RELATÓRIO DE CONTRA' in s]
                    cont.append(indice_extra[0])

    indice = max(cont)

    pacientcond = pacientcond + str(text_data[indice+1:])

    return(pacientcond.replace('OBS:', 'OBS.').replace('\\t', '').replace("['",'').replace("', '", '').replace("']", '').replace('  ', ''))

def get_specialty (dict, tables_data, text_data):
    #this function get all the specialtys in document

    new_table = lowercase_table(tables_data)

    new_text = lowercase_text(text_data)

    #print(new_table)

    specialty = 'ESPECIALIDADES: '

    for i in new_table:
        for j in dict:
            if j in i:
                if specialty.find(str(dict[j])) == -1 :
                    specialty = specialty + str(dict[j]) + '; '
    for i in new_text:
        for j in dict:
            if j in i:
                if specialty.find(str(dict[j])) == -1 :
                    specialty = specialty + str(dict[j]) + '; '

    return specialty

def get_returndate (tables_data, raw_tablesdata, text_data):
    #this function get the date that the pacient must come back

    index_list = ['Data', 'Consulta', 'Médico', 'Local']

    index_lc = lowercase_text(index_list)

    tables_lc = lowercase_table(raw_tablesdata)

    index = []

    returndate = 'DATA DO RETORNO: '

    returnreason = 'MOTIVO RETORNO: '

    for i in text_data:
        if 'RONOGRAMA DE RETORNO CONSULTA' in i or 'RONOGRAMA DE RETORNO PARA CONSULTA' in i:
            for i in range(len(tables_lc)):
                #if tables_lc[i:i+len(index_lc)] == index_lc:
                    #index.append((i, i+len(index_list)))
                    #index.append((i+len(index_list)))
                #if index_lc[0] in tables_lc[i] and index_lc[1] in tables_lc[i+1] and index_lc[2] in tables_lc[i+2] and index_lc[3] in tables_lc[i+3]:
                if index_lc[0] in tables_lc[i] and index_lc[2] in tables_lc[i+2] and index_lc[3] in tables_lc[i+3]:
                    #index.append((i, i+len(index_list)))
                    index.append((i+len(index_list)))

            max_ind = max(index)

            if (len(raw_tablesdata)) > max_ind:
                date = r.findall(r"\d{2}[./]\d{2}[./]\d{4}", raw_tablesdata[max_ind])
                if not date:
                    date = r.findall(r"\d{2}[./]\d{2}[./]\d{2}", raw_tablesdata[max_ind])

                if date:
                    date = convert_year(date[0])

                if not date:
                    date.append(raw_tablesdata[max_ind])
                    date = date[0]

                date = str(date)

                returnreason = returnreason + str(raw_tablesdata[max_ind + 1])
            else:
                date = [' ']
                date = str(date)

            #date = str(date)

            returndate = returndate + date

            tables_data.append(returndate)

            tables_data.append(returnreason)

            return (tables_data)

    tables_data.append(returndate)

    tables_data.append(returnreason)

    return (tables_data)

def get_deltareturndate (tables_data):
    #get time between provisional discharge and return date

    time_data = 'TEMPO ALTA-RETORNO: '

    for i in tables_data:
        if 'DATA DA ALTA:' in i:
            start_temp = r.findall(r"\d{2}[./]\d{2}[./]\d{4}", i)
            if not start_temp:
                start_temp = r.findall(r"\d{2}[./]\d{2}[./]\d{2}", i)
            if not start_temp:
                indices = [i for i, s in enumerate(tables_data) if 'DATA DO RETORNO:' in s]
                tables_data.insert(indices[0]+1, time_data)
                return (tables_data)
            init = convert_year(start_temp[0])
            init = datetime.strptime(init, "%d/%m/%Y").date()

        if 'DATA DO RETORNO:' in i:
            end_temp = r.findall(r"\d{2}[./]\d{2}[./]\d{4}", i)
            if not end_temp:
                indices = [i for i, s in enumerate(tables_data) if 'DATA DO RETORNO:' in s]
                tables_data.insert(indices[0]+1, time_data)
                return (tables_data)
            finish = convert_year(end_temp[0])
            finish = datetime.strptime(finish, "%d/%m/%Y").date()

    time = finish - init

    time_data = time_data + str(time.days)
    
    indices = [i for i, s in enumerate(tables_data) if 'DATA DO RETORNO:' in s]
    tables_data.insert(indices[0]+1, time_data)

    return (tables_data)

def get_path(file_path):
    #get path of the project and generate a hyperlink

    path = 'CAMINHO: file:///'
    path = path + str(file_path)
    path = path.replace("\\","/")
    return (path)

def get_ethnicity(tables_data, ethnicity_dict):
    #this function apply a fix in ethniticity column

    ethnicity = 'ETNIA: '

    lc_table = lowercase_table (tables_data)

    for i in lc_table:
        for j in ethnicity_dict:
            if j in i:
                if 'etnia:' in i:
                    ethnicity = ethnicity + str(ethnicity_dict[j])
                    #indice = [i for i, s in enumerate(tables_data) if 'ETNIA:' in s]
                    #tables_data.insert(indice[0]+1, ethnicity)

                    tables_data.append(ethnicity)
                    return (tables_data)

    return (tables_data)

def get_dsei(tables_data):
    #this function apply a fix in dsei column

    dsei_dict = {
        'alto rio negro' : 'ALTO RIO NEGRO',
        'arn' : 'ALTO RIO NEGRO',
        'alto rio solimoes' : 'ALTO RIO SOLIMÕES',
        'alto solimões' : 'ALTO RIO SOLIMÕES',
        'alto solimoes' : 'ALTO RIO SOLIMÕES',
        'manaus' : 'MANAUS',
        'medio purus' : 'MÉDIO RIO PURUS',
        'medio solimoes' : 'MÉDIO RIO SOLIMÕES',
        'parintins' : 'PARINTINS',
        'vrj' : 'VALE DO JAVARI',
        'vale do javari' : 'VALE DO JAVARI',
        'arn/yan' : 'ALTO RIO NEGRO',
        'mp' : 'MÉDIO RIO PURUS',
        'ars' : 'ALTO RIO NEGRO',
        'alto rio solimões' : 'ALTO RIO SOLIMÕES',
        'mao' : 'MANAUS',
        'ms' : 'MÉDIO RIO SOLIMÕES',
        'medio rio purus' : 'MÉDIO RIO PURUS',
        'mrs' : 'MÉDIO RIO SOLIMÕES',
        'mrp' : 'MEDIO RIO PURUS',
        'medio solimões' : 'MÉDIO RIO SOLIMÕES',
        'mrsa' : 'MÉDIO RIO SOLIMÕES E AFLUENTES',
        'vj' : 'VALE DO JAVARI',
        'yanomami' : 'YANOMAMI',
        'chico camilo' : '?',
        'alto rio negro.' : 'ALTO RIO NEGRO',
        'tonantins' : 'ALTO RIO SOLIMÕES',
        'alro solimões' : 'ALTO RIO SOLIMÕES',
        'alto soli mões' : 'ALTO RIO SOLIMÕES',
        'alvaraes' : 'MÉDIO RIO SOLIMÕES',
        'autazes' : 'MANAUS',
        'rmp' : 'MÉDIO RIO PURUS',
        'medio rio solimões' : 'MÉDIO RIO SOLIMÕES',
        'medio rio solimoes' : 'MÉDIO RIO SOLIMÕES',
        'm. rio solimoes' : 'MÉDIO RIO SOLIMÕES',
        'medio rio solimôes' : 'MÉDIO RIO SOLIMÕES',
        'medio solimoes.' : 'MÉDIO RIO SOLIMÕES',
        'vale do rio javari' : 'VALE DO JAVARI',
        'v. do javari' : 'VALE DO JAVARI'
    }

    dsei = 'DSEI DE ORIGEM: '

    lc_table = lowercase_table (tables_data)

    for i in lc_table:
        for j in dsei_dict:
            if j in i:
                if 'dsei de origem:' in i:
                    dsei = dsei + str(dsei_dict[j])
                    #indice = [i for i, s in enumerate(tables_data) if 'ETNIA:' in s]
                    #tables_data.insert(indice[0]+1, dsei)

                    tables_data.append(dsei)
                    return (tables_data)

    return (tables_data)

def get_to(tables_data):
    #this function apply a fix in para column

    to_dict = {
        'sao gabriel da cachoeira' : 'São Gabriel da Cachoeira',
        'sao gabreil da cachoeira' : 'São Gabriel da Cachoeira',
        'tabatinga' : 'Tabatinga',
        'autazes' : 'Autazes',
        'rio preto da eva' : 'Rio Preto da Eva',
        'nova olinda do norte' : 'Nova Olinda do Norte',
        'borba' : 'Borba',
        'urucara' : 'Urucará',
        'labrea' : 'Lábrea',
        'tefe' : 'Tefé',
        'maues' : 'Maués',
        'barreirinha' : 'Barreirinha',
        'atalaia do norte' : 'Atalaia do Norte',
        'santa isabel do rio negro' : 'Santa Isabel do Rio Negro',
        'barcelos' : 'Barcelos',
        'sao gabriel dacachoeira' : 'São Gabriel da Cachoeira',
        'sao gabriel da cachoeiro' : 'São Gabriel da Cachoeira',
        'franciane moreira' : '?',
        'benjamin constant' : 'Benjamin Constant',
        'sao paulo de olivenca' : 'São Paulo de Olivença',
        'santo antonio do ica' : 'Santo Antônio do Içá',
        'benjamim constant' : 'Benjamin Constant',
        'tonantins' : 'Tonantins',
        'amatura' : 'Amaturá',
        's.p. de olivenca' : 'São Paulo de Olivença',
        'manacapuru' : 'Manacapuru',
        'itacoatiara' : 'Itacoatiara',
        'manicore' : 'Manicoré',
        'silves' : 'Silves',
        'anama' : 'Anama',
        'beruri' : 'Beruri',
        'com. nsra da saude' : 'Manaus',
        'pb nsra da saude' : 'Manaus',
        'manaus' : 'Manaus',
        'careiro castanho' : 'Careiro Castanho',
        'polo base nsra da saude' : 'Manaus',
        'autazez' : 'Autazes',
        'nossa senhora da saude' : 'Manaus',
        'manaus / polo base' : 'Manaus',
        'careiro da varzea' : 'Careiro da Várzea',
        'polo base nossa senhora da saude' : 'Manaus',
        'taruma acu' : 'Manaus',
        'manaquiri' : 'Manaquiri',
        'jutai' : 'Jutaí',
        'tapaua' : 'Tapauá',
        'japura' : 'Japurá',
        'eirunepe' : 'Eirunepé',
        'jurua' : 'Juruá',
        'fonte boa' : 'Fonte Boa',
        'ipixuna' : 'Ipixuna',
        'maraa' : 'Maraã',
        'parintins' : 'Parintins',
        'santo antõnio do ica' : 'Santo Antônio do Içá',
        'n.o.n' : 'Nova Olinda do Norte',
        'barreitinha' : 'Barreirinha',
        'sgc' : 'São Gabriel da Cachoeira',
        'sao gabariel da cachoeira' : 'São Gabriel da Cachoeira',
        'boa vista do ramos' : 'Boa Vista do Ramos',
        'vale do javari' : '?',
        'manaus (paricatuba)' : 'Manaus',
        'itacotiara' : 'Itacoatiara',
        'carauari' : 'Carauari',
        'atalai ado norte' : 'Atalaia do Norte',
        'tocantins' : 'Tocantins',
        'santo antônio do ica' : 'Santo Antônio do Içá',
        'parinrins' : 'Parintins',
        'nhamunda' : 'Nhamundá',
        'sao gabriel da cahoeira' : 'São Gabriel da Cachoeira',
        'santa izabel do rio negro' : 'Santa Isabel do Rio Negro',
        'sao gabriel cachoeira' : 'São Gabriel da Cachoeira',
        'sao gabriel da cacheoira' : 'São Gabriel da Cachoeira',
        's ao gabriel da cachoeira' : 'São Gabriel da Cachoeira',
        'sao gabril da cachoeira' : 'São Gabriel da Cachoeira',
        'saõ gabriel da cachoeira' : 'São Gabriel da Cachoeira',
        'tonatins' : 'Tonantins',
        'santo antonio de ica' : 'Santo Antônio do Içá',
        'beijamin constant' : 'Benjamin Constant',
        'alvaraes' : 'Alvarães',
        'benjamin constante' : 'Benjamin Constant',
        'rio reto da eva' : 'Rio Preto da Eva',
        'rio preto d eva' : 'Rio Preto da Eva',
        'autazes / pantaleao' : 'Autazes',
        'manocore' : 'Manicoré',
        'novo olinda do norte' : 'Nova Olinda do Norte',
        'carreiro castanho' : 'Careiro Castanho',
        'novo airao' : 'Novo Airão',
        'canutama' : 'Canutama',
        'itamarati' : 'Itamarati',
        'coari' : 'Coari',
        'japura-tefe' : '?',
        'uarini' : 'Uarini',
        'eurunepe' : 'Eirunepé',
        'inhamunda' : 'Nhamundá',
        '' : ''
    }

    to = 'PARA: '

    lc_table = lowercase_table (tables_data)

    for i in lc_table:
        for j in to_dict:
            if j in i:
                if 'para:' in i:
                    to = to + str(to_dict[j])
                    #indice = [i for i, s in enumerate(tables_data) if 'ETNIA:' in s]
                    #tables_data.insert(indice[0]+1, to)

                    tables_data.append(to)
                    return (tables_data)

    return (tables_data)

def get_transport(tables_data):
    #this function apply a fix in transport column

    transport_dict = {
        'fluvial' : 'fluvial',
        'ajato' : 'fluvial',
        'terrestre' : 'terrestre',
        'expresso' : 'fluvial',
        'barco com camarote/aereo ou a jato' : '?',
        'aereo' : 'aéreo',
        'aereo/fluvial.' : 'aéreo e fluvial',
        'aereo/barco(camarote)' : 'fluvial e aéreo',
        'aereo/lancha à jato' : 'fluvial e aéreo',
        'fluvial/aereo' : 'fluvial e aéreo',
        'fluvial /ajato' : 'fluvial',
        'barco' : 'fluvial',
        'rodoviario' : 'terrestre',
        'terrestre/fluvial' : 'terrestre e fluvial',
        'fluvial/terrestre' : 'fluvial e terrestre',
        'fluvial/aereo/terrestre' : 'fluvial, aéreo e terrestre',
        'terrestre/aereo/fluvial' : 'fluvial, aéreo e terrestre',
        'fluvial/aereo.' : 'fluvial e aéreo',
        'aereo, lancha a jato ou barco com camarote' : 'fluvial e aéreo',
        'f luvial/ terrestre' : 'terrestre e fluvial',
        'lancha ajato' : 'fluvial',
        'expesso' : 'fluvial',
        'via aereo' : 'aéreo',
        'expresso obs: paciente especial de colo com paralisia cerebral' : 'fluvial',
        'fluvial barco' : 'fluvial',
        'expresso obs.: paciente gravida' : 'fluvial',
        'expresso obs: paciente oncologico em tratamento' : 'fluvial',
        'fluvial/barco' : 'fluvial',
        'expresso obs: paciente gravida' : 'fluvial',
        'expresso obs.: paciente pos transplante de cornea' : 'fluvial',
        'expresso/ crianca de colo chorosa devido a patologia' : 'fluvial',
        'expresso / por conta do diagnostico de c.a' : 'fluvial',
        'expresso obs: paciente em uso de bolsa de colostomia' : 'fluvial',
        'barco de linha' : 'fluvial',
        'fluvial expresso' : 'fluvial',
        'expresso obs: crianca de colo cardiopata' : 'fluvial',
        'expresso obs: paciente idoso, pos cirurgico de amputacao de membro (cid n35)' : 'fluvial',
        'expresso paciente de colo com icc' : 'fluvial',
        'expresso obs: paciente cardiopata-especial' : 'fluvial',
        'expresso obs. com crianca de colo' : 'fluvial',
        'fluvial ou carona aerea' : '?',
        'expresso obs. paciente debilitado' : 'fluvial',
        'fluvial ou carona aereo' : 'fluvial',
        'expresso/ paciente em uso de medicacões injetaveis de 3 em 3 dias.' : 'fluvial',
        'expresso crianca realizou cirurgia' : 'fluvial',
        'expresso crianca realizou cirurgia.' : 'fluvial',
        'a criterio do dsei' : '?',
        'expresso/fluvial em leito ou aereo' : '?',
        '--' : '',
    }

    transport = 'MEIO DE TRANSPORTE: '

    lc_table = lowercase_table (tables_data)

    for i in lc_table:
        for j in transport_dict:
            if j in i:
                if 'meio de transporte:' in i:
                    transport = transport + str(transport_dict[j])
                    #indice = [i for i, s in enumerate(tables_data) if 'ETNIA:' in s]
                    #tables_data.insert(indice[0]+1, transport)

                    tables_data.append(transport)
                    return (tables_data)

    return (tables_data)

def get_dataintext (argument):
    #this function get the names of ethnicity
    abs_path = os.path.abspath(os.curdir)

    files = glob.glob(abs_path + '/**/*.docx', recursive=True)

    ethnicity = argument.upper() + ':'

    f = open(argument.replace(' ', '_') + ".txt","w+")

    issues = 0
    invalid = 0

    argument = argument + ':'

    for file_path in range (len(files)):

        temp = files[file_path].split('\\')[-1]
    
        if '~$' in temp[:2]:
            issues = issues + 1
        if '$~' in temp[:2]:
            invalid = invalid + 1
        else:
            wordDoc = Document(files[file_path])
            #print(files[file_path])
            tables_data = get_tables_data(wordDoc)

            tables_data = lowercase_table(tables_data)
            
            for i in tables_data:
                if argument in i:
                        ethnicity_temp = str(r.findall(r':(.*)', i))
                        ethnicity_temp = ethnicity_temp.replace("[' ", "").replace("['", "").replace(" ']", "").replace("']", "")

                        if ethnicity.find(ethnicity_temp) == -1 :
                            ethnicity = ethnicity + ethnicity_temp + ';'

                            print(ethnicity_temp)
    
    
    ethnicity = ethnicity.replace(';', "' : ''\r")

    f.write ('%s' %ethnicity)

def get_dataintext_adult (argument):
    #this function get the names of ethnicity
    abs_path = os.path.abspath(os.curdir)

    files = glob.glob(abs_path + '/**/*.docx', recursive=True)

    ethnicity = argument.upper() + ':'

    f = open(argument.replace(' ', '_') + ".txt","w+")

    issues = 0
    invalid = 0

    argument = argument + ':'

    for file_path in range (len(files)):

        temp = files[file_path].split('\\')[-1]
    
        if '~$' in temp[:2]:
            issues = issues + 1
        if '$~' in temp[:2]:
            invalid = invalid + 1
        else:
            wordDoc = Document(files[file_path])
            #print(files[file_path])
            tables_data = get_tables_data(wordDoc)

            text_data = get_text(wordDoc)

            raw_tables_data = get_raw_tables_data (wordDoc)

            tables_data = get_entrydate(tables_data, text_data)

            tables_data = get_age(tables_data)

            tables_data.append(get_servicereceived (tables_data, raw_tables_data, text_data))

            tables_data = lowercase_table(tables_data)
            
            for j in tables_data:
                if 'vidade:' in j:
                    age_temp = (r.findall(r':(.*)', j))
                    age_temp = age_temp[0].replace(' ', '')
                    if age_temp:
                        age_temp = int(age_temp)
                    if isinstance(age_temp, int):
                        if age_temp >= 18:
                            for i in tables_data:
                                if argument in i:
                                    ethnicity_temp = str(r.findall(r':(.*)', i))
                                    ethnicity_temp = ethnicity_temp.replace("[' ", "").replace("['", "").replace(" ']", "").replace("']", "")

                                    if ethnicity.find(ethnicity_temp) == -1 :
                                        ethnicity = ethnicity + ethnicity_temp + ';'

                                        print(ethnicity_temp)
    
    
    ethnicity = ethnicity.replace(';', "' : ''\r")

    f.write ('%s' %ethnicity)

def get_servicereceived (tables_data, raw_tables_data, text_data, dict) :
    #get all the services received during the internment

    index_lc = ['data', 'consulta', 'medico', 'local']

    index_lc_ = ['data', 'exames realizados', 'local']

    endindex_lc = ['data', 'medicamento', 'tratamento']

    tables_lc = lowercase_table(raw_tables_data)

    end_index = [len(tables_lc)]

    index = []

    examlist = 'ATENDIMENTO RECEBIDO: '

    examlist_new = 'ATENDIMENTOS RECEBIDOS: '

    for i in tables_data:
        if 'DATA DA ALTA:' in i:
            finish = ''
            end_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            if not end_temp:
                break
            finish = convert_year(end_temp)
            finish = datetime.strptime(finish, "%d/%m/%Y").date()

            break

    for j in text_data:
        if 'REGISTRO DE INTERVEN' in j:
            for i in range(len(tables_lc)):
                if index_lc_[0] in tables_lc[i] and index_lc_[1] in tables_lc[i+1] and index_lc_[2] in tables_lc[i+2]:
                    index.append((i+len(index_lc_)))

        if 'CONSULTAS/EXAME/CIRURGIA' in j:
            for i in range(len(tables_lc)):
                if index_lc[0] in tables_lc[i] and index_lc[2] in tables_lc[i+2] and index_lc[3] in tables_lc[i+3]:
                    index.append((i+len(index_lc)))

    for i in range(len(tables_lc)):
        if endindex_lc[0] in tables_lc[i] and endindex_lc[1] in tables_lc[i+1] and endindex_lc[2] in tables_lc[i+2]:
            end_index.append(i)
        if 'protocolo' in tables_lc[i]:
            end_index.append(i)

    if not index:
        index = [len(tables_lc)]
        min_ind = min(index)
    else:
        min_ind = min(index)

    max_ind = min(end_index)

    examslist_temp = tables_lc[min_ind:max_ind]

    for i in range (len(examslist_temp)):
        date_temp = examslist_temp[i]
        if date_temp[:2].isdigit():
            date_new = r.findall(r"\d{2}[./]\d{2}[./]\d{4}", date_temp)
            if not date_new:
                date_new = r.findall(r"\d{2}[./]\d{2}[./]\d{2}", date_temp)
            if not date_new:
                continue
            exam_date = convert_year(date_new[0])
            exam_date = datetime.strptime(exam_date, "%d/%m/%Y").date()

            if not finish:
                break

            if finish > exam_date:
                if not 'ista' in examslist_temp[i+1]:
                    #print(examslist_temp[i+1])

                    if examlist.find(examslist_temp[i+1]):
                        examlist = examlist + str(examslist_temp[i+1]).replace('\t', '') + '; '
                for j in dict:
                    if j in examslist_temp[i+1]:
                        if examlist_new.find(str(dict[j])) == -1 :
                            examlist_new = examlist_new + str(dict[j]) + '; '
    
    tables_data.append(examlist_new)

    tables_data.append(examlist)

    return (tables_data)

def get_examsperformed (argument):
    #this function get the exams performed during the interment

    abs_path = os.path.abspath(os.curdir)

    files = glob.glob(abs_path + '/**/*.docx', recursive=True)

    examlist = argument.upper() + ': '

    f = open(argument.replace(' ', '_') + ".txt","w+")

    issues = 0
    invalid = 0

    for file_path in range (len(files)):

        temp = files[file_path].split('\\')[-1]
    
        if '~$' in temp[:2]:
            issues = issues + 1
        if '$~' in temp[:2]:
            invalid = invalid + 1
        else:
            wordDoc = Document(files[file_path])
            #print(files[file_path])

            tables_data = get_tables_data(wordDoc)

            raw_tables_data = get_raw_tables_data (wordDoc)

            text_data = get_text(wordDoc)

            #column_number: 1 - consulta, 2 - medico, 3 - local

            index_lc = ['data', 'consulta', 'medico', 'local']

            index_lc_ = ['data', 'exames realizados', 'local']

            endindex_lc = ['data', 'medicamento', 'tratamento']

            tables_lc = lowercase_table(raw_tables_data)

            #text_lc = lowercase_text(text_data)

            index = []

            end_index = [len(tables_lc)]

            for i in tables_data:
                if 'DATA DA ALTA:' in i:
                    end_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
                    if not end_temp:
                        break
                    finish = convert_year(end_temp)
                    finish = datetime.strptime(finish, "%d/%m/%Y").date()

                    break

            for j in text_data:
                if 'REGISTRO DE INTERVEN' in j:
                    for i in range(len(tables_lc)):
                        if index_lc_[0] in tables_lc[i] and index_lc_[1] in tables_lc[i+1] and index_lc_[2] in tables_lc[i+2]:
                            index.append((i+len(index_lc_)))

                if 'CONSULTAS/EXAME/CIRURGIA' in j:
                    for i in range(len(tables_lc)):
                        if index_lc[0] in tables_lc[i] and index_lc[2] in tables_lc[i+2] and index_lc[3] in tables_lc[i+3]:
                            index.append((i+len(index_lc)))

            for i in range(len(tables_lc)):
                if endindex_lc[0] in tables_lc[i] and endindex_lc[1] in tables_lc[i+1] and endindex_lc[2] in tables_lc[i+2]:
                    end_index.append(i)
                if 'protocolo' in tables_lc[i]:
                    end_index.append(i)

            if not index:
                index = [len(tables_lc)]
                min_ind = min(index)
            else:
                min_ind = min(index)

            max_ind = min(end_index)

            examslist_temp = tables_lc[min_ind:max_ind]

            for i in range (len(examslist_temp)):
                date_temp = examslist_temp[i]
                if date_temp[:2].isdigit():
                    date_new = r.findall(r"\d{2}[./]\d{2}[./]\d{4}", date_temp)
                    if not date_new:
                        date_new = r.findall(r"\d{2}[./]\d{2}[./]\d{2}", date_temp)
                    if not date_new:
                        continue
                    exam_date = convert_year(date_new[0])
                    exam_date = datetime.strptime(exam_date, "%d/%m/%Y").date()

                    if not finish:
                        break

                    if finish > exam_date:
                        if not 'ista' in examslist_temp:
                            #print(examslist_temp)

                            for i in range (len(examslist_temp)):
                                if not '18' in examslist_temp[i] and not '19' in examslist_temp[i] and not '20' in examslist_temp[i] and not '21' in examslist_temp[i] and not '17' in examslist_temp[i]:
                                    if examlist.find(str(examslist_temp[i])) == -1 :
                                        print(examslist_temp[i])
                                        examlist = examlist + str(examslist_temp[i]) + ';'

    examlist = examlist.replace(';', "' : ''\r")

    f.write ('%s' %examlist)

def get_outputlog (list, issues, invalid, valid):
    #create a log the projet's root with a short resume of document's status

    f= open("output_log.txt","w+")

    f.write ('**********************************************************\r')
    f.write ('\nvalid files: (%d file(s))\n\r' %valid)

    f.write ('**********************************************************\r')
    f.write ('\nlist of corrupted files: (%d file(s))\n\r' %issues)

    for i in range (len(list)):
        if '~$' in list[i]:
            f.write ("%s\r" % list[i])

    f.write ('\n**********************************************************\r')
    f.write ('\nlist of invalid files: (%d file(s))\n\r' %invalid)

    for i in range (len(list)):
        if '$~' in list[i]:
            f.write ("%s\r" % list[i])

    f.close()

def organizer (tables_data):
    #organize the colluns

    #print(tables_data)

    new_table = ['s'] * 37
    
    for i in tables_data:
        if 'ANO:' in i:
            new_table[0] = i
        elif 'MÊS:' in i:
            new_table[1] = i
        elif 'DSEI DE ORIGEM:' in i:
            new_table[2] = i
        elif 'SEXO:' in i:
            new_table[3] = i
        elif 'NOME DO PACIENTE:' in i:
            new_table[4] = i
        elif 'DN:' in i:
            new_table[5] = i
        elif 'IDADE:' in i:
            new_table[6] = i
        if 'COMUNIDADE:' in i:
            new_table[7] = i
        elif 'ETNIA:' in i:
            new_table[8] = i
        elif 'DATA DO INGRESSO:' in i:
            new_table[9] = i
        elif 'DATA DA ALTA:' in i:
            new_table[10] = i
        elif 'TEMPO NA CASAI:' in i:
            new_table[11] = i
        elif 'DATA DO RETORNO:' in i:
            new_table[12] = i
        elif 'TEMPO ALTA-RETORNO:' in i:
            new_table[13] = i
        elif 'MOTIVO RETORNO:' in i:
            new_table[14] = i
        elif 'HD:' in i:
            new_table[15] = i
        elif 'ESPECIALIDADES:' in i:
            new_table[16] = i
        elif 'CONDIÇÃO DO INGRESSO:' in i:
            new_table[17] = i
        elif 'CONDIÇÃO DO EGRESSO:' in i:
            new_table[18] = i
        elif 'INTERNAÇÃO HOSPITALAR:' in i:
            new_table[19] = i
        elif 'ATENDIMENTOS RECEBIDOS:' in i:
            new_table[20] = i
        elif 'ATENDIMENTO RECEBIDO:' in i:
            new_table[21] = i
        elif 'UNIDADE REFERENCIADA:' in i:
            new_table[22] = i
        elif 'DESLOCAMENTO:' in i:
            new_table[23] = i
        elif 'PARA:' in i:
            new_table[24] = i
        elif 'MEIO DE TRANSPORTE:' in i:
            new_table[25] = i
        elif 'ACOMPANHANTE:' in i:
            new_table[26] = i
        elif 'ALTA PROVISÓRIA:' in i:
            new_table[27] = i
        elif 'DOENÇA NEGLIGENCIADA:' in i:
            new_table[28] = i
        elif 'MOTIVO NEGLIGENCIADA:' in i:
            new_table[29] = i
        elif 'DOENÇA SENSÍVEL' in i:
            new_table[30] = i
        elif 'MOTIVO DOENÇA DE CONDI' in i:
            new_table[31] = i
        elif 'SITUAÇÃO DO PACIENTE:' in i:
            new_table[32] = i
        elif 'PROBLEMA RESOLVIDO:' in i:
            new_table[33] = i
        elif 'DESISTÊNCIA:' in i:
            new_table[34] = i
        if 'MOTIVO DESIST:' in i:
            new_table[35] = i
        elif 'CAMINHO:' in i:
            new_table[36] = i
    return new_table

def get_data (wordDoc, ethnicity_dict, spec_dict, sensitive_dict, servicereceived_dict, hospital_dict , file_path):
    #generate tables_data
    
    tables_data = get_tables_data(wordDoc)

    raw_tables_data = get_raw_tables_data (wordDoc)

    text_data = get_text(wordDoc)

    tables_data.insert(0, get_year(text_data))

    tables_data.insert(1, get_month(text_data))

    tables_data.insert(2, get_gender())

    tables_data = get_entrydate(tables_data, text_data)

    tables_data = get_ethnicity(tables_data, ethnicity_dict)

    tables_data = get_dsei(tables_data)

    tables_data = get_to(tables_data)

    tables_data = get_transport(tables_data)

    tables_data = get_age(tables_data)

    tables_data = get_time(tables_data)

    tables_data.append(get_specialty(spec_dict, raw_tables_data, text_data))

    tables_data.append(get_companion(tables_data))

    tables_data.append(get_provdischarge(text_data))

    tables_data.append(get_giveup(text_data))

    tables_data.append(get_giveup_reason(text_data))

    tables_data = get_problemsolved(tables_data)

    tables_data.append(get_neglecteddiseases(tables_data, text_data))

    tables_data.append(get_neglecteddiseases_reason(tables_data, text_data))

    tables_data.append(get_conditionsensitive(sensitive_dict, tables_data, text_data))

    tables_data.append(get_conditionsensitive_reason(sensitive_dict, tables_data, text_data))

    tables_data.append(get_conditition(text_data))

    tables_data.append(get_internment(text_data))

    tables_data = get_servicereceived (tables_data, raw_tables_data, text_data, servicereceived_dict)

    tables_data.append(get_referencedunit(hospital_dict, tables_data, text_data))

    tables_data = get_returndate(tables_data, raw_tables_data, text_data)

    tables_data = get_deltareturndate(tables_data)

    tables_data.append(get_path(file_path))

    new_table = organizer(tables_data)

    return new_table

def run_automation():
    #run the automation tool
    abs_path = os.path.abspath(os.curdir)

    files = glob.glob(abs_path + '/**/*.docx', recursive=True)

    bad_files = glob.glob(abs_path + '/**/*.doc', recursive=True)

    issues = 0
    valid = 0
    invalid = 0

    book = xlwt.Workbook(encoding="utf-8")

    sheet1 = book.add_sheet("Sheet 1")

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True
    style.font = font

    specs = []
    infos = []

    #all_tables_data = [[0]*(len(files))]*26
    for file_path in range (len(files)):

        temp = files[file_path].split('\\')[-1]
    
        if '~$' in temp[:2]:
            issues = issues + 1
        if '$~' in temp[:2]:
            invalid = invalid + 1

        else:
            wordDoc = Document(files[file_path])
            #print(files[file_path])
            tables_data = get_data(wordDoc, ethnicity_dict, specialist_dict, conditionsensitive_dict, servicereceived_dict, hospital_dict, files[file_path])

            for j in tables_data:
                specs_temp = str(r.findall(r'(.*):', j)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
                infos_temp = str(r.findall(r':(.*)', j)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
                specs.append(specs_temp)
                infos.append(infos_temp)

            for j in range (len(tables_data)):
                if valid == 0:
                    sheet1.write(0, j, specs[j], style=style)
                    sheet1.write((valid+1), j, infos[j])
                else:
                    sheet1.write((valid+1), j, infos[j])

            del specs[:]
            del infos[:]

            valid = valid + 1
            
            os.system('cls')

            print('%d of ' %valid, (len(files)))
            #for columns in range (len(tables_data)):
            #    all_tables_data[file_path][columns] = tables_data[columns]

    for file_path in range (len(bad_files)):
        temp = bad_files[file_path].split('\\')[-1]
        if '~$' in temp[:2]:
            issues = issues + 1
        if '$~' in temp[:2]:
            invalid = invalid + 1

    sheet1.col(0).width = 1400
    sheet1.col(1).width = 1400
    sheet1.col(2).width = 5000
    sheet1.col(3).width = 1400
    sheet1.col(4).width = 7000
    sheet1.col(5).width = 2600
    sheet1.col(6).width = 2000
    sheet1.col(7).width = 5000
    sheet1.col(8).width = 4000
    sheet1.col(9).width = 2600
    sheet1.col(10).width = 2600
    sheet1.col(11).width = 4000
    sheet1.col(12).width = 4000

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")

    book.save("output_" + dt_string + ".xls")
    
    list = []
    list = files
    list.extend(bad_files)

    get_outputlog(list, issues, invalid, valid)

    #book.save("test.xls")

    print ('\n**********************************************************')
    print ('There is %d corrupted files!' %issues)
    print ('There is %d invalid files!' %invalid)
    print ('There is a total of %d valid files!' %valid)
    print ('**********************************************************')

    return (0)

def create_sheet (data):
    #this function create a sheet
    
    book = xlwt.Workbook(encoding="utf-8")

    sheet1 = book.add_sheet("Sheet 1")

    specs = []
    infos = []

    for i in data:
        specs_temp = str(r.findall(r'(.*):', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
        infos_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
        specs.append(specs_temp)
        infos.append(infos_temp)

    for i in range (len(data)):
        sheet1.write(0, i, specs[i])
        sheet1.write(1, i, infos[i])

    book.save("test.xls")



#there's some dicts that are used

specialist_dict = {
        'acupuntu' : 'ACUPUNTURISTA',
        'alergia e imunologia' : 'ALERGIA E IMUNOLOGIA',
        'aneste' : 'ANESTESIOLOGIA',
        'angiologia' : 'ANGIOLOGIA',
        'cardiol' : 'CARDIOLOGISTA',
        'cirurgia cardiovascular' : 'CIRURGIA CARDIOVASCULAR',
        'cardiovascular' : 'CIRURGIA CARDIOVASCULAR',
        'cirurgia da mao' : 'CIRURGIA DA MÃO',
        'cirurgiao de cabeca e pescoco' : 'CIRURGIÃO DE CABEÇA E PESCOÇO',
        'cirurgia de cabeca e pescoco' : 'CIRURGIÃO DE CABEÇA E PESCOÇO',
        'cirurgiao cabeca e pescoco' : 'CIRURGIÃO DE CABEÇA E PESCOÇO',
        'cirurgia cabeca e pescoco' : 'CIRURGIÃO DE CABEÇA E PESCOÇO',
        'cirurgia do aparelho digestivo' : 'CIRURGIA DO APARELHO DIGESTIVO',
        'cirurgia geral' : 'CIRURGIA GERAL',
        'cirurgia oncologica' : 'CIRURGIA ONCOLÓGICA',
        'cirurgia pediatrica' : 'CIRURGIA PEDIÁTRICA',
        'cirurgiao pediatri' : 'CIRURGIA PEDIÁTRICA',
        'cirurgiao plastico' : 'CIRURGIÃO PLÁSTICO',
        'cirurgia plastica' : 'CIRURGIÃO PLÁSTICO',
        'cirurgia torácica' : 'CIRURGIA TORÁCICA',
        'cirurgia vascular' : 'CIRURGIA VASCULAR',
        'clinica medica' : 'CLÍNICO',
        'clinico' : 'CLÍNICO',
        'coloproctologia' : 'COLOPROCTOLOGIA ',
        'dermato' : 'DERMATOLOGISTA',
        'endocrino' : 'ENDÓCRINOLOGISTA',
        'endoscopia' : 'ENDOSCOPIA',
        'gastro' : 'GASTROENTEROLOGIA',
        'genetica medica' : 'GENÉTICA MÉDICA',
        'geriatria' : 'GERIATRIA',
        'ginecologi' : 'GINECOLOGIA E OBSTETRÍCIA',
        'hematologi' : 'HEMATOLOGISTA',
        'hemotera' : 'HEMATOLOGISTA',
        'hepat' : 'HEPATOLOGISTA',
        'homeopat' : 'HOMEOPATA',
        'infecto' : 'INFECTOLOGISTA',
        'mastolo' : 'MASTOLOGISTA',
        'medicina de emergencia' : 'MEDICINA DE EMERGÊNCIA',
        'medicina de familia' : 'MEDICINA DE FAMÍLIA',
        'medicina do trabalho' : 'MEDICINA DO TRABALHO',
        'medicina de trafego' : 'MEDICINA DE TRÁFEGO',
        'medicina esportiva' : 'MEDICINA ESPORTIVA',
        'medicina fisica e reabilitacao' : 'MEDICINA FÍSICA E REABILITAÇÃO',
        'medicina intensiva' : 'MEDICINA INTENSIVA',
        'medicina legal e pericia medica' : 'MEDICINA LEGAL E PERÍCIA MÉDICA',
        'medicina nuclear' : 'MEDICINA NUCLEAR',
        'medicina preventiva' : 'MÉDICO DE FAMÍLIA',
        'nefrolog' : 'NEFROLOGISTA',
        'neurocirurg' : 'NEUROLOGISTA',
        'neurol' : 'NEUROLOGISTA',
        'nutrologia' : 'NUTROLOGIA',
        'oftalmo' : 'OFTALMOLOGISTA',
        'oncol' : 'ONCOLOGISTA',
        'ortoped' : 'ORTOPEDISTA',
        'otorrino' : 'OTORRINOLARINGOLOGIA',
        'patolog' : 'PATOLOGIA',
        'obstetr' : 'OBSTETRA',
        'patologia clínica/medicina laboratorial' : 'PATOLOGIA CLÍNICA/MEDICINA LABORATORIAL',
        'pediatr' : 'PEDIATRIA',
        'pneumolog' : 'PNEUMOLOGISTA',
        'psiquiat' : 'PSIQUIATRIA',
        'radiolog' : 'RADIOLOGIA E DIAGNÓSTICO POR IMAGEM',
        'radioterapia' : 'RADIOTERAPIA',
        'reumatolo' : 'REUMATOLOGISTA ',
        'urolog' : 'UROLOGISTA',
    }

neglecteddiseases_dict = {
    'malaria' : 'MALÁRIA',
    'doença de Chagas' : 'DOENÇA DE CHAGAS',
    'leishmaniose' : 'LEISHMANIOSE',
    'tuberculose' : 'TUBERCULOSE',
    'dengue' : 'DENGUE',
    'hanseniase' : 'HANSENÍASE',
    'esquistossomose' : 'ESQUISTOSSOMOSE',
    'oncocercose' : 'ONCOCERCOSE',
    'filariose' : 'FILARIOSE',
    'tracoma' : 'TRACOMA',
    'helmintos' : 'HELMINTOS',
    'nematoides de solo' : 'NEMATÓIDES DE SOLO'
}

conditionsensitive_dict = {

    'coqueluche' : 'COQUELUCHE',
    'difteria' : 'DIFTERIA',
    'tetano' : 'TÉTANO',
    'parotidite' : 'PAROTIDITE',
    'rubeola' : 'RUBÉOLA',
    'sarampo' : 'SARAMPO',
    'febre amarela' : 'FEBRE AMARELA',
    'hepatite b' : 'HEPATITE B',
    'meningite por haemophilus' : 'MENINGITE POR HAEMOPHILUS',
    'meningite tuberculosa' : 'MENINGITE TUBERCULOSA',
    'meningite' : 'MENINGITE',
    'tuberculose miliar' : 'TUBERCULOSE MILIAR',
    'tuberculose pulmonar' : 'TUBERCULOSE PULMONAR',
    'tuberculose' : 'TUBERCULOSE',
    'tb' : 'TUBERCULOSE',
    'febre reumatica' : 'FEBRE REUMÁTICA',
    'sifilis congenita' : 'SÍFILIS CONGÊNITA',
    'sifilis' : 'SÍFILIS',
    'malaria' : 'MALÁRIA',
    'ascaridiase' : 'ASCARIDÍASE',
    'desidratacao' : 'DESIDRATAÇÃO',
    'gastroenterite' : 'GASTROENTERITE',
    'anemia por deficiencia de ferro' : 'ANEMIA POR DEFICIÊNCIA DE FERRO',
    'anemia' : 'ANEMIA',
    'otite media supurativa' : 'OTITE MÉDIA SUPURATIVA',
    'nasofaringite aguda' : 'RESFRIADO COMUM',
    'resfriado' : 'RESFRIADO COMUM',
    'sinusite aguda' : 'SINUSITE AGUDA',
    'sinusite' : 'SINUSITE',
    'faringite aguda' : 'FARINGITE AGUDA',
    'amigdalite aguda' : 'AMIGDALITE AGUDA',
    'infeccao aguda vas' : 'INFECÇÃO AGUDA VAS',
    'rinite' : 'RINITE',    
    'nasofaringite cronica' : 'NASOFARINGITE CRÔNICA',
    'faringite cronica' : 'FARINGITE CRÔNICA',
    'faringite' : 'FARINGITE',
    'pneumonia pneumococica' : 'PNEUMONIA PNEUMOCÓCICA',
    'pneumonia por haemophilus infuenzae' : 'PNEUMONIA POR HAEMOPHILUS INFUENZAE',
    'pneumonia por streptococus' : 'PNEUMONIA POR STREPTOCOCUS',
    'pneumonia bacteriana' : 'PNEUMONIA BACTERIANA NE',
    'pneumonia lobar' : 'PNEUMONIA LOBAR NE',
    'pneumonia' : 'PNEUMONIA',
    'asma' : 'ASMA',
    'bronquite aguda' : 'BRONQUITE AGUDA',
    'bronquite cronica' : 'BRONQUITE CRÔNICA',
    'bronquite' : 'BRONQUITE',
    'enfisema' : 'ENFISEMA',
    'bronquectasia' : 'BRONQUECTASIA',
    'doenca pulmonar' : 'DOENÇAS PULMONARES OBSTRUTIVAS CRÔNICAS',
    'hipertensao essencial' : 'HIPERTENSÃO ESSENCIAL',
    'doenca cardiaca hipertensiva' : 'DOENÇA CARDÍACA HIPERTENSIVA',
    'angina pectoris' : 'ANGINA PECTORIS',
    'insuficiencia cardiaca' : 'INSUFICIÊNCIA CARDÍACA',
    'edema agudo de pulmao' : 'EDEMA AGUDO DE PULMÃO',
    'doenca cerebrovascular' : 'DOENÇA CEREBROVASCULAR',
    'diabetes melitus' : 'DIABETES MELITUS',
    'cistite' : 'EPILEPSIA',
    'nefrite tubulo-intersticial aguda' : 'NEFRITE TÚBULO-INTERSTICIAL AGUDA',
    'nefrite tubulo-intersticial cronica' : 'NEFRITE TÚBULO-INTERSTICIAL CRÔNICA',
    'nefrite tubulo-intersticial ne aguda' : 'NEFRITE TÚBULO-INTERSTICIAL NE AGUDA CRÔNICA',
    'cistite' : 'CISTITE',
    'uretrite' : 'URETRITE',
    'infeccao do trato urinario' : 'INFECÇÃO DO TRATO URINÁRIO',
    'infecção no trato urinario na gravidez' : 'INFECÇÃO NO TRATO URINÁRIO NA GRAVIDEZ',
    'infeccao urina' : 'INFECÇÃO URINÁRIA',
    'erisipela' : 'ERISIPELA',
    'impetigo' : 'IMPETIGO',
    'abscesso cutaneo' : 'ABSCESSO CUTÂNEO',
    'abscesso' : 'ABSCESSO',
    'furunculo' : 'FURÚNCULO',
    'carbunculo' : 'CARBÚNCULO',
    'celulite' : 'CELULITE',
    'linfadenite aguda' : 'LINFADENITE AGUDA',
    'salpingite' : 'SALPINGITE',
    'doenca inflamatoria do utero' : 'OOFORITE',
    'doencas da glandula de bartholin' : 'DOENÇAS DA GLÂNDULA DE BARTHOLIN',
    'ulcera gastrointestinal' : 'ÚLCERA GASTROINTESTINAL',
    'sindrome da rubeola congenita' : 'SÍNDROME DA RUBÉOLA CONGÊNITA'
}

hospital_dict = {
    'spa e policlinica dr. danilo correa' : 'SPA E POLICLÍNICA DR. DANILO CORRÊA',
    'policlinica dr. danilo correa' : 'SPA E POLICLÍNICA DR. DANILO CORRÊA',
    'policlinica danilo correa' : 'SPA E POLICLÍNICA DR. DANILO CORRÊA',
    '. danilo correa' : 'SPA E POLICLÍNICA DR. DANILO CORRÊA',
    'spa dr. danilo correa' : 'SPA E POLICLÍNICA DR. DANILO CORRÊA',
    'spa danilo correa' : 'SPA E POLICLÍNICA DR. DANILO CORRÊA',
    'pam codajas' : 'POLICLÍNICA CODAJÁS',
    'codajas' : 'POLICLÍNICA CODAJÁS',
    'policlinica codajas' : 'POLICLÍNICA CODAJÁS',
    'pam da codajas' : 'POLICLÍNICA CODAJÁS',
    'fundacao hospital do coracao francisca mendes' : 'FUNDAÇÃO HOSPITAL DO CORAÇÃO FRANCISCA MENDES',
    'francisca mendes' : 'FUNDAÇÃO HOSPITAL DO CORAÇÃO FRANCISCA MENDES',
    'caic moura tapajos' : 'CAIC MOURA TAPAJÓS',
    'caic dr. jose contente' : 'CAIC DR. JOSÉ CONTENTE',
    'spa zona sul' : 'SPA ZONA SUL',
    'caic ana maria dos santos pereira braga' : 'CAIC ANA MARIA DOS SANTOS PEREIRA BRAGA',
    'hospital psiquiatrico eduardo ribeiro' : 'HOSPITAL PSIQUIÁTRICO EDUARDO RIBEIRO',
    'policlinica antônio aleixo' : 'POLICLÍNICA ANTÔNIO ALEIXO',
    'instituto de saude da crianca do amazonas' : 'INSTITUTO DE SAÚDE DA CRIANÇA DO AMAZONAS – ICAM',
    'ican' : 'INSTITUTO DE SAÚDE DA CRIANÇA DO AMAZONAS – ICAM',
    'icam' : 'INSTITUTO DE SAÚDE DA CRIANÇA DO AMAZONAS – ICAM',
    'hospital geral dr. geraldo da rocha' : 'HOSPITAL GERAL DR. GERALDO DA ROCHA',
    'hospital e maternidade chapot prevost' : 'HOSPITAL E MATERNIDADE CHAPOT PREVOST',
    'dr. joao lucio pereira machado' : 'HPS - DR. JOÃO LÚCIO PEREIRA MACHADO',
    'ps joao lucio' : 'HPS - DR. JOÃO LÚCIO PEREIRA MACHADO',
    'h.p.s joao lucio' : 'HPS - DR. JOÃO LÚCIO PEREIRA MACHADO',
    'ps platao araujo' : 'HPS - DR. ARISTÓTELES PLATÃO BEZERRA DE ARAÚJO',
    'platao araujo' : 'HPS - DR. ARISTÓTELES PLATÃO BEZERRA DE ARAÚJO',
    'hps dr. aristoteles platao bezerra de araujo' : 'HPS - DR. ARISTÓTELES PLATÃO BEZERRA DE ARAÚJO',
    'hps platao' : 'HPS - DR. ARISTÓTELES PLATÃO BEZERRA DE ARAÚJO',
    'hps da crianca - zona sul' : 'HPS DA CRIANÇA - ZONA SUL',
    'caimi andre araujo' : 'CAIMI ANDRÉ ARAÚJO',
    'caimi paulo lima' : 'CAIMI PAULO LIMA',
    'maternidade estadual balbina mestrinho' : 'MATERNIDADE ESTADUAL BALBINA MESTRINHO',
    'maternidade azilda da silva marreiro' : 'MATERNIDADE AZILDA DA SILVA MARREIRO',
    'maternidade azilda marreiro' : 'MATERNIDADE AZILDA DA SILVA MARREIRO',
    'spa enfermeira eliameme rodrigues mady' : 'SPA ENFERMEIRA ELIAMEME RODRIGUES MADY',
    'spa coroado' : 'SPA COROADO',
    'spa sao raimundo' : 'SPA SÃO RAIMUNDO',
    'caic dra. maria helena freitas de goes' : 'CAIC DRA. MARIA HELENA FREITAS DE GÓES',
    'caic dr. gilson moreira' : 'CAIC DR. GILSON MOREIRA',
    'caic gilson moreira' : 'CAIC DR. GILSON MOREIRA',
    'caic dr. rubim de sa' : 'CAIC DR. RUBIM DE SÁ',
    'caic jose carlos mestrinho' : 'CAIC JOSÉ CARLOS MESTRINHO',
    'caic dr. edson melo' : 'CAIC DR. EDSON MELO',
    'caic dr. afrânio soares' : 'CAIC DR. AFRÂNIO SOARES',
    'caic alberto carreira' : 'CAIC ALBERTO CARREIRA',
    'caic dra. josephina de mello' : 'CAIC ALEXANDRE MONTORIL',
    'maternidade cidade nova dona nazira daou' : 'MATERNIDADE CIDADE NOVA DONA NAZIRA DAOU',
    'maternidade nazira daou' : 'MATERNIDADE CIDADE NOVA DONA NAZIRA DAOU',
    'spa joventina dias' : 'SPA JOVENTINA DIAS',
    'centro de atencao psicossocial silverio tundis' : 'CENTRO DE ATENÇÃO PSICOSSOCIAL SILVÉRIO TUNDIS',
    'caps silverio tundis' : 'CENTRO DE ATENÇÃO PSICOSSOCIAL SILVÉRIO TUNDIS',
    'hospital infantil dr. fajardo' : 'HOSPITAL INFANTIL DR. FAJARDO',    
    'fajardo' : 'HOSPITAL INFANTIL DR. FAJARDO',
    'policlinica cardoso fontes' : 'POLICLÍNICA CARDOSO FONTES',
    'policlinica ana barreto' : 'POLICLÍNICA ANNA BARRETO PEREIRA',
    'polic. ana  barreto' : 'POLICLÍNICA ANNA BARRETO PEREIRA',
    'polic. ana barreto' : 'POLICLÍNICA ANNA BARRETO PEREIRA',
    'pol. ana barreto' : 'POLICLÍNICA ANNA BARRETO PEREIRA',
    'policlinica anna barreto' : 'POLICLÍNICA ANNA BARRETO PEREIRA',
    'cema' : 'CEMA',
    'lacen' : 'LABORATÓRIO CENTRAL',
    'laboratorio central' : 'LABORATÓRIO CENTRAL',
    'spa e policlinica dr. jose de jesus lins de albuquerque' : 'SPA E POLICLÍNICA DR. JOSÉ DE JESUS LINS DE ALBUQUERQUE',
    'caic alexandre montoril' : 'CAIC ALEXANDRE MONTORIL',
    'caimi ada rodrigues viana' : 'CAIMI ADA RODRIGUES VIANA',
    'cepra' : 'CEPRA',
    'maternidade alvorada' : 'MATERNIDADE ALVORADA',
    'maternidade ana braga' : 'MATERNIDADE ANA BRAGA',
    'fundacao de hematologia e hemoterapia do amazonas' : 'FUNDAÇÃO DE HEMATOLOGIA E HEMOTERAPIA DO AMAZONAS - FHEMOAM',
    'fhemoam' : 'FUNDAÇÃO DE HEMATOLOGIA E HEMOTERAPIA DO AMAZONAS - FHEMOAM',
    'hemoam' : 'FUNDAÇÃO DE HEMATOLOGIA E HEMOTERAPIA DO AMAZONAS - FHEMOAM',
    'hemoan' : 'FUNDAÇÃO DE HEMATOLOGIA E HEMOTERAPIA DO AMAZONAS - FHEMOAM',
    'spa alvorada' : 'SPA ALVORADA',
    'policlinica zeno lanzini' : 'POLICLÍNICA ZENO LANZINI',
    'policlinica joao dos santos braga' : 'POLICLÍNICA JOÃO DOS SANTOS BRAGA',
    'hps 28 de agosto' : 'HPS 28 DE AGOSTO',
    'hps 28  de agosto' : 'HPS 28 DE AGOSTO',
    '28 de agosto' : 'HPS 28 DE AGOSTO',
    'policlinica gilberto mestrinho' : 'POLICLÍNICA GOVERNADOR GILBERTO MESTRINHO',
    'policlinica governador gilberto mestrinho' : 'POLICLÍNICA GOVERNADOR GILBERTO MESTRINHO',
    'pol. gilberto mestrinho' : 'POLICLÍNICA GOVERNADOR GILBERTO MESTRINHO',    
    'polic.gilberto mestrinho' : 'POLICLÍNICA GOVERNADOR GILBERTO MESTRINHO',
    'hps da crianca zona leste' : 'HPS DA CRIANÇA - ZONA LESTE',
    'hps da crianca zona oeste' : 'HPS DA CRIANÇA - ZONA OESTE',
    'hps da crianca zona sul' : 'HPS DA CRIANÇA - ZONA SUL',
    'hps zona sul' : 'HPS DA CRIANÇA - ZONA SUL',
    'fcecon' : 'FUNDAÇÃO CECON',
    'fundacao cecon' : 'FUNDAÇÃO CECON',
    'hospital universitario getulio vargas' : 'HOSPITAL UNIVERSITÁRIO GETÚLIO VARGAS – HUGV',
    'hugv' : 'HOSPITAL UNIVERSITÁRIO GETÚLIO VARGAS – HUGV',
    'huvg' : 'HOSPITAL UNIVERSITÁRIO GETÚLIO VARGAS – HUGV',
    'araujo lima' : 'HOSPITAL UNIVERSITÁRIO GETÚLIO VARGAS – HUGV',
    'fundacao de medicina tropical' : 'FUNDAÇÃO DE MEDICINA TROPICAL – FMT',
    'fmt' : 'FUNDAÇÃO DE MEDICINA TROPICAL – FMT',
    'adriano jorge' : 'FUNDAÇÃO HOSPITAL ADRIANO JORGE – FHAJ',
    'fundacao adriano jorge' : 'FUNDAÇÃO HOSPITAL ADRIANO JORGE – FHAJ',
    'fundacao hospital adriano jorge' : 'FUNDAÇÃO HOSPITAL ADRIANO JORGE – FHAJ',
    'fhaj' : 'FUNDAÇÃO HOSPITAL ADRIANO JORGE – FHAJ',
    'hfaj' : 'FUNDAÇÃO HOSPITAL ADRIANO JORGE – FHAJ',
    'alfredo da mata' : 'FUNDAÇÃO ALFREDO DA MATTA – FAM',
    'fundacao alfredo da matta' : 'FUNDAÇÃO ALFREDO DA MATTA – FAM',
    'fundacao universitaria alfredo da mata' : 'FUNDAÇÃO ALFREDO DA MATTA – FAM',
    'fundacao universitaria alfredo da matta' : 'FUNDAÇÃO ALFREDO DA MATTA – FAM',
    'fundacao de vigilância em saude do amazonas - dra. rosemary costa pinto' : 'FUNDAÇÃO DE VIGILÂNCIA EM SAÚDE DO AMAZONAS - DRA. ROSEMARY COSTA PINTO',
    'instituto da mulher dona lindu' : 'INSTITUTO DA MULHER DONA LINDÚ',
    'instituto da mulher' : 'INSTITUTO DA MULHER DONA LINDÚ',
    'hospital delphina aziz' : 'HOSPITAL DELPHINA AZIZ',
    'delfina aziz' : 'HOSPITAL DELPHINA AZIZ',
    'delphina aziz' : 'HOSPITAL DELPHINA AZIZ',
    'upa campos sales' : 'UPA CAMPOS SALES',
    'upa jose rodrigues' : 'UPA JOSÉ RODRIGUES',
    'ubs' : 'UBS',
    'hapvida' : 'HAPVIDA',
    'sensumed' : 'SENSUMED',
    'check up' : 'CHECK UP',
    'hospital santo alberto' : 'HOSPITAL SANTO ALBERTO',
    'hospital beneficente portuguesa' : 'HOSPITAL BENEFICENTE PORTUGUESA',
    'beneficente portuguesa' : 'HOSPITAL BENEFICENTE PORTUGUESA',
    'h.b.portuguesa' : 'HOSPITAL BENEFICENTE PORTUGUESA',
    'hosp.benef. portuguesa' : 'HOSPITAL BENEFICENTE PORTUGUESA',
    'hospital adventista' : 'HOSPITAL ADVENTISTA',
    'hospital santa julia' : 'HOSPITAL SANTA JÚLIA',
    'instituto de oftalmologia de manaus' : 'INSTITUTO DE OFTALMOLOGIA DE MANAUS - IOM',
    'iom' : 'INSTITUTO DE OFTALMOLOGIA DE MANAUS - IOM',
    'hps' : 'HPS',
    'spa' : 'SPA',
    'caic' : 'CAIC',
    'caimi' : 'CAIMI',
    'upa' : 'UPA',
    'maternidade' : 'MATERNIDADE',
    'poloclinica' : 'POLICLÍNICA'
}

ethnicity_dict = {
    'bare' : 'Baré',
    'bara' : 'Baré',
    'kuripaco' : 'Koripako',
    'hupda' : 'Hupda',
    'ticuna' : 'Tikuna',
    'mura' : 'Mura',
    'satere' : 'Sateré Mawé',
    'kocama' : 'Kokama',
    'munduruku' : 'Munduruku',
    'maragua' : 'Maraguá',
    'paumari' : 'Paumari',
    'apurina' : 'Apurinã',
    'matis' : 'Matis',
    'marubo' : 'Marubo',
    'curipaco' : 'Koripako',
    'yanomami' : 'Yanomami',
    'baniwa' : 'Baniwa',
    'tariano' : 'Tariana',
    'nadeb' : 'Nadöb',
    'dessana' : 'Desana',
    'tukano' : 'Tukano',
    'piratapuia' : 'Pira-tapuya',
    'werekena' : 'Warekena',
    'maku nadeb' : 'Nadöb',
    'tuyuca' : 'Tuyuka',
    'dessano' : 'Desana',
    'kokama' : 'Kokama',
    'tikuna' : 'Tikuna',
    'tenharim' : 'Tenharim',
    'piraha' : 'Pirahã',
    'mundurucu' : 'Munduruku',
    'tora' : 'Torá',
    'jarawara' : 'Jarawara',
    'banawa' : 'Banawá',
    'kanamari' : 'Kanamari',
    'banaewa' : 'Baniwa',
    'kulina' : 'Kulina',
    'culina' : 'Kulina',
    'miranha' : 'Miranha',
    'satere mawe' : 'Sateré Mawé',
    'korubo' : 'Korubo',
    'tucano' : 'Tukano',
    'werekene' : 'Warekena',
    'tiyuka' : 'Tuyuka',
    'hexkaryana' : 'Hixkaryana',
    'tenharin' : 'Tenharim',
    'sarere' : 'Sateré Mawé',
    'deni' : 'Deni',
    'dow' : 'Dâw',
    '01/11/1977' : '?',
    'kambeba' : 'Kambeba',
    'jamamadi' : 'Jamamadi',
    'nao consta' : '?',
    'bara' : 'Bará',
    'tuyuka' : 'Tuyuka',
    'tikuna ' : 'Tikuna',
    'satera' : 'Sateré Mawé',
    'kanamary' : 'Kanamari',
    'daw' : 'Dâw',
    'curupaco' : 'Koripako',
    'piratupaia' : 'Pira-tapuya',
    'icuripaco' : 'Koripako',
    'cubeu' : 'Kubeo',
    'werequina' : 'Warekena',
    'curripaco' : 'Koripako',
    'tuiuca' : 'Tuyuka',
    'kubeo' : 'Kubeo',
    'korupaco' : 'Koripako',
    'kiripaco' : 'Koripako',
    '22.09.1988' : '?',
    'kaixiawa' : 'Kaixana',
    'valcileia pinto ramos' : '?',
    'cokama' : 'Kokama',
    'ticuna ' : 'Tikuna',
    'kaixana' : 'Kaixana',
    'muduruku' : 'Munduruku',
    'parintintin' : 'Parintintim',
    'munducuku' : 'Munduruku',
    'muncuruku' : 'Munduruku',
    'satere-mawe' : 'Sateré Mawé',
    '?' : '?',
    'escarianob' : 'Hixkaryana', 
    'excariano' : 'Hixkaryana',
    'escariano' : 'Hixkaryana',
    'escariana' : 'Hixkaryana',
    'hexcariano' : 'Hixkaryana',
    'apaurina' : 'Apurinã',
    'jamandi' : 'Jamamadi',
    'jamadi' : 'Jamamadi',
    'caixana' : 'Kaixana',
    'kanmari' : 'Kanamari',
    'arapaco' : 'Arapaso',
    'caxinaua' : 'Caxinauá',
    'mayurura' : 'Mayoruna',
    'macu' : 'Maku',
    'mayoruna' : 'Mayoruna',
    'maku yupy' : 'Maku',
    'rupida' : 'Hupda',
    'mayuryna' : 'Mayoruna',
    'wanana' : 'Wanana',
    'wanano' : 'Wanana', 
    'nadele' : '?',
    'maku' : 'Maku',
    'mayuruna' : 'Mayoruna',
    'mauyruna' : 'Mayoruna',
    'wexequena' : '?',
    'iauarete' : '?',
    'weewkema' : '?',
    'branca' : '?'
}

servicereceived_dict = {
    'usg de joelho' : 'exame',
	'laboratoriais' : 'exame',
	'mamografia' : 'exame',
	'usg mama' : 'exame',
	'laboratoriais e mielograma' : 'exame',
	'rx de torax' : 'exame',
	'laboratoriais' : 'exame',
	'eeg' : 'exame',
	'rnm crânio' : 'exame',
	'laboratoriais' : 'exame',
	'rx de torax' : 'exame',
	'ecg' : 'exame',
	'laboratoriais' : 'exame',
	'ecg' : 'exame',
	'rx torax' : 'exame',
	'litotripsia extracorporea' : 'procedimento cirúrgico',
	'ecg' : 'exame',
	'laboratoriais' : 'exame',
	'cirurgiao cabeca e pescoco' : 'procedimento cirúrgico',
	'eeg' : 'exame',
	'cirurgiao geral' : 'procedimento cirúrgico',
	'cirurgiao geral' : 'procedimento cirúrgico',
	'exames laboratoriais' : 'exame',
	'usg de abdome' : 'exame',
	'exame de panorâmico' : 'exame',
	'exames laboratoriais' : 'exame',
	'rnm' : 'exame',
	'rx de femur d' : 'exame',
	'cirurgiao vascular' : 'procedimento cirúrgico',
	'curativo' : 'curativo',
	'cirurgiao vascular' : 'procedimento cirúrgico',
	'cirurgiao vascular' : 'procedimento cirúrgico',
	'cirurgiao vascular' : 'procedimento cirúrgico',
	'rx ' : 'exame',
	'tc de abdômen superior e pelve.' : 'exame',
	'exames laboratoriais' : 'exame',
	'exame coleta de material – pele' : 'exame',
	'triagem' : '?',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'clinica geral' : 'consulta',
	'exames laboratoriais ' : 'exame',
	'conizacao ' : 'procedimento cirúrgico',
	'curativo' : 'curativo',
	'internacao' : 'internação',
	'cirurgiao plastico' : 'procedimento cirúrgico',
	'exames laboratoriais/rx de torax' : 'exame',
	'tc de abdome e pelve' : 'exame',
	'ecocardiograma' : 'exame',
	'holter 24horas' : 'exame',
	'cirurgiao plastico' : 'procedimento cirúrgico',
	'curativo' : 'curativo',
	'rx ' : 'exame',
	'curativo' : 'curativo',
	'curativo' : 'curativo',
	'curativo' : 'curativo',
	'curativo' : 'curativo',
	'rnm de bacia/pelve' : 'exame',
	'clinico geral' : 'consulta',
	'cirurgiao geral' : 'consulta',
	'usg de abdome superior' : 'exame',
	'exames laboratoriais' : 'exame',
	'rx de torax' : 'exame',
	'cirurgiao geral' : 'consulta',
	'rx' : 'exame',
	'exames laboratoriais' : 'exame',
	'tc de torax' : 'exame',
	'tc de torax c/ contraste' : 'exame',
	'teste de baar' : 'exame',
	'cirurgiao toracico' : 'consulta',
	'clinico geral' : 'consulta',
	'medicacao injetavel de 12/12hs' : 'medicação',
	'exames laboratoriais + medicacao' : 'exame e medicação',
	'medicacao injetavel 1x ao dia' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'exames laboratoriais ' : 'exame',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'exame de pele' : 'exame',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'exames laboratoriais' : 'exame',
	'medicacao injetavel' : 'medicação',
	'exames laboratoriais' : 'exame',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'exames laboratoriais e medicacao' : 'exame e medicação',
	'exames laboratoriais e medicacao' : 'exame e medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'medicacao injetavel' : 'medicação',
	'cirurgiao geral' : 'consulta',
	'usg de abdômen/colangiorressonância' : 'exame',
	'exames laboratoriais' : 'exame',
	'rx, ecg' : 'exame',
	'cirurgiao geral' : 'consulta',
	'exame de ppd' : 'exame',
	'prova ventilatoria' : 'exame',
	'internacao' : 'internação',
	'cirurgiao buco maxilo' : 'consulta',
	'cirurgiao buco maxilo' : 'consulta',
	'tc de face' : 'exame',
	'exames laboratoriais' : 'exame',
	'ecg' : 'exame',
	'cirurgiao buco maxilo' : 'consulta',
	'exames laboratoriais, eas e epf' : 'exame',
	'biopsia' : 'procedimento cirúrgico',
	'exames laboratoriais' : 'exame',
	'rnm de crânio' : 'exame',
	'obstetra' : 'consulta',
	'quimioterapia' : 'tratamento',
	'teste de covid-19' : 'exame',
	'quimioterapia' : 'tratamento',
	'quimioterapia' : 'tratamento',
	'clinico geral' : 'consulta',
	'rnm de abdômen' : 'exame',
	'clinico geral' : 'consulta',
	'tc de torax e abdômen' : 'exame',
	'rx de torax' : 'exame',
	'radioterapia' : 'tratamento',
	'radioterapia' : 'tratamento',
	'radioterapia' : 'tratamento',
	'radioterapia' : 'tratamento',
	'radioterapia' : 'tratamento',
	'radioterapia' : 'tratamento',
	'radioterapia' : 'tratamento',
	'radioterapia' : 'tratamento',
	'clinico geral' : 'consulta',
	'radioterapia' : 'tratamento',
	'consulta de enfermagem ' : 'consulta',
	'usg do aparelho urinario' : 'exame',
	'exames laboratoriais' : 'exame',
	'psiquiatra' : 'consulta',
	'baar' : 'exame',
	'ppd' : 'exame',
	'beta hcg' : 'exame',
	'obstetra' : 'consulta',
	'exames laboratoriais, ppd, vacina' : 'exame',
	'leitura de ppd' : 'exame',
	'usg obstetrica' : 'exame',
	'obstetra' : 'consulta',
	'sorologia' : 'exame',
	'exames laboratoriais' : 'exame',
	'baciloscopia de pele' : 'exame',
	'exames laboratoriais, rx de torax, maos e punho.' : 'exame',
	'rnm de coluna lombar' : 'exame',
	'exames laboratoriaias' : 'exame',
	'exames laboratoriais' : 'exame',
	'rnm de crânio' : 'exame',
	'pccu' : 'exame',
	'usg transvaginal e beta hcg' : 'exame',
	'beta hcg quantitativo' : 'exame',
	'beta hcg quantitativo/epf/eas' : 'exame',
	'beta hcg quantitativo' : 'exame',
	'usg transvaginal e de abdome total' : 'exame',
	'beta hcg quantitativo' : 'exame',
	'beta hcg quantitativo/ exames laboratoriais' : 'exame',
	'beta hcg quantitativo' : 'exame',
	'rx de torax' : 'exame',
	'beta hcg quantitativo' : 'exame',
	'beta hcg quantitativo' : 'exame',
	'beta hcg quantitativo' : 'exame',
	'usg transvaginal' : 'exame',
	'cirurgia geral' : 'consulta',
	'conizacao' : 'procedimento cirúrgico',
	'clinico' : 'consulta',
	'clinico' : 'consulta',
	'clinico' : 'consulta',
	'exames laboratoriais' : 'exame',
	'usg de vias urinarias' : 'exame',
	'usg transvaginal' : 'exame',
	'usg com dopller venoso' : 'exame',
	'vascular' : 'consulta',
	'vascular' : 'consulta',
	'usg de regiao cervical' : 'exame',
	'exames laboratoriais' : 'exame',
	'enfermagem(triagem)' : '?',
	'exames laboratoriais e carga viral' : 'exame',
	'exame oftalmologico' : 'exame',
	'consulta c/ otorino' : 'consulta',
	'rx de coluna' : 'exame',
	'exames laboratoriais' : 'exame',
	'exame de urodinamico completo' : 'exame',
	'retinologo' : 'consulta',
	'laboratoriais' : 'exame',
	'laboratoriais' : 'exame',
	'laboratoriais' : 'exame',
	'usg obstetrica' : 'exame',
	'pre-natal' : 'consulta',
	'pre-natal' : 'consulta',
	'pre-natal' : 'consulta',
	'usg de abdome total' : 'exame',
	'internacao para eda' : 'exame',
	'usg de abdome total' : 'exame',
	'rx de joelho e coxa' : 'exame',
	'realizou exames laboratoriais e rx de torax + vacinas crie' : 'exame',
	'realizou coleta de exame preventivo' : 'exame',
	'realizou usg transvaginal, tireoide e abdome total ' : 'exame',
	'enfermagem(triagem)' : '?',
	'obstetra' : 'consulta',
	'obstetra' : 'consulta',
	'obstetra' : 'consulta',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'exame baar' : 'exame',
	'prova ventilatoria' : 'exame',
	'realizou exames laboratoriais' : 'exame',
	'realizou rx de torax ' : 'exame',
	'clinico geral' : 'consulta',
	'clinico geral' : 'consulta',
	'clinico geral' : 'consulta',
	'obstetra' : 'consulta',
	'clinica medica' : 'consulta',
	'exames laboratoriais' : 'exame',
	'clinico geral' : 'consulta',
	'exame de trm(escarro)' : 'exame',
	'rx de torax' : 'exame',
	'clinico geral ' : 'consulta',
	'rx de torax' : 'exame',
	'internacao' : 'internação',
	'exame baar' : 'exame',
	'exame de bcr' : 'exame',
	'curativos' : 'curativo',
	'exames laboratoriais' : 'exame',
	'curativos' : 'curativo',
	'rx de torax' : 'exame',
	'eas, epf, exames laboratoriais, usg de abdômen.' : 'exame',
	'exames laboratoriais' : 'exame',
	'eda' : 'exame',
	'rnm de vias biliares' : 'exame',
	'exames laboratoriais, usg de tireoide, ecg, eco.' : 'exame',
	'mapa' : 'exame',
	'retirada de mapa' : 'exame',
	'holter' : 'exame',
	'retirada de holter' : 'exame',
	'paaf' : 'exame',
	'ex. sorologia, ex. laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'rnm de abdômen total' : 'exame',
	'eda' : 'exame',
	'hmg completo,epf ' : 'exame',
	'eas ' : 'exame',
	'enfermeira ' : '?',
	'cirurgia-retirada de melanoma nodular ' : 'procedimento cirúrgico',
	'exames laboratoriais' : 'exame',
	'quimioterapia ' : 'tratamento',
	'exame de audiometria' : 'exame',
	'exames laboratoriais' : 'exame',
	'exame de raio x' : 'exame',
	'tc de torax ' : 'exame',
	'usg de abdome total ' : 'exame',
	'ecott ' : 'exame',
	'mamografia ' : 'exame',
	'biopsia de mama' : 'procedimento cirúrgico',
	'setor de hepatites' : '?',
	'exame de carga viral de hepatite' : 'exame',
	'sorologia' : 'exame',
	'exames de bioquimica' : 'exame',
	'prova de funcao pulmonar completa' : 'exame',
	'carga viral da hepatite b e exames laboratoriais' : 'exame',
	'ultrassom com doppler' : 'exame',
	'raio x de torax' : 'exame',
	'eletrocardiograma' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais e sorologia' : 'exame',
	'rx de torax e bacia' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'tc de crânio' : 'exame',
	'exames laboratoriais' : 'exame',
	'usg com doppler' : 'exame',
	'consulta por tfd ' : 'exame',
	'ecocardiograma' : 'exame',
	'psiquiatrico' : 'consulta',
	'psiquiatrico' : 'consulta',
	'rnm de crânio' : 'exame',
	'psiquiatrico' : 'consulta',
	'usg de abdomen superior ' : 'exame',
	'ecg ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'rnm de coluna lombo-sacra ' : 'exame',
	'rx de antebraco' : 'exame',
	'ecocardiograma' : 'exame',
	'triagem' : '?',
	'exames laboratoriais' : 'exame',
	'ultrassonografia de mamas' : 'exame',
	'rx de torax' : 'exame',
	'exames laboratoriais' : 'exame',
	'usg transvaginal + usg abdominal' : 'exame',
	'densitometria ossea' : 'exame',
	'usg transvaginal' : 'exame',
	'tc de crânio' : 'exame',
	'hemograma' : 'exame',
	'urocultura' : 'exame',
	' usg de abdome total' : 'exame',
	'covid-19' : 'exame',
	'ultrassonografia de tireoide' : 'exame',
	'tc de abdômen' : 'exame',
	'exames laboratoriais' : 'exame',
	'avaliacao transplante figado' : 'consulta',
	'exames laboratoriais' : 'exame',
	'ressonância magnetica ' : 'exame',
	'medico da radioterapia ' : 'consulta',
	'exame de beta hcg quantitativo ' : 'exame',
	'medico da radioterapia ' : 'consulta',
	'exames laboratoriais ' : 'exame',
	'medico da quimioterapia ' : 'consulta',
	'exames laboratoriais ' : 'exame',
	'medico da radioterapia ' : 'consulta',
	'medico da radioterapia ' : 'consulta',
	'exames laboratoriais' : 'exame',
	'1ª sessao de pulsoterapia' : 'tratamento',
	'2ª sessao de pulsoterapia' : 'tratamento',
	'exames laboratoriais carga viral' : 'exame',
	'beta hcg' : 'exame',
	'raio x de coluna cervical' : 'exame',
	'ultrassonografia de rins e prostata' : 'exame',
	'teste do covid-19' : 'exame',
	'exame de raio x' : 'exame',
	'exame de raio x' : 'exame',
	'tomografia computadorizada de torax' : 'exame',
	'medica da dor' : 'consulta',
	'cirurgiao toracico' : 'consulta',
	'exames laboratoriais' : 'exame',
	'exame de raio x de torax' : 'exame',
	'eletrocardiograma' : 'exame',
	'tomografia computadorizada de torax, abdômen superior e pelve.' : 'exame',
	'2ª parte com contraste dos exames de tomografia computadorizada de torax, abdômen superior e pelve.' : 'exame',
	'exames laboratoriais' : 'exame',
	'rx de bacia' : 'exame',
	'exames laboratoriais' : 'exame',
	'ressonância magnetica de crânio' : 'exame',
	'exames laboratoriais ' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais, eas e proteinuria de 24 horas' : 'exame',
	'exame de albumina serica e combo direto' : 'exame',
	'consulta de pre natal' : 'consulta',
	'ecocardiografia fetal' : 'exame',
	'consulta de pre natal' : 'consulta',
	'exames laboratoriais' : 'exame',
	'gota espessa' : '?',
	'ultrassonografia morfologica' : 'exame',
	'estudo urodinamico' : 'exame',
	'rnm de pelve' : 'exame',
	'ecocardiograma com doppler' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'raio x de torax' : 'exame',
	'exames laboratoriais' : 'exame',
	'oncologia' : 'consulta',
	'exames laboratoriais' : 'exame',
	'oncologia' : 'consulta',
	'exames laboratoriais' : 'exame',
	'oncologia' : 'consulta',
	'exames laboratoriais' : 'exame',
	'enf. binda' : '?',
	'exames laboratoriais' : 'exame',
	'oncologia' : 'consulta',
	'exames laboratoriais' : 'exame',
	'oncologia' : 'consulta',
	'raio x de torax' : 'exame',
	'biopsia' : 'procedimento cirúrgico',
	'ultrassonografia de mama' : 'exame',
	'toxoplasmose(igm/igg)' : 'exame',
	'servico de hepatites.' : 'exame',
	'otorrinolaringologia' : 'consulta',
	'dermatologia' : 'consulta',
	'hemograma completo e bioquimicos' : 'exame',
	'dermatologia' : 'consulta',
	'buco-maxilo' : '?',
	'clonixinato de lisina 125 mg + cloridrato de ciclobenzaprina 5 mg' : '?',
	'patricia jane' : '?',
	'exames de: carga viral, exames laboratoriais, beta hcg e eas' : 'exame',
	'exame de eletrocardiograma' : 'exame',
	'exame de ecocardiograma' : 'exame',
	'exames laboratorias' : 'exame',
	'usg abdome total' : 'exame',
	'ecg' : 'exame',
	'cirurgiao deral' : 'consulta',
	'ressonância magnetica de abdome e pelve' : 'exame',
	'exames laboratoriais ' : 'exame',
	'eletrocardiograma ' : 'exame',
	'raio x de torax ' : 'exame',
	'raio x de torax ' : 'exame',
	'xenodiagnostico ' : 'exame',
	'procedimento cirurgico de pterigio em olho direito' : 'procedimento cirúrgico',
	'rnm de abdome superior ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'exames de: sorologia, xenodiagnostico e eletrocardiograma.' : 'exame',
	'ecocardiograma' : 'exame',
	'realizou ecg  ' : 'exame',
	'realizou rx de torax  ' : 'exame',
	'realizou exames laboratoriais  ' : 'exame',
	'cirurgiao oncologico' : 'consulta',
	'exame de ultrassonografia' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'tomografia computadorizada' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'medica da quimioterapia' : 'exame',
	'exames laboratoriais, eas e proteinuria de 24 horas.' : 'exame',
	'raio x de torax' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'pesquisa de baar ' : 'exame',
	'cultura' : 'exame',
	'raio x de torax ap/perfil' : 'exame',
	'exames laboratoriais' : 'exame',
	'exame de raio x de torax' : 'exame',
	'exame de eletrocardiograma' : 'exame',
	'ultrassonografia de prostata, abdome total.' : 'exame',
	'teste de covid- 19' : 'exame',
	'rm de pelve abdome superior' : 'exame',
	'tc’s de face, torax e pescoco  hufm' : 'exame',
	'realizou rx de clavicula' : 'exame',
	'realizou tc de crânio' : 'exame',
	'hemograma + usg de abdômen+ rx de torax  ' : 'exame',
	'rx de torax ' : 'exame',
	'realizou exames laboratoriais' : 'exame',
	'realizou  laboratoriais ecg ' : 'exame',
	'exames laboratoriais' : 'exame',
	'tc de abdome ' : 'exame',
	'realizou exame laboratoriais ' : 'exame',
	'realizou rx ' : 'exame',
	'realizou exame de laboratoriais' : 'exame',
	'realizou exame laboratoriais ' : 'exame',
	'rx de torax ' : 'exame',
	'realizou ecg' : 'exame',
	'rx de mao' : 'exame',
	'exame laboratoriais ' : 'exame',
	'exame rnm vias biliares' : 'exame',
	'realizou rx de torax ' : 'exame',
	'realizou usg do aparelho urinario ' : 'exame',
	'realizou usg abdômen e transvaginal' : 'exame',
	'realizou exame laboratoriais' : 'exame',
	'eletroencefalograma' : 'exame',
	'realizou exame laboratoriais' : 'exame',
	'realizou rx do torax ' : 'exame',
	'realizou ecg' : 'exame',
	'exames laboratoriais' : 'exame',
	'raio-x de torax' : 'exame',
	'usg de abdome total' : 'exame',
	'mamografia bilateral' : 'exame',
	'exames laboratoriais ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'raio-x de torax' : 'exame',
	'exames laboratoriais ' : 'exame',
	'ecg + risco cirurgico' : 'exame',
	'tgo-tgp-gama gt- fosfastase- alcalina-bilirrubina.' : 'exame',
	'exames laboratoriais  ' : 'exame',
	'usg obstetrica  ' : 'exame',
	'usg abdome superior ' : 'exame',
	'tonometria' : 'exame',
	'usg globo ocular' : 'exame',
	'exames laboratoriais ' : 'exame',
	'raio-x de torax pa/p' : 'exame',
	'eletrocardiograma ' : 'exame',
	'parecer de risco cirurgico ' : 'exame',
	'usg de abdome total' : 'exame',
	'tc de abdome' : 'exame',
	'endoscopia digestiva com biopsia' : 'exame',
	'hcv, hb e vdrl' : 'exame',
	'hiv' : 'exame',
	'usg de abdome' : 'exame',
	'ressonancia de abdome' : 'exame',
	'eda' : 'exame',
	'exames laboratoriais ' : 'exame',
	'eletrocardiograma' : 'exame',
	'raio-x de torax' : 'exame',
	'parecer de risco cirurgico ' : 'exame',
	'usg de globo ocular' : 'exame',
	'biomicroscopia de fundo de olho' : 'exame',
	'destro de 231 mg/dl,' : 'exame',
	'cea- aff, bhq' : 'exame',
	'atendido em carater de urgencia' : 'urgência',
	'urgencia/ internacao' : 'urgência',
	'bhcg quantitativo' : 'exame',
	'atendida em carater de urgencia pelo obstetra' : 'consulta',
	'hemograma, tgo, tgp.' : 'exame',
	'urgencia/internado' : 'urgência',
	'realizou exames laboratoriais ' : 'exame',
	'urgencia/ intenacao ' : 'urgência',
	'exames laboratoriais' : 'exame',
	'hemograma' : 'exame',
	'usg de vias urinarias' : 'exame',
	'psa, eas, cultura.' : 'exame',
	'usg aparelho urinario' : 'exame',
	' foi atendido pela' : '?',
	'foi avaliado pela clinico geral' : 'consulta',
	'xenodiagnostico' : 'exame',
	'urgencia/internacao ' : 'urgência',
	'internacao ' : 'internação',
	'realizou curativo ' : 'curativo',
	'cirurgiao vascular ' : 'consulta',
	'realizou eco' : 'exame',
	'realizou exames laboratoriais' : 'exame',
	'realizou usg de abdome' : 'exame',
	'realizou endoscopia digestiva' : 'exame',
	'realizou tc de abdome total' : 'exame',
	' realizou exames laboratoriais' : 'exame',
	'realizou consulta ' : 'consulta',
	'retorno' : 'consulta',
	'atendido pela ' : '?',
	'foi avaliado em carater de urgencia' : 'consulta',
	'realizou consulta com psiquiatra' : 'consulta',
	'realizou consulta ' : 'consulta',
	'realizou consulta com psiquiatra' : 'consulta',
	'consulta em carater de urgencia' : 'consulta',
	'carga viral hepatite b, hemograma completo bioquimico, eas+epf.' : 'exame',
	'usg de abdome' : 'exame',
	'coleta de material para biopsia' : 'procedimento cirúrgico',
	'entregue material para biopsia' : 'procedimento cirúrgico',
	'raio-x de torax' : 'exame',
	'exames laboratoriais ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'ecg e risco cirurgico ' : 'exame',
	'realizou exame de sangue.' : 'exame',
	'realizou raio-x do joelho' : 'exame',
	'realizou exame laboratoriais ' : 'exame',
	'realizou eda com coleta de biopsia' : 'exame e procedimento cirúrgico',
	'exame de refracao ocular oe' : 'exame',
	'realizou exames hemograma completo ' : 'exame',
	'realizou exame de ecg' : 'exame',
	'realizou tc de torax ' : 'exame',
	'realizou exames laboratoriais' : 'exame',
	'realizou triagem dermatologica ' : 'exame',
	'realizou rnm de bacia e pelvica' : 'exame',
	'realizou exames laboratoriais.' : 'exame',
	'realizou biopsia / com resultados pendentes' : 'procedimento cirúrgico',
	'realizou exames laboratoriais' : 'exame',
	'realizou radioterapia' : 'tratamento',
	'realizou preventivo' : 'exame',
	'realizar procedimento cirurgico (herniorrafia)' : 'procedimento cirúrgico',
	'realizou consulta oncologico ' : 'consulta',
	'exames laboratoriais' : 'exame',
	'realizou sangria terapeutica' : 'tratamento',
	'realizou laboratoriais e sorologias  ' : 'exame',
	'realizou usg de abdome total' : 'exame',
	'realizou raio x de torax ' : 'exame',
	'realizou exames laboratoriais ' : 'exame',
	'realizou ecg' : 'exame',
	'neurocirurgiao' : 'consulta',
	'exames laboratoriais' : 'exame',
	'usg prostata' : 'exame',
	'sorologias ' : 'exame',
	'urgencia /internacao' : 'urgência',
	'urgencia /internacao' : 'urgência',
	'urgencia /internacao' : 'urgência',
	'exames laboratoriais' : 'urgência',
	'usg transretal prostata' : 'exame',
	'urologia' : 'consulta',
	'urgencia/internacao' : 'urgência',
	'pos-operatorio' : 'consulta',
	'pos-operatorio' : 'consulta',
	'tomografia computorizada de abdome' : 'exame',
	'realizou laboratoriais, usg de abdômen  ' : 'exame',
	'realizou rx de crânio ' : 'exame',
	'realizou rnm de coluna' : 'exame',
	'realizou exame laboratoriais ' : 'exame',
	'realizou exame de rx' : 'exame',
	'realizou procedimentos cirurgico biopsia' : 'procedimento cirúrgico',
	'realizou coleta de biopsia' : 'procedimento cirúrgico',
	'rnm de crânio' : 'exame',
	'realizou refracao do olho d' : 'exame',
	'realizou exame topografia' : 'exame',
	'realizou usg' : 'exame',
	'realizou exame laboratoriais ' : 'exame',
	'realizou exame laboratoriais' : 'exame',
	'realizou usg do abdômen superior ' : 'exame',
	'realizou usg transvaginal' : 'exame',
	'realizou mamografia (particular)' : 'exame',
	'exames laboratoriais' : 'exame',
	'rnm de bacia e pelve' : 'exame',
	'exame densitometria ossea' : 'exame',
	'raio-x de joelho d/e' : 'exame',
	'exames laboratoriais ' : 'exame',
	'usg de cotovelo direito ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'raio-x de torax' : 'exame',
	'exames laboratoriais' : 'exame',
	'tomografia computadorizada de pelve e abdome superior' : 'exame',
	'raio-x de mao direita' : 'exame',
	'realizou exames laboratoriais ' : 'exame',
	'realizou exames laboratoriais' : 'exame',
	'urgencia /intencao' : 'urgência',
	'usg de prostata' : 'exame',
	'hemograma, ureia, creatinina, glicemia, eas psa total' : 'exame',
	'consulta carater de urgencia para, avaliado pelo' : 'consulta',
	'hemograma completo e ' : 'exame',
	'beta hcg' : 'exame',
	'realizou rx de torax ' : 'exame',
	'realizou tc de pescoco, laringe, tireoide, crânio. ' : 'exame',
	'realizou exames laboratoriais ' : 'exame',
	'realizou ecg' : 'exame',
	'realizou cirurgia ' : 'procedimento cirúrgico',
	'cirurgiao cabeca e pescoco' : 'consulta',
	'cirurgiao cabeca e pescoco' : 'consulta',
	'cirurgiao plastico' : 'consulta',
	'realizou exames laboratoriais ' : 'exame',
	'realizou usg de prostata ' : 'exame',
	'realizou exames laboratoriais ' : 'exame',
	'realizou usg de mama' : 'exame',
	'tc de torax' : 'exame',
	'exames laboratoriais' : 'exame',
	'realizou exame de eco b' : 'exame',
	'realizou exames pre-operatorios' : 'exame',
	'avaliacao urgencia oftalmologia' : 'consulta',
	'oftalmologia' : 'consulta',
	'tc de crânio' : 'exame',
	'rx' : 'exame',
	'consulta em carater de urgencia com neurocirurgiao ' : 'consulta',
	'realizou exame eco b ' : 'exame',
	'rm' : 'exame',
	'raio x de torax' : 'exame',
	'ppd' : 'exame',
	'tc de torax' : 'exame',
	'realizado exame de ecocardiograma' : 'exame',
	'realizou fisioterapia' : 'tratamento não medicamentoso',
	'realizou exames de sorologias' : 'exame',
	'realizou o rx de torax' : 'exame',
	'realizou preventivo e usg transvaginal' : 'exame',
	'realizou consulta ' : 'consulta',
	'realizou consulta' : 'consulta',
	'realizou consulta' : 'consulta',
	'realizou consulta com psiquiatra' : 'consulta',
	'exames laboratoriais+eletrocardiograma' : 'exame',
	'teste ergometrico' : 'exame',
	'usg de abdome total, ecocardiograma e mapa' : 'exame',
	'pi prevencao de incapacidade e baar-baciloscopia' : 'exame',
	'endoscopia digestiva alta-eda com biopsia' : 'procedimento cirúrgico',
	'eletrocardiograma' : 'exame',
	'parecer de risco cirurgico ' : 'exame',
	'realizou exame oftalmologico ' : 'exame',
	'realizou anti-hiv -1 , hiv 2' : 'exame',
	'realizou colostomia e biopsia' : 'exame',
	'realizou exame de raio – x' : 'exame',
	'exame laboratoriais' : 'exame',
	'realizou raio-x de torax, hemograma e ecg ' : 'exame',
	'realizou procedimento cirurgico traqueostomia' : 'exame',
	'realizou pccu' : 'exame',
	'realizou exame de colposcopia' : 'exame',
	'raio-x' : 'exame',
	'exames laboratoriais ' : 'exame',
	'realizou conizacao ' : 'procedimento cirúrgico',
	'realizado eeg ' : 'exame',
	'realizou exame audiometria, imitanciometria, eoa e bera' : 'exame',
	'consulta para avaliacao auditiva ' : 'consulta',
	'realizou procedimento cirurgico ' : 'procedimento cirúrgico',
	'realizou exames laboratoriais ' : 'exame',
	'urgencia/internacao' : 'urgência',
	'consulta cirurgiao cabeca e pescoco' : 'consulta',
	'tc de pescoco ' : 'exame',
	'raio-x de ombro' : 'exame',
	'usg de ombro' : 'exame',
	'raio-x de torax' : 'exame',
	'exames laboratoriais' : 'exame',
	'eletrocardiograma ' : 'exame',
	'ecg' : 'exame',
	'raio-x' : 'exame',
	'exame de ultrassonografia de mama' : 'exame',
	'exame de mamografia' : 'exame',
	'core biopsia ' : 'procedimento cirúrgico',
	'realizou exame ' : 'exame',
	'realizou tc de abome superior' : 'exame',
	'realizou ecg ' : 'exame',
	'realizar laboratoriais ' : 'exame',
	'realizou laboratoriais ' : 'exame',
	'realizou exame ' : 'exame',
	'usg transvaginal' : 'exame',
	'consulta' : 'consulta',
	'consulta' : 'consulta',
	'realizou usg abdômen ' : 'exame',
	'ressonância magnetica de coluna' : 'exame',
	'tomografia computadorizada de crânio' : 'exame',
	'anti-hiv –vdrl – hcv – hbsag. ' : 'exame',
	'realizou biopsia de pele que foi coletado pela drª kamila.' : 'procedimento cirúrgico',
	'raio-x de torax' : 'exame',
	'exames laboratoriais' : 'exame',
	'eletrocardiograma ' : 'exame',
	'ecocardiograma' : 'exame',
	'eletrocardiograma' : 'exame',
	'parecer de risco cirurgico ' : 'exame',
	'internacao para procedimento cirurgico de colecistectomia' : 'procedimento cirúrgico',
	'campimetria' : 'exame',
	'gonioscopia, bio de fo, ctd' : 'exame',
	'raio-x de coluna toracica e bacia' : 'exame',
	'exames laboratoriais' : 'exame',
	'realizou exames laboratoriais' : 'exame',
	'eas, hemograma completo, vdrl.' : 'exame',
	'exames laboratoriais' : 'exame',
	'raio x de torax' : 'exame',
	'otorrino' : 'consulta',
	'usg transvaginal ' : 'exame',
	'cirurgia de mioma' : 'procedimento cirúrgico',
	'avaliacao pos- operatorio ' : 'consulta',
	'urgencia ' : 'urgência',
	'usg + exames laboratoriais ' : 'exame',
	'urgencia obstetra' : 'urgência',
	'urgencia obstetra' : 'urgência',
	'urgencia obstetra' : 'urgência',
	'dr. guilherme' : '?',
	'imitoncimetria' : 'exame',
	'servico social ' : '?',
	'realizou sessões de fisioterapia ' : 'tratamento não medicamentoso',
	'neurologia ( urgencia )' : 'urgência',
	'neurologia (urgencia ) ' : 'urgência',
	'ppd' : 'exame',
	'sorologia' : 'exame',
	'rx de punho' : 'exame',
	'exame de usg transvaginal' : 'exame',
	'realizou usg de partes moles, punho d e e mao d e e pe d e e' : 'exame',
	'realizou exame de mamografia' : 'exame',
	'realizou audiometria' : 'exame',
	'foi atendida pela' : '?',
	'realizou exames laboratoriais' : 'exame',
	'realizou exame ecg' : 'exame',
	'realizou raio-x de coluna lombar' : 'exame',
	'realizou exames tc de abdome e eas' : 'exame',
	'rx de tornozelo' : 'exame',
	'realizou rnm' : 'exame',
	'realizou mamografia ' : 'exame',
	'tc de cranio' : 'exame',
	'exame de rnm' : 'exame',
	'realizou tc de face' : 'exame',
	'realizou exame de baar' : 'exame',
	'realizou exames laboratoriais ' : 'exame',
	'consulta cirurgiao de cabeca e pescoco' : 'consulta',
	'tomografia de crânio ' : 'exame',
	'exames laboratoriais e ecg' : 'exame',
	'ultrassonografia de abdome total ' : 'exame',
	'tomografia de crânio, exames laboratoriais ' : 'exame',
	'tomografia de crânio ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'ecografico ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'cirurgia de histerectomia' : 'procedimento cirúrgico',
	'encaminhada à urgencia' : 'urgência',
	'psa total e eas' : 'exame',
	'usg de prostata' : 'exame',
	'exames laboratoriais' : 'exame',
	'usg de vias urinaria' : 'exame',
	'usg de prostata' : 'exame',
	'realizou consulta com cirurgiao geral ' : 'consulta',
	'realizou consulta urgencia' : 'consulta',
	'rnm de coluna dorsal' : 'exame',
	'rnm de coluna lombar' : 'exame',
	'foi avaliado pelo ' : '?',
	'exame laboratorial' : 'exame',
	'realizou consulta com neurocirurgiao' : 'consulta',
	'realizou exame de psa total e eas' : 'exame',
	'eas' : 'exame',
	'realizou usg de prostata' : 'exame',
	'realizou exames laboratoriais' : 'exame',
	'realizou exame de usg' : 'exame',
	'realizou consulta com ' : 'consulta',
	'realizou consulta residente' : 'consulta',
	'realizou exames laboratoriais ' : 'exame',
	'realizou ecocardiograma ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'exame de eas ' : 'exame',
	'hemograma completo tgo-tgp e bioquimica ' : 'exame',
	'endoscopia digestiva alta. ' : 'exame',
	'exames laboratoriais ' : 'exame',
	'ultrassonografia de abdome total com doppler. ' : 'exame',
	'endoscopia digestiva alta. ' : 'exame',
	'ultrassonografia de abdome. ' : 'exame',
	'carga viral da hepatite b, hemograma completo bioquimico. ' : 'exame',
	'usg abdominal' : 'exame',
	'exames de sangue ' : 'exame',
	'rnm de crânio' : 'exame',
	'exames laboratoriais' : 'exame',
	'realizou raio x' : 'exame',
	'exame laboratoriais' : 'exame',
	'realizou eeg' : 'exame',
	'realizou rnm de crânio ' : 'exame',
	'realizou usg de abdome' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais + raio x de torax ' : 'exame',
	'realizou ecg' : 'exame',
	'realizou usg com dopller' : 'exame',
	'exames laboratoriais' : 'exame',
	'realizou usg transvaginal ' : 'exame',
	'usg bolsa escrotal' : 'exame',
	'usg abdome total' : 'exame',
	'tc de abdome' : 'exame',
	'rx de torax' : 'exame',
	'exame de tomografia computadorizada de crânio' : 'exame',
	'ultrassonografia de prostata' : 'exame',
	'ressonância magnetica de pelve' : 'exame',
	'carga viral hepatite b, bioquimica, eas+epf.' : 'exame',
	'ultrassonografia' : 'exame',
	'exames laboratoriais e teste rapido' : 'exame',
	'tc de torax' : 'exame',
	'realizou consulta com dr. wornei' : 'consulta',
	'realizou usg vias urinarias' : 'exame',
	'realizou exames laboratorias' : 'exame',
	'exame realizado audiometria' : 'exame',
	'tc de mastoide' : 'exame',
	'rnm de crânio' : 'exame',
	'tc de crânio' : 'exame',
	'exame  realizado audiometria' : 'exame',
	'tc de mastoide' : 'exame',
	'rnm de crânio ' : 'exame',
	'cintilografia' : 'exame',
	'cintilografia' : 'exame',
	'tomografia de crânio' : 'exame',
	'exame de fan- anticorpos e anti-nucleo.' : 'exame',
	'tc de torax ' : 'exame',
	'baciloscopia' : 'exame',
	'usg de prostata e abdome total ' : 'exame',
	'rx de torax ' : 'exame',
	'raio-x de joelho e e d' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'exame de eas' : 'exame',
	'hemograma completo tgo-tgp e bioquimica' : 'exame',
	'endoscopia digestiva alta.' : 'exame',
	'exames laboratoriais' : 'exame',
	'ultrassonografia de abdome total com doppler.' : 'exame',
	'endoscopia digestiva alta.' : 'exame',
	'ultrassonografia de abdome.' : 'exame',
	'carga viral da hepatite b, hemograma completo bioquimico.' : 'exame',
	'usg abdominal ' : 'exame',
	'exames de sangue' : 'exame',
	'rnm de coluna cervical' : 'exame',
	'atendimento em carater de urgencia ' : 'urgência',
	'atendimento em carater de urgencia' : 'urgência',
	'realizou usg transvaginal' : 'exame',
	'foi avaliada pelo clinico geral' : 'consulta',
	'consulta' : 'consulta',
	'consulta de urgencia' : 'consulta',
	'realizou consulta ' : 'consulta',
	'realizou raio-x torax ' : 'exame',
	'realizou exame laboratoriais' : 'exame',
	'realizou exame ecg' : 'exame',
	'realizou usg de prostata' : 'exame',
	'realizou ecg' : 'exame',
	'realizou raio   x de torax' : 'exame',
	'realizou exames laboratoriais' : 'exame',
	'realizou consulta com cirurgiao' : 'exame',
	'realizou consulta clinico geral' : 'consulta',
	'raio x torax e hmg completo' : 'exame',
	'urgencia' : 'urgência',
	'hemograma, bioquimica, glicemia, tgo +tgp' : 'exame',
	'sorologia' : 'exame',
	'exames laboratoriais' : 'exame',
	'tc bacia/pelve' : 'exame',
	'usgs torax, pelve e abdome' : 'exame',
	'raio x torax' : 'exame',
	'urgencia' : 'urgência',
	'cirurgiao' : 'consulta',
	'cirurgiao' : 'consulta',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'raio x torax' : 'exame',
	'ecg' : 'exame',
	'realizou avaliacao de rx de face' : 'exame',
	'realizou usg  transvaginal' : 'exame',
	'raio x de torax ' : 'exame',
	'realizou ecg' : 'exame',
	'exames laboratoriais ' : 'exame',
	'exame eas' : 'exame',
	'realizou usg transvaginal' : 'exame',
	'teste rapido para hiv 1 e 2, vdrl' : 'exame',
	'tc de torax' : 'exame',
	'exames laboratoriais' : 'exame',
	'baar e ppd ' : 'exame',
	'tc de abdome e pelve' : 'exame',
	'hemograma' : 'exame',
	'qt ' : 'tratamento',
	'exames laboratoriais' : 'exame',
	'realizou o exame de ecocardiograma' : 'exame',
	'exames laboratoriais' : 'exame',
	'realizou tc de abdome superior pelve bacia e pescoco' : 'exame',
	'mi realizado exame de tcs' : 'exame',
	'foi avaliado pelo cirurgiao geral' : 'consulta',
	'foi avaliado pela medica ' : 'consulta',
	'foi atendido ' : '?',
	'atendido pela ' : '?',
	'internacao /cirurgia ' : 'procedimento cirúrgico',
	'curativo ' : 'curativo',
	'foi avaliada em carater de urgencia ' : 'urgência',
	'consulta de pos-operatorio ' : 'consulta',
	'foi avaliado pela buco maxilo' : 'consulta',
	'realizou exame rx' : 'exame',
	'realizou consulta  ' : 'consulta',
	'carga viral de hepatite b, pcr de delta, hemograma completo, bioquimica tgo+tgp, eas+epf.' : 'exame',
	'exame de ultrassonografia de abdome superior' : 'exame',
	'realizou exame laboratoriais' : 'exame',
	'realizou exame laboratoriais ' : 'exame',
	'exames laboratoriais' : 'exame',
	'cirurgiao geral' : 'consulta',
	'cirurgiao geral' : 'consulta',
	'cirurgiao geral' : 'consulta',
	'rm de pelve' : 'exame',
	'carga viral, hemograma completo.' : 'exame',
	'eas e epf' : 'exame',
	'eda c/ biopsia' : 'procedimento cirúrgico',
	'raio x' : 'exame',
	'exames laboratoriais' : 'exame',
	'ecg + risco cirurgico' : 'exame',
	'exames laboratoriais ' : 'exame',
	'tx hepatico com dr. tarcisio.' : 'exame',
	'realizou retirada de ponto do local da cirurgia ' : 'procedimento de remoção dos fios cirúrgicos',
	'realizou usg de abdômen ' : 'exame',
	'exames laboratoriais' : 'exame',
	'exames laboratoriais' : 'exame',
	'clearance de creatinina, proteinuria de 24h' : 'exame',
	'usg de prostata' : 'exame',
	'raio-torax, hemograma completo' : 'exame',
	'hemograma completo' : 'exame',
	'tomografia do torax' : 'exame',
	'endoscopia digestiva alta' : 'exame',
	'exames laboratoriais' : 'exame',
	'usg de abdome superior' : 'exame',
	'continuidade em seu tratamento de tfd' : '?',
	'realizou exames laboratoriais' : 'exame',
	'realizou consulta as' : 'consulta'
}