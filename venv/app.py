# app.py
import os
import sys
from flask import Flask, request, render_template

import mysql.connector

#root paths and settings
sys.path.insert(0, os.path.dirname(__file__))
project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates')
app = Flask(__name__, template_folder=template_path)
app.static_folder = 'static'


@app.route("/")
def search():
    query = request.args.get('query')
    if(query!=None):
        print(query, file=sys.stdout)
        return render_template('index.html', search="True", keywords=query)
    elif(request.method == 'GET'):
        return render_template('index.html')


@app.route("/search")
def searchresults():
    query = request.args.get('query')
    print("Searching for "+query)
    consultants = searchDB(query)
    consultantsHTML = buildData(consultants)
    #print("found "+str(consultants))
    return render_template('search.html', keywords=query, data=consultantsHTML)

@app.route('/testdb')
def testdb():
    try:
        connection=get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("You are connected to MySQL version: ", db_version)
        close_connection(connection)
        queryResult = getAllFromDb()
        return '<h1>It works.</h1>'+'<h2>found '+str(queryResult)+'</h2>'
    except Exception as e:
        # see Terminal for description of the error
        print("\nThe error:\n" + str(e) + "\n")
        return '<h1>Something is broken.</h1>'

def get_connection():
    connection = mysql.connector.connect(host='localhost',
                                         database='consultants',
                                         user='root',
                                         password='root')
    return connection

def close_connection(connection):
    if connection:
        connection.close()


def getAllFromDb():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM consult;")
    allConsultants = cursor.fetchall()
    close_connection(connection)
    return allConsultants

def searchDB(query):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM consult WHERE '"+query+"' IN (consultant_name, consultant_role, location);")
    results = cursor.fetchall()
    close_connection(connection)
    return results

def buildData(data):
    query = request.args.get('query')
    consultants = searchDB(query)
    finalHTML = ""
    #for debug
    for consult in consultants:
        start = '<li class="entity-result"> <div class="searchResult"> <div class="result-img"> <img class="profile-img"src="' + \
                consult[4] + '"> </div> <div class="result-name">' + consult[1] + '</div> <div class="result-role">' + consult[2] + '</div> <div class="table"> <ul class="result-tags-list">'
        tags = consult[3].split(",")
        HTMLtags = ""
        for tag in tags:
            HTMLtags = HTMLtags + '<li class="tag">' + tag + '</li>'

        end = '</ul></div><div class="description">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ligula urna,pharetra id accumsan sit amet, congue sed erat. Integer sed finibus enim. Donec sit amet bibendumsapien. </div> <div class="result-location"><img class="location-tag"src="https://flyclipart.com/thumb2/location-pin-emoji-934877.png">' + \
              consult[5] + '</div></div></li>'
        finalHTML = finalHTML + start + HTMLtags + end;
    return finalHTML

if __name__ == '__main__':
    app.run(debug=True)
