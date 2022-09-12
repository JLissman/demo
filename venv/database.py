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
        #tags
        cursor.execute("SELECT * FROM tags")
        tags = cursor.fetchall()
        #consultants
        cursor.execute("SELECT * FROM consult")
        consults = cursor.fetchall()
        #tag_consultants connections
        cursor.execute("SELECT * FROM consult_tags")
        consult_tags = cursor.fetchall()

        close_connection(connection)
        return '<h1>It works.</h1>'+'<h2>Consultants:'+str(consults)+'</h2>'+'<h2>Tags:'+str(tags)+'</h2>'+'<h2>consult_tag connections:'+str(consult_tags)+'</h2>'
    except Exception as e:
        # see Terminal for description of the error
        print("\nThe error:\n" + str(e) + "\n")
        return '<h1>Something is broken.</h1>'



#def get_all_consultants():
#    connection = get_connection()
#    cursor = connection.cursor(dictionary=True)
#    cursor.execute("SELECT DISTINCT consult.id, firstname, lastname, role, image_url, location, description FROM consultants.consult LEFT JOIN tags on consult.id = tags.id LEFT JOIN consult_tags on consult.id = consult_tags.consult_id ORDER BY firstname ASC")
#    allConsultants = cursor.fetchall()
#    tupleCursor = connection.cursor()
#    for profile in allConsultants:
#        tupleCursor.execute(
#            "SELECT tag FROM tags INNER JOIN consult_tags on consult_tags.tag_id = tags.id WHERE consult_id = '" + str(profile["id"]) + "'")
#        profilePos = allConsultants.index(profile)
#        allConsultants[profilePos]["tags"] = []
#        tags = tupleCursor.fetchall()
#        for tag in tags:
#            allConsultants[profilePos]["tags"].append(tag[0])
#    close_connection(connection)
#    return allConsultants

def get_all_consultants():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT consult.id, firstname, lastname, role, image_url, location, description FROM consultants.consult LEFT JOIN tags on consult.id = tags.id LEFT JOIN consult_tags on consult.id = consult_tags.consult_id ORDER BY firstname ASC")
    allConsultants = cursor.fetchall()
    tupleCursor = connection.cursor()
    resultDict = {}
    for profile in allConsultants:
        resultDict[profile["id"]] = {"name": profile["firstname"] + " " + profile["lastname"], "role": profile["role"],
                                     "location": profile["location"], "image_url": profile["image_url"],
                                     "description": profile["description"], "tags": []}
        tupleCursor.execute(
            "SELECT tag FROM tags INNER JOIN consult_tags on consult_tags.tag_id = tags.id WHERE consult_id = '" + str(profile["id"]) + "'")

        tags = tupleCursor.fetchall()
        for tag in tags:
            resultDict[profile["id"]]["tags"].append(tag[0])
    close_connection(connection)
    return resultDict


def get_all_tags():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT ID,TAG from TAGS")
    allTags = cursor.fetchall()
    close_connection(connection)
    return allTags

def get_all_names():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT firstname, lastname FROM  consult")
    allNames = cursor.fetchall()
    close_connection(connection)
    return allNames


def get_all_locations():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT location FROM  consult")
    allLocations = cursor.fetchall()
    close_connection(connection)
    return allLocations

def get_all_roles():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT role FROM  consult")
    allRoles = cursor.fetchall()
    close_connection(connection)
    return allRoles



def search_multiple(*args):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT DISTINCT id, firstname, lastname, role, image_url, location, description FROM consultants.consult_tags LEFT JOIN tags on consult_tags.tag_id = tags.id LEFT JOIN consult on consult_tags.consult_id = consult.id "
    for arg in args[0]:
        if arg == args[0][0]:
            #first
            query = query + "WHERE '"+str(arg)+"' in (firstname, lastname, role, location, tag) "
        elif arg == args[0][-1]:
            #last
            query = query + "OR '"+str(arg)+"' in (firstname, lastname, role, location, tag);"
        else:
            query = query + "OR '"+str(arg)+"' in (firstname, lastname, role, location, tag) "
    cursor.execute(query)
    results = cursor.fetchall()
    #add tags to each profile
    tupleCursor = connection.cursor()
    for profile in results:
        tupleCursor.execute("SELECT tag FROM tags INNER JOIN consult_tags on consult_tags.tag_id = tags.id WHERE consult_id = '"+str(profile["consult_id"])+"'")
        profilePos = results.index(profile)
        results[profilePos]["tags"] = []
        tags = tupleCursor.fetchall()
        for tag in tags:
            results[profilePos]["tags"].append(tag[0])

    close_connection(connection)
    return results

def search_multiple_v2(*args):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT DISTINCT consult.id, firstname, lastname, role, image_url, location, description FROM consultants.consult_tags LEFT JOIN tags on consult_tags.tag_id = tags.id LEFT JOIN consult on consult_tags.consult_id = consult.id "
    for arg in args[0]:
        if arg == args[0][0]:
            #first
            query = query + "WHERE '"+str(arg)+"' in (firstname, lastname, role, location, tag) "
        elif arg == args[0][-1]:
            #last
            query = query + "OR '"+str(arg)+"' in (firstname, lastname, role, location, tag);"
        else:
            query = query + "OR '"+str(arg)+"' in (firstname, lastname, role, location, tag) "
    cursor.execute(query)
    results = cursor.fetchall()
    print("SEARCH MUTL RESULTSLEN")
    print(len(results))
    #add tags to each profile and convert result dictionary to new dictionary using consult id as key
    resultDict = {}
    tupleCursor = connection.cursor()
    for profile in results:
        if profile["id"] is not None:
            print(profile)
            tupleCursor.execute("SELECT tag FROM tags INNER JOIN consult_tags on consult_tags.tag_id = tags.id WHERE consult_id = '"+str(profile["id"])+"'")
            tags = tupleCursor.fetchall()

            resultDict[profile["id"]] = {"name":profile["firstname"]+" "+profile["lastname"],"role":profile["role"], "location":profile["location"],"image_url":profile["image_url"],"description":profile["description"], "tags":[]}
            #resultDict[profilePos]["tags"] = []
            for tag in tags:
                resultDict[profile["id"]]["tags"].append(tag[0])

    close_connection(connection)
    return resultDict



def get_tags(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT tag FROM consult_tags INNER JOIN tags on consult_tags.tag_id = tags.id WHERE consult_id = '"+str(id)+"'")
    tags = cursor.fetchall()
    close_connection(connection)
    return tags

def get_consult_by_id(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM consult WHERE ID = '"+id+"'")
    consult = cursor.fetchone()
    cursor.execute("SELECT tag FROM consult_tags INNER JOIN tags on tags.id=tag_id WHERE consult_id = '"+id+"'")
    tags = cursor.fetchall()


    close_connection(connection)
    if(len(consult) > 0):
        consult_dict = {"name": consult[1] + " " + consult[2], "role": consult[3], "image_url": consult[4],
                        "location": consult[5], "description": consult[6], "tags": tags}
        return consult_dict;


def add_consultants_to_db(list_to_add):
    connection = get_connection()
    cursor = connection.cursor()
    for profile in list_to_add:
        #check that profile doesnt exist
        cursor.execute("SELECT id from consult where firstname = '"+profile[0]+"' and lastname = '"+profile[1][0]+"' and role = '"+profile[2]+"' and location = '"+profile[4]+"';")
        result = cursor.fetchall()
        if(len(result) == 0):
            cursor.execute("INSERT INTO consult (firstname, lastname, role, image_url, location, description) VALUES('"+profile[0]+"','"+profile[1][0]+"','"+profile[2]+"','"+profile[3]+"','"+profile[4]+"','"+profile[5]+"');")
            connection.commit()
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
            print("Consult "+str(profile)+" already exists in database")
    close_connection(connection)

def add_tags_to_db(list_of_tags):
    connection = get_connection()
    cursor = connection.cursor()
    for tag in list_of_tags:
        cursor.execute("SELECT id FROM tags where tag = '"+tag+"';")
        results = cursor.fetchall()
        if (len(results) == 0):
            cursor.execute("INSERT INTO tags(tag) VALUES ('"+tag+"');")
            connection.commit()
        else:
            print("Tag "+tag+" already exists in database")
    close_connection(connection)

def connect_consult_to_tag(consult_id, tag_id):
    connection = get_connection()
    cursor = connection.cursor()

    #convert variables from list in tuple to string
    print()
    try:
        consult_id = str(consult_id[0][0])
    except:
        consult_id = str(consult_id[0])
    try:
        tag_id = str(tag_id[0][0])
    except:
        tag_id = str(tag_id[0])
    #check that connection doesnt already exist
    cursor.execute("SELECT consult_tag_id FROM consult_tags WHERE consult_id = '"+consult_id+"' and tag_id = '"+tag_id+"'")
    results_consult_tag = cursor.fetchall()

    #check that consult id exists
    cursor.execute("SELECT id FROM consult where id = '"+consult_id+"'")
    result_consult = cursor.fetchall()
    print("LEN RESULT CONSULT CONNECTION ")
    print(len(result_consult))
    #check that tag id exists
    cursor.execute("SELECT id FROM tags WHERE id = '"+tag_id+"'")
    result_tag = cursor.fetchall()
    print("LEN RESULT TAG CONNECTION")
    print(len(result_tag))


    if (len(results_consult_tag) == 0 and len(result_consult) != 0 and len(result_tag) != 0):
        cursor.execute("INSERT INTO consult_tags(consult_id, tag_id) VALUES ('"+consult_id+"',"+tag_id+");")
        connection.commit()
        close_connection(connection)
        return True
    else:
        print("connection between tag_id "+tag_id+" and consult_id "+consult_id+" already exists")
        close_connection(connection)
        return False

def remove_tag_from_consult(consult_id, tag_id):
    connection = get_connection()
    cursor = connection.cursor()
    print(consult_id, tag_id)
    cursor.execute("SELECT consult_tag_id FROM consult_tags WHERE consult_id = '"+str(consult_id)+"' AND tag_id ='"+str(tag_id[0])+"'")
    result = cursor.fetchone()
    if(result):
        print("deleting "+str(result))
        #sql = "DELETE FROM consult_tags WHERE consult_id = '"+str(consult_id)+"' AND tag_id ='"+str(tag_id)+"'"
        #cursor.execute(sql)
        #connection.commit()
        close_connection(connection)
        return True
    else:
        close_connection(connection)
        return False


def get_tag_id(tag_name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id from tags where tag = '"+tag_name+"'")
    result = cursor.fetchone()
    close_connection(connection)
    return result

def add_consult(consult):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM CONSULT WHERE firstname = '"+consult["firstname"]+"' AND lastname = '"+consult["lastname"]+"'")
    result = cursor.fetchone()
    print(result)
    if not result:
        print("adding consult to DB")
        cursor.execute("INSERT INTO CONSULT(firstname, lastname, role, location, description, image_url) "
                       "VALUES('"+consult["firstname"]+"','"+consult["lastname"]+"','"+consult["role"]+"','"+consult["location"]+"','"+consult["description"]+"','"+consult["image_url"]+"')")

        cursor.execute("SELECT ID FROM CONSULT WHERE firstname = '"+consult["firstname"]+"' and lastname = '"+consult["lastname"]+"' and role = '"+consult["role"]+"'")
        consult_id = cursor.fetchone()
        print("**********************")
        print(consult["tags"])
        print("***************")
        print(consult_id)
        print("******************")
        connection.commit()
        for tag in consult["tags"]:
            tag_id = get_tag_id(tag)
            connect_consult_to_tag_status = connect_consult_to_tag(consult_id, tag_id)
            print("connect consult to tag status is "+str(connect_consult_to_tag_status))

        return True
    else:
        return False

def add_tag(tagname):
    connection = get_connection()
    cursor = connection.cursor(buffered=True)
    results = cursor.execute("SELECT * from TAGS where tag ='"+tagname+"'")
    if not results:
        cursor.execute("INSERT INTO tags (tag) Values('"+tagname+"');")
        connection.commit()
        close_connection(connection)
        return True
    else:
        return False

def remove_tag(tagname):
    connection = get_connection()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * from tags where lower(tag) = lower('"+tagname+"')")
    result = cursor.fetchall()
    if result:
        cursor.execute("DELETE FROM tags WHERE lower(tag) = lower('"+tagname+"') LIMIT 1;")
        connection.commit()
        close_connection(connection)
        return True
    else:
        close_connection(connection)
        return False

def remove_consult(consult_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("Select * from consult where id = '"+consult_id+"'")
    result = cursor.fetchall()
    if result:
        cursor.execute("DELETE FROM CONSULT WHERE id = '" + consult_id + "' LIMIT 1;")
        connection.commit()
        close_connection(connection)
        return True
    else:
        close_connection(connection)
        return False

