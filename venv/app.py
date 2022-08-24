# app.py
import os
import sys
from flask import Flask, request, render_template
import database as db
from login_app import index_page, login_page, callback_page, logout_page, login_is_required
import builders as build


#root paths and settings
sys.path.insert(0, os.path.dirname(__file__))
project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates')
app = Flask(__name__, template_folder=template_path)
app.static_folder = 'static'
app = Flask("Competence_Finder")
app.secret_key = "4179" #it is necessary to set a password when dealing with OAuth 2.0
#register blueprints from login_app
app.register_blueprint(index_page)
app.register_blueprint(login_page)
app.register_blueprint(callback_page)
app.register_blueprint(logout_page)


@app.route("/home")
@login_is_required
def home():
    programmingTags = build.build_tags()
    return render_template('index.html', programmingLanguages=programmingTags)


@app.route("/search")
@login_is_required
def searchresults():
    programmingTags = build.build_tags()

    arguments  = request.args.get('query')

    if(arguments is not None):
        queryList = arguments.split(" ")
        consultantsHTML = ""
        #just nu är det AND istället för OCH
        for query in queryList:
            print("Searching for "+query)
            consultants = db.search_db(query)
            consultantsHTML = consultantsHTML + build.build_consultants(consultants)
        return render_template('search.html', keywords="Searching for "+str(queryList), data=consultantsHTML, programmingLanguages=programmingTags)


    else:
        consultants = db.get_all_consultants()
        consultantsHTML = build.build_consultants(consultants)
        return render_template('search.html',keywords="Do a search for more specific results", data=consultantsHTML, programmingLanguages=programmingTags)


@app.route("/testdb")
@login_is_required
def dbtest():
    return db.test_connection()



@app.route("/addToDbTests")
def addTest():
    db.add_tags_to_db(("Java", "bosse bildoktorn"))
    return "Completed"

if __name__ == '__main__':
    app.run(debug=True)
