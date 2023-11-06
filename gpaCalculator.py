import PySimpleGUI as sg
import PySimpleGUI as sg

class Course:
    gradeDict = {"A+": 4.3, "A": 4, "A-": 3.7, "B+": 3.3, "B": 3, "B-": 2.7, "C+": 2.3, "C": 2, "C-": 1.7, "D+": 1.3, "D": 1, "D-": 0.7, "F": 0}
    
    def __init__(self):
        self.academicTerm = ""
        self.faculty = ""
        self.courseCode = ""
        self.courseName = ""
        self.units = 0
        self.percentGrade = 0
        self.letterGrade = ""
        self.gradePoint = 0.0
        self.comparativeMean = 0.0
        self.classSize = 0
    
    def __str__(self):
        """
        Returns a string representation of the course
        
        eg.
        CSC 110 - Fundamentals of Programming I (1.5 units)
        Grade: 94% / A+ (9)
        Comparative Mean / Size: 77% / 86 students
        """
        res = ""
        res += f"{self.faculty} {self.courseCode} - {self.courseName} ({self.units} units)\n"
        res += f"Grade: {self.percentGrade}% / {self.letterGrade} ({self.gradePoint})\n"
        res += f"Comparative Mean / Size: {self.comparativeMean}% / {self.classSize} students\n"
        return res
    
    def addData(self, term, data):
        # print(data)
        self.academicTerm = term
        self.faculty = data[0]
        self.courseCode = data[1]
        i = 3
        while not data[i][0].isdigit():
            i += 1
        self.courseName = " ".join(data[3:i])
        self.units = float(data[i])
        self.percentGrade = int(data[i+1][:-1])
        self.letterGrade = data[i+2]
        self.gradePoint = int(data[i+3])
        mean, size = data[i+5].split("%")
        self.comparativeMean = int(mean)
        self.classSize = int(size)
        # print(self)
    
    def get43grade(self):
        return self.gradeDict[self.letterGrade]
        
class Student:
    """
    A class representing a student.

    Attributes:
    - name (str): the name of the student
    - courses (list): a list of Course objects taken by the student
    - gpa9 (float): the GPA of the student on a 9.0 scale
    - gpa43 (float): the GPA of the student on a 4.3 scale
    - score (float): the average score of the student in percentage
    - units (float): the total number of units taken by the student
    """
    def __init__(self, name):
        self.name = name
        self.courses = []
        self.gpa9 = 0.0
        self.gpa43 = 0.0
        self.score = 0.0
        self.units = 0.0
    
    def __str__(self):
        """
        Returns a string representation of the student

        eg.
        Ryan Nicholas Permana
        GPA 9       : 9.0
        GPA 4.3     : 4.3
        """
        res = ""
        res += f"\n{self.name}\n"
        res += "=============================\n"
        res += f"GPA 9         :{self.gpa9: .2f}\n"
        res += f"GPA 4.3       :{self.gpa43: .2f}\n"
        res += f"Average Score :{self.score: .2f}%\n"
        return res

    def addCourse(self, course):
        self.courses.append(course)
        self.units += course.units
    
    def getAverages(self):
        totalGpa9 = 0.0
        totalGpa433 = 0.0
        totalScore = 0.0
        for course in self.courses:
            totalGpa9 += course.gradePoint * course.units
            totalGpa433 += course.get43grade() * course.units
            totalScore += course.percentGrade * course.units
        self.gpa9 = totalGpa9 / self.units
        self.gpa43 = totalGpa433 / self.units
        self.score = totalScore / self.units
    

    # Add this function to the Student class
    def displayGUI(self):
        # Define the layout of the GUI
        layout = [
            [sg.Text(f"Name: {self.name}")],
            [sg.Text(f"GPA 9: {self.gpa9:.2f}")],
            [sg.Text(f"GPA 4.3: {self.gpa43:.2f}")],
            [sg.Text(f"Average Score: {self.score:.2f}%")],
            [sg.Button("Close")]
        ]
        
        # Create the window
        window = sg.Window("GPA Calculator", layout)
        
        # Event loop
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Close":
                break
        
        # Close the window
        window.close()

def main():
    s = Student("Ryan Nicholas Permana")
    
    with open("gpa_stats.txt", "r") as f:
        data = [line.rstrip() for line in f.readlines()]
        
        termDict = {}
        curTerm = ""
        
        for x in data:
            if len(x.split()) == 2:
                # is term
                curTerm = x
                termDict[curTerm] = []
            else:
                termDict[curTerm].append(x)
        
        for term in termDict:
            courses = termDict[term]
            for course in courses:
                c = Course()
                course = course.split()
                if len(course) >= 10: 
                    c.addData(term, course)
                    s.addCourse(c)
    
    s.getAverages()
    print(s)
    s.displayGUI()
    
if __name__ == '__main__':
    main()
    
        