from flask import Flask, render_template, redirect, request, session, url_for, flash, get_flashed_messages, jsonify
from db import return_query, commit_query
import os
from predict import predict
from diseasecontroller import get_disease_info
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/login')
def login():
    msg = get_flashed_messages()
    return render_template('login.html', msg=msg)


@app.route('/signup')
def register():
    return render_template('signup.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/user')
def user():
    if 'loggedin' in session:
        pwd = len(session['password'])
        return render_template('user.html', name=session['name'], email=session['email'], password=session['password'], pwd=pwd)
    else:
        return redirect(url_for('login'))


@app.route('/predictions')
def predictions():
    return render_template('predictions.html')


@app.route('/disease/<name>')
def disease_info(name):
    disease_info, status_code = get_disease_info(name)
    # app.logger.info(disease_info)
    # app.logger.info(status_code)
    return jsonify(disease_info), status_code


@app.route('/predict', methods=['POST'])
def handle_prediction():
    # Get the uploaded image and model name from the request
    image_file = request.files['image']
    model_name = request.form['model']

    # Call the predict function from predict.py
    prediction = predict(image_file, model_name)

    # Return the prediction as a JSON object
    return jsonify(prediction)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('name', None)
    session.pop('password', None)
    return redirect('/login')


@app.route('/login_validate', methods=['POST'])
def login_validate():
    email = request.form.get('l-email')
    password = request.form.get('l-password')
    sql = """SELECT * FROM `users` WHERE `email` LIKE '%{}%' AND `password` LIKE '%{}%'""".format(
        email, password)
    record = return_query(sql)
    if record:
        session['loggedin'] = True
        session['name'] = record[1]
        session['email'] = record[2]
        session['password'] = record[3]
        return redirect('/user')
    else:
        msg = 'Incorrect email/password, try again!'
        flash(msg)
        return redirect(url_for('login'))


@app.route('/signup_validate', methods=['POST'])
def signup_validate():
    name = request.form.get('s-name')
    email = request.form.get('s-email')
    password = request.form.get('s-password')
    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    values = (name, email, password)
    commit_query(sql, values)
    return redirect('/login')


@app.route('/update_profile', methods=['POST'])
def update_profile():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    # update the user data in the database
    sql = """UPDATE `users` SET `name`=%s, `email`=%s, `password`=%s WHERE `email`=%s"""
    values = (name, email, password, session['email'])
    commit_query(sql, values)
    return 'Profile updated successfully!'


if __name__ == '__main__':
    app.run(debug=True)
