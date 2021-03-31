#!/usr/bin/env python
# coding: utf-8

# In[1]:


from RSA import *
import pickle
import copy
from datetime import datetime


# In[2]:


#@title Progress Mod {display-mode: "form"}
# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import sys, math

def progress(value,  length=40, title = " ", vmin=0.0, vmax=1.0):
    """
    Text progress bar
    Parameters
    ----------
    value : float
        Current value to be displayed as progress
    vmin : float
        Minimum value
    vmax : float
        Maximum value
    length: int
        Bar length (in character)
    title: string
        Text to be prepend to the bar
    """
    # Block progression is 1/8
    blocks = ["", "▏","▎","▍","▌","▋","▊","▉","█"]
    vmin = vmin or 0.0
    vmax = vmax or 1.0
    lsep, rsep = "▏", "▕"

    # Normalize value
    value = min(max(value, vmin), vmax)
    value = (value-vmin)/float(vmax-vmin)
    
    v = value*length
    x = math.floor(v) # integer part
    y = v - x         # fractional part
    base = 0.125      # 0.125 = 1/8
    prec = 3
    i = int(round(base*math.floor(float(y)/base),prec)/base)
    bar = "█"*x + blocks[i]
    n = length-len(bar)
    bar = lsep + bar + " "*n + rsep

    sys.stdout.write("\r" + title + bar + " %.1f%%" % (value*100))
    sys.stdout.flush()


# In[26]:


class PROFILE:
    def __init__(self, username, password,BD, bio = None):
        #________________________ATTRIBUTES_____________________________#
        self.username = username
        self.bio = bio #Optional
        self.Reward_Options = {}
        self.__keychain = {}
        self.__balance = 0
        self.PASSWORD = 'Whatthehell'
        #ENCRYPTION INTIALIZATION
        self.__RSA_init(password)
        ###___Project_B25____###
        self.booklist  = {}
        self.birthday = BD #%Y-%m-%d
        self.bookshelf = BookShelf()
        self.register_date = str(datetime.today().date())
        
    
    def __RSA_init(self,password:int)->None:
        "Generate a pair of Random Keys"
        N,e,d = RSA_sys(200)
        d_hat = self.__d_mutate(password,N,e,d) # A Bijective Transformation
        self.__keychain = {"N":N,"e":e,"d_hat": d_hat}
        
    def __d_mutate(self,password,N,e,d):
        self.PASSCODE = ENC(self.PASSWORD,N,e)
        return d - password
    
    def __d_mutate_inv(self,password,d_hat)->int:
        return d_hat + password
        
    def Verified(self,password:int)->bool:
        "Verifies if the Pass Word is Correct"
        d_hat = self.__keychain['d_hat']
        N = self.__keychain['N']
        d_tempt = self.__d_mutate_inv(password,d_hat)
        if DEC(C = self.PASSCODE,d = d_tempt,N=N) == self.PASSWORD:
            return True
        else:
            return False

    def save(self,file_path,format = "P25")->None:
        if file_path.split(".")[-1] == format:
            OUTfile = open(file_path ,"wb")
            pickle.dump(self,OUTfile)
            OUTfile.close()
        else:
            print(f"Error.File must be .{format} file.")


# In[27]:


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def judgement_day(BD,nyear=25):
    year = BD.split("-")[0]
    year = int(year) + nyear
    Jd = BD.split("-")
    Jd[0] = str(year)
    JD = ""
    for i in Jd:
        JD += i+"-" 
    return str(JD[:-1])

def CountDown(BD):
    "Return the number of days before you turn age 25, given your birthday"
    return days_between(judgement_day(BD),str(datetime.today().date()))

CountDown("1999-05-25")


# In[50]:


class book:
    def __init__(self,title,pagetotal):
        self.title = title
        self.pagetotal = pagetotal
        self.current_page = 0
        self.progress = progress(self.PROGRESS())
        self.log = {}
        self.profile = None
        
    def update(self,page):
        "Update current page number"
        self.log[datetime.today()] = int(page) - int(self.current_page)
        self.current_page = page
        self.progress = progress(self.PROGRESS())
        
        
    def PROGRESS(self,show = True):
        prog = self.current_page / self.pagetotal
        return prog
    
class BookShelf(book):
    def __init__(self):
        self.books = {}
        
    def add(self,title,pagetotal):
        self.books[title] = book(title,pagetotal)
        
    def delete(self,title):
        self.books.pop(title)
        
    def num_books_finished(self):
        n = 0
        for book in list(self.books.values()):
            n += book.PROGRESS(show=False)
        return n
    
    def sync_profile(self,profile):
        self.profile = profile
        
    def Statistics(self):
        if True:#try:
            self.V = self.num_books_finished()/(1+days_between(self.profile.register_date,str(datetime.today().date())))
            days_left = CountDown(self.profile.birthday)
            print(f"You are estimated to be able to finish {days_left*self.V} books before your turn 25.")
        else:#except:
            print("ERROR")
        
    
            


# In[51]:


#The UI
def B25_login():
    instruction = """
    Menu: Enter the following to execute (CASE SENSITIVE)
    ____________________________________________________________
    
    【Q】uit the program
    【L】ogin account
    【R】egister account
    """
    while True:
        print(instruction)
        cmd = input("Please Enter the corresponding commands...\n")
        if cmd == "Q":
            return 
        elif cmd == "R":
            if True: #try
                username = input("Please enter your user name:\n")
                password =  int(input("Please enter your pin (Digits Only):\n"))
                BD = input("Please enter your birthday in the following format: 2012-12-12 Year-Month-Day:\n")
                bio = input("Leave a biography!")
                Profile = PROFILE(username,password,BD,bio)
                #Create File 
                save_path = "D:\\360MoveData\\Users\\alienware\\Desktop\\GPK\\saves\\"
                save_path += username + ".P25"
                Profile.save(save_path)
            else:#except:
                print("Error Creating accounts, please try again later...")
        elif cmd == "L":
            username = input("Please enter your user name:\n")
            acc_file_path = "D:\\360MoveData\\Users\\alienware\\Desktop\\GPK\\saves\\" + username + ".P25"
            INfile = open(acc_file_path,"rb")
            __Profile = pickle.load(INfile)
            INfile.close()
            if __Profile.Verified(int(input("Please enter your pin (Digits Only):\n"))): #Successful Login
                print(f"Dear user {username}, welcome back")
                Profile = copy.copy(__Profile)
                B25_main(Profile,acc_file_path)
            else:
                print("WRONG PASSWORD, ACCESS DENIED")
        else:
            pass
            
            
        


# In[52]:


def B25_main(profile,save_path):
    instruction = """
    Menu: Enter the following to execute (CASE SENSITIVE)
    ____________________________________________________________
    
    【Q】uit the program and Return to the main menu
    【A】dd a new book to the bookshelf
    【D】elete an existing book from the bookshelf
    【U】pdate page number of an existing book 
    【S】tatistical analysis 
    ____________________________________________________________
    \n
    """
    while True:
        cmd = input(instruction)
        if cmd == "Q":
            return 
        elif cmd == "A":#【A】dd a new book to the bookshelf
            print("Which book do you wish to ADD to the bookshelf?\n")
            profile.bookshelf.add(input("Title:\n"),int(input("Total Page Number:\n")))
        elif cmd == "D":
            print("Which book do you wish to REMOVE from the bookshelf?\n")
            profile.bookshelf.delete(input("Title:\n"))
        elif cmd == "U":
            print("Which book would you like to update?")
            try:
                Title = input("Title:\n")
                profile.bookshelf.books[Title].update(int(input("Which Page are you CURRENTLY on?")))
            except KeyError:
                print("Sorry, we couldn't find your book in the bookshelf.")
        elif cmd == "S":
            profile.bookshelf.sync_profile(profile)
            profile.bookshelf.Statistics()
        else:
            pass
        profile.save(save_path)



if __name__ == '__main__':
    print("Welcome to project B25")
    B25_login()


#Edited On Github!!!


