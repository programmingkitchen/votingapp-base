import sys, os
from flask import Flask, render_template, request, render_template, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

# Create a login manager object
login_manager = LoginManager()
app = Flask(__name__)

# Often people will also separate these into a separate config.py file
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'votes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(memberId):
    return Member.query.get(memberId)


'''
============================================================
                    FORMS
============================================================
'''
#TODO:  Explore error propagation.  Where does the ValidationError go?
# https://wtforms.readthedocs.io/en/stable/validators.html
# https://wtforms.readthedocs.io/en/stable/fields.html#basic-fields


class LoginForm(FlaskForm):
    name = StringField('Login: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login')

class VoteForm(FlaskForm):
    show = SelectField(u'Show',
    choices=[('Ain\'t Too Proud', 'Ain\'t Too Proud'),
    ('Chicago', 'Chicago'),
    ('Girl from the North Country', 'Girl From the North Country'),
    ('Hamilton', 'Hamilton'),
    ('In the Heights', 'In the Heights'),
    ('Jesus Christ Superstar', 'Jesus Christ Superstar'),
    ('The Book of Mormon', 'The Book of Mormon')], default='Hamilton')
    submit = SubmitField('Vote')



'''
============================================================
                    MODELS
============================================================
'''
#TODO:  We are trying to set the table name as members, but it's being created
# as member, which is the same as the name of the class
class Member(db.Model, UserMixin):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True, index=True)
    passwordHash = db.Column(db.String(128))

    def __init__(self, name, password):
        self.name = name
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.passwordHash, password)

    def genPassword(self, password):
        return generate_password_hash(password)

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key = True)
    userName = db.Column(db.String(64))
    showName = db.Column(db.String(64))
    memberId = db.Column(db.Integer, db.ForeignKey("members.id"))

    def __init__(self, userName, showName, memberId):
        self.userName = userName
        self.showName = showName
        self.memberId = memberId

'''
============================================================
                        HOME
============================================================
'''

@app.route('/')
def index():
    return redirect(url_for('login'))

'''
============================================================
            USER LOGIN/REGISTRATION
============================================================
'''
@app.route('/logout')
@login_required
def logout():
    logout_user()
    #flash('Logged out!')
    return redirect(url_for('login'))

#TODO: for some reason this form is never valid.  We can trick it by
# using request.method.  It is true on submit for the login form, but
# not here.  This is because we are not passing the CSRF
# https://stackoverflow.com/questions/10722968/flask-wtf-validate-on-submit-is-never-executed
# TODO:  Strip surrounding spaces
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("LOGIN: Valid Form on Login Submit: ", form.validate_on_submit(), file=sys.stderr)
        # Grab the user from our User Models table
        name = form.name.data
        name = name.lower()
        member = Member.query.filter_by(name=name).first()
        print(type(member), file=sys.stderr)
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not
        if member is not None:
            isValid = member.checkPassword(form.password.data)
            print("Password Match: ", isValid, file=sys.stderr)

            #If password matches, log in the user
            if (isValid):
                login_user(member)
                flash('Logged in successfully.')
                # If a user was trying to visit a page that requires a login
                # flask saves that URL as 'next'.  Check if that next exists,
                # otherwise we'll go to the welcome page.
                next = request.args.get('next')
                if next == None or not next[0]=='/':
                    next = url_for('vote')
                return redirect(next)
            else: # bad password
                flash('Your password is incorrect.')
                return render_template('login.html', form=form)
        else: # Member not in the db
            flash('Login name not found, please register.')
            return render_template('login.html', form=form)

    print("LOGIN:  Valid Form on login GET: ", form.validate_on_submit(), file=sys.stderr)
    return render_template('login.html', form=form)


'''
============================================================
                        VOTE
============================================================
'''
'''
    Vote for a musical
    Tried to grab the result list up front.  This does not work because
    this results in neededing two threads.   We put the query inside the flow
    for POST and GET (2 times) to get around this.

    The fetchall() converts from the SQLAlchemy Resultset Proxy (we previously iterated
    using the proxy) to a normal list (or list of tuples).  Now we do normal Python/Jinja
    iteration in the template.
'''
@app.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    form = VoteForm()
    data = []
    label = []
    rating = 0
    sql = '''select showName, count(*) as total
    from votes
    group by showName
    order by total desc'''

    if form.validate_on_submit():
        userName = current_user.name
        showName = form.show.data
        memberId = current_user.id
        print("VOTE: ", showName, file=sys.stderr)
        print("USER: ", current_user.name, file=sys.stderr)
        print("ID: ", current_user.id, file=sys.stderr)
        try:
            toAdd = Vote(userName, showName, memberId)
            db.session.add(toAdd)
            db.session.commit()
            flash('Thanks for Voting!')
            resultList = db.engine.execute(sql)
            rows = resultList.fetchall()
            for i in rows:
                label.append(str(i[0]))
                data.append(i[1])
            return render_template('combo.html', form = form, results = rows, rating = rating, label = label, data = data)
        except:
            flash('Voting Error.')
            return render_template('combo.html', form = form, results = rows, rating = rating, label = label, data = data)

    # Convert the Result Set Proxy into a normal Python list.  convert
    # the list of tuples to two separate lists since the labels property and
    # data expect corresponding lists.
    resultList = db.engine.execute(sql)
    rows = resultList.fetchall()
    for i in rows:
        label.append(str(i[0]))
        data.append(i[1])
    return render_template('combo.html', form = form, results = rows, rating = rating, label = label, data = data)


    # Convert the Result Set Proxy into a normal Python list.  convert
    # the list of tuples to two separate lists since the labels property and
    # data expect corresponding lists.
    resultList = db.engine.execute(sql)
    rows = resultList.fetchall()
    for i in rows:
        label.append(str(i[0]))
        data.append(i[1])
    return render_template('combo.html', form = form, results = rows, rating = rating, label = label, data = data)

'''
============================================================
                        UTILITIES AND STATS
============================================================
'''
@app.route('/stats')
def stats():
    data = []
    label = []
    sql = '''select members.name, members.id, count(*) AS "total"
    from members join votes on members.name = votes.userName
    group by members.name
    ORDER BY total desc'''
    resultList = db.engine.execute(sql)
    rows = resultList.fetchall()
    for i in rows:
        label.append(str(i[0]))
        data.append(i[1])
    return render_template('stats.html', results = rows, label = label, data = data)

@app.route('/stats/<int:memberId>')
def countVotes(memberId):
    data = []
    label = []
    sql = '''select showName, count(*) as "total"
    from votes
    where memberId = ?
    group by showName
    order by total desc, showName
    '''
    resultList = db.engine.execute(sql, (memberId,))
    rows = resultList.fetchall()
    for i in rows:
        label.append(str(i[0]))
        data.append(i[1])
    print("resultList: ", type(resultList), file=sys.stderr)
    member = load_user(memberId)
    return render_template('showlist.html', member = member, results = rows, label = label, data = data)





@app.route('/member')
@login_required
def listMembers():
    memberList = db.session.query(Member)
    return render_template('memberlist.html', memberList = memberList)

@app.route('/results')
@login_required
def results():
    # memberList = db.session.query(Member)
    sql = '''select showName, count(*) as total
    from votes
    group by showName
    order by total desc'''
    resultList = db.engine.execute(sql)
    return render_template('results.html', resultList = resultList)

'''
============================================================
                        HELPER METHODS
============================================================
'''

if __name__ == '__main__':
    app.debug = True
    #app.run()
    app.run(host='0.0.0.0')
