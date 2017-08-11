from flask import Flask, redirect, render_template
from flask_script import Manager

# Tell Flask where to look the 'working files'
app = Flask(__name__)
# Provides CLI properties when debugging the webapp
manager = Manager(app)

# This tells flask what to run once a get request is
# sent to the server. In this case, it is the 'main'
# webpage that, if called, will exectue this
# part of the code
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)

# The 'redirect' method allows the webpage to take you
# to another page and return a 302 response: redirect
@app.route("/redirect")
def goto_github():
    return redirect("https://github.com/gerdm")

if __name__ == "__main__":
    #Replaces 'app.run(debug=True)' in order 
    # to give CLI functionalities (see manager)
    manager.run()
