from operator import itemgetter
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
#from datetime import date
import unicodedata, os, sys, requests, xlrd, re, random

class date:
    def __init__(self,day,month,year):
        self.day = day
        self.year = year
        self.month = month
    def sub (self, other):
        return (self.year - other.year)*365 + (self.month - other.month)*30 + (self.day - other.day)

#Function return dates
Months = ['ιαν', 'φεβ', 'μαρ', 'απρ', 'μαιος', 'ιουν', 'ιουλ', 'αυγ', 'σεπ', 'οκτ','νοεμ', 'δεκ']
    
def Aux_Define_Dates (word):
    global Months
    return (word in Months)

def Define_dates (list_of_words):
    global Months
    only_month = list(filter(Aux_Define_Dates, list_of_words))
    day = int(re.sub("[^0-9]", "", list_of_words[list_of_words.index(only_month[0]) + 1]))
    month = int(Months.index(only_month[0]) + 1)
    year =  int(re.sub("[^0-9]", "", list_of_words[list_of_words.index(only_month[0]) + 2]))
    return [day, month, year]



#Read and Extract from Excel
Excel_Cell_Values = []


def Extract_From_Excel (folder):
    book = xlrd.open_workbook("/Users/alexandroskyriakakis/MyProjects/Python_Projects/Project_One/EXAMS SCHEDULE/" + folder + "/excel/Read_Info.xlsx")
    global Excel_Cell_Values
    for book_sheet_i in range(book.nsheets):
        current_sheet = book.sheet_by_index(book_sheet_i)
        for row_j in range(current_sheet.nrows):
            for column_k in range(current_sheet.ncols):
                current_cell = current_sheet.cell(row_j,column_k)
                if (current_cell.value != '' and type(current_cell.value) is str):
                    Excel_Cell_Values.insert(len(Excel_Cell_Values),current_cell.value)


                    
#Track Information From "shmmy.ntua.gr"
Release_dates_of_posts = []
Content_of_Posts = []

def Track_shmmy_Data (page_id, no_of_pages):
    global Release_dates_of_posts
    global Content_of_Posts
    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15' }
    next_page = 0
    
    while (next_page <= no_of_pages):
        URL = 'https://shmmy.ntua.gr/forum/viewtopic.php?f=290&t='+ page_id + '&start=' + str(next_page)
        page = requests.get(URL, headers = headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        date = soup.findAll( "p", {"class": "author"})
        for author in date:
            Release_dates_of_posts.append(author.text)
        post = soup.findAll ( "div", {"class" : "content"})
        for content in post:
            Content_of_Posts.append(content.text)
        next_page += 20
    #print (Release_dates_of_posts[5], Content_of_Posts[5],page_id)

#Function to keep only letters
def Keep_only_letters (list_of_words):
    only_letters_list = []
    for word_i in list_of_words:
        word_i.replace("-"," ")
        word_i.replace("\n"," ")
        word_i.replace("\b"," ")
        current_word = ''.join(filter(str.isalpha, word_i))
        if (current_word == ''): list_of_words.remove(word_i)
        else: only_letters_list.append(current_word)
    return only_letters_list

    
#Function that removes accents (') in a given string


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


#Tracking the dates on excel       ----day/month/year----
Excel_lessons_date_of_exam = []

def Track_Dates_in_posts (list_of_strings):
    current_date_of_exam = [0,0,0]
    for cell_i in list_of_strings:
      #  print (cell_i,type(cell_i))
        a = re.search("\d\d/\d\d/\d\d\d\d", cell_i)
        if (a == None): Excel_lessons_date_of_exam.append(current_date_of_exam)
        else:
            current_date_of_exam = a.group().split('/')
            current_date_of_exam = list(map(int, current_date_of_exam))
            Excel_lessons_date_of_exam.append(current_date_of_exam)
            
    
#Remove some meaningless words 
Meaningless_Words = ['εξαμηνο','για','ηλ', 'αμφ', 'αιθ','και','η','το','τα','ο','οι','&','\n','της','των','απο','στα','στο','στη','επι', 'πτυχιο', 'πτυχιω', 'θεματα', 'με','την']


def Remove_Meaningless_Words (words):
    global Meaningless_Words
    return list(w for w in words if w not in Meaningless_Words)

#Do the changes, input string return list

def Normalize (Input_String):
     a = (remove_accents(Input_String.lower())).split() #Lowercase, remove accents, make list of words
     a = Remove_Meaningless_Words (a)
     return a


def Remove_words_greater_than_six (Input_list_of_words):
    Output_list_of_words = []
    index = 0
    while (index < len(Input_list_of_words) and index < 8):
        Output_list_of_words.append(Input_list_of_words[index])
        index += 1
    return Output_list_of_words

#For a lesson search a post for common words and returns the number of letters in common words 


def Max_common_letters_in_words (lesson, posts_content):
     max_sentence_size = 0
     for lesson_word_i in lesson:
          max_word_size = 0
          for post_word_j in posts_content:
               if (lesson_word_i == post_word_j):
                    length_of_common_letters = len(lesson_word_i)
                    if (length_of_common_letters > max_word_size): max_word_size = length_of_common_letters
          max_sentence_size += max_word_size 
     return max_sentence_size




#For each one of excel cells we put in the list the post with the most common letters with the cell 
CommonLetters_Post_CellValue_Date = []     

def Create_List_with_all_data(Content_of_Posts_copy):
    for Excel_value_j in Excel_Cell_Values:
        max_common_letter_post = 0
        for Post_i in Content_of_Posts:
            a = Max_common_letters_in_words (Excel_value_j,Post_i)
            
            if (max_common_letter_post <= a):
                max_common_letter_post = a
                if (a != 0):
                    exam_date = Excel_lessons_date_of_exam[Excel_Cell_Values_Copy.index(Excel_value_j)]
                    grades_release_date = Release_dates_of_posts[Content_of_Posts_copy.index(Post_i)]
                    CommonLetters_Post_CellValue_Date.append([a , Post_i , Excel_value_j, exam_date, grades_release_date])
                   
#Aux function to sort for only the first value

def getKey(item):
     return item.number
# Repeat the idea for better results  and CommonLetters_Post_CellValue_Date[0][0] > 14

def Repeat_Idea ():
    global CommonLetters_Post_CellValue_Date
    Repeated_list = []
    while ((Excel_Cell_Values != [] and Content_of_Posts != [])  ):
        Create_List_with_all_data(Content_of_Posts_copy) 
        CommonLetters_Post_CellValue_Date.sort(key=itemgetter(0))
        CommonLetters_Post_CellValue_Date.reverse()
        if (CommonLetters_Post_CellValue_Date == []): break
        current_max_value = CommonLetters_Post_CellValue_Date.pop(0)
        #print (current_max_value)
        if (current_max_value[2] in Excel_Cell_Values):
            Excel_Cell_Values.remove(current_max_value[2])
        if ((current_max_value[1] in Content_of_Posts)):
            Content_of_Posts.remove(current_max_value[1])
        Repeated_list.append(current_max_value)
        CommonLetters_Post_CellValue_Date = []
    CommonLetters_Post_CellValue_Date = Repeated_list

#Main
#Mistakes -> 17-18 Summer, 12-13 Autumn, 11-12 Autumn
#Choose tuple by input
Running_Tuples = [
    ["18-19 Winter",'22479',80],["18-19 Summer",'22765',80],["18-19 Autumn",'22827',0],
    ["17-18 Winter",'21986',100],["17-18 Summer",'22175',100],["17-18 Autumn",'22241',100],
    ["16-17 Winter",'21269',120],["16-17 Summer",'21629',120],["16-17 Autumn",'21695',100],
    ["15-16 Winter",'20582',140],["15-16 Summer",'20901',140],["15-16 Autumn",'20989',120],
    ["14-15 Winter",'19705',140],["14-15 Summer",'20105',140],["14-15 Autumn",'20212',140],
    ["13-14 Winter",'18698',160],["13-14 Summer",'19181',80],["13-14 Autumn",'19213',140],
    ["12-13 Winter",'17420',100],["12-13 Summer",'17899',100],["12-13 Autumn",'18035',20],
    ["11-12 Winter",'15961',100],["11-12 Summer",'16496',100],["11-12 Autumn",'16729',160]
]
input_i = input("")
tuple_i = Running_Tuples[int(input_i)]
    #tuple_i = Running_Tuples[4]
    #  try:
text_file = open("/Users/alexandroskyriakakis/MyProjects/Python_Projects/Project_One/EXAMS SCHEDULE/" + tuple_i[0] + "/excel/Results.txt","w+")
Names_file = open("/Users/alexandroskyriakakis/MyProjects/Python_Projects/Project_One/EXAMS SCHEDULE/" + tuple_i[0] + "/excel/Lessons_Names.txt","w+")
Results = open("/Users/alexandroskyriakakis/MyProjects/Python_Projects/Project_One/EXAMS SCHEDULE/" + tuple_i[0] + "/excel/ResultsOnly.txt","w+")


Track_shmmy_Data(tuple_i[1],tuple_i[2])
Extract_From_Excel(tuple_i[0])
Track_Dates_in_posts(Excel_Cell_Values)
    
    
Release_dates_of_posts = list(map(Normalize, Release_dates_of_posts))
Content_of_Posts = list(map(Normalize, Content_of_Posts))
Content_of_Posts = list(map(Keep_only_letters, Content_of_Posts))
Content_of_Posts = list(map(Remove_words_greater_than_six, Content_of_Posts))
Excel_Cell_Values = list(map(Normalize, Excel_Cell_Values))
Excel_Cell_Values = list(map(Keep_only_letters, Excel_Cell_Values))
Release_dates_of_posts = list(map(Define_dates, Release_dates_of_posts))
Excel_Cell_Values_Copy = Excel_Cell_Values[:]
print(Excel_Cell_Values_Copy)

#print ('\n'.join(list(' '.join(w[:w.index('ηλ')] + ' '.join(Excel_lessons_date_of_exam[Excel_Cell_Values_Copy.index(w)])) for w in Excel_Cell_Values if 'ηλ' in w)), file = Names_file)
#Aux file for names
counter_socia = 0
for w in Excel_Cell_Values_Copy:
    if ('ηλ' in w):
        print(' '.join(w[:w.index('ηλ')]), Excel_lessons_date_of_exam[counter_socia], '\n', file = Names_file)
    counter_socia += 1
        #print('\n'.join(list(' '.join(w[:w.index('ηλ')])) + str(Excel_lessons_date_of_exam[Excel_Cell_Values_Copy.index(w)])), file = Names_file)


Content_of_Posts_copy = Content_of_Posts[:]

Create_List_with_all_data(Content_of_Posts_copy)
CommonLetters_Post_CellValue_Date.sort(key=itemgetter(0))
CommonLetters_Post_CellValue_Date.reverse()
random.shuffle(Excel_Cell_Values)



Repeat_Idea()

#Run Big for loop
    #Print
counter = 0
        


for i in CommonLetters_Post_CellValue_Date:
    days = (i[4][2] - i[3][2])*365 + (i[4][1] - i[3][1])*30 + (i[4][0] - i[3][0])
    CommonWords = list(filter(lambda j: j in i[1], i[2]))
    if (i[0] < 8 or days < 0 or days > 365): del i
    else:
        counter += 1
        print(counter, '     ','Days took: ', days ,'\n','Common Words: ', CommonWords , '\n', "Number of common letters: ", i[0],'\n',"Date of exam: ",i[3],'\n', "Date of grades release: ",i[4],'\n',i[2],'\n',i[1],'\n', file = text_file)
        print(' '.join(i[2]), ' ', days, file = Results)

#EOF
