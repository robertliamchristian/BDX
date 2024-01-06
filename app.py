from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from datetime import datetime
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask import flash


load_dotenv()
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'





#############################################






class UserSighting(db.Model):
    __tablename__ = 'user_sighting'
    sightingid = db.Column(db.Integer, primary_key=True)
    birdref = db.Column(db.Integer, db.ForeignKey('log.birdid'))
    userid = db.Column(db.Integer, db.ForeignKey('alluser.id'))
    sighting_time = db.Column(db.DateTime, nullable=True)
    listid = db.Column(db.Integer, db.ForeignKey('user_list.listid'))

class UserList(db.Model):
    __tablename__ = 'user_list'
    listid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('alluser.id'))
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
   
class User(UserMixin, db.Model):
    __tablename__ = 'alluser'  # Set the new table name here
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    insert_date = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(255))
    is_admin = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class Log(db.Model): 
    __tablename__ = 'log'
    birdid = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), nullable=False)
    bird = db.Column(db.String(255), nullable=False)
    family = db.Column(db.String(255), nullable=False)
    latin = db.Column(db.String(255), nullable=True)
    flags = db.Column(db.String(255), nullable=True)
    #sighting_time = db.Column(db.DateTime, nullable=True)
    bird_type = db.Column(db.String(255), nullable=True)
    typeref = db.Column(db.Integer, db.ForeignKey('bird_types.typeid'))
    #user_id = db.Column(db.Integer, db.ForeignKey('alluser.id'))  

class BirdType(db.Model):
    __tablename__ = 'bird_types'
    typeid = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)

class RegionJunction(db.Model):
    __tablename__ = 'region_junction'
    region_association_id = db.Column(db.Integer, primary_key=True)
    bird_ref = db.Column(db.Integer, db.ForeignKey('log.birdid'))
    region_ref = db.Column(db.Integer, db.ForeignKey('region.regionid'))

class RegionDim(db.Model):
    __tablename__ = 'region_dim'
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), nullable=False)


    def __repr__(self):
        return f'<log {self.birdid}>'
    





#############################################





# Login Logic
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))








# Main Routes

# Suggestions Route
@app.route('/suggest_birds')
def suggest_birds():
    query = request.args.get('query')
    if not query:
        return jsonify([])  

    matching_birds = Log.query.filter(Log.bird.ilike(f'%{query}%')).all()
    bird_names = [bird.bird for bird in matching_birds]
    return jsonify(bird_names)


# View User Lists Route
@app.route('/userlist', methods=['GET', 'POST'])
@login_required
def userlist():
    if request.method == 'POST':
        
        list_name = request.form.get('list_name')
        if list_name:

            new_list = UserList(userid=current_user.id, title=list_name)
            db.session.add(new_list)
            db.session.commit()

            return redirect(url_for('view_list', listid=new_list.listid))

        
        listid = request.form.get('listid')
        bird_name = request.form.get('bird')
        if listid and bird_name:
           
            new_bird = Log.query.filter_by(bird=bird_name).first()
            if new_bird:
                new_sighting = UserSighting(
                    birdref=new_bird.birdid,
                    userid=current_user.id,
                    sighting_time=datetime.now(),
                    listid=listid
                )
                db.session.add(new_sighting)
                db.session.commit()

    
    lists = UserList.query.filter_by(userid=current_user.id).all()
    csrf_token = session.get('_csrf_token')
    return render_template('index.html', lists=lists, csrf_token=csrf_token)



# User List Edit/Add Route
@app.route('/list/<int:listid>', methods=['GET', 'POST'])
@login_required
def view_list(listid):
    list = UserList.query.get_or_404(listid)
    message = None  

    if list.userid != current_user.id:
        return redirect(url_for('index'))

    sightings_with_names = []
    if request.method == 'POST':
        bird_name = request.form.get('bird')
        if bird_name:
            new_bird = Log.query.filter_by(bird=bird_name).first()
            if new_bird:
                existing_sighting = UserSighting.query.filter_by(
                    birdref=new_bird.birdid, listid=listid
                ).order_by(UserSighting.sighting_time.desc()).first()
                
                if existing_sighting:
                    existing_sighting.sighting_time = datetime.now()
                    message = f"{bird_name} sighting updated."
                else:
                    new_sighting = UserSighting(
                        birdref=new_bird.birdid, 
                        userid=current_user.id, 
                        sighting_time=datetime.now(), 
                        listid=listid
                    )
                    db.session.add(new_sighting)
                    message = f"New sighting of {bird_name} added!"
                db.session.commit()
                flash(message)

    distinct_sightings = db.session.query(
        UserSighting.birdref,
        Log.bird,
        db.func.max(UserSighting.sighting_time).label('latest_sighting_time')
    ).join(
        Log, UserSighting.birdref == Log.birdid
    ).filter(
        UserSighting.listid == listid,
        UserSighting.userid == current_user.id
    ).group_by(
        UserSighting.birdref,
        Log.bird
    ).all()


    for birdref, bird_name, latest_sighting_time in distinct_sightings:
        sighting_id = UserSighting.query.filter(
            UserSighting.birdref == birdref,
            UserSighting.sighting_time == latest_sighting_time
        ).first().sightingid

        sightings_with_names.append((sighting_id, birdref, bird_name, latest_sighting_time))

    if request.method == 'POST':
        return redirect(url_for('view_list', listid=listid))

    bird_count = UserSighting.query.filter_by(listid=listid).distinct(UserSighting.birdref).count()


    return render_template('view_list.html', list=list, sightings=sightings_with_names, bird_count=bird_count)




# Delete Items
@app.route('/delete_sighting/<int:sightingid>', methods=['POST'])
@login_required
def delete_sighting(sightingid):
    sighting = UserSighting.query.get_or_404(sightingid)
    if sighting.userid != current_user.id:
        # Prevent users from deleting sightings that do not belong to them
        return redirect(url_for('index'))
    
    db.session.delete(sighting)
    db.session.commit()
    # Redirect to the previous page or the user list
    return redirect(request.referrer or url_for('userlist'))

@app.route('/delete_list/<int:listid>', methods=['POST'])
@login_required
def delete_list(listid):
    list_to_delete = UserList.query.get_or_404(listid)
    if list_to_delete.userid != current_user.id:
        # Prevent users from deleting lists that do not belong to them
        return redirect(url_for('index'))

    # Delete all associated sightings if not using cascading deletes
    UserSighting.query.filter_by(listid=listid).delete()

    # Now delete the list itself
    db.session.delete(list_to_delete)
    db.session.commit()

    return redirect(url_for('userlist'))





#############################################




'''
@app.route('/', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    distinct_sighted_bird_count = UserSighting.query.with_entities(UserSighting.birdref).filter_by(userid=current_user.id).distinct().count()
    total_distinct_bird_count = Log.query.distinct(Log.birdid).count()


    return render_template('home.html',
                            sighted_count=distinct_sighted_bird_count, 
                            total_bird_count=total_distinct_bird_count,)
'''




# Main Route for Birdedex
@app.route('/', methods=['GET', 'POST'])
def index():
    show_sighted_only = request.args.get('show_sighted_only', 'false') == 'true'
    filter_state = request.args.get('filter_state', None)  # None means no state filter is applied
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # Initialize variables
    message = ""
    anchor_id = ""

    # Handle form submission
    if request.method == 'POST':
        # Get bird name from form
        new_bird_name = request.form['bird']
        # Query for bird in the Log table
        new_bird = Log.query.filter_by(bird=new_bird_name).first()

        # If bird exists in the Log table
        if new_bird:
            # Check if a sighting of this bird by the current user already exists
            existing_sighting = UserSighting.query.filter_by(birdref=new_bird.birdid, userid=current_user.id).first()
            if existing_sighting:
                # If sighting exists, update the sighting time
                existing_sighting.sighting_time = datetime.now()
                message = f"{new_bird_name} sighting updated."
            else:
                # If sighting does not exist, create a new sighting
                new_sighting = UserSighting(birdref=new_bird.birdid, userid=current_user.id, sighting_time=datetime.now())
                db.session.add(new_sighting)
                message = f"New sighting of {new_bird_name} added."

            # Commit changes to the database
            db.session.commit()
            anchor_id = f"bird-{new_bird.birdid}"  

    # Get all birds
    # Fetch all bird types
    all_bird_types = BirdType.query.all()
    bird_type_dict = {bird_type.typeid: bird_type.type for bird_type in all_bird_types}

   # Fetch all user sightings
    user_sightings = UserSighting.query.filter_by(userid=current_user.id).all()
    user_sightings_dict = {sighting.birdref: sighting for sighting in user_sightings}
    sighted_birds = {sighting.birdref for sighting in user_sightings}

    # If a state filter is applied, modify the query
    if filter_state:
        all_birds = (
            Log.query
            .join(RegionJunction, Log.birdid == RegionJunction.bird_ref)
            .join(RegionDim, RegionJunction.region_ref == RegionDim.id)
            .filter(RegionDim.region == filter_state)
            .order_by(Log.birdid)
            .all()
        )
    else:
        all_birds = Log.query.order_by(Log.birdid).all()

    # Fetch and group all birds by type, filtered based on the show_sighted_only flag
    #all_birds = Log.query.order_by(Log.birdid).all()
    birds_by_type = {}

    for bird in all_birds:
        if not show_sighted_only or bird.birdid in sighted_birds:
            bird_type_name = bird_type_dict.get(bird.typeref, "Unknown Type")
            if bird_type_name not in birds_by_type:
                birds_by_type[bird_type_name] = []

            sighting = user_sightings_dict.get(bird.birdid)
            bird_info = {
                "bird": bird.bird,
                "sighted": bird.birdid in sighted_birds,
                "sighting_time": sighting.sighting_time if sighting else None
            }
            birds_by_type[bird_type_name].append(bird_info)

    birds_by_type_list = [(bird_type, birds) for bird_type, birds in birds_by_type.items()]

    # Count distinct sighted birds and total distinct birds
    distinct_sighted_bird_count = len(sighted_birds)
    total_distinct_bird_count = len(all_birds)

    # Get all lists by the current user
    lists = UserList.query.filter_by(userid=current_user.id).all()

    states = [rd.region for rd in RegionDim.query.with_entities(RegionDim.region).distinct().order_by(RegionDim.region)]
    # Render the template
    return render_template('index.html',
                           birds_by_type_list=birds_by_type_list,
                           message=message,
                           sighted_count=distinct_sighted_bird_count, 
                           total_bird_count=total_distinct_bird_count,
                           anchor_id=anchor_id,
                           lists=lists,
                           states=states)




#############################################






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)


