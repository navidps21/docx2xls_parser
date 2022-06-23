#import functions
from docx import Document
from datetime import *
import re as r
from matplotlib.pyplot import text
import xlwt


def get_raw_tables_data (wordDoc):
    raw_data = []
    data = []

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

        else:
            temp_data = raw_data[i]

        temp_data = temp_data.replace("\n", ' ').replace('  ',' ')
        
        if ':' in temp_data:
            data.append(temp_data)

    #for i in data:
    #    print(i)
    
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
    lc_fullText = []
    for i in fullText:
        lc_fullText.append(i.lower().replace('ç', 'c').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ã', 'a').replace('ê', 'e'))
        
    #print(lc_fullText)
    return (lc_fullText)

def lowercase_table (tables_data):
    lc_tablesdata = []
    for i in tables_data:
        lc_tablesdata.append(i.lower().replace('ç', 'c').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ã', 'a').replace('ê', 'e'))
        
    #print(lc_tablesdata)
    return (lc_tablesdata)

def get_year (fullText):
    #get the year of the document

    for i in fullText:
        if 'Manaus,' in i:
            temp_year = i
            year = r.search(r"\d{4}", temp_year).group(0)
            label = 'ANO: '
            return (label + year)

def get_month (fullText):
    #get the month of the document

    month = 'MÊS: '
    for i in fullText:
        if 'Manaus,' in i:
            temp_month = i
            if 'Janeiro' in temp_month:
                month = month + '01'
                return month
            elif 'Fevereiro' in temp_month:
                month = month + '02'
                return month
            elif 'Março' in temp_month:
                month = month + '03'
                return month
            elif 'Abril' in temp_month:
                month = month + '04'
                return month
            elif 'Maio' in temp_month:
                month = month + '05'
                return month
            elif 'Junho' in temp_month:
                month = month + '06'
                return month
            elif 'Julho' in temp_month:
                month = month + '07'
                return month
            elif 'Agosto' in temp_month:
                month = month + '08'
                return month
            elif 'Setembro' in temp_month:
                month = month + '09'
                return month
            elif 'Outubro' in temp_month:
                month = month + '10'
                return month
            elif 'Novembro' in temp_month:
                month = month + '11'
                return month
            elif 'Dezembro' in temp_month:
                month = month + '12'
                return month

def get_gender ():
    gender = 'SEXO: '
    return gender

def get_age (tables_data):
    #get age between birth and document date

    for i in tables_data:
        if 'DN:' in i:
            born_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            born = convert_year(born_temp)
            born = datetime.strptime(born, "%d/%m/%Y").date()
        if 'DATA DO INGRESSO:' in i:
            today_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            today = convert_year(today_temp)
            today = datetime.strptime(today, "%d/%m/%Y").date()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    age_data = 'IDADE: '
    age_data = age_data + str(age)
    
    indices = [i for i, s in enumerate(tables_data) if 'DN:' in s]
    tables_data.insert(indices[0]+10, age_data)

    return (tables_data)

def get_time (tables_data):
    #get time in hospital

    for i in tables_data:
        if 'DATA DO INGRESSO:' in i:
            start_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            init = convert_year(start_temp)
            init = datetime.strptime(init, "%d/%m/%Y").date()
        if 'DATA DA ALTA:' in i:
            end_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            finish = convert_year(end_temp)
            finish = datetime.strptime(finish, "%d/%m/%Y").date()

    time = finish - init

    time_data = 'TEMPO DE INTERNAÇÃO: '
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

    date_temp = str(r.findall(r'/(.{2}$)', date)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
    date_temp = int(date_temp)
    if date_temp <= 23:
        complete = '20'
        date_temp = str(date_temp)
        date_new = complete + date_temp
    else:
        complete = '19'
        date_temp = str(date_temp)
        date_new = complete + date_temp

    date = date[:-2] + date_new

    return (date)

def get_companion(tables_data):
    #This function return if the pacient have companion

    companion = 'ACOMPANHANTE: '
    for i in tables_data:
        if 'NOME DO ACOMPANHANTE:' in i:
            companion_temp = str(r.findall(r':(.*)', i)).replace("[' ", '').replace(" ']", '').replace("['", '').replace("']", '')
            if len(companion_temp) >= 5:
                companion = companion + "S"
                return companion
            else:
                companion = companion + "N"
                return companion

def get_neglecteddiseases (text_data):

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

    neglected = 'DOENÇA NEGLIGENCIADA: '

    for i in new_text:
        for j in neglecteddiseases:
            if j in i:
                neglected = neglected + 'S'
                return (neglected)
    
    neglected = neglected + 'N'
    return (neglected)

def get_giveup(text_data):
    #this function return if pacient give up or not
    giveup = 'DESISTÊNCIA: '

    lc_text = lowercase_text(text_data)

    for i in lc_text:
        if 'desist' in i:
            giveup = giveup + "S"
            return giveup

    giveup = giveup + "N"
    return giveup

def get_internment(text_data):
    #this function return if pacient were internment or not
    internment = 'INTERNAÇÃO HOSPITALAR: '
    
    lc_text = lowercase_text(text_data)

    for i in lc_text:
        if 'interna' in i:
            internment = internment + "S"
            return internment

    internment = internment + "N"
    return internment

def get_provdischarge (text_data):
    #this functions return if pacient had a provisional discharge
    #this function return if pacient give up or not

    provdischarge = 'ALTA PROVISÓRIA: '

    new_text = lowercase_text(text_data)

    for i in new_text:
        if 'paciente de alta provisoria para seu municipio de origem' in i:
            provdischarge = provdischarge + "S"
            return provdischarge

    provdischarge = provdischarge + "N"
    return provdischarge

def get_problemsolved (tables_data):
    #this function return if the problem were solved
    problemsolved = 'PROBLEMA RESOLVIDO: '
    for i in tables_data:
        if 'ALTA PROVISÓRIA: N' in i:
            for i in tables_data:
                if 'DESISTÊNCIA: S' in i:
                    problemsolved = problemsolved + 'N'
                if 'DESISTÊNCIA: N' in i:
                    problemsolved = problemsolved + 'S'
        if 'ALTA PROVISÓRIA: S' in i:
            problemsolved = problemsolved + 'N'
        
    indices = [i for i, s in enumerate(tables_data) if 'ALTA PROVISÓRIA:' in s]
    tables_data.insert(indices[0]+1, problemsolved)

    return (tables_data)

def get_conditition (text_data):
    #this function return the pacient situation
    
    pacientcond = 'SITUAÇÃO DO PACIENTE: '

    cont = []

    for i in text_data:
        if 'PENDENCIAS EM FILA DE ESPERA NO SISREG' in i:
            indice_1 = [i for i, s in enumerate(text_data) if 'PENDENCIAS EM FILA DE ESPERA NO SISREG' in s]
            cont.append(indice_1[0])
        if 'CRONOGRAMA DE RETORNO CONSULTA/EXAME/CIRURGIA' in i:
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

    indice = max(cont)

    pacientcond = pacientcond + str(text_data[indice+1:])

    return(pacientcond.replace('OBS:', 'OBS.').replace("['",'').replace("', '", '').replace("']", '').replace('  ', ''))

def get_specialty (dict, tables_data):

    new_table = lowercase_table(tables_data)

    #print(new_table)

    specialty = 'ESPECIALIDADES: '

    for i in new_table:
        for j in dict:
            if j in i:
                if specialty.find(str(dict[j])) == -1 :
                    specialty = specialty + str(dict[j]) + '; '

    return specialty

def get_path(file_path, abs_path):
    #get path of the project and generate a hyperlink

    path = 'CAMINHO: file:///'
    path = path + str(abs_path) + '\\' + str(file_path)
    path = path.replace("\\","/")
    return (path)

def organizer (tables_data):
    #organize the table
    new_table = ['s'] * 27
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
        elif 'TEMPO DE INTERNAÇÃO:' in i:
            new_table[11] = i
        elif 'HD:' in i:
            new_table[12] = i
        elif 'ESPECIALIDADES:' in i:
            new_table[13] = i
        elif 'CONDIÇÃO DO INGRESSO:' in i:
            new_table[14] = i
        elif 'CONDIÇÃO DO EGRESSO:' in i:
            new_table[15] = i
        elif 'INTERNAÇÃO HOSPITALAR:' in i:
            new_table[16] = i
        elif 'DESLOCAMENTO:' in i:
            new_table[17] = i
        elif 'PARA:' in i:
            new_table[18] = i
        elif 'MEIO DE TRANSPORTE:' in i:
            new_table[19] = i
        elif 'ACOMPANHANTE:' in i:
            new_table[20] = i
        elif 'ALTA PROVISÓRIA:' in i:
            new_table[21] = i
        elif 'DOENÇA NEGLIGENCIADA:' in i:
            new_table[22] = i
        elif 'SITUAÇÃO DO PACIENTE:' in i:
            new_table[23] = i
        elif 'PROBLEMA RESOLVIDO:' in i:
            new_table[24] = i
        elif 'DESISTÊNCIA:' in i:
            new_table[25] = i
        elif 'CAMINHO:' in i:
            new_table[26] = i
    return new_table

def get_data (wordDoc, dict, file_path, abs_path):
    #generate tables_data
    
    tables_data = get_tables_data(wordDoc)

    raw_tables_data = get_raw_tables_data (wordDoc)

    text_data = get_text(wordDoc)

    tables_data.insert(0, get_year(text_data))

    tables_data.insert(1, get_month(text_data))

    tables_data.insert(2, get_gender())

    tables_data = get_age(tables_data)

    tables_data = get_time(tables_data)

    tables_data.append(get_specialty(dict, raw_tables_data))

    tables_data.append(get_companion(tables_data))

    tables_data.append(get_provdischarge(text_data))

    tables_data.append(get_giveup(text_data))

    tables_data = get_problemsolved(tables_data)

    tables_data.append(get_neglecteddiseases(text_data))

    tables_data.append(get_conditition(text_data))

    tables_data.append(get_internment(text_data))

    tables_data.append(get_path(file_path, abs_path))

    new_table = organizer(tables_data)

    return new_table

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
        'anestesiologia' : 'ANESTESIOLOGIA',
        'angiologia' : 'ANGIOLOGIA',
        'cardio' : 'CARDIOLOGISTA',
        'cirurgia cardiovascular' : 'CIRURGIA CARDIOVASCULAR',
        'cirurgia da mao' : 'CIRURGIA DA MÃO',
        'cirurgiao de cabeca e pescoco' : 'CIRURGIÃO DE CABEÇA E PESCOÇO',
        'cirurgia de cabeca e pescoco' : 'CIRURGIÃO DE CABEÇA E PESCOÇO',
        'cirurgiao cabeca e pescoco' : 'CIRURGIÃO DE CABEÇA E PESCOÇO',
        'cirurgia do aparelho digestivo' : 'CIRURGIA DO APARELHO DIGESTIVO',
        'cirurgia geral' : 'CIRURGIA GERAL',
        'cirurgia oncologica' : 'CIRURGIA ONCOLÓGICA',
        'cirurgia pediatrica' : 'CIRURGIA PEDIÁTRICA',
        'cirurgiao plastico' : 'CIRURGIÃO PLÁSTICO',
        'cirurgia plastica' : 'CIRURGIÃO PLÁSTICO',
        'cirurgia torácica' : 'CIRURGIA TORÁCICA',
        'cirurgia vascular' : 'CIRURGIA VASCULAR',
        'clinica medica' : 'CLÍNICO',
        'clinico' : 'CLÍNICO',
        'coloproctologia' : 'COLOPROCTOLOGIA ',
        'dermato' : 'DERMATOLOGISTA',
        'endocrino' : 'ENDÓCRINO',
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
        'mastologia' : 'MASTOLOGIA',
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
        'neurolog' : 'NEUROLOGISTA',
        'nutrologia' : 'NUTROLOGIA',
        'oftalmo' : 'OFTALMOLOGISTA',
        'onco' : 'ONCOLOGISTA',
        'ortoped' : 'ORTOPEDISTA',
        'otorrino' : 'OTORRINOLARINGOLOGIA',
        'patolog' : 'PATOLOGIA',
        'patologia clínica/medicina laboratorial' : 'PATOLOGIA CLÍNICA/MEDICINA LABORATORIAL',
        'pediatria' : 'PEDIATRIA',
        'pneumolog' : 'PNEUMOLOGISTA',
        'psiquiat' : 'PSIQUIATRIA',
        'radiolog' : 'RADIOLOGIA E DIAGNÓSTICO POR IMAGEM',
        'radioterapia' : 'RADIOTERAPIA',
        'reumatolo' : 'REUMATOLOGISTA ',
        'urolo' : 'UROLOGISTA',
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