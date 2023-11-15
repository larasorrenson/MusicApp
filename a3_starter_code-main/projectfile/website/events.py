from flask import Blueprint, render_template, flash, request, redirect, url_for
from .models import Concert, Comment
from .forms import ConcertForm, UpdateConcertForm
from . import db
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

my_events_bp = Blueprint('events', __name__, url_prefix='/events')

@my_events_bp.route('/')
@login_required
def events():
    # Query events created by the current user
    user_events = Concert.query.filter_by(userCreator=current_user).all()
    return render_template('user/events.html', user_events=user_events)

@my_events_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = ConcertForm()

    if form.validate_on_submit():
        DateResult=form.EventDate.data.strftime("%d/%m/%Y")
        TimeResult=form.EventTime.data.strftime("%H:%M")

        print(DateResult)
        print(TimeResult)
        event = Concert(
            EventName=form.EventName.data,
            EventDesc=form.EventDesc.data,
            EventImage=None, 
            EventDate=DateResult,
            EventLocation=form.EventLocation.data,
            EventInfo=form.EventInfo.data,
            EventPrice=form.EventPrice.data,
            EventStatus='open',
            EventTicketCount=form.EventTicketCount.data,
            UserId=current_user.id,
            EventTime=TimeResult
        )

        if form.EventImage.data:
            event.EventImage = check_upload_file(form) 

        db.session.add(event)
        db.session.commit()
        flash('Event created successfully', 'success')
        return redirect(url_for('events.events'))

    return render_template('concerts/create.html', form=form)

@my_events_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Concert.query.get(id)

    form = UpdateConcertForm(obj=event)
    
    if form.validate_on_submit():
        DateResult=form.EventDate.data
        TimeResult=form.EventTime.data
        
        event.EventName = form.EventName.data
        event.EventDesc = form.EventDesc.data
        event.EventDate = DateResult
        event.EventTime = TimeResult
        event.EventLocation = form.EventLocation.data
        event.EventInfo = form.EventInfo.data
        event.EventPrice = form.EventPrice.data
        event.EventTicketCount = form.EventTicketCount.data

        if form.EventImage.data:
            event.EventImage = check_upload_file(form)

        db.session.commit()
        flash('Event updated successfully', 'success')
        return redirect(url_for('events.events'))

    return render_template('user/eventsedit.html', form=form, event=event)

@my_events_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_event(id):
    event = Concert.query.get(id)

    if event is None or event.userCreator != current_user:
        flash('Event not found or unauthorized', 'danger')
        return redirect(url_for('events.events'))

    event.EventStatus = "Cancelled"
    db.session.commit()
    flash('Event deleted successfully', 'success')
    return redirect(url_for('events.events'))



def check_upload_file(form):
  #get file data from form  
  fp = form.EventImage.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path