from flask_login import UserMixin
from . import db
from datetime import datetime

class User(db.Model,UserMixin):
    __tablename__ = 'User' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100), index=True, unique=True, nullable=False)
    UserEmail = db.Column(db.String(100), index=True, nullable=False)
    
	# password should never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long, depending on your hashing algorithm
    UserPass_hash = db.Column(db.String(255), nullable=False)
    Phone_Num = db.Column(db.NUMERIC(20), nullable=False)
    # relation to call user.comments and comment.created_by
    Comments = db.relationship('Comment', backref='user')
    
    # string print method
    def __repr__(self):
        return f"Name: {self.UserName}"

class Concert(db.Model):
    __tablename__ = 'Event'
    id = db.Column(db.Integer, primary_key=True)
    EventName = db.Column(db.String(80))
    EventDesc = db.Column(db.String(200))
    EventImage = db.Column(db.String(400))
    EventDate = db.Column(db.String(100))
    EventLocation = db.Column(db.String(100))
    EventInfo = db.Column(db.String(200))
    EventPrice = db.Column(db.DECIMAL(9, 2))
    EventStatus = db.Column(db.String(20))
    EventTicketCount = db.Column(db.Integer)
    UserId = db.Column(db.Integer, db.ForeignKey('User.id'))
    userCreator = db.relationship('User', backref='events_created')
    EventTime = db.Column(db.String(100))
    # ... Create the Comments db.relationship
    # relation to call destination.comments and comment.destination
    Comments = db.relationship('Comment', backref='concert')

    # string print method
    def __repr__(self):
        return f"Name: {self.EventName}"

class Comment(db.Model):
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, primary_key=True)
    CommentContent = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    UserID = db.Column(db.Integer, db.ForeignKey('User.id'))
    EventID = db.Column(db.Integer, db.ForeignKey('Event.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.CommentContent}"
    
class Booking(db.Model):
    __tablename__ = 'Bookings'
    id = db.Column(db.Integer, primary_key=True)
    TicketQuantity = db.Column(db.Integer)
# add the foreign key
    UserID = db.Column(db.Integer, db.ForeignKey('User.id'))
    EventID = db.Column(db.Integer, db.ForeignKey('Event.id'))
    # Integer print method
    def __repr__(self):
        return f"Ticket quantity: {self.TicketQuantity}"
    
