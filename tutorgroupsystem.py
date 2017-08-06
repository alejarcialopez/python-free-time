import json
import getpass
from datetime import *

file1 = open('teacherUsers.json', 'r+')
emptyfile = False
try:
    teacher_login = json.load(open('teacherUsers.json'))
except json.decoder.JSONDecodeError:
    emptyfile = True
admin_login = json.load(open('adminUser.json'))
user1 = ""
location = ""
accountype = None
def login():
    bloop = True
    bloop2 = True
    while True:
        username = input("username ")
        try:
            iUsername = int(username)
            print ("no numbers")
        except ValueError:
            break
    password = getpass.getpass("password ")
    global location
    global accountype
    global user1
    global avoiderror
    while bloop == True:
        for x in range (0, len(admin_login["users"])):
            if username == admin_login["users"][x]["username"]:
                if password == admin_login["users"][x]["password"]:
                    print ("logged in")
                    location = x
                    accountype = 0
                    user1 = admin(username, password)
                    menu()
                    bloop = False
        if emptyfile != True:
            for y in range (0, len(teacher_login["users"])):
                if username == teacher_login["users"][y]["username"]:
                    if password == teacher_login["users"][y]["password"]:
                        print ("logged in")
                        location = y
                        accountype = 1
                        user1 = teacher(username, password)
                        menu()
                        bloop = False
class report():


    def __init__(self, database):
        pass


    def age_report(self):
        return sorted(self.database, key=lambda x: datetime.strptime(x['birth'], "%d/%m/%Y"))


    def gender_report(self):
        newData = []
        output = input("show only male (m) or only female (f)? ")
        if output == 'm':
            for item in self.database:
                if item['gender'] == 'male':
                    newData.append(item)
        elif output == 'f':
            for item in self.database:
                if item['gender'] == 'female':
                    newData.append(item)
        else:
            print("incorrect command")
        return newData


    def alphabetic_report(self):
        return sorted(self.database, key=lambda element: element['lastname'])


class admin(report):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def database(self):
        if emptyfile != True:
            sDatabases = ""
            n = 0
            for item in teacher_login['users']:
                sDatabases += f"{n} database --> {teacher_login['users'][n]['database']} \n"
                n += 1
            print(sDatabases)
            while True:
                choice = input("choose the number of the database to be seen ")
                try:
                    iChoice = int(choice)
                    value = json.load(open(teacher_login['users'][iChoice]['database']))
                    break
                except ValueError:
                    print("no letters")
            return value['students']
        else:
            return None


    def viewdatabase(self, report):
        if emptyfile != True:
            data = report
            records = ""
            count = 0
            for item in data:
                IDnumber = data[count]['ID']
                fullname = data[count]['firstname'] + " " + data[count]['lastname']
                birth = data[count]['birth']
                address = data[count]['home']
                phone = data[count]['phone']
                gender = data[count]['gender']
                tutorGroup = data[count]['tutorgroup']
                email = data[count]['email']
                records += f'''
ID: {IDnumber}, full name: {fullname}, date of birth: {birth},
home address: {address}, phone number: {phone}, gender: {gender},
tutor group: {tutorGroup}, email: {email}
'''
                count += 1
            print(records)

    def AddorDelete(self):
        option = input ("do you want to add (a) or delete (d)? ")
        if option == 'd' and emptyfile != True:
            account = input("enter the username of the account to be deleted ")
            x = 0
            error = True
            for item in teacher_login['users']:
                if account == teacher_login['users'][x]['username']:
                    del teacher_login['users'][x]
                    print(teacher_login)
                    file1.write(json.dumps(teacher_login))
                    print ("acount deleted")
                    error = False
                x += 1
            if error == True:
                print ("username not found")
        if option == 'd' and emptyfile == True:
            print ("there are no accounts to be deleted")
        elif option == 'a':
            newUsername = input("enter username ")
            newPassword = getpass.getpass("enter password ")
            newDB = input("enter name of your database ")
            realDB = newDB + ".json"
            newdatabase = open(realDB, 'w+')
            jsonstructure = {'students':[]}
            newdatabase.write(json.dumps(jsonstructure))
            if emptyfile != True:
                teacher_login['users'].append({'username': newUsername, 'password': newPassword, 'database': realDB})
                file1.write(json.dumps(teacher_login))
            else:
                backupjson = {'users': [{'username': newUsername, 'password': newPassword, 'database': realDB}]}
                file1.write(json.dumps(backupjson))
            newdatabase.close()


class teacher(admin, report):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def database(self):
        value = json.load(open(teacher_login['users'][location]['database']))
        return value['students']

    def populatedatabse(self):
        bLoop = True
        data = self.database
        writetoDB = open(teacher_login['users'][location]['database'], 'w')
        while bLoop == True:
            lengthData = len(data['students'])
            if lengthData == 0:
                newIDnum = 1
            else:
                newIDnum = int(data['students'][lengthData - 1]['ID']) + 1
            newFName = input("first name ")
            newLName = input ("last name ")
            newDay = input ("day of birth (DD) ")
            newMonth = input ("month of birth (MM) ")
            newYear = input ("year of birth (YYYY) ")
            newBirth = f"{newDay}/{newMonth}/{newYear}"
            newHomeAddress = input("home address ")
            newPhoneNumber = input ("phone number ")
            newGender = input("male or female? ")
            newTutorGroup = input ("tutor group ")
            newEmail = f"{newLName}{newFName[0]}@oakschool.com"
            data['students'].append({'ID': str(newIDnum), 'firstname': newFName, 'lastname': newLName, 'birth': newBirth, 'home': newHomeAddress, 'phone': newPhoneNumber, 'gender': newGender, 'tutorgroup': newTutorGroup, 'email': newEmail})
            Continue = input("add more? (no/yes) ")
            if Continue == 'no':
                writetoDB.write(json.dumps(data))
                writetoDB.close()
                bLoop = False




def menu():
    if accountype == 0:
        choice = input ("view database (v) or change teacher users database(c)? ")
        if choice == 'v':
            viewtype = input("view database in age (e), gender (g), or alphabetical (a) order? (press enter for normal view) ")
            if viewtype == 'e':
                user1.viewdatabase(user1.age_report())
            elif viewtype == 'g':
                user1.viewdatabase(user1.gender_report())
            elif viewtype == 'a':
                user1.viewdatabase(user1.alphabetic_report())
            else:
                user1.viewdatabase(user1.database)
        elif choice == 'c':
            user1.AddorDelete()

    elif accountype == 1:
        choice = input ("view (v) or populate (p) database? ")
        if choice == 'v':
            viewtype = input("view database in age (e), gender (g), or alphabetical (a) order? (press enter for normal view) ")
            if viewtype == 'e':
                user1.viewdatabase(user1.age_report())
            elif viewtype == 'g':
                user1.viewdatabase(user1.gender_report())
            elif viewtype == 'a':
                user1.viewdatabase(user1.alphabetic_report())
            else:
                user1.viewdatabase(user1.database)
        elif choice == 'p':
            user1.populatedatabse()

login()
file1.close()
