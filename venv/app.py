# app.py
import os
import sys
from flask import Flask, request, render_template, jsonify, url_for
import database as db
from login_app import index_page, login_page, callback_page, logout_page, login_is_required
import builders as build
import copy
import tasks as task
from werkzeug.utils import secure_filename
#root paths and settings
sys.path.insert(0, os.path.dirname(__file__))
project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates')
app = Flask(__name__, template_folder=template_path)
app.static_folder = 'static'
app = Flask("Competence_Finder")
app.secret_key = "4179" #it is necessary to set a password when dealing with OAuth 2.0
app.config['UPLOAD_FOLDER'] = app.static_folder
#register blueprints
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
        #consultantsHTML = build.build_consultants_v2(consultantsChecked)
        return render_template('search.html', keywords="Your search for: "+searchString+" Returned "+str(len(consultantsChecked))+" Result(s)", data=consultantsChecked, programmingLanguages=programmingTags)
    else:
        consultants = db.get_all_consultants()
        #consultantsHTML = build.build_consultants_v2(consultants)
        return render_template('search.html',keywords="Do a search for more specific results", data=consultants, programmingLanguages=programmingTags)


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


@app.route("/testdb")
@login_is_required
def dbtest():
    return db.test_connection()


@app.route("/test")
def test():
    return checkWorker()


@app.route("/profile")
@login_is_required
def profile():
    programmingTags = build.build_tags()

    id = request.args.get('id')
    consult = db.get_consult_by_id(id)
    return render_template('profile.html', consult=consult, programmingLanguages=programmingTags)



#admintools
@app.route("/admin", methods=['POST', 'GET'])
@login_is_required
def admin():
    #check whats running
    linked = 0
    cvreader = 0
    consultants = db.get_all_consultants()
    #cleanConsultants = {}
    connectList = db.get_all_tags()
    programmingTags = build.build_tags()
    #for consult in consultants:
    #    cleanConsultants[consult["id"]]={"name":consult["firstname"]+" "+consult["lastname"],"role":consult["role"],"location":consult["location"],"tags":consult["tags"]}
    if request.method == 'POST' and request.form["action"] ==  'linkedin':
        task.runLinkedinScraper.delay()
        print("debug start linkedin")
        linked = 1
    elif request.method == 'POST' and request.form["action"] == 'cvreader':
        #task.cvReader()
        print("debug start cvreader")
        cvreader = 1

    return render_template('admin.html', linked=linked, cvreader=cvreader, consultantsOptions=consultants, programmingLanguages=connectList)

#admintools
@app.route('/admin/celeryStatus', methods=['POST', 'GET'])
@login_is_required
def celeryStatusPage():
    if request.method=='POST' and request.form["action"] == 'start':
        task.startWorker()
        celery = task.get_celery_worker_status()
        while celery['availability'] is None:
            celery = task.get_celery_worker_status()
        return render_template('celeryStatus.html', celeryStatus=celery)
    elif request.method == 'POST' and request.form["action"] == 'end':
        task.killAllWorkers()
        celery = task.get_celery_worker_status()
        while celery['availability'] != None:
            celery = task.get_celery_worker_status()
        return render_template('celeryStatus.html', celeryStatus=celery)
    else:
        celery = task.get_celery_worker_status()
        return render_template('celeryStatus.html', celeryStatus=celery)

#admintools
@app.route('/admin/consult/delete', methods=['POST'])
@login_is_required
def deleteConsult():
    return "deleting consult with ID:"+str(request.form["id"])

#admintools
@app.route('/admin/consult/add', methods=['POST'])
@login_is_required
def addConsult():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    role = request.form['role']
    description = request.form['description']
    image_url = 'profilePictures/'+request.files['profilePicture'].filename
    picture = request.files['profilePicture']
    pictureUploadStatus = uploadPicture(picture)
    tags = request.form['tags'].split(":")
    cleanTags = [tag for tag in tags if tag.strip()]
    location = request.form["location"]
    consult = {"firstname":firstname, "lastname":lastname, "role":role, "description":description, "location":location, "image_url":image_url, "tags":cleanTags, "pictureStats":pictureUploadStatus}

    addStatus = db.add_consult(consult)
    if(addStatus):
        return "Successfully added consult "+str(consult)
    else:
        return "something went wrong" + str(consult)


#admintools
@app.route('/admin/cv/upload',methods = ['POST'])
@login_is_required
def uploadCV():
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER']), filename)
        return 'file uploaded successfully'


#admintools
@app.route("/admin/tag/remove", methods = ['POST'])
@login_is_required
def removeTag():
    tagname = request.form["tag"]
    removeTagStatus = db.remove_tag(tagname)
    if(removeTagStatus):
        return "Successfully removed tag "+request.form["tag"]
    else:
        return "something went wrong - is tag already removed?"

#admintools
@app.route("/admin/tag/add", methods = ['POST'])
@login_is_required
def addTag():
    tagname = request.form["tag"]
    addTagStatus = db.add_tag(tagname)
    if(addTagStatus):
        return "Successfully added tag "+request.form["tag"]
    else:
        return "Something went wrong - tag might already exist"


#admintools
@app.route("/admin/consult/tag/connect", methods =['POST'])
@login_is_required
def connectConsulttoTag():
    consult_id = request.form["consult-id"]
    tag_id = request.form["tag"]
    connectStatus = db.connect_consult_to_tag(consult_id, tag_id)
    if(connectStatus):
        return request.form
    else:
        return "couldnt connect - maybe connection already exists?"

#admintools
@app.route("/admin/consult/tag/remove", methods=['POST'])
@login_is_required
def removeTagFromConsult():
    consult_id = request.form["consult-id"]
    tag = request.form["tag"]
    tag_id = db.get_tag_id(tag)
    removeTagStatus = db.remove_tag_from_consult(consult_id, tag_id)
    if(removeTagStatus):
        return request.form
    else:
        return "Tag to Consult connection not found"

#admintools
@app.route("/admin/consult/remove", methods=['POST'])
@login_is_required
def removeConsult():
    consult_id = request.form["id"]
    removeConsultStatus = db.remove_consult(consult_id)
    if(removeConsultStatus):
        return "Successfully deleted consult with id:"+request.form["id"]+ "<button onclick='history.back()'>Go Back</button>"
    else:
        return "something went wrong. oops"


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




def uploadPicture(pic):
    filename = secure_filename(pic.filename)
    try:
        fileExists = open(app.config['UPLOAD_FOLDER']+"\\profilePictures\\"+filename, "r")
        return "File Exists"
    except FileNotFoundError:
        pic.save(os.path.join(app.config['UPLOAD_FOLDER']+"\\profilePictures\\"+filename))
        return "Success"
    except Exception as e:
        print("error occured during file upload")
        print(e)
        return "Error "+e


@app.route('/click', methods=['GET'])
def buttonClick():
    print("CLICKED")
    return "clicked"



if __name__ == '__main__':
    app.run(debug=True)

