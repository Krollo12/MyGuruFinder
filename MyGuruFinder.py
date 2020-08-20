import sys
import re
import mysql.connector
from NN import *
from collections import Counter
from bs4 import BeautifulSoup
import urllib.request
import os
from prettytable import PrettyTable

# Function to test if string is all ASCII
def is_ascii(s):
    return all(ord(c) < 128 for c in s)


# Initialize database
#Chech if already loaded
print("Checking for database...")
con = mysql.connector.connect(user='Gurufinder')
c = con.cursor()
c.execute("show databases like 'starwars';")

# Load database if not loaded
if not c.fetchall():
    print('Loading database...')
    c.execute("create database starwars;")
    c.execute("use starwars;")
    os.system("mysql -u Gurufinder starwars < ../starwars.sql")
    print('Finished loading database.')
    print('\n')
else:
    print("Database ok \n")

# The my GuruFinder class
class MyGuruFinder:
    # Initializes a MyGuruFinder object
    def __init__(self, InputUrl):
        self.wikipage = InputUrl.split(sep = "/")[-1]
        self.webpage = InputUrl
        self.wiki_id = 0
        self.autRevDict = {}
        self.authorAccoladeDict = {}
        self.globalAutRevDict = {}
        self.con = mysql.connector.connect(user='Gurufinder',database = 'starwars')
        self.c = self.con.cursor()
        self.NOU = int(sys.argv[2])

    # Gets the top NOU of users based on revisions on the inputted site.
    def getActiveAuthorsList(self):
        # Get page_id
        self.c.execute("select page_id from page where page_title = '%s'" % (self.wikipage))
        page_id = self.c.fetchall()
        page_id = page_id[0][0]
        self.wiki_id = page_id

        # Get the user names that have made revisions on the page
        self.c.execute("select rev_user_text from revision where rev_minor_edit=0 and rev_deleted=0 and rev_page='%s'" % (page_id))
        p = self.c.fetchall()
        names = []

        # Make sure the type is the same on both Mac OS and WSL
        if isinstance(p[0][0], bytearray):
            for i in range(len(p)):
                t = p[i][0].decode("utf-8")
                t1 = t.replace('.','1')
                if not t1.isdigit() and ':' not in t1 and is_ascii(t1):
                    names.append(t)
        else:
            for i in range(len(p)):
                t = p[i][0]
                t1 = t.replace('.','1')
                if not t1.isdigit() and ':' not in t1 and is_ascii(t1):
                    names.append(t)

        #Make dictionary over top NOU Wikipedians based on number of revisions.
        count = Counter(names)
        count1 = count.most_common(self.NOU)
        autRevDict = {count1[j][0]: count1[j][1] for j in range(self.NOU)}
        self.autRevDict = autRevDict

        return autRevDict

    #Closes SQL connection to database
    def sqlCloser(self):
        self.con.close()
        return

    # Crawls the  userpage to fill the accolade dictionary
    def userPageCrawler(self, user):

        # Create user in the accolade dict
        if user in self.authorAccoladeDict.keys():
            return
        else:
            self.authorAccoladeDict[user] = [' ' for _ in range(6)]

        # Open the userpage and generate the "Beautiful soup"
        crawler = urllib.request.urlopen('https://en.wikipedia.org/wiki/User:{}'.format(user.replace(' ','_'))).read()
        soup = BeautifulSoup(crawler, 'html.parser')
        text = soup.get_text()


        # Check if the Wikipedian has even made a userpage
        if 'Wikipedia does not have a user page' in text:
            self.authorAccoladeDict[user] = ['\x1b[31mThis\x1b[0m','\x1b[31muser\x1b[0m','\x1b[31mdoes\x1b[0m','\x1b[31mnot\x1b[0m','\x1b[31mhave\x1b[0m','\x1b[31ma userpage\x1b[0m']
            return
        if 'This account has been blocked indefinitely' in text:
            self.authorAccoladeDict[user] = ['\x1b[31mThis\x1b[0m','\x1b[31muser\x1b[0m','\x1b[31mhas\x1b[0m','\x1b[31mbeen\x1b[0m','\x1b[31mblocked\x1b[0m','\x1b[31mfrom Wikipedia\x1b[0m']
            return

        #Fill out the accolades
        # Get emails and store in accolade dictionary
        rgx = r'(?:\.?)([\w\-_+#~!$&\'\.]+(?<!\.)(@|[ ]?\(?[ ]?(at|AT)[ ]?\)?[ ]?)(?<!\.)[\w]+[\w\-\.]*\.[a-zA-Z-]{2,3})(?:[^\w])'
        matches = re.findall(rgx, text)
        get_first_group = lambda y: list(map(lambda x: x[0], y))
        emails = get_first_group(matches)
        if emails:
                if '@' in emails[0]:
                    if "infoEmail" in emails[0]:
                        self.authorAccoladeDict[user][0] = emails[0][9:]
                    else:
                        self.authorAccoladeDict[user][0] = emails[0]

        # Get private twitter and store in accolade dictionary
        for link in soup.find_all('a'):
            if 'twitter.com' in str(link.get('href')).lower():
                self.authorAccoladeDict[user][1] = str(link.get('href'))

        # Find the education levels the Wikipedian has and store in accolade dictionary
        if 'bachelor of' in text.lower():
            self.authorAccoladeDict[user][2] = 'Ba'
        if 'master of' in text.lower():
            if self.authorAccoladeDict[user][2] == ' ':
                self.authorAccoladeDict[user][2] = 'Ma'
            else:
                self.authorAccoladeDict[user][2] += ', Ma'

        # Find the overall number of contributions (number of revisions in our database) and store in accolade dictionary
        self.c.execute("SELECT COUNT(*) FROM revision WHERE rev_user_text = '%s'" % (user))
        self.authorAccoladeDict[user][3] = self.c.fetchall()[0][0]

        # Grade the "seriousness" of the user page and store in accolade dictionary
        if len(text) < 5000:
            self.authorAccoladeDict[user][4] = 'low'
        elif len(text) > 5000 and len(text) < 10000:
            self.authorAccoladeDict[user][4] = 'medium'
        elif len(text) > 10000:
            self.authorAccoladeDict[user][4] = 'high'

        # Get the number of barnstars and store in accolade dictionary
        # Barnstars which logo is not called barnstar or bstar is not found but they all seem to be
        nBarnstars = 0
        for link in soup.find_all('a'):
            lcLink = str(link.get('href')).lower()
            if '/wiki/file' in lcLink:
                if 'barnstar' in lcLink or 'bstar' in lcLink:
                    nBarnstars += 1
        self.authorAccoladeDict[user][5] = nBarnstars

        return

    # Loads the texts from the articles so that the NN.py can train the model
    def nearest(self):

        data = []

        # Get the page titles
        self.c.execute("select page_title from page")
        titles = self.c.fetchall()

        # Converts the type to strings
        titles_decoded = []
        if isinstance(titles[0][0],bytearray):
            for i in range(len(titles)):
                t = titles[i][0].decode("utf-8")
                titles_decoded.append(t)

            # Get the text from each page
            for i in range(len(titles_decoded)):
                self.c.execute("select old_text from page inner join revision on page_latest=rev_id inner join text on rev_text_id = old_id where page_title = '%s' and page_namespace=0" % (titles_decoded[i]))
                text = self.c.fetchall()
                text = text[0][0].decode("utf-8")
                text.replace("\\","")
                data.append(text)

        else:
            for i in range(len(titles)):
                t = titles[i][0]
                titles_decoded.append(t)

            # Get the text from each page
            for i in range(len(titles_decoded)):
                self.c.execute("select old_text from page inner join revision on page_latest=rev_id inner join text on rev_text_id = old_id where page_title = '%s' and page_namespace=0" % (titles_decoded[i]))
                text = self.c.fetchall()
                text = text[0][0]
                text.replace("\\","")
                data.append(text)

        return data,titles_decoded



    # Gets the top NOU wikipedians for the similar articles
    def GetSimUserRef(self,neighbours_list):
        # Store relevant page id's
        names = []
        id_list = []
        for i in range(len(neighbours_list)):
            self.c.execute("select page_id from page where page_title = '%s'" % (neighbours_list[i]))
            temp = self.c.fetchall()
            id_list.append(temp[0][0])


        # Append the original article ID
        id_list.append(self.wiki_id)
        for i in range(len(id_list)):
            self.c.execute("select rev_user_text from revision where rev_minor_edit=0 and rev_deleted=0 and rev_page='%s'" % (id_list[i]))
            p = self.c.fetchall()

            # Make sure the type is the same on both Mac OS and WSL
            if isinstance(p[0][0], bytearray):
                for i in range(len(p)):
                    t = p[i][0].decode("utf-8")
                    t1 = t.replace('.','1')
                    if not t1.isdigit() and ':' not in t1 and is_ascii(t1):
                        names.append(t)
            else:
                for i in range(len(p)):
                    t = p[i][0]
                    t1 = t.replace('.','1')
                    if not t1.isdigit() and ':' not in t1 and is_ascii(t1):
                        names.append(t)

        #Make dictionary over top NOU Wikipedians based on number of revisions.
        count = Counter(names)
        count1 = count.most_common(self.NOU)
        autRevDict = {count1[j][0]: count1[j][1] for j in range(self.NOU)}
        self.globalAutRevDict = autRevDict
        return

    # Makes a nice table with all found Wikipedians with their accolades
    def TableMaker(self, revDict, accoladeDict):
        t = PrettyTable(['User','# of revisions', '',  'Email', 'Twitter','Education', '#    of contributions', '"Seriousness"', "Barnstars" ])
        for user in revDict.keys():
            t.add_row([user, revDict[user], '', accoladeDict[user][0], accoladeDict[user][1], accoladeDict[user][2], accoladeDict[user][3], accoladeDict[user][4], accoladeDict[user][5]])
        print(t)
        return

def main():

    print("MyGuruFinder is finding your Guru...")

    #Initialize MyGuruFinder Object
    pageGuru = MyGuruFinder(sys.argv[1])

    # Get top NOU wikipedians on article
    pageGuru.getActiveAuthorsList()

    # Get neighbouring articles
    neighbourList, scorelist = NearestNeighbourFinder(pageGuru,train=False)

    # Get top NOU wikipedians on neighbouring articles
    pageGuru.GetSimUserRef(neighbourList)

    # Web crawl all Userpages
    for user in pageGuru.autRevDict.keys():
        pageGuru.userPageCrawler(user)
    for user in pageGuru.globalAutRevDict.keys():
        pageGuru.userPageCrawler(user)

    # Print all of the results
    print('\n')
    print("The top users for the Wikipedia page for " + pageGuru.wikipage.replace('_', ' ') + " are:")
    pageGuru.TableMaker(pageGuru.autRevDict, pageGuru.authorAccoladeDict)
    print('\n')
    print("MyGuruFinder found similar pages to " + pageGuru.wikipage.replace('_', ' ') + " to be:")
    for num, neighbour in enumerate(neighbourList, start = 1):
        print("\t" + str(num) + " " +  neighbour.replace('_', ' ') + " (Score: " + str(scorelist[num-1])[0:4] + ")")
    print("The top users for the Wikipedia page for " + pageGuru.wikipage.replace('_', ' ') + " and similar pages are:")
    pageGuru.TableMaker(pageGuru.globalAutRevDict, pageGuru.authorAccoladeDict)
    pageGuru.sqlCloser()

    return

if __name__ == "__main__":
    main()
