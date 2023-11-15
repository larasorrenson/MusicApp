from flask import Blueprint, render_template,request, redirect, url_for
from sqlalchemy import text
from .models import Concert, User, Booking
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import re

usebookbp = Blueprint('userbooking', __name__)

@usebookbp.route('/userbookings', methods=['GET', 'POST'])

@login_required
def userbookings():
    id= current_user.id
    userquery = db.select(Booking.EventID).where(Booking.UserID==id)
    userresult = db.session.execute(userquery).scalars()
    userbookings = userresult.all()
    
    concerts = db.session.scalars(db.select(Concert).where(Concert.id.in_(userbookings)))
    
    eventIDs = db.session.scalars(db.select(Concert.id).where(Concert.id.in_(userbookings))).all()
    

    results = []
    i = 0
    while i < len(eventIDs):
        # tickets = db.session.scalars(db.select(Booking).where(Booking.UserID == id) and (Booking.EventID == eventIDs[i]))
        query = db.session.query(Booking).filter(Booking.UserID == id).filter(Booking.EventID == eventIDs[i])
        tickets = db.session.execute(query)
        results.append(tickets.first())
        i += 1
    print(results)

    j = 0
    while j < len(results):
        input = results[j]
        print(results[j])
        stringInput = '%s' %input
        integerInput = int(re.search(r'\d+', stringInput).group())
        results[j] = integerInput
        j += 1

    
    
    return render_template('user/bookings.html',concerts = concerts, tickets = results)



