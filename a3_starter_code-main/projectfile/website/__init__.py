from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import datetime

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    
    Bootstrap5(app)
    
    Bcrypt(app)
    
    app.secret_key = 'somerandomvalue'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ConcertsDB.db'
    db.init_app(app)
    
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))    
    
    #add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import concerts
    app.register_blueprint(concerts.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)
    from . import bookings
    app.register_blueprint(bookings.bookbp)
    from . import userbooking
    app.register_blueprint(userbooking.usebookbp)
    from . import events
    app.register_blueprint(events.my_events_bp)
    
    @app.errorhandler(404) 
    # inbuilt function which takes error as parameter 
    def not_found(e): 
      return render_template("404.html", error=e)

    #this creates a dictionary of variables that are available
    #to all html templates
    @app.context_processor
    def get_context():
      year = datetime.datetime.today().year
      return dict(year=year)
    
    
    migrate = Migrate(app, db)

    return app





