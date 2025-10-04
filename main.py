import sqlite3
from flask import Flask, session, render_template, request, g, redirect, url_for

from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.secret_key = "your_secret_key"
    
    
@app.route('/')
def home():
    db = getattr(g, '_database', None)
    if app.jinja_env.globals.get('departments') is None:
        global departments
        if db is None:
            db = g._database = sqlite3.connect("batteries.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM batteries ORDER by Warnings DESC")
        batteries = cursor.fetchall()
        cursor.close()
    return render_template('index.html', batteries=batteries)

@app.route('/Register')
def register():
    return render_template('Register.html')


@app.errorhandler(HTTPException)
def http_error_handler(error):
    return redirect(url_for('home'))
    
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    
        
if __name__ == '__main__':
    app.run(debug=True)