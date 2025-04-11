from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key="12345"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "codedpad.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/create', methods=['GET', 'POST'])
def create():
    content=""
    id=session.get('id')
    if request.method == 'POST':
        content = request.form['content']
        conn = get_db_connection()
        cursor=conn.cursor()
        cursor.execute('INSERT INTO users (id, content) VALUES (?, ?)', (id, content))
        conn.commit()
        conn.close()
        return redirect(url_for('enter'))
    return render_template('codedpadcreate.html',id=id)

@app.route('/', methods=['GET', 'POST'])
def enter():
    content=""
    if request.method == 'POST':
        action=request.form['action']
        if action=='submit':
            id = request.form['id'].strip()
            session['id']=id
            print(id)
            conn = get_db_connection()
            cursor=conn.cursor()
            cursor.execute('SELECT content FROM users WHERE id = ?', (id,))
            row=cursor.fetchone()
            conn.close()
            if row:
                content=row['content']
            else:
                return redirect(url_for('create'))
        else:
            id = request.form['id'].strip()
            session['id']=id
            content=request.form['content']
            conn = get_db_connection()
            cursor=conn.cursor()
            cursor.execute('UPDATE users SET content = ? WHERE id = ?', (content,id))
            row=cursor.fetchone()
            conn.commit()
            conn.close()
    return render_template('codedpad.html',content=content,id=session.get('id') if session.get('id')!=None else " ")

import os

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )
app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

