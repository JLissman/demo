import os
import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from flask import Blueprint, session, redirect, request,abort
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
    return "<a href='/login'><button>Login</button></a>"

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