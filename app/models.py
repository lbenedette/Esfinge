from app import db
import datetime


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25), unique=True)
    username = db.Column(db.String(25))
    password = db.Column(db.String(25))
    authenticated = db.Column(db.Boolean, default=False)
    follows = db.relationship('Follow', foreign_keys='Follow.follower_id')

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Follow(db.Model):
    __tablename__ = 'follow'

    id = db.Column(db.Integer, primary_key=True)
    follow_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    follow = db.relationship('User', foreign_keys=[follow_id])
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    follower = db.relationship('User', foreign_keys=[follower_id])


# TODO: search a way to have relationship in two tables
# add question.user.username
class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    posttime = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='question')
    answers = db.relationship('Answer', backref='question', lazy='dynamic')


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='answer')
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

