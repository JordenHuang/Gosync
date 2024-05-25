from flask import Blueprint, request, jsonify
# from flask import redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
# from flask import session
from . import db
from .models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    phone = data["phone"]
    user = User.query.filter_by(phone=phone).first()
    msg = dict()
    msg["event"] = "login"

    if user is not None:
        if data["passwd"] == user.passwd:
            msg["state"] = "success"
            return jsonify(msg)
        else:
            msg["state"] = "failed"
            msg["reply"] = "incorrect password"
            return jsonify(msg)
        # login_user(user)
        # return redirect()

    else:
        msg["state"] = "failed"
        msg["reply"] = "account not exist"
        return jsonify(msg)


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    phone = data["phone"]
    user = User.query.filter_by(phone=phone).first()
    msg = dict()
    msg["event"] = "signup"

    # check if the account not yet been registed
    if user is None:
        try:
            new_user = User(**data)
            new_user.credit_score = 100
        except TypeError:
            msg["state"] = "failed"
            msg["reply"] = "missing value"
            return jsonify(msg)

        # add new user to database
        db.session.add(new_user)
        db.session.commit()
        msg["state"] = "success"
        return jsonify(msg)
    else:
        msg["state"] = "failed"
        msg["reply"] = "account already exist"
        return jsonify(msg)