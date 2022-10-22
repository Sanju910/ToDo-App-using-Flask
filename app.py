from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  complete = db.Column(db.Boolean)

@app.route("/")
def index():
  todo = ToDo.query.all()
  return render_template("index.html",todo_list = todo)

@app.route("/add",methods=["POST"])
def add():
  t = request.form.get("title")
  new_todo = ToDo(title=t,complete=False)
  db.session.add(new_todo)
  db.session.commit()
  return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
  up_todo = ToDo.query.filter_by(id=todo_id).first()
  up_todo.complete = not up_todo.complete
  db.session.commit()
  return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
  up_todo = ToDo.query.filter_by(id=todo_id).first()
  db.session.delete(up_todo)
  db.session.commit()
  return redirect(url_for("index"))

# @app.route("/about")
# def about():
#   return "About"

if __name__=="__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)

