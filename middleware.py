#import functions
from docx import Document
from datetime import *
import re as r
import xlwt


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

        else:
            temp_data = raw_data[i]

        temp_data = temp_data.replace("\n", '')
        
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
    #return '\n'.join(fullText)
    print (fullText)
    return (fullText)

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
    tables_data.insert(indices[0]+1, age_data)

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
            if len(companion) >= 5:
                companion = companion + "S"
                return companion
            else:
                companion = companion + "N"
                return companion

def get_giveup(text_data):
    #this function return if pacient give up or not
    giveup = 'DESISTÊNCIA: '
    for i in text_data:
        if 'desist' in i:
            giveup = giveup + "S"
            return giveup
        elif 'Desist' in i:
            giveup = giveup + "S"
            return giveup
        else:
            giveup = giveup + "N"
            return giveup

def get_provdischarge (text_data):
    #this functions return if pacient had a provisional discharge
    #this function return if pacient give up or not
    provdischarge = 'ALTA PROVISÓRIA: '
    for i in text_data:
        if 'ALTA PROVISÓRIA PARA SEU MUNICÍPIO DE ORIGEM' in i:
            provdischarge = provdischarge + "S"
            return provdischarge
        else:
            provdischarge = provdischarge + "N"
            return provdischarge

def get_problemsolved (tables_data):
    #this function return if the problem were solved
    problemsolved = 'PROBLEMA RESOLVIDO: '
    for i in tables_data:
        if 'ALTA PROVISÓRIA: N' in i:
            problemsolved = problemsolved + 'S'
        if 'ALTA PROVISÓRIA: S' in i:
            problemsolved = problemsolved + 'N'
        
    indices = [i for i, s in enumerate(tables_data) if 'ALTA PROVISÓRIA:' in s]
    tables_data.insert(indices[0]+1, problemsolved)

    return (tables_data)

def get_path(file_path, abs_path):
    #get path of the project and generate a hyperlink

    path = 'CAMINHO: file:///'
    path = path + str(abs_path) + '\\' + str(file_path)
    path = path.replace("\\","/")
    return (path)

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