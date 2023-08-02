from flask import Flask, render_template, redirect, request, session, url_for, flash, get_flashed_messages, jsonify
from db import return_query, commit_query
import os
from dotenv import load_dotenv
from predict import predict
from diseasecontroller import get_disease_info
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = os.urandom(24)

load_dotenv()


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


@app.route('/sendmsg', methods=['POST'])
def sendmsg():
    name = request.form.get('mname')
    phone = request.form.get('mphone')
    email = request.form.get('memail')
    subject = request.form.get('msubject')
    message = request.form.get('mmessage')
    sender_email = os.environ.get('EMAIL_ADDRESS')
    sender_password = os.environ.get('EMAIL_PASSWORD')
    receiver_email = os.environ.get('SENDER_EMAIL')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = sender_email
    msg['Subject'] = subject
    body = f"Name: {name}\nPhone: {phone}\nEmail: {email}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    return redirect('/')


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


@app.route('/fungal')
def fungal():
    return render_template('fungal.html')


@app.route('/bacterial')
def bacterial():
    return render_template('bacterial.html')


@app.route('/viral')
def viral():
    return render_template('viral.html')


@app.route('/background')
def background():
    return render_template('background.html')


if __name__ == '__main__':
    app.run(debug=True)
