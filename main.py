#Import functions
from middleware import *


#Run the automation for all files

run_automation()


#**********************************************************
#Run the automation for one specific file

"""

#Get document in path
#file_path = 'data\CONTRA REF 2019\MAO\OUTUBRO\ARGEL PALHETA DE MENEZES.docx'
file_path = 'data/CONTRA-REF. 2018/ARN/SETEMBRO/INELDINA AZEVEDO ARAUJO.docx'

wordDoc = Document(file_path)
abs_path = os.path.abspath(os.curdir)
abs_path = abs_path + '/' + file_path

#Get data from the tables and text
tables_data = get_data(wordDoc, ethnicity_dict, specialist_dict, conditionsensitive_dict, servicereceived_dict, hd_dict, hospital_dict, abs_path)
create_sheet(tables_data)

print ('Work done!')

"""


#**********************************************************
#Get any collum data in the sheet

#get_dataintext ('atendimento recebido')

#get_dataintext_adult ('atendimento recebido')

#get_examsperformed ('especialista')