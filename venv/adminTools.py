from flask import Blueprint, request, render_template
from login_app import login_is_required
import database as db
import tasks as task
from werkzeug.utils import secure_filename


admin_page = Blueprint('admin page', __name__, template_folder='templates')
celery_status = Blueprint('celery status', __name__, template_folder="templates")

add_consult = Blueprint('add consult',__name__, template_folder="templates")
remove_consult = Blueprint('remove consult', __name__, template_folder="templates")

upload_cv = Blueprint('upload cv',__name__, template_folder="templates")

add_tag = Blueprint('add tag', __name__, template_folder="templates")
remove_tag = Blueprint('remove tag', __name__, template_folder="templates")

add_tag_to_consult = Blueprint('add tag to consult',__name__,template_folder="templates")
remove_tag_from_consult = Blueprint('remove tag form consult', __name__, template_folder="templates")

#admintools
@admin_page.route("/admin", methods=['POST', 'GET'])
@login_is_required
def admin():
    #check whats running
    status = task.get_celery_worker_status()
    consultants = db.get_all_consultants()
    tags = db.get_all_tags()
    print(request.form)
    if request.method == 'POST' and request.form["action"] ==  'linkedin':
        linked = task.runLinkedinScraper.delay()
        print("debug start linkedin")
        print(linked.ready())
        print(linked.result)

    elif request.method == 'POST' and request.form["action"] == 'cvreader':
        #task.cvReader()
        print("debug start cvreader")
    elif request.method == 'POST' and request.form["action"] == 'singlelinkedin':
        url = request.form["url"]
        if('www' not in url):
            return render_template('admin.html', consultantsOptions=consultants, programmingLanguages=tags)
        else:
            print(url)
            task.getLinkedinProfile(url).delay()

    return render_template('admin.html', consultantsOptions=consultants, programmingLanguages=tags)

#admintools
@celery_status.route('/admin/celeryStatus', methods=['POST', 'GET'])
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
@add_consult.route('/admin/consult/add', methods=['POST'])
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
@upload_cv.route('/admin/cv/upload',methods = ['POST'])
@login_is_required
def uploadCV():
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER']), filename)
        return 'file uploaded successfully'


#admintools
@remove_tag.route("/admin/tag/remove", methods = ['POST'])
@login_is_required
def removeTag():
    tagname = request.form["tag"]
    removeTagStatus = db.remove_tag(tagname)
    if(removeTagStatus):
        return "Successfully removed tag "+request.form["tag"]
    else:
        return "something went wrong - is tag already removed?"

#admintools
@add_tag.route("/admin/tag/add", methods = ['POST'])
@login_is_required
def addTag():
    tagname = request.form["tag"]
    addTagStatus = db.add_tag(tagname)
    if(addTagStatus):
        return "Successfully added tag "+request.form["tag"]
    else:
        return "Something went wrong - tag might already exist"


#admintools
@add_tag_to_consult.route("/admin/consult/tag/connect", methods =['POST'])
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
@remove_tag_from_consult.route("/admin/consult/tag/remove", methods=['POST'])
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
@remove_consult.route("/admin/consult/remove", methods=['POST'])
@login_is_required
def removeConsult():
    consult_id = request.form["id"]
    removeConsultStatus = db.remove_consult(consult_id)
    if(removeConsultStatus):
        return "Successfully deleted consult with id:"+request.form["id"]+ "<button onclick='history.back()'>Go Back</button>"
    else:
        return "something went wrong. oops"
