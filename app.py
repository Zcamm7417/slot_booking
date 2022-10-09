from unicodedata import name
from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_bootstrap import Bootstrap
import pymysql, yaml, os
import pymysql.cursors
from config import *
# from flask_mail import Mail, Message

app = Flask(__name__)
Bootstrap(app)

# email
# password = yaml.load(open('password.yaml'), Loader=yaml.Loader)
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'samwilson7417@gmail.com'
# app.config['MAIL_PASSWORD'] = password['email_password']
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

#setting connection variables
password = yaml.load(open('password.yaml'), Loader=yaml.Loader)
USERNAME = 'admin' 
PASSWORD = password['my_password']
ENDPOINT = "slot-booking-db.c8a7xdiy73v8.us-east-1.rds.amazonaws.com"
PORT = 3306
REGION = "us-east-1f"
DBNAME = 'slot_schema'
SSL_CA = "rds-combined-ca-bundle.pem"
CURSORCLASS = pymysql.cursors.DictCursor
app.config['SECRET_KEY'] = os.urandom(24)

#definning connection
def start_rds_connection():
    try:
        connection = pymysql.connect(host=ENDPOINT,
                                     port=PORT,
                                     user=USERNAME,
                                     password=PASSWORD,
                                     db=DBNAME,
                                     cursorclass=CURSORCLASS,
                                     ssl_ca=SSL_CA)
        print('[+] RDS Connection Successful')
    except Exception as e:
        print(f'[+] RDS Connection Failed: {e}')
        connection = None

    return connection
#initiating connection
connection = start_rds_connection()

#creating routes
@app.route("/", methods=['POST', 'GET'])
def booking():
    if request.method == 'POST':
        form = request.form
        tableName = 'booking_table'
        firstName = form['firstName']
        lastName = form['lastName']
        email = form['email']
        phone = form['phone']
        datetime = form['datetime']
        session['name'] = firstName + " " + lastName
        session['email'] = email
        
        try:
            # msg = Message('Hello', sender = 'samwilson7417@gmail.com', recipients = [email])
            # # assert msg.sender == "samwilson74117@gmail.com <samwilson74117@gmail.com>"
            # msg.body = "Good day " + firstName + " " + lastName +"!! "+ "Your booking as been received and being process. Thank for your patience. Feel free to cancel booking on occasion arise. BOOKING: "+ datetime 
            # mail.send(msg)
            # flash("Email sent", "success")
            with connection.cursor() as cursor:
                sql = f"INSERT INTO `{tableName}` (`firstName`, `lastName`, `email`, `phone`, `datetime`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (firstName, lastName, email, phone, datetime))
            connection.commit()
            return render_template('success.html')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('booking.php')

#creating routes
@app.route("/success")
def login():
    return render_template('success.html')


if __name__=="__main__":
    app.run(debug=True)