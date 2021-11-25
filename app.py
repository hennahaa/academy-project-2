#!/usr/bin/python
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from datetime import datetime
import psycopg2
import os


def get_db_connection():
    return psycopg2.connect(host=os.getenv('POSTGRES_HOST'), database=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'))

#


def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = %s',
                        (post_id,))
    post = cursor.fetchone()
    cursor.close()                    
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'do_not_touch_or_you_will_be_fired'


# this function is used to format date to a finnish time format from database format
# e.g. 2021-07-20 10:36:36 is formateed to 20.07.2021 klo 10:36
def format_date(post_date):
    return post_date.strftime('%d.%m.%Y') + ' klo ' + post_date.strftime('%H:%M')


# this index() gets executed on the front page where all the posts are
@app.route('/')
def index():
    conn = None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    # we need to iterate over all posts and format their date accordingly

    dictrows = []

    for row in posts:
        a_row = {"id": row[0], "created":row[1], "title":row[2], "content":row[3] }
        dictrows.append(a_row)

    for post in dictrows:
        # using our custom format_date(...)
        post['created'] = format_date(post['created'])
    return render_template('index.html', posts=dictrows)


# here we get a single post and return it to the browser
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    dictpost = {"id": post[0], "created":post[1], "title":post[2], "content":post[3] }
    dictpost['created'] = format_date(dictpost['created']) #KORJAUS päivämäärän formatointi
    return render_template('post.html', post=dictpost)


# here we create a new post
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO posts (title, content) VALUES (%s, %s)',
                         (title, content))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    dictpost = {"id": post[0], "created":post[1], "title":post[2], "content":post[3] }
    dictpost['created'] = format_date(dictpost['created']) #KORJAUS päivämäärän formatointi<

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE posts SET title = %s, content = %s WHERE id = %s',
                         (title, content, id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=dictpost)


# Here we delete a SINGLE post. KORJAUS, lisätty WHERE id = ?
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    post_title = {'title':post[2]}
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id  = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post_title['title']))
    return redirect(url_for('index'))
