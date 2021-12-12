from django.shortcuts import render
from django.db import connection

# Create your views here.

def display(request):
    outputCategories = []
    outputOfQuery1 = []
    with connection.cursor() as cursor:
        sqlQueryStudents = ""
        cursor.execute(sqlQueryStudents)
        fetchResultStudents = cursor.fetchall()
        
        sqlQueryProfessors = ""
        cursor.execute(sqlQueryProfessors)
        fetchResultProfessors = cursor.fetchall()
        
        sqlQueryCounties = ""
        cursor.execute(sqlQueryCounties)
        fetchResultCounties = cursor.fetchall()
        
        sqlQueryCOVID = ""
        cursor.execute(sqlQueryCOVID)
        fetchResultCOVID = cursor.fetchall()

        sqlQuery1 = "" 
        cursor.execute(sqlQuery1)
        fetchResultQuery1 = cursor.fetchall()
        
        sqlQuery2 = "" 
        cursor.execute(sqlQuery2)
        fetchResultQuery2 = cursor.fetchall()

        sqlQuery3 = "" 
        cursor.execute(sqlQuery3)
        fetchResultQuery3 = cursor.fetchall()

        sqlQuery4 = "" 
        cursor.execute(sqlQuery4)
        fetchResultQuery4 = cursor.fetchall()
        
        sqlQuery5 = "" 
        cursor.execute(sqlQuery5)
        fetchResultQuery5 = cursor.fetchall()

        connection.commit()
        connection.close()

        for temp in fetchResultStudents:
            eachRow = {'categoryid': temp[0], 'categoryname': temp[1], 'categorydescription': temp[2]}
            outputCategories.append(eachRow)

        for temp in fetchResultQuery1:
            eachRow = {'categoryname': temp[0], 'categorydescription': temp[1]}
            outputOfQuery1.append(eachRow)

    return render(request, 'myApp/index.html',{"categories": outputCategories, "output1": outputOfQuery1})
