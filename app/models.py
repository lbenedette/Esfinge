from app import db


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(50), primary_key=True)
    encrypt_password = db.Column(db.String(15))
    name = db.Column(db.String(20))
    authenticated = db.Column(db.Boolean, default=False)
    questions = db.relationship('Question', backref='user', lazy='dynamic')
    answers = db.relationship('Answer', backref='user', lazy='dynamic')

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    user_id = db.Column(db.String(50), db.ForeignKey('user.email'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text)
    user_id = db.Column(db.String(50), db.ForeignKey('user.email'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
