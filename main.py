#Import functions
from middleware import *
import os


#Get document in path
file_path = 'data\CONTRA REF 2019\MAO\OUTUBRO\ARGEL PALHETA DE MENEZES.docx'
wordDoc = Document(file_path)

abs_path = os.path.abspath(os.getcwd())

#Get data from the tables and text
tables_data = get_tables_data(wordDoc)

text_data = get_text(wordDoc)

tables_data.insert(0, get_year(text_data))

tables_data.insert(1, get_month(text_data))

tables_data.insert(2, get_gender())

tables_data = get_age(tables_data)

tables_data = get_time(tables_data)

tables_data.append(get_companion(tables_data))

tables_data.append(get_provdischarge(text_data))

tables_data = get_problemsolved(tables_data)

tables_data.append(get_giveup(text_data))

tables_data.append(get_path(file_path, abs_path))

print (tables_data)

#Create sheet
create_sheet(tables_data)