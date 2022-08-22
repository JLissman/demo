# app.py
import os
import sys
from flask import Flask, request, render_template, session, abort, redirect
import database as db
import mysql.connector
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from functools import wraps
import google.auth.transport.requests


#root paths and settings
sys.path.insert(0, os.path.dirname(__file__))
project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates')
app = Flask(__name__, template_folder=template_path)
app.static_folder = 'static'



#login config
app = Flask("Competence Finder")  #naming our application
app.secret_key = "4179"  #it is necessary to set a password when dealing with OAuth 2.0
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  #this is to set our environment to https because OAuth 2.0 only supports https environments

GOOGLE_CLIENT_ID = "1062577514794-8kmir3s5edma9m80f6lhuv9vfoh22815.apps.googleusercontent.com"  #enter your client id you got from Google console
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")  #set the path to where the .json file you got Google console is

flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    redirect_uri="http://127.0.0.1:5000/callback"  #and the redirect URI is the point where the user will end up after the authorization
)

def login_is_required(function):  #a function to check if the user is authorized or not
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  #authorization required
            return abort(401)
        else:
            return function()
    wrapper.__name__ = function.__name__
    return wrapper



@app.route("/")
def index():
    return "<a href='/login'><button>Login</button></a>"

@app.route("/login")  #the page where the user can login
def login():
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)




@app.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")  #defing the results to show on the page
    session["name"] = id_info.get("name")
    return redirect("/home")  #the final page where the authorized users will end up

@app.route("/logout")  #the logout page and function
def logout():
    session.clear()
    return redirect("/home")


@app.route("/home")
@login_is_required
def home():
    return render_template('index.html')


@app.route("/search")
@login_is_required
def searchresults():
    arguments  = request.args.get('query')
    if(arguments is not None):
        queryList = arguments.split(" ")
        consultantsHTML = ""
        #just nu är det AND istället för OCH
        for query in queryList:
            print("Searching for "+query)
            consultants = db.searchDB(query)
            consultantsHTML = consultantsHTML + buildData(consultants)
        return render_template('search.html', keywords="Searching for "+str(queryList), data=consultantsHTML)


    else:
        consultants = db.getAllFromDb()
        consultantsHTML = buildData(consultants)
        return render_template('search.html',keywords="Do a search for more specific results", data=consultantsHTML)


@app.route("/testdb")
@login_is_required
def dbtest():
    return db.testconnection()




def buildData(data):
    finalHTML = ""
    for consult in data:
        start = '<li class="entity-result"> <div class="searchResult"> <div class="result-img"> <img class="profile-img"src="' + \
                consult[4] + '"> </div> <div class="result-name">' + consult[1] +' '+ consult[2] + '</div> <div class="result-role">' + consult[3] + '</div> <div class="table"> <ul class="result-tags-list">'
        tags = db.getTags(consult[0])
        HTMLtags = ""
        for tag in tags:
            HTMLtags = HTMLtags + '<li class="tag">' + tag[0] + '</li>'

        end = '</ul></div><div class="description">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ligula urna,pharetra id accumsan sit amet, congue sed erat. Integer sed finibus enim. Donec sit amet bibendumsapien. </div> <div class="result-location"><img class="location-tag"src="https://flyclipart.com/thumb2/location-pin-emoji-934877.png">' + \
              consult[5] + '</div></div></li>'
        finalHTML = finalHTML + start + HTMLtags + end;
    return finalHTML








if __name__ == '__main__':
    app.run(debug=True)
