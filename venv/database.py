import mysql.connector


def get_connection():
    connection = mysql.connector.connect(host='localhost',
                                         database='consultants',
                                         user='root',
                                         password='cometSatelight$42',
                                         auth_plugin='mysql_native_password'
                                         )
    return connection

def close_connection(connection):
    if connection:
        connection.close()

def test_connection():
    try:
        connection=get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("You are connected to MySQL version: ", db_version)
        queryResult = get_all_consultants()
        close_connection(connection)
        return '<h1>It works.</h1>'+'<h2>found '+str(queryResult)+'</h2>'
    except Exception as e:
        # see Terminal for description of the error
        print("\nThe error:\n" + str(e) + "\n")
        return '<h1>Something is broken.</h1>'



def get_all_consultants():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM consult ORDER BY firstname ASC;")
    allConsultants = cursor.fetchall()
    close_connection(connection)
    return allConsultants


def get_all_tags():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT TAG from TAGS")
    allTags = cursor.fetchall()
    close_connection(connection)
    return allTags


def search_db(query):
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


def get_tags(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT tag from tags WHERE id = '"+str(id)+"'")
    tags = cursor.fetchall()
    close_connection(connection)
    return tags

def add_consultants_to_db(list_to_add):
    connection = get_connection()
    cursor = connection.cursor()
    for profile in list_to_add:
        #doublecheck that profile doesnt exist
        print("PROFILE:")
        print(profile[0]+"' and lastname = '"+profile[1][0]+"' and role = '"+profile[2]+"' and location = '"+profile[4])
        cursor.execute("SELECT id from consult where firstname = '"+profile[0]+"' and lastname = '"+profile[1][0]+"' and role = '"+profile[2]+"' and location = '"+profile[4]+"';")
        result = cursor.fetchall()
        if(len(result) == 0):
            cursor.execute("INSERT INTO consult (firstname, lastname, role, image_url, location, description) VALUES('"+profile[0]+"','"+profile[1][0]+"','"+profile[2]+"','"+profile[3]+"','"+profile[4]+"','"+profile[5]+"');")
            cursor.execute("SELECT id from consult where firstname = '"+profile[0]+"' and lastname = '"+profile[1][0]+"' and role = '"+profile[2]+"' and image_url = '"+profile[3]+"' and location = '"+profile[4]+"' and description = '"+profile[5]+"';")
            consult_id = cursor.fetchall()
            add_tags_to_db(profile[6])
            tag_id_list = []
            for tag in profile[6]:
                cursor.execute("SELECT id FROM tags WHERE tag = '"+tag+"'")
                tag_id = cursor.fetchone()
                if tag_id is not None:
                    connect_consult_to_tag(consult_id, tag_id)
        else:
            print("Consult "+str(consult)+" already exists in database")
    close_connection(connection)

def add_tags_to_db(list_of_tags):
    connection = get_connection()
    cursor = connection.cursor()
    for tag in list_of_tags:
        cursor.execute("SELECT id FROM tags where tag = '"+tag+"';")
        results = cursor.fetchall()
        if (len(results) == 0):
            cursor.execute("INSERT INTO tags(tag) VALUES ('"+tag+"');")
        else:
            print("Tag "+tag+" already exists in database")
    close_connection(connection)

def connect_consult_to_tag(consult_id, tag_id):
    connection = get_connection()
    cursor = connection.cursor()
    #check if connection exists
    print("debug")
    print("connect consult to tag")
    print("consult_id "+str(consult_id))
    print("tag_id "+str(tag_id))
    cursor.execute("SELECT consult_tag_id FROM consult_tags WHERE consult_id = '"+consult_id[0]+"' and tag_id = '"+tag_id[0]+"'")
    results = cursor.fetchall()
    if (len(results) == 0):
        cursor.execute("INSERT INTO consult_tags(consult_id, tag_id) VALUES ('"+consult_id[0]+"',"+tag_id[0]+");")
    else:
        print("connection between tag_id "+str(tag_id)+" and consult_id "+consult_id[0]+" already exists")
    close_connection(connection)
