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



def get_all_consultants():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT consult_id, firstname, lastname, role, image_url, location, description FROM consultants.consult_tags LEFT JOIN tags on consult_tags.tag_id = tags.id LEFT JOIN consult on consult_tags.consult_id = consult.id ORDER BY firstname ASC;")
    allConsultants = cursor.fetchall()
    tupleCursor = connection.cursor()
    for profile in allConsultants:
        tupleCursor.execute(
            "SELECT tag FROM tags INNER JOIN consult_tags on consult_tags.tag_id = tags.id WHERE consult_id = '" + str(
                profile["consult_id"]) + "'")
        profilePos = allConsultants.index(profile)
        allConsultants[profilePos]["tags"] = []
        tags = tupleCursor.fetchall()
        for tag in tags:
            allConsultants[profilePos]["tags"].append(tag[0])
    close_connection(connection)
    return allConsultants


def get_all_tags():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT TAG from TAGS")
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


#################### old
#def search_db(*queries):
#    connection = get_connection()
#    cursor = connection.cursor()
#    print("QUERIES")
#    print(queries)
#    for query in queries[0]:
#        cursor.execute("SELECT * FROM consult WHERE '"+query+"' IN (firstname, lastname, role, location);")
#        consult_results = cursor.fetchall()
#        cursor.execute("SELECT id FROM tags WHERE '"+query+"' LIKE (tag)")
#        tags_ids = cursor.fetchall()
#        for tag_id in tags_ids:
#            cursor.execute("SELECT consult_id from consult_tags WHERE tag_id = '"+str(tag_id[0])+"'")
#            tags_consult_ids = cursor.fetchall()
#            for consult_id in tags_consult_ids:
#                cursor.execute("SELECT * FROM consult WHERE id = '" + str(consult_id[0]) + "'")
#                consult = cursor.fetchall()
#                consult_results = consult_results + consult
#
#
#    close_connection(connection)
#    return consult_results
####################

def search_multiple(*args):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT DISTINCT consult_id, firstname, lastname, role, image_url, location, description FROM consultants.consult_tags LEFT JOIN tags on consult_tags.tag_id = tags.id LEFT JOIN consult on consult_tags.consult_id = consult.id "
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
    query = "SELECT DISTINCT consult_id, firstname, lastname, role, image_url, location, description FROM consultants.consult_tags LEFT JOIN tags on consult_tags.tag_id = tags.id LEFT JOIN consult on consult_tags.consult_id = consult.id "
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
    #add tags to each profile and convert result dictionary to new dictionary using consult id as key
    resultDict = {}
    tupleCursor = connection.cursor()
    for profile in results:
        tupleCursor.execute("SELECT tag FROM tags INNER JOIN consult_tags on consult_tags.tag_id = tags.id WHERE consult_id = '"+str(profile["consult_id"])+"'")
        tags = tupleCursor.fetchall()
        resultDict[profile["consult_id"]] = {"name":profile["firstname"]+" "+profile["lastname"],"role":profile["role"], "location":profile["location"],"image_url":profile["image_url"],"description":profile["description"], "tags":[]}
        #resultDict[profilePos]["tags"] = []
        for tag in tags:
            resultDict[profile["consult_id"]]["tags"].append(tag[0])

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
        #doublecheck that profile doesnt exist
        print("PROFILE:")
        #print(profile[0]+"' and lastname = '"+profile[1][0]+"' and role = '"+profile[2]+"' and location = '"+profile[4])
        cursor.execute("SELECT id from consult where firstname = '"+profile[0]+"' and lastname = '"+profile[1][0]+"' and role = '"+profile[2]+"' and location = '"+profile[4]+"';")
        result = cursor.fetchall()
        print("add_consultants_to_db result var")
        print(len(result))
        print(result)
        if(len(result) == 0):
            cursor.execute("INSERT INTO consult (firstname, lastname, role, image_url, location, description) VALUES('"+profile[0]+"','"+profile[1][0]+"','"+profile[2]+"','"+profile[3]+"','"+profile[4]+"','"+profile[5]+"');")
            connection.commit()
            cursor.execute("SELECT id from consult where firstname = '"+profile[0]+"' and lastname = '"+profile[1][0]+"' and role = '"+profile[2]+"' and image_url = '"+profile[3]+"' and location = '"+profile[4]+"' and description = '"+profile[5]+"';")
            consult_id = cursor.fetchall()
            print("add_consult_to_db consult_id after its been added to DB")
            add_tags_to_db(profile[6])
            tag_id_list = []
            for tag in profile[6]:
                cursor.execute("SELECT id FROM tags WHERE tag = '"+tag+"'")
                tag_id = cursor.fetchone()
                if tag_id is not None:
                    print("consult_tag connection does not exist")
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
    #check if connection exists
    print("debug")
    print("connect consult to tag")
    print("consult_id "+str(consult_id))
    print("tag_id "+str(tag_id))

    #convert variables from list in tuple to string
    consult_id = str(consult_id[0][0])
    tag_id = str(tag_id[0])

    #check that connection doesnt already exist
    cursor.execute("SELECT consult_tag_id FROM consult_tags WHERE consult_id = '"+consult_id+"' and tag_id = '"+tag_id+"'")
    results_consult_tag = cursor.fetchall()

    #check that consult id exists
    cursor.execute("SELECT id FROM consult where id = '"+consult_id+"'")
    result_consult = cursor.fetchall()
    #check that tag id exists
    cursor.execute("SELECT id FROM tags WHERE id = '"+tag_id+"'")
    result_tag = cursor.fetchall()

    if (len(results_consult_tag) == 0 and len(result_consult) != 0 and len(result_tag) != 0):
        cursor.execute("INSERT INTO consult_tags(consult_id, tag_id) VALUES ('"+consult_id+"',"+tag_id+");")
        connection.commit()
    else:
        print("connection between tag_id "+tag_id+" and consult_id "+consult_id+" already exists")
    close_connection(connection)
