from setting import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue())
    login_pwd = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    login_salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    # the salt is a random code used to encrypt cookie info

class Answers(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    practice_name = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue())
    content = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue())

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    practice_name = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.String(256), nullable=False, server_default=db.FetchedValue())

class Message(db.Model):
    __tablename__ = 'messages'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    app_type = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    message_id = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.Text, nullable=False, server_default=db.FetchedValue())
