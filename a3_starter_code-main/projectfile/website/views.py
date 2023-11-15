from flask import Blueprint, render_template,request, redirect, url_for
from .models import Concert
from . import db


mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    concerts = db.session.scalars(db.select(Concert)).all()    
    return render_template('index.html',concerts = concerts)

@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        concerts = db.session.scalars(db.select(Concert).where(Concert.EventDesc.like(query)))
        return render_template('index.html', concerts= concerts)
    else:
        return redirect(url_for('main.index'))


