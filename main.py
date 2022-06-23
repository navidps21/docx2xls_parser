#Import functions
from middleware import *
import os


#Get document in path
#file_path = 'data\CONTRA REF 2019\MAO\OUTUBRO\ARGEL PALHETA DE MENEZES.docx'
file_path = 'data\CONTRA REF 2019\MAO\OUTUBRO\PAULO CESAR M. DO ROSARIO.docx'

wordDoc = Document(file_path)

#get project's path
abs_path = os.path.abspath(os.getcwd())

#Get data from the tables and text
tables_data = get_data(wordDoc, specialist_dict, file_path, abs_path)

text_data = get_text(wordDoc)
#print (tables_data)

print ('Work done!')

#Create sheet
create_sheet(tables_data)