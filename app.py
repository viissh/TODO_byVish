from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user

app = Flask(__name__)
app.app_context().push()
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Users.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todoApp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "abc"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# db.init_app(app)python



class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), nullable = False)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

 

@app.route('/register', methods=["GET", "POST"])
def register():
  # If the user made a POST request, create a new user
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        # Once user account created, redirect them
        # to login route (created later on)
        return redirect(url_for("login"))
    # Renders sign_up template if user made a GET request
    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # If a post request was made, find the user by
    # filtering for the username
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the
        # same as the user's password
        if user is None:
            return render_template("login.html")
            
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            return redirect(url_for("home"))
            
        # Redirect the user back to the home
        # (we'll create the home route in a moment)
    return render_template("login.html")



@app.route("/")
def home():
    # Render home.html on "/" route
    return render_template("home.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
    



@app.route('/todos/<string:name>',methods=['GET','POST'])
def create(name):
    
    if request.method == 'POST':
        userName = name
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(username = userName, title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    #allTodo = Todo.query.all()
    allTodo = Todo.query.filter_by(username = name)  #.first()
    print(allTodo)
    return render_template('index.html',allTodo =allTodo)

@app.route('/update/<int:Sno>', methods=['GET','POST'])
def update(Sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno = Sno).first() 
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/todos')

    todo = Todo.query.filter_by(sno = Sno).first()
    return render_template('update.html',todo =todo) 

@app.route('/delete/<int:Sno>')
def delete(Sno):
    todo = Todo.query.filter_by(sno = Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todos')

@app.route('/products')
def products():
#allTodo = Todo.query.all()
#print(allTodo)
    return 'this is a products page'

@app.route('/search', methods=['GET','POST'])
def searchTodoByTitle():
    if request.method == 'POST':
        todosTitle = request.form['todosTitle']
        
        todo = Todo.query.filter_by(title = todosTitle).first()
        return render_template('testingDevelopment.html',todo = todo)
        




if __name__ == "__main__":
    app.run(debug=True)

