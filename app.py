from flask import Flask,render_template,request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite3'
app.config['SECRET_KEY'] = "Secret String"

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)
    
    def __repr__(self):
        return '<Todo %r>' %self.text
    
db.create_all()
#db.drop_all()
db.session.commit()

@app.route('/', methods=['GET','POST'])
def index():
    todo_list = Todo.query.all()
    if request.method =='POST':
        if not request.form['text']:
            flash("Enter ToDo list item")
        else:
            item = request.form['text']
            todo = Todo(text=item, complete=False)
            db.session.add(todo)
            db.session.commit()
            return redirect(url_for('index'))
    
    return render_template('index.html', todo_list=todo_list)

@app.route('/delete/<id>')
def erase(id):
    item = Todo.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/update/<id>")
def update(id):
    item = Todo.query.get(id)
    item.complete = not item.complete
    db.session.commit()
    return redirect(url_for("index"))   
    
if __name__ == '__main__':
    
    app.run(debug = True)