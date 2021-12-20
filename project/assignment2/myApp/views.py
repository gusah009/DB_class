from django.shortcuts import render, redirect
from django.db import connection
import pandas as pd
import os

# Create your views here.

def display(request):
    outputStudents = []
    outputProfessors = []
    outputCounties = []
    outputCOVID = []
    outputOfQuery1 = []
    with connection.cursor() as cursor:
        sqlQueryStudents = """  
                            SELECT `studentID`, `name`, `score`, `county`
                            FROM `Students`;
                            """
        cursor.execute(sqlQueryStudents)
        fetchResultStudents = cursor.fetchall()
        
        sqlQueryProfessors = """
                            SELECT `facultyID`, `name`, `age`, `county`
                            FROM `Professors`;
                            """
        cursor.execute(sqlQueryProfessors)
        fetchResultProfessors = cursor.fetchall()
        
        sqlQueryCounties = """
                            SELECT `countyName`, `population`, `city`
                            FROM `Counties`;
                            """        
        cursor.execute(sqlQueryCounties)
        fetchResultCounties = cursor.fetchall()
        
        sqlQueryCOVID = """
                            SELECT `patientID`, `city`
                            FROM `COVID`;
                        """        
        cursor.execute(sqlQueryCOVID)
        fetchResultCOVID = cursor.fetchall()

        # sqlQuery1 = """
        # """
        # cursor.execute(sqlQuery1)
        # fetchResultQuery1 = cursor.fetchall()
        
        # sqlQuery2 = """
        # """
        # cursor.execute(sqlQuery2)
        # fetchResultQuery2 = cursor.fetchall()

        # sqlQuery3 = """
        # """
        # cursor.execute(sqlQuery3)
        # fetchResultQuery3 = cursor.fetchall()

        # sqlQuery4 = """
        # """
        # cursor.execute(sqlQuery4)
        # fetchResultQuery4 = cursor.fetchall()
        
        # sqlQuery5 = """
        # """
        # cursor.execute(sqlQuery5)
        # fetchResultQuery5 = cursor.fetchall()

        connection.commit()
        connection.close()

        for temp in fetchResultStudents:
            eachRow =   {'studentID': temp[0], 'name': temp[1], 'score': temp[2], 'county': temp[3]}
            outputStudents.append(eachRow)

        for temp in fetchResultProfessors:
            eachRow =   {'facultyID': temp[0], 'name': temp[1], 'age': temp[2], 'county': temp[3]}
            outputProfessors.append(eachRow)
                            
        for temp in fetchResultCounties:
            eachRow =   {'countyName': temp[0], 'population': temp[1], 'city': temp[2]}
            outputCounties.append(eachRow)

        for temp in fetchResultCOVID:
            eachRow =   {'patientID': temp[0], 'city': temp[1]}
            outputCOVID.append(eachRow)

        # for temp in fetchResultQuery1:
        #     eachRow = {'categoryname': temp[0], 'categorydescription': temp[1]}
        #     outputOfQuery1.append(eachRow)

    return render(request, 'myApp/index.html', {"Students": outputStudents,
                                                "Professors": outputProfessors,
                                                "Counties": outputCounties,
                                                "COVID": outputCOVID})


def students(request):
    df = pd.read_csv("./myApp/templates/myApp/students.csv", header=None)
    with connection.cursor() as cursor:
        for _, row in df.iterrows():
            sqlQueryStudents = f"""
                INSERT INTO Students(`studentID`, `name`, `score`, `county`)
                VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}');
                """
            cursor.execute(sqlQueryStudents)
        cursor.fetchall()
        connection.commit()
        connection.close()
        
    return redirect('index')
    
def professors(request):
    df = pd.read_csv("./myApp/templates/myApp/professors.csv", header=None)
    with connection.cursor() as cursor:
        for _, row in df.iterrows():
            sqlQueryProfessors = f"""
                INSERT INTO Professors(`facultyID`, `name`, `age`, `county`)
                VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}');
                """
            cursor.execute(sqlQueryProfessors)
        cursor.fetchall()
        connection.commit()
        connection.close()
        
    return redirect('index')

def counties(request):
    df = pd.read_csv("./myApp/templates/myApp/counties.csv", header=None)
    with connection.cursor() as cursor:
        for _, row in df.iterrows():
            sqlQueryCounties = f"""
                INSERT INTO Counties(`countyName`, `population`, `city`)
                VALUES ('{row[0]}', '{row[1]}', '{row[2]}');
                """
            cursor.execute(sqlQueryCounties)
        cursor.fetchall()
        connection.commit()
        connection.close()
        
    return redirect('index')
    
def covid(request):
    df = pd.read_csv("./myApp/templates/myApp/students.csv", header=None)
    with connection.cursor() as cursor:
        for _, row in df.iterrows():
            sqlQueryCOVID = f"""
                INSERT INTO COVID(`patientID`, `city`)
                VALUES ('{row[0]}', '{row[1]}');
                """
            cursor.execute(sqlQueryCOVID)
        cursor.fetchall()
        connection.commit()
        connection.close()
        
    return redirect('index')