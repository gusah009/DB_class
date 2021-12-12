from django.shortcuts import render
from django.db import connection

# Create your views here.

def display(request):
    outputStudents = []
    outputProfessors = []
    outputCounties = []
    outputCOVID = []
    outputOfQuery1 = []
    with connection.cursor() as cursor:
        sqlQueryStudents = """  
                            SELECT `students`.`studentID`,
                                `students`.`name`,
                                `students`.`score`,
                                `students`.`county`
                            FROM `assignment2db`.`students`;
                            """
        cursor.execute(sqlQueryStudents)
        fetchResultStudents = cursor.fetchall()
        
        sqlQueryProfessors = """
                            SELECT `professor`.`facultyID`,
                                `professor`.`name`,
                                `professor`.`age`,
                                `professor`.`county`
                            FROM `assignment2db`.`professor`;
                            """
        cursor.execute(sqlQueryProfessors)
        fetchResultProfessors = cursor.fetchall()
        
        sqlQueryCounties = """
                            SELECT `counties`.`countyName`,
                                `counties`.`population`,
                                `counties`.`city`
                            FROM `assignment2db`.`counties`;
                            """        
        cursor.execute(sqlQueryCounties)
        fetchResultCounties = cursor.fetchall()
        
        sqlQueryCOVID = """
                        SELECT `covid`.`patientID`,
                            `covid`.`city`
                        FROM `assignment2db`.`covid`;
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
            eachRow =   {'facultyID', temp[0], 'name', temp[1], 'age', temp[2], 'county', temp[3]}
            outputProfessors.append(eachRow)
                            
        for temp in fetchResultCounties:
            eachRow =   {'countyName': temp[0], 'population': temp[1], 'city': temp[2]}
            outputCounties.append(eachRow)

        for temp in fetchResultCOVID:
            eachRow =   {'patientID': temp[0], 'name': temp[1]}
            outputCOVID.append(eachRow)

        # for temp in fetchResultQuery1:
        #     eachRow = {'categoryname': temp[0], 'categorydescription': temp[1]}
        #     outputOfQuery1.append(eachRow)

    return render(request, 'myApp/index.html', {"Students": outputStudents,
                                                "Professors": outputProfessors,
                                                "Counties": outputCounties,
                                                "COVID": outputCOVID})
