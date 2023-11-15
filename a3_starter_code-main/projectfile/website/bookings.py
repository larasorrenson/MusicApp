from flask import Blueprint, render_template, flash, request ,redirect, url_for
from .models import Booking, Concert
from .forms import BookingForm, UpdateBookingForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

bookbp = Blueprint('bookings', __name__, url_prefix='/bookings')

@bookbp.route('/<id>/', methods=['GET', 'POST'])
@login_required
def book(id):
      concert = db.session.scalar(db.select(Concert).where(Concert.id==id))
      print(current_user)
      print(id)
      bform = BookingForm(event_id=id)
      if bform.validate_on_submit():  
        booking = Booking(TicketQuantity=bform.TicketQuantity.data, UserID = current_user.id, EventID = id) 
      #   booking = Booking(TicketQuantity=bform.TicketQuantity.data, UserID = 2, EventID = 1) 
        db.session.add(booking) 
        db.session.commit() 
        print('Booking complete', 'success') 
        return redirect(url_for('concert.show', id=id))
      return render_template('concerts/book.html', concert = concert, form = bform)


@bookbp.route('/<id>/edit/', methods=['GET', 'POST'])
@login_required
def edit(id):
    concert = db.session.scalar(db.select(Concert).where(Concert.id==id))
    ubform = UpdateBookingForm()
    print('Test1')
    if ubform.validate_on_submit():  
      delbooking = Booking.query.filter(Booking.EventID == id).first()
    

      db.session.delete(delbooking)
      db.session.commit() 
      booking = Booking(TicketQuantity=ubform.TicketQuantity.data, UserID = current_user.id, EventID = id) 
      
      db.session.add(booking) 
      db.session.commit() 
      print('Booking updated', 'success') 
      return redirect(url_for('userbooking.userbookings'))

    return render_template('user/editbookings.html', concert = concert, form = ubform)


@bookbp.route('/<id>/delete/', methods=['GET', 'POST'])
@login_required
def delete(id):

    booking = Booking.query.filter(Booking.EventID == id).first()
    

    db.session.delete(booking)
    db.session.commit()
    print('Booking cancelled')
    return redirect(url_for('userbooking.userbookings', id=id))