from datetime import datetime
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Task : ' + str(self.id)


class Task1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return 'Task1 : ' + str(self.id)


@app.route('/',methods=['GET',"POST"])
def home():
    if request.method=='POST':
        tasks = request.form['task']
        newPost = Task(task=tasks)
        db.session.add(newPost)
        db.session.commit()
        return redirect('/')
    else:
        tasks = Task.query.all()
        return render_template('index.html',tasks = tasks)


@app.route('/delete/<int:id>')
def delete(id):
    post = Task.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post = Task.query.get_or_404(id)
    if request.method=='POST':
        post.task = request.form['task']
        db.session.commit()
        return redirect('/')
    else:
        
        return render_template('edit.html',tasks = post)
        


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html")
if __name__ == "__main__":
    app.run(debug=True)

