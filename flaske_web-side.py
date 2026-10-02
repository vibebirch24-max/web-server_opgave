from flask import Flask , request , render_template
import sqlite3
from pathlib import Path
from flask import current_app   

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_FANFIC = "./db/fanfic.db"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db(db, query, params=()):
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(query, params)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

@app.route("/")
@app.route("/forside")
def hello_world():
    data = get_db(DB_FANFIC, "select * from stories")
    return render_template ("index.html", title="Black_Angel", items=data)

@app.route("/side1")
def fanfic1():
    return render_template ("index2.html", tilde= "fanfic1")

@app.route("/search", methods=["GET", "POST"])
def search_page():
    if request.method == "POST":
        search_term = request.form.get("search_term", "")
        app.logger.info("jer er her", search_term)
        return db_search(search_term)
    return render_template("search.html", title="Search Page", members=[])

@app.route("/fanfic")
def get_fanfic():
    return render_template(request.args["file"])

def db_search(search_term):
    # Perform a search in the database with the LIKE operator
    data = get_db(
        DB_FANFIC,
        "SELECT title, filename FROM stories WHERE title LIKE ?",
        ('%' + search_term + '%',),
    )
    #rows = {"members": [dict(u) for u in data]}
    app.logger.info("jer er her", data)

    return render_template("search.html", overskrift="Search Results", fanfics=data)

@app.route ("/get_unknowen_rider")
def get_unknowen_rider():
    return render_template ("unknown-rider.html", title="unknown-rider", members=[])

@app.route ("/get_unknowen_rider_2")
def get_unknowen_rider_2():
    return render_template ("unknown-rider-2.html", title="unknown-rider-2", members=[])


if __name__=="__main__":
    app.run(host="0.0.0.0", port= 8080, debug=True)
