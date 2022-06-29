#Import functions
from middleware import *


#Run the automation for all files
run_automation()


#Run the automation for one specific file
"""
#Get document in path
#file_path = 'data\CONTRA REF 2019\MAO\OUTUBRO\ARGEL PALHETA DE MENEZES.docx'
file_path = 'data\Contra Referência 2020\AGOSTO\MAO\POLIANA DE OLIVEIRA GUEDES.docx'

wordDoc = Document(file_path)
abs_path = os.path.abspath(os.curdir)
abs_path = abs_path + '/' + file_path

#Get data from the tables and text
tables_data = get_data(wordDoc, specialist_dict, abs_path)
create_sheet(tables_data)

print ('Work done!')

"""