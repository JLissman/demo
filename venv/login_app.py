import os
import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from flask import Blueprint, session, redirect, request,abort, render_template
from pip._vendor import cachecontrol
from functools import wraps
import google.auth.transport.requests
import requests
#login config

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  #this is to set our environment to https because OAuth 2.0 only supports https environments

GOOGLE_CLIENT_ID = "1062577514794-8kmir3s5edma9m80f6lhuv9vfoh22815.apps.googleusercontent.com"  #enter your client id you got from Google console
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")  #set the path to where the .json file you got Google console is

flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    redirect_uri="http://127.0.0.1:5000/callback"  #and the redirect URI is the point where the user will end up after the authorization
)

index_page = Blueprint('index page', __name__, template_folder='templates')
login_page = Blueprint('Login', __name__, template_folder="templates")
callback_page = Blueprint('callback',__name__, template_folder="templates")
logout_page = Blueprint('Logout', __name__, template_folder="templates")


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    wrapper.__name__ = function.__name__
    return wrapper

@index_page.route('/')
def index():
    print(session)
    if "google_id" in session:
        login_data = "<div class='login'> Already logged in as: "+session["name"]+" </div>"
    else:
        login_data = '<a id="login-button" ms-hide-element="true" href="/login" class="button logout login w-button"><img class="google-icon" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"/>Login with Google</a>'
#'<form class="login-form" action="/login"><button class="google-login-button"> <div class="google-btn"><div class="google-icon-wrapper"><img class="google-icon" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"/></div><p class="btn-text"><b>Sign in with google</b></p></div></button></form>'

    return render_template("login.html", loginData=login_data)

#@app.route("/login")
@login_page.route("/login")
def login():
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)




#@app.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
@callback_page.route('/callback')
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

#@app.route("/logout")  #the logout page and function
@logout_page.route('/logout')
def logout():
    session.clear()
    return redirect("/")