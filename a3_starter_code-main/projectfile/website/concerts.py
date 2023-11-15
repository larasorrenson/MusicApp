from flask import Blueprint, render_template, flash, request ,redirect, url_for
from .models import Concert, Comment
from .forms import ConcertForm,CommentForm
from .status import showEventStatus
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
destbp = Blueprint('concert', __name__, url_prefix='/concerts')

@destbp.route('/<id>')
def show(id):
    concert = db.session.scalar(db.select(Concert).where(Concert.id==id))
    eventStatus = showEventStatus(id)
    print(eventStatus)
    cform = CommentForm()   
    return render_template('concerts/show.html', concert = concert, status = eventStatus, form = cform)


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

@destbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    concert = db.session.scalar(db.select(Concert).where(Concert.id==id))
    if form.validate_on_submit():  
      comment = Comment(CommentContent=form.CommentContent.data, concert=concert,user=current_user) 
      db.session.add(comment) 
      db.session.commit() 
      print('Your comment has been added', 'success') 
    return redirect(url_for('concert.show', id=id))