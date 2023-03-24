from flask import (Flask, render_template, abort, jsonify,
                   request, redirect, url_for)
from model import db, save_db

# __name__ is the name of the module passed to this here constructor
app = Flask(__name__)


# this line turns method into "view function", an endpoint the server
@app.route("/")
def welcome():
    return render_template(
        "welcome.html",
        message="paragraph",
        x="em",
        cards=db)


@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template("card.html",
                               card=card,
                               index=index,
                               max_index=len(db) - 1)
    except IndexError:
        abort(404)


@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        new_card = {"question": request.form['question'],
                    "answer": request.form['answer']}
        db.append(new_card)
        save_db()
        return redirect(url_for('card_view', index=len(db) - 1))
    else:
        return render_template("add_card.html")


@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('welcome'))
        else:
            return render_template("remove_card.html", card=db[index])
    except IndexError:
        abort(404)


@app.route("/api/card/")
def api_card_list():
    # return db  <= not allowed to just pass DB for sec reasons
    return jsonify(db)


@app.route("/api/card/<int:index>")
def api_card_details(index):
    try:
        return db[index]
    except IndexError:
        abort(404)
