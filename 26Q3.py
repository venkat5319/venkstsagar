class Student:
# Class attributes
 department =""
 course =""
 college ="" 

 def __init__(self, name, age,grade):
    
    self.name = name
    self.age = age
    self.grade = grade
 def printname(self):
    print("Name is "+self.name)
 def printage(self):
    print("Age is "+self.age)
 def printgrade(self):
    print("Grade is "+self.grade)
 @classmethod
 def firstmethod(obj):
    print("department = ",obj.department,"course = ",obj.course,"college = ",obj.college) 

 @classmethod
 def secondmethod(obj,a,b,c):
    obj.department=a
    obj.course=b
    obj.college=c

s1 = Student("Ravuri","27","A")
s1.printname()
s1.printage()
s1.printgrade()

Student.secondmethod('Msc','PG','AV PG College')
Student.firstmethod()

s2 = Student("Venkat","28","A")
s2.printname()
s2.printage()
s2.printgrade()

Student.secondmethod('BSC','UG ','Saint Marys college')
Student.firstmethod()

s3 = Student("Chandra","23","A")
s3.printname()
s3.printage()
s3.printgrade()

Student.secondmethod('Btech','UG','Khadari College')
Student.firstmethod()