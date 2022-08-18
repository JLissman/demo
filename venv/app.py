# app.py
import os
import sys
from flask import Flask, request, render_template
import flask


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



if __name__ == '__main__':
    app.run(debug=True)
