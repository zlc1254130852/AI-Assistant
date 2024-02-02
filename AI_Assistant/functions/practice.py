from flask import Blueprint, render_template, request

from utils.login_check import check_login
from tables import Answers, Record
from setting import db

practice_bp = Blueprint('practice', __name__)

@practice_bp.route('/reading/<id>',methods=['GET'])
def reading(id):
    """ render html file """
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("reading/reading"+id+".html", current_user=user_info.login_name)
    else:
        return render_template("reading/reading"+id+".html")

@practice_bp.route('/listening/<id>',methods=['GET'])
def listening(id):
    """ render html file """
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("listening/listening"+id+".html", current_user=user_info.login_name)
    else:
        return render_template("listening/listening"+id+".html")

@practice_bp.route('/submit/<practice_name>',methods=['GET'])
def submit(practice_name):
    """ submit answers """
    answer = Answers.query.filter_by(practice_name=practice_name).first()
    return eval(answer.content)

@practice_bp.route('/save',methods=['POST'])
def save():
    """ save progress """
    req = request.values
    current_user = req['current_user']
    practice_name = req['practice_name']
    answers_to_save = req['answers_to_save']

    print(eval(answers_to_save))

    record_info = Record.query.filter_by(user_name=current_user, practice_name=practice_name).first()
    if record_info:
        print(record_info)
        db.session.delete(record_info)
        db.session.commit()

    model_record = Record()
    model_record.user_name = current_user
    model_record.practice_name = practice_name
    model_record.content = answers_to_save
    db.session.add(model_record)
    db.session.commit()

    return {"code":200}

@practice_bp.route('/load',methods=['POST'])
def load():
    """ load saved answers """
    req = request.values
    current_user = req['current_user']
    practice_name = req['practice_name']

    record_info = Record.query.filter_by(user_name=current_user, practice_name=practice_name).first()
    print(record_info)
    if record_info:
        return {"record_info": eval(record_info.content), "code":200}
    else:
        return {"record_info": "", "code":-1}