import mysql.connector
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

#Apply Harmonic Series to results
def Harmonic_Series (lista):
    if (len(lista) == 0): return lista
    if (len(lista) == 1): return np.random.normal(lista[0], 1, 100)
    else:
        Result_list = []
        lcm = 0
        freq_list = Aux_Series(lista) # [33,45,67] -> [3,2,1] 
        if (len(lista) == 2): lcm =  2
        else: lcm = np.lcm.reduce(freq_list) # lcm = 6
        for i in freq_list:
            for j in np.random.normal(lista[freq_list.index(i)], 1, 100*(lcm//i)): #Randomize the result
                Result_list.append(j) #6/3 = 2 -> [33,33,45,45,45,67,67,67,67,67,67]
        return Result_list
    
def Aux_Series (lista):
    result = []
    for i in lista:
        result.append(len(lista) - lista.index(i))
    return result

#Connect to database
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "***********",
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
            #print(i)
    Lessons_Names.append(lista.pop(0))
    Lessons_Numbers.append(lista)
    
a = list(map(Harmonic_Series,Lessons_Numbers)) 
Mean_Std = []
j = 0

#Update Database with Mean and STD
for i in a:
    print(Lessons_Numbers[j])
    mean, std = np.mean(i), np.std(i)
    print(mean, std, stats.norm(mean, std).cdf(30), '\n')
    if (math.isnan(mean)):
        Mean_Std.append([None,None])
        sqlFormula1 = "update "+ 'AutumnExams' +" set std = "+ 'NULL' +" where lessons_name = ('"+ Lessons_Names[j] +"')"
        sqlFormula2 = "update "+ 'AutumnExams' +" set mean = "+ 'NULL' +" where lessons_name = ('"+ Lessons_Names[j] +"')"
        mycursor.execute(sqlFormula1)
        mycursor.execute(sqlFormula2)
        mydb.commit()
    else:
        Mean_Std.append([mean, std])
        sqlFormula1 = "update "+ 'AutumnExams' +" set std = "+ str(std) +" where lessons_name = ('"+ Lessons_Names[j] +"')"
        sqlFormula2 = "update "+ 'AutumnExams' +" set mean = "+ str(mean) +" where lessons_name = ('"+ Lessons_Names[j] +"')"
        mycursor.execute(sqlFormula1)
        mycursor.execute(sqlFormula2)
        mydb.commit()
    j+=1

print(len(a), len(Lessons_Numbers), len(Lessons_Names), len(Mean_Std))
print(Mean_Std)
print(Lessons_Numbers[1], np.mean(a[1]), stats.norm(np.mean(a[1]), np.std(a[1])).pdf(33.))
