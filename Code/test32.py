import mysql.connector
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "*********",
    database = "Grades_Schedule"
)

mycursor = mydb.cursor()


Lessons_Numbers = []
Lessons_Names = []
mycursor.execute('select * from AutumnExams')
for db in mycursor:
    lista = []
    for i in db:
        if (i != None):
            lista.append(i)
            print(i)
    Lessons_Names.append(lista.pop(0))
    Lessons_Numbers.append(lista)
    
print(Lessons_Names, Lessons_Numbers)
print(int(math.ceil(Lessons_Numbers[-1][-2])))
dates_file = open('/Users/alexandroskyriakakis/MyProjects/Python_Projects/Project_One/EXAMS SCHEDULE/18-19 Autumn/excel/Lessons_Names.txt', encoding = 'utf-8', mode = 'r+')
#print(dates_file.read().split('\n'))
All_data = dates_file.read().split('\n')
Lessons = []
Dates = []
k,l = 0,0
for d in All_data:
    if (d == ''): continue
    if ('[' in d):
        Lessons.append(d[:d.index('[')])
        Dates.append(d[d.index('[') + 1:d.index(']')])
Dates = list(map(lambda i: list(map(lambda j: int(j),i.split(','))), Dates))
Lessons_copy = []
for i in Lessons:
    Lessons_copy.append(i[:-1])
Dates_Clas = []
for d in Dates:
    Dates_Clas.append(datetime.datetime(d[2],d[1],d[0]))
    
print(Lessons_copy, Dates, (Dates_Clas[1] + datetime.timedelta(days=10)).strftime("%x"), len(Lessons), len(Dates))
print(Lessons_Numbers[Lessons_Names.index(Lessons_copy[6])])
fileout = open('/Users/alexandroskyriakakis/MyProjects/Python_Projects/Project_One/EXAMS SCHEDULE/18-19 Autumn/excel/emojiList.json', encoding = 'utf-8', mode = 'w+')
Data_For_Page = []
print ('[\n', file = fileout)
indexb = 0
for w in Lessons_copy:
    if ( w == '' or Lessons_Numbers[Lessons_Names.index(w)] == [] ): continue
    a = Dates_Clas[indexb] + datetime.timedelta(  days= int(  math.ceil( Lessons_Numbers[Lessons_Names.index(w)][-2])))
    print('  {\n    "title": "'+ w + ' Expected Grades Release: ' + (a).strftime("%x") + '",\n    "keywords": "' + w + '"\n  },', file = fileout)
    indexb += 1
print(']', file = fileout)

