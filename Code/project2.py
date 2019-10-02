from operator import itemgetter
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
import unicodedata, os, sys, requests, xlrd, re, random, codecs
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "*********",
    database = "Grades_Schedule"
)
#file_txt = open("/Users/alexandroskyriakakis/MyProjects/Python_Projects/All_Lessons.txt", encoding='utf-8', mode='r+')
#Lessons = file_txt.read().split('\n') #list of strings
#Lessons = tuple(Lessons)
#Lessons = list(filter(lambda i:i is not '',Lessons))
#print (Lessons)
mycursor = mydb.cursor()
#student1 = ("λογικη σχεδιαση")
#     tables = ['SummerExams', 'WinterExams', 'AutumnExams']
#for table_i in tables:
#for table in tables:
#    for les in Lessons:
#        #tuple_i = ('"' + les + '"')
#        #print(tuple_i)

def Max_common_letters_in_words (lesson, posts_content):
     max_sentence_size = 0
     for lesson_word_i in lesson:
          max_word_size = 0
          for post_word_j in posts_content:
               if (lesson_word_i == post_word_j):
                    length_of_common_letters = len(lesson_word_i)
                    if (length_of_common_letters > max_word_size):
                        max_word_size = length_of_common_letters
          max_sentence_size += max_word_size 
     return max_sentence_size



def Create_List_with_all_data():
    global Lessons
    global ResultsAlpha
    CommonLetters = []
    for lesson_i in Lessons:
        max_common_letter_post = 0
        for result_j in ResultsAlpha:
            a = Max_common_letters_in_words (lesson_i,result_j)
            if (max_common_letter_post <= a):
                max_common_letter_post = a
                if (a != 0): 
                 CommonLetters.append([a , list(filter(lambda j: j in result_j, lesson_i)) , result_j , lesson_i])
    return CommonLetters
                   


def Repeat_Idea ():
    Repeated_list = []
    while ((Lessons != [] and ResultsAlpha != [])):
        CommonLetters = Create_List_with_all_data() 
        CommonLetters.sort(key=itemgetter(0))
        CommonLetters.reverse()
        if (CommonLetters == []): break
        current_max_value = CommonLetters.pop(0)
        #print (current_max_value)
        if (current_max_value[2] in ResultsAlpha):
            ResultsAlpha.remove(current_max_value[2])
        if ((current_max_value[3] in Lessons)):
            Lessons.remove(current_max_value[3])
        Repeated_list.append(current_max_value)
        CommonLetters = []
    return Repeated_list


Running_Tuples = [
     "18-19 Winter","18-19 Summer","18-19 Autumn",
     "17-18 Winter", "17-18 Summer","17-18 Autumn",
     "16-17 Winter","16-17 Summer","16-17 Autumn",
     "15-16 Winter","15-16 Summer","15-16 Autumn",
     "14-15 Winter","14-15 Summer","14-15 Autumn",
     "13-14 Winter","13-14 Summer","13-14 Autumn",
     "12-13 Winter","12-13 Summer","12-13 Autumn",
     "11-12 Winter","11-12 Summer","11-12 Autumn"
]

input_i = input("")
tuple_i = Running_Tuples[int(input_i)]
Current_Results = open("/Users/alexandroskyriakakis/MyProjects/Python_Projects/Project_One/EXAMS SCHEDULE/" + tuple_i + "/excel/ResultsOnly.txt","r+")

print(tuple_i.split(' ')[1])
print(tuple_i.split(' ')[0][3:])

                                      
#List Of Lessons
All_Lessons = open("/Users/alexandroskyriakakis/MyProjects/Python_Projects/All_Lessons.txt",encoding='utf-8', mode='r+')
Lessons = All_Lessons.read().split('\n') #list of strings
Lessons = list(map(str.split,Lessons)) #list of list of words
Lessons_Copy = Lessons[:]
#List of current tracked lessons

Results = Current_Results.read().split('\n') #list of strings
ResultsNum = list(map(lambda i: ''.join(list(filter(str.isnumeric,i))),Results))
Results = list(map(str.split,Results)) #list of list of words
ResultsAlpha = list(map(lambda i: i[:len(i)-1], Results))
ResultsAlpha_Copy = ResultsAlpha[:]
All = Repeat_Idea()
print (ResultsNum)
print(ResultsAlpha)
Return_Result = []

#Update Database with Data from past years
for All in All:
    if (All[0] > 8):
         sqlFormula = "update "+ tuple_i.split(' ')[1] +'Exams' +" set year_20"+ tuple_i.split(' ')[0][3:] +" = " +str(ResultsNum[ResultsAlpha_Copy.index(All[2])]) +" where lessons_name = ('"+ ' '.join(All[3]) +"')"
         mycursor.execute(sqlFormula)
         mydb.commit() #Save Data
