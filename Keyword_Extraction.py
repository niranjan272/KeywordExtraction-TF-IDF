########--------------------------------------####
#MySQL db schema-
# DATABASE NAME - global_words_freq

# Table global_words_freq_t -> "Stores words occurring in documents and their count."
# Column names => 1) word(String) 2) no_of_doc_occurance(int)

#Table document_count -> "Stores the number of documents have been evaluated." 
#Column names => 1) count(int)


#Input
1. A file containing a list of paths to training set
2. A document for which you want the key-words
#########-------------------------------------####



#function to initiate count in document_count
def ini_db():
    db=MySQLdb.connect(host="localhost", port=3306, user="shek", passwd="3147", db="global_words_freq")
    c=db.cursor()
    #query to clear data in document_count
    sql="DELETE FROM document_count";
    try:
        #execute
        c.execute(sql)
        db.commit()
    except:
        db.rollback()
    #query to clear data in global_words_freq_t
    sql="DELETE FROM global_words_freq_t";
    try:
        #execute
        c.execute(sql)
        db.commit()
    except:
        db.rollback()
        
    #query to set value to zero
    sql= "INSERT INTO document_count(count)VALUES(0)"
    try:
        #execute
        c.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
#end of intiate function



# return count of document
def no_doc():
    db= MySQLdb.connect(host="localhost", port=3306, user="shek", passwd="3147", db="global_words_freq")
    c=db.cursor()
    sql="SELECT count FROM document_count"
    try:
        #execution
        c.execute(sql)
        result=c.fetchall()
        
        for row in result:
            o=row[0]
        
        return o
    except:
        print "failed to retrive no of document"
    db.close()
#end of no_doc

#no of occurance
def no_of_occurance(word):
    db= MySQLdb.connect(host="localhost", port=3306, user="shek", passwd="3147", db="global_words_freq")
    c=db.cursor()
    sql="SELECT no_of_doc_occurance FROM global_words_freq_t \
         WHERE word = '%s' " %(word)
    try:
        #execution
        c.execute(sql)
        result=c.fetchall()
        for row in result:
            x=row[0]
        
        return x
    except:
        print "failed to retrive no of document"
    db.close()

#end of no of occurance


#function update the count of documents in db
def document_count():
        
    db= MySQLdb.connect(host="localhost", port=3306, user="shek", passwd="3147", db="global_words_freq")
    c=db.cursor()
    #query
    sql="UPDATE document_count SET count=count+1"
    try:
        #execute
        c.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
#end of document_count function


#function to check word in global table returns 0 or 1
def check(word):
    import MySQLdb
    db= MySQLdb.connect(host="localhost", port=3306, user="shek", passwd="3147", db="global_words_freq")
    c=db.cursor()
    #query
    sql="SELECT word FROM global_words_freq_t WHERE word = '%s' " \
            %(word)
    try:
        #execution
        c.execute(sql)
        results=c.fetchall()
        
        if (results != ()):
            return 1
        else:
            return 0
    except:
        print word
        print "error while checking"
        
    db.close()
#end of check function


#function to add a word if it is not present in the global table
def add_new_word(word):
    import MySQLdb
    db= MySQLdb.connect(host="localhost", port=3306, user="shek", passwd="3147", db="global_words_freq")
    c=db.cursor()
    #query
    sql="INSERT INTO global_words_freq_t(word,no_of_doc_occurance )VALUES('%s','%d')"%(word,1)
    try:
        #execution
        c.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()
#end of add_new_word function


#fuction to update occurance of word in global table
def update_record(word):
    import MySQLdb
    db= MySQLdb.connect(host="localhost", port=3306, user="shek", passwd="3147", db="global_words_freq")
    c=db.cursor()
    #query
    sql="UPDATE global_words_freq_t SET no_of_doc_occurance=no_of_doc_occurance+1 \
        WHERE word='%s'" %(word)

    try:
        #execution
        c.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()
#end of update_record function   

#tag filter
def filter_for_tags(tagged, tags=['NN', 'JJ', 'NNP']):
    return [item[0] for item in tagged if item[1] in tags]
#end of tag filter

def callback() :
        print "abc"


##button 1 event startup
def OnButtonClick ():
        file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file')
        if file != None:
            print "Initializing... Please Wait"
            ini_db()
            
            file_list=file.readlines()

            for line in file_list:
                
                line=line.strip()
                fp1=open(line,"r")
                document_count()
                text=fp1.read()    
                #dictonary to store word frequency in text(temporary)
                doc_word_freq={}
                #Tokenize 
                from nltk.tokenize import WordPunctTokenizer
                tokenizer = WordPunctTokenizer()
                text2=tokenizer.tokenize(text)
            



                #removing stopwords
                from nltk.corpus import stopwords
                eng_stop=set(stopwords.words('english'))
                text3=[word for word in text2 if word not in eng_stop]

                #pos tag
                import nltk
                text4=nltk.pos_tag(text3)
                text5=filter_for_tags(text4)


                #calculate frequency of word in the text
                for word in text5:
                    if word in doc_word_freq:
                        doc_word_freq[word] += 1
                    else:
                        if(word != "'"):
                            doc_word_freq[word] = 1

                #update occurance of word in global table
                for (word,freq) in doc_word_freq.items():
                    if (check(word)):
                        update_record(word)
                    else:
                        add_new_word(word)
            print "Initialization Done...\n\n"
            file.close()
###end of onButtonclick


###function to select input ( Main calculation of tf-idf)
def SelectS():
        file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file')
        if file != None:
            text = file.read()
            doc_word_freq={}

            document_count()

            #Tokenize 
            from nltk.tokenize import WordPunctTokenizer
            tokenizer = WordPunctTokenizer()
            text2=tokenizer.tokenize(text)

            #removing stopwords
            from nltk.corpus import stopwords
            eng_stop=set(stopwords.words('english'))
            text3=[word for word in text2 if word not in eng_stop]

            #pos tag
            import nltk
            text4=nltk.pos_tag(text3)
            text5=filter_for_tags(text4)



            #calculate frequency of word in the text
            for word in text5:
                if word in doc_word_freq:
                    doc_word_freq[word] += 1
                else:
                    if(word != "'" or word !=".'"):
                        doc_word_freq[word] = 1

            #update occurance of word in global table
            for (word,freq) in doc_word_freq.items():
                if (check(word)):
                    update_record(word)
                else:
                    add_new_word(word)
            max_freq=0
            for word,freq in doc_word_freq.items():
                if freq > max_freq:
                    max_freq=freq

            tfidf={}

#### !!!!Algo to find tf-idf !!!!
            for word,freq in doc_word_freq.items():
                tf=float(freq)/float(max_freq)
                idf= math.log(float(no_doc())/float(1+no_of_occurance(word)))
                tfidf[word]=tf*idf
####
            no=0
            word_list=[]
            print "\nKeywords:"
            for word in sorted(tfidf, key=tfidf.get, reverse=True):
                print word
                word_list.append(word)
                no=no+1
                if(no==5):
                    break;
            

            
            
            
            file.close()
###end of function to select input





#main
import Tkinter
from Tkinter import *
import tkFileDialog
import tkMessageBox
import math
import numpy
import MySQLdb

doc_word_freq={}
class App:
    def __init__(self,root):
        fm=Frame(root,width=300, height=200, bg="orange")
        fm.pack(side=TOP, expand=YES, fill=NONE)
        root.title("Key Word Extraction")
                
        button = Button(fm,text = "perform start up",command=OnButtonClick)
        button.place(x=60,y=80)
        button2= Button(fm,text="start",command=SelectS)
        button2.place(x=190,y=80)
        
        
if __name__=="__main__":
    root=Tk()
    display= App(root)
    root.mainloop()
        

