import mysql.connector


def get_connection():
    connection = mysql.connector.connect(host='localhost',
                                         database='consultants',
                                         user='root',
                                         password='root')
    return connection

def close_connection(connection):
    if connection:
        connection.close()

def testconnection():
    try:
        connection=db.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("You are connected to MySQL version: ", db_version)
        queryResult = db.getAllFromDb()
        db.close_connection(connection)
        return '<h1>It works.</h1>'+'<h2>found '+str(queryResult)+'</h2>'
    except Exception as e:
        # see Terminal for description of the error
        print("\nThe error:\n" + str(e) + "\n")
        return '<h1>Something is broken.</h1>'



def getAllConsultants():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM consult ORDER BY firstname ASC;")
    allConsultants = cursor.fetchall()
    close_connection(connection)
    return allConsultants


def getAllTags():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT TAG from TAGS")
    allTags = cursor.fetchall()
    close_connection(connection)
    return allTags


def searchDB(query):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM consult WHERE lower('"+query+"') IN (lower(firstname), lower(lastname),lower(role), lower(location));")
    consult_results = cursor.fetchall()
    cursor.execute("SELECT id FROM tags WHERE lower(tag) LIKE lower('"+query+"')")
    tags_consult_ids = cursor.fetchall()
    for consult_id in tags_consult_ids:
        cursor.execute("SELECT * FROM consult WHERE id = '"+str(consult_id[0])+"'")
        consult = cursor.fetchall()
        consult_results = consult_results + consult
    close_connection(connection)
    return consult_results


def searchMultiple(*arguments):
    connection = get_connection()
    cursor = connection.cursor()
    print(arguments)
    #for question in arguments[0]:
    #    cursor.execute("SELECT * FROM consult WHERE lower('" + question + "') IN (lower(firstname), lower(lastname),lower(role), lower(location));")
    #    consult_results = cursor.fetchall()
    #    cursor.execute("SELECT id FROM tags WHERE lower(tag) LIKE lower('" + question + "')")
    #    consult_ids = cursor.fetchall()
    #    for consult_id in consult_ids:
    #        cursor.execute("SELECT * FROM consult WHERE id = '" + str(consult_id[0]) + "'")
    #        consult = cursor.fetchall()
    #        consult_results = consult_results + consult
    consultQuery=""
    #OCH på consult table
    #for question in arguments[0]:
    #    if arguments[0][0] == question:
    #        consultQuery = consultQuery + "SELECT * FROM consult WHERE '" + question + "' IN (firstname, lastname,role, location) "
    #    elif arguments[0][-1] == question:
    #        consultQuery = consultQuery + "AND '" + question + "' IN (firstname, lastname, role, location);"
    #    else:
    #        consultQuery = consultQuery + "AND '"+question+"' IN (firstname, lastname, role, location) "
    #cursor.execute(consultQuery)
    #consult_results = cursor.fetchall()
    #
    #for question in arguments[0]:
    #    if arguments[0][0] == question:
    #        #first line
    #    elif arguments[0][-1] == question:
    #        #endline
    #    else:
            #midline
    cursor.execute(query)
    results = cursor.fetchall()



    close_connection(connection)
    return consult_results


def getTags(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT tag from tags WHERE id = '"+str(id)+"'")
    tags = cursor.fetchall()
    close_connection(connection)
    return tags

