'''
    This version requires that we do db.create_all() to set up the database
    before we do anything else.  The creation of the account is optional.
    How can we create the db dynamically using Flask-SQLAlchemy?

    The DB cannot already exist when we run this. Delete the existing DB
    manually.

'''

# Import database info
from vote.voteapp import db
from vote.voteapp import Member, Vote

# Create the tables in the database
# (Usually won't do it this way!)
db.create_all()

defaultpw = 'password'

users = ['randall', 'jerry', 'wendy']

for user in users:
    member = Member(user, 'password-clear')
    member.passwordHash = member.genPassword(defaultpw)
    db.session.add(member)
    db.session.commit()

vote = Vote('randall', 'Hamilton', '1')
db.session.add(vote)
db.session.commit()

print ("Setup complete.")
