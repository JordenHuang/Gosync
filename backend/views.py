from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from datetime import datetime
from .models import User, Event
from . import db

from sys import stdout

views = Blueprint("views", __name__)

date_format = "%Y-%m-%d"

# Greeting
@views.route('/greeting')
def greeting():
    return jsonify('Hello, World!')


# Main page
@views.route('/main', methods=['POST'])
def main_page():
    data = request.get_json()
    phone = data["phone"]
    user = User.query.filter_by(phone=phone).first()
    msg = dict()
    msg["event"] = "main page"

    if user is not None:
        events = Event.query.all()
        reply = dict()
        reply["length"] = len(events)
        for i in range(len(events)):
            reply[str(i)] = events[i].to_dict()
        # print(reply, file=stdout)
        msg["state"] = "success"
        msg["reply"] = reply
        return jsonify(msg)
    else:
        msg["state"] = "failed"
        msg["reply"] = "please login"
        return jsonify(msg)


# Add events
@views.route('/add-event', methods=['POST'])
def add_event():
    data = request.get_json()
    phone = data["phone"]
    user = User.query.filter_by(phone=phone).first()
    msg = dict()
    msg["event"] = "add event"

    if user is not None:
        new_event_data = data["event"]
        new_event_data["host"] = phone
        time = new_event_data["time"]
        new_event_data["time"] = datetime.strptime(time, date_format).date()
        new_event = Event(**new_event_data)

        # check if a user hosts more than 3 events
        user_host_events = Event.query.filter_by(host=new_event_data["host"]).all()
        if len(user_host_events) < 3:
            flag = 0
        else:
            flag = 1

        # check if event already exist
        # Not yet finish
        '''
        same_name_event = Event.query.filter_by(name=new_event_data["name"])
        flag = 1
        if same_name_event is not None:
            same_name_event = same_name_event.to_dict()
            for k in new_event_data:
                # if not (k in same_name_event and new_event_data[k] == same_name_event[k]):
                if k in same_name_event:
                    if new_event_data[k] != same_name_event[k]:
                        print(new_event_data[k], file=stdout)
                        flag = 0
                        break
                else:
                    print("not", new_event_data[k], file=stdout)
        '''

        if flag == 0:
            db.session.add(new_event)
            cur_user = User.query.filter_by(phone=phone).first()
            new_event.users.append(cur_user)  ## check here
            db.session.commit()
            msg["state"] = "success"
        else:
            msg["state"] = "failed"
            msg["reply"] = "max hosts limit"

        return jsonify(msg)
    else:
        msg["state"] = "failed"
        msg["reply"] = "please login"
        return jsonify(msg)


'''
# @views.route('/ios', methods=['POST'])
# def add_user():
#     if request.method == "POST":
#         data = request.get_json()
#         new_user = User(**data)
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify(new_user.to_dict())

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
'''