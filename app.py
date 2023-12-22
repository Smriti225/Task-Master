from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

with app.app_context():
    db.create_all()

@app.route("/", methods=['POST','GET'])
def index():
    if request.method=="POST":
        txt_content=request.form["context"]
        new_task = Todo(content=txt_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "No data is added"
    else:
        task=Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html",tasks=task)
    
@app.route("/delete/<int:id>")
def delete(id):
    data=Todo.query.get_or_404(id)
    try:
        db.session.delete(data)
        db.session.commit()
        return redirect("/")
    except:
        return "Error in deleting data"


@app.route("/update/<int:id>",methods=['POST','GET'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=="POST":
        task.content=request.form['context']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Error occured while updating"
    else:
        return render_template("update.html",task=task)



if __name__=="__main__":
    app.run(debug=True)
