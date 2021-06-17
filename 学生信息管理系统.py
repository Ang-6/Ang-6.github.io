class StudentInfo:
    def __init__(self, name, stuid, gender, age, major, tel):
        self.name = name
        self.stuid = stuid
        self.gender = gender
        self.age = age
        self.major = major
        self.tel = tel

    def info(self):
        # 字符串的拼接
        if self.gender == '1':
            self.gender = 'Male'
        else:
            self.gender = 'Female'
        msg = self.name.center(8) + self.stuid.center(16) + self.gender.center(6) + self.age.center(6) + self.major.center(10) + self.tel.center(16) + '\n'
        return msg
def add():
    if_continue = '1'
    global flag
    flag = 1
    # the file has been created, appending，and will be closed automatically
    while if_continue == '1':
        with open('student.txt', 'a') as f:
            name = input("Name: ")
            stuid = input("Student ID: ")
            gender = input("1.Male  2.Female : ")
            age = input("Age: ")
            major = input("Major: ")
            tel = input("Telephone: ")
            student = StudentInfo(name, stuid, gender, age, major, tel)
            f.write(student.info())
            print("Adding successfully!")
            print('姓名'.center(8)+'学号'.center(16)+'性别'.center(4)+'年龄'.center(6)+'专业'.center(8)+'电话'.center(13))
            print(student.info(), end='')
        if_continue = input("Press 0 to stop, 1 to continue.\n")
def delete():
    if_continue='1'
    global flag
    flag=1
    while if_continue == '1':
        with open('student.txt', 'r+')as f:
            lines=[]
            lines = f.readlines()
        with open('student.txt', 'w+')as f:
            # f.seek(0, 0)
            discard = input('please input you want to delete:')
            for line in lines:
                if discard not in line:
                    f.write(line)
                else:
                    print('delete successfully!')
                    print(line, end='')
            # f.truncate()
        if_continue = input("Press 0 to stop, 1 to continue.\n")
def revise():
    if_contiune='1'
    while if_contiune=='1':
        with open('student.txt','r+')as f:
            lines=f.readlines()
        with open('student.txt','w+')as f:
            revise_line=input('please input need modify information:')
            for line in lines:
                if revise_line in line:
                    print(line)
                    old_information=input('old information:')
                    new_information=input('new information:')
                    line=line.replace(old_information,new_information)
                    f.write(line)
                    print("Revise successfully!")
                    print(line,end='')
                else:
                    f.write(line)
        if_contiune = input("Press 0 to stop, 1 to continue.\n")

def clear():
    if_continue = '1'
    global flag
    flag = 1
    while if_continue == '1':
        with open("student.txt", 'r+') as f:
            f.truncate()
        print("Clear successfully!")
        if_continue = input("Press 0 to menu.\n")
def research():
    if_continue = '1'
    global flag
    flag = 1
    key=0
    while if_continue == '1':
        with open('student.txt','r')as f:
            lines=f.readlines()
            search=input('please input you want to search:')

            for line in lines:
                if search in line:
                    key=1
                    print(line,end='')
                else:
                    key=0
            if key==1:
                print('Successfully find')
            else:
                print('No such student!')
        if_continue = input("Press 0 to the menu.\n")
def view():
        if_continue = '1'
        global flag
        flag = 1
        while if_continue == '1':
            with open("student.txt", 'r+') as f:
                lines=f.readlines()
                for line in lines:
                    print(line,end='')
            if_continue = input("Press 0 to the menu.\n")
def menu():
    global flag
    flag=1
    while flag == 1:
        flag = 0
        print("********MENU*********")
        print("*** 1.Add         ***")
        print("*** 2.Delete      ***")
        print("*** 3.revise      ***")
        print("*** 4.clear       ***")
        print("*** 5.research    ***")
        print("*** 6.view        ***")
        print("*** 7.exit        ***")
        print("*********************")
        num = input("Function: ")  # more convenient using dictionary?
        if num == '1':
            add()
        elif num == '2':
            delete()
        elif num == '3':
            revise()
        elif num == '4':
            clear()
        elif num == '5':
            research()
        elif num == '6':
            view()
        elif num == '7':
            logout()
        else:
            flag = 1
            print("Wrong input!")


def logout():
    print("Are you sure to log out?")
    print("1.Yes", end=' ')
    print("2.No")
    if input("yes or not: ") == '1':
        exit()
    else:
        pass
def start():
    print("*************************************************")
    print("*** Welcome to the student management system! ***")
    print("*** 1.log in                                  ***")
    print("*** 2.exit                                    ***")
    print("*************************************************")

def main():
    while True:
        start()
        num = input("Choose the number: ")
        if num == '1':
            menu()
        elif num == '2':
            logout()
        else:
            print("Wrong! Enter again!")
main()