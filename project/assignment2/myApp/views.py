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
    outputOfQuery2 = []
    outputOfQuery3 = []
    outputOfQuery4 = []
    outputOfQuery5 = []
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

        sqlQuery1 = """
            SELECT county AS countyName, AVG(score) AS score
            FROM Students
            GROUP BY county
            ORDER BY county ASC;
                    """
        cursor.execute(sqlQuery1)
        fetchResultQuery1 = cursor.fetchall()
        
        sqlQuery2 = """
            SELECT city AS cityName, AVG(score) AS score
            FROM Students JOIN Counties
            ON county = countyName 
            GROUP BY city
            ORDER BY city ASC;
                    """
        cursor.execute(sqlQuery2)
        fetchResultQuery2 = cursor.fetchall()

        sqlQuery3 = """
            SELECT profName, name
            FROM (SELECT t1.county, name
                FROM Students as t1 
                JOIN (SELECT MAX(score) as score, county
                    FROM Students
                    GROUP BY county) as t2
                ON t1.county = t2.county and
                t1.score = t2.score
                ORDER BY t1.county) as t1
            JOIN
                (SELECT t1.county, name as profName
                FROM Professors as t1 
                JOIN (SELECT MAX(age) as age, county
                    FROM Professors
                    GROUP BY county) as t2
                ON t1.county = t2.county and
                t1.age = t2.age
                ORDER BY t1.county) as t2
            ON t1.county = t2.county
            ORDER BY t1.county;
                    """
        cursor.execute(sqlQuery3)
        fetchResultQuery3 = cursor.fetchall()


        sqlQuery4 = """
            SELECT profName, name
            FROM (SELECT t1.city, name
                FROM (SELECT * FROM Students as std JOIN Counties as c ON std.county = c.countyName) as t1 
                JOIN (SELECT MAX(score) as score, city
                    FROM (SELECT * FROM Students as std JOIN Counties as c ON std.county = c.countyName) as t3
                    GROUP BY city) as t2
                ON t1.city = t2.city and
                t1.score = t2.score
                ORDER BY t1.city) as t1
            JOIN
                (SELECT t1.city, name as profName
                FROM (SELECT * FROM Professors as prof JOIN Counties as c ON prof.county = c.countyName) as t1 
                JOIN (SELECT MAX(age) as age, city
                    FROM (SELECT * FROM Professors as prof JOIN Counties as c ON prof.county = c.countyName) as t3
                    GROUP BY city) as t2
                ON t1.city = t2.city and
                t1.age = t2.age
                ORDER BY t1.city) as t2
            ON t1.city = t2.city
            ORDER BY t1.city;
                    """
        cursor.execute(sqlQuery4)
        fetchResultQuery4 = cursor.fetchall()
        
        sqlQuery5 = """
            SELECT 
                tt.name as name, tt.city as city
            FROM
                (SELECT *
                    FROM Students as t1
                    JOIN Counties as t2
                    ON t1.county = t2.countyName) as tt
            WHERE
                tt.city IN (SELECT 
                        tmp.city
                    FROM
                        (SELECT 
                            t1.city
                        FROM
                            (SELECT 
                                city, SUM(population) AS pop
                            FROM
                                Counties
                            GROUP BY city) AS t1
                        JOIN (SELECT 
                                city, COUNT(patientID) AS pat
                            FROM
                                COVID
                            GROUP BY city) AS t2
                        ON t1.city = t2.city
                        ORDER BY t2.pat / t1.pop DESC
                        LIMIT 3 
                        ) AS tmp
                    );
                    """
        cursor.execute(sqlQuery5)
        fetchResultQuery5 = cursor.fetchall()

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

        for temp in fetchResultQuery1:
            eachRow = {'countyName': temp[0], 'score': round(temp[1], 3)}
            outputOfQuery1.append(eachRow)

        for temp in fetchResultQuery2:
            eachRow = {'cityName': temp[0], 'score': round(temp[1], 3)}
            outputOfQuery2.append(eachRow)

        for temp in fetchResultQuery3:
            eachRow = {'profName': temp[0], 'name': temp[1]}
            outputOfQuery3.append(eachRow)

        for temp in fetchResultQuery4:
            eachRow = {'profName': temp[0], 'name': temp[1]}
            outputOfQuery4.append(eachRow)

        for temp in fetchResultQuery5:
            eachRow = {'name': temp[0], 'city': temp[1]}
            outputOfQuery5.append(eachRow)

    return render(request, 'myApp/index.html', {"Students": outputStudents,
                                                "Professors": outputProfessors,
                                                "Counties": outputCounties,
                                                "COVID": outputCOVID,
                                                "output1": outputOfQuery1,
                                                "output2": outputOfQuery2,
                                                "output3": outputOfQuery3,
                                                "output4": outputOfQuery4,
                                                "output5": outputOfQuery5})


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
    df = pd.read_csv("./myApp/templates/myApp/covid.csv", header=None)
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