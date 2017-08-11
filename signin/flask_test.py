from flask import Flask
from flask import redirect

# Tell Flask where to look the 'working files'
app = Flask(__name__)

# This tells flask what to run once a get request is
# sent to the server. In this case, it is the 'main'
# webpage that, if called, will exectue this
# part of the code
@app.route("/")
def index():
    return "<h1>Hello, world!</h1>"

@app.route("/user/<name>")
def user(name):
    return "<h1> Hello, {name}</h1>".format(name=name)

# The 'redirect' method allows the webpage to take you
# to another page and return a 302 response: redirect
@app.route("/redirect")
def goto_github():
    return redirect("https://github.com/gerdm")

if __name__ == "__main__":
    app.run(debug=True)
