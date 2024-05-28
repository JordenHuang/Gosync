from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from datetime import datetime
from .models import User, Event, Chat_content, Chatroom
from . import db

from sys import stdout

views = Blueprint("views", __name__)

date_format = "%Y-%m-%d %H:%M:%S"

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


#
#   Events
#

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
        new_event_data["time"] = datetime.strptime(time, date_format)
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
            new_event.users.append(cur_user)  ## TODO: check here
            db.session.commit()
            msg["state"] = "success"
        else:
            msg["state"] = "failed"
            msg["reply"] = "max hosts limit"

    else:
        msg["state"] = "failed"
        msg["reply"] = "please login"

    return jsonify(msg)


# Delete event
@views.route('/delete-event', methods=['POST'])
def del_event():
    data = request.get_json()
    phone = data["phone"]
    event_id = data["event_id"]
    user = User.query.filter_by(phone=phone).first()
    event = Event.query.filter_by(event_id=event_id).first()
    msg = dict()
    msg["event"] = "delete event"

    if (user is not None) and (event is not None):
        # Check if user already join that event
        print(type(event.host), event.host, "==", type(phone), phone)
        if str(event.host) == str(phone):
            db.session.delete(event)  ## TODO: check here
            db.session.commit()
            msg["state"] = "success"
        else:
            msg["state"] = "failed"
            msg["reply"] = "user is not host"
    else:
        msg["state"] = "failed"
        msg["reply"] = "no such event or user"

    return jsonify(msg)


# Join event
@views.route('/join-event', methods=['POST'])
def join_event():
    data = request.get_json()
    phone = data["phone"]
    event_id = data["event_id"]
    user = User.query.filter_by(phone=phone).first()
    event = Event.query.filter_by(event_id=event_id).first()
    msg = dict()
    msg["event"] = "join event"

    if (user is not None) and (event is not None):
        # Check if user already join that event
        if db.session.query(Chatroom).filter_by(phone=phone, event_id=event_id).first() is None:
            event.users.append(user)  ## TODO: check here
            db.session.commit()
            msg["state"] = "success"
        else:
            msg["state"] = "failed"
            msg["reply"] = "already join event"
    else:
        msg["state"] = "failed"
        msg["reply"] = "no such event or user"

    return jsonify(msg)


# Leave event
@views.route('/leave-event', methods=['POST'])
def leave_event():
    data = request.get_json()
    phone = data["phone"]
    event_id = data["event_id"]
    user = User.query.filter_by(phone=phone).first()
    event = Event.query.filter_by(event_id=event_id).first()
    msg = dict()
    msg["event"] = "leave event"

    if (user is not None) and (event is not None):
        # Check if user is in that event
        if db.session.query(Chatroom).filter_by(phone=phone, event_id=event_id).first() is not None:
            db.session.query(Chatroom).filter_by(phone=phone, event_id=event_id).delete()
            db.session.commit()
            msg["state"] = "success"
        else:
            msg["state"] = "failed"
            msg["reply"] = "user not in event"
    else:
        msg["state"] = "failed"
        msg["reply"] = "user or event not found"

    return jsonify(msg)



#
#   Chatroom Contents
#

# Add chatroom contents
@views.route('/add-chat-content', methods=['POST'])
def add_chat_contents():
    data = request.get_json()
    phone = data["phone"]
    event_id = data["event_id"]
    user = User.query.filter_by(phone=phone).first()
    event = Event.query.filter_by(event_id=event_id).first()
    msg = dict()
    msg["event"] = "add chat contents"

    if (user is not None) and (event is not None):
        time = data["time"]
        data["time"] = datetime.strptime(time, date_format)
        new_chat_data = Chat_content(**data)

        db.session.add(new_chat_data)
        db.session.commit()
        msg["state"] = "success"
    else:
        msg["state"] = "failed"
        msg["reply"] = "no such event or user"

    return jsonify(msg)


# Get chatroom contents
@views.route('/get-chat-content', methods=['POST'])
def get_chat_contents():
    data = request.get_json()
    phone = data["phone"]
    event_id = data["event_id"]
    user = User.query.filter_by(phone=phone).first()
    event = Event.query.filter_by(event_id=event_id).first()
    msg = dict()
    msg["event"] = "get chat contents"

    if (user is not None) and (event is not None):
        chat = Chat_content.query.filter_by(event_id=event_id).all()
        # print(type(chat[0].time), file=stdout)

        # Sort chat content by time
        chat = sorted(chat, key=lambda r: r.time)

        msg["state"] = "success"
        reply = dict()
        reply["length"] = len(chat)
        reply["cur_user"] = phone
        for i in range(len(chat)):
            reply[str(i)] = chat[i].to_dict()
            # print(reply, file=stdout)
        msg["state"] = "success"
        msg["reply"] = reply
        return jsonify(msg)
    else:
        msg["state"] = "failed"
        msg["reply"] = "no such event or user"

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