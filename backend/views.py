from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from .models import User
from .database import db

views = Blueprint("views", __name__)


# domain root
@views.route('/')
def home():
    return 'Hello, World!'

@views.route('/ios', methods=['POST'])
def add_user():
    if request.method == "POST":
        data = request.get_json()
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict())

        # phone = data["phone"]
        # name = data["name"]
        # nickname = data["nickname"]
        # passwd = data["passwd"]
        # credit_score = data["credit_score"]
        # new_user = User(phone, name, nickname, passwd, credit_score)
        # db.session.add(new_user)
        # db.session.commit()
        # return jsonify(new_user.to_dict())

# @views.route('/add-user', methods=['GET', 'POST'])
# def addUser():
#     if request.method == "POST":
#         phone = request.form.get("phone")
#         name = request.form.get("name")
#         new_user = User(phone, name)
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify(new_user.to_dict())
#     else:
#         return render_template("add_user.html")