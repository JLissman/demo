# app.py
import os
import sys
from flask import Flask, request, render_template
import database as db
from login_app import index_page, login_page, callback_page, logout_page, login_is_required
import builders as build
import copy

#root paths and settings
sys.path.insert(0, os.path.dirname(__file__))
project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates')
app = Flask(__name__, template_folder=template_path)
app.static_folder = 'static'
app = Flask("Competence_Finder")
app.secret_key = "4179" #it is necessary to set a password when dealing with OAuth 2.0

#register blueprints from login_app.py
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
        queryList = arguments.split(",")
        print(queryList)
        if("," in arguments):
            searchString = arguments.replace(",", " & ")
        else:
            searchString = arguments

        consultants = db.search_multiple_v2(queryList)
        print(len(consultants))
        consultantsChecked = checkSearch_v2(queryList, consultants)
        print(len(consultantsChecked))
        consultantsHTML = build.build_consultants_v2(consultantsChecked)
        return render_template('search.html', keywords="Your search for: "+searchString+" Returned "+str(len(consultantsChecked))+" Result(s)", data=consultantsHTML, programmingLanguages=programmingTags)
    else:
        consultants = db.get_all_consultants()
        consultantsHTML = build.build_consultants(consultants)
        return render_template('search.html',keywords="Do a search for more specific results", data=consultantsHTML, programmingLanguages=programmingTags)


@app.route("/advSearch")
@login_is_required
def advanced_search():
    programmingTags = build.build_tags()
    nameList = build.build_names()
    locationList = build.build_locations()
    titleList = build.build_roles()
    arguments = request.args
    if arguments is not None:
        name = arguments.get('nam')
        location = arguments.get('loc') #OR
        title = arguments.get('tit')
        tags = arguments.get('tag')
        print(name, location, title, tags)
        return render_template('advancedSearch.html', programmingLanguages=programmingTags,nameList=nameList,locationList=locationList, titleList = titleList)
    else:
        return render_template('advancedSearch.html', programmingLanguages=programmingTags,nameList=nameList,locationList=locationList, titleList = titleList)

@app.route("/test")
def test():

    return str(db.search_multiple_v2(["test"]))


@app.route("/testdb")
@login_is_required
def dbtest():
    return db.test_connection()



@app.route("/profile")
@login_is_required
def profile():
    programmingTags = build.build_tags()

    id = request.args.get('id')
    consult = db.get_consult_by_id(id)
    return render_template('profile.html', consult=consult, programmingLanguages=programmingTags)


def checkSearch(queryList, dataList):
    res = copy.deepcopy(dataList)
    for profile in dataList:
        for query in queryList:
            tags_lower = []
            for tag in profile["tags"]:
                tags_lower.append(tag.lower())
            if (query.lower() not in tags_lower and (query.lower() not in profile["firstname"] or query.lower() not in profile["lastname"] or query.lower() not in profile["role"] or query.lower() not in profile["location"])):
                if profile in res:
                    res.remove(profile)
            else:
                pass
                print("profile: "+str(profile["consult_id"])+": "+query+" is in "+str(tags_lower))
    return res

def checkSearch_v2(queryList, dataList):
    res = copy.deepcopy(dataList)
    for id in dataList:
        for query in queryList:
            tags_lower = []
            for tag in dataList[id]["tags"]:
                tags_lower.append(tag.lower())
            if (query.lower() not in tags_lower and (query.lower() not in dataList[id]["name"]  or query.lower() not in dataList[id]["role"] or query.lower() not in dataList[id]["location"])):
                if id in res:
                    del res[id]
            else:
                pass
                print("profile: "+str(id)+": "+query+" is in "+str(tags_lower))
    return res


if __name__ == '__main__':
    app.run(debug=True)
