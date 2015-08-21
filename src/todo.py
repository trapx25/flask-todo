import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
conn = sqlite3.connect('../todo.db', check_same_thread=False)
c = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    tasks = []
    for task in c.execute('select * from tasks').fetchall():
      tasks.append(task)
    return render_template('index.html', tasks=tasks)
  elif request.method == 'POST':
    return add_task()

def add_task():
  if request.form['task']:
    c.execute('insert into tasks (task) values (?)', [request.form['task']])
    conn.commit()
  return redirect(url_for('index'))

@app.route('/edit/')
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id=None):
  if request.method == 'GET':
    if id is not None:
      task = c.execute('select * from tasks where id=?', [id]).fetchone()
      if not task:
        return redirect(url_for('index'))
      else:
        return render_template('edit.html', task=task)
    else:
      return redirect(url_for('index'))
  elif request.method == 'POST':
    return update_task(id)

def update_task(id):
  if request.form['task']:
    c.execute('update tasks set task=? where id=?', [request.form['task'], id])
    conn.commit()
  return redirect(url_for('index'))

@app.route('/delete/')
@app.route('/delete/<int:id>')
def delete_task(id=None):
  if id is not None:
    c.execute('delete from tasks where id=?', [id])
    conn.commit()
  return redirect(url_for('index'))

if __name__=='__main__':
  app.run(debug=True)