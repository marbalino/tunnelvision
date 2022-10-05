from flask import Flask, render_template, url_for, request,redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test7.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Integer, nullable=False)
    value1 = db.Column(db.String, nullable=False)
    value2 = db.Column(db.String(20), nullable=False)
    value3 = db.Column(db.Integer, nullable=False)
    value4 = db.Column(db.Integer, nullable=False)
    value5 = db.Column(db.String(20), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    state= db.Column(db.Integer, default =1)
    
    def __repr__(self):
        return '<Task %r>' %self.id


@app.route('/', methods=['POST','GET'])

def index():
    if request.method == 'POST':
        task_content =request.form['content']
        task_value1 =request.form['value1']
        task_value2 =request.form['value2']
        task_value3 =request.form['value3']
        task_value4 =request.form['value4']
        task_value5 =request.form['value5']
        
    
        
        new_task = Todo(content=task_content,value1=task_value1,value2=task_value2,value3=task_value3,value4=task_value4, value5=task_value5)
                
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There was an issue adding the tast'
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
        
    
    except:
        return 'There was a problem deleting that tast'
    

if __name__=="__main__":
    from waitress import serve
    serve(app, host="0.0.0.0",port=5000)
    app.run(debug = True)