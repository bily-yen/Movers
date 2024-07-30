from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import os


"MYSQL_PASSWORD:", os.environ.get('MYSQL_PASSWORD')
"MAIL_PASSWORD:", os.environ.get('MAIL_PASSWORD')

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'toners'

mysql = MySQL(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Update with your SMTP server
app.config['MAIL_PORT'] = 465  # Update with your SMTP port
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'bilyokwaro95@gmail.com'  # Update with your email
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'bilyokwaro95@gmail.com'  # Update with your email
mail = Mail(app)

@app.route("/")
def Index():
    return render_template('home.html')

@app.route("/aboutus")
def aboutus():
    return render_template ('aboutus.html')


@app.route("/services")
def housemoving():
    return render_template ('housemoving.html')

@app.route("/blog")
def blog():
    return render_template ('blog.html')



@app.route('/customers')
def customers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customerdetails ORDER BY CustomerID ASC")
    data = cur.fetchall()
    cur.close()
    return render_template('customers.html', customerdetails=data)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/newcustomer', methods=['POST'])
def newcustomer():
    if request.method == "POST":
        Name = request.form['Name']
        Email = request.form['Email']
        Phone = request.form['Phone']
        Address = request.form['Address']
        Age_group = request.form['Age_group']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customerdetails (Name, Email, Phone, Address, Age_group) VALUES (%s, %s,%s, %s, %s)", (Name, Email, Phone, Address, Age_group))
        mysql.connection.commit()

        # Fetch all remaining rows, renumber the rows, and update the IDs...
        cur.execute("SELECT CustomerID FROM customerdetails")
        remaining_rows = cur.fetchall()
        for index, row in enumerate(remaining_rows, start=1):
            new_id = index
            if new_id != row[0]:
                cur.execute("UPDATE customerdetails SET CustomerID=%s WHERE CustomerID=%s", (new_id, row[0]))
                mysql.connection.commit()
        
        cur.close()
        flash("Data Inserted Successfully")
        
        return redirect(url_for('customers'))
    
@app.route('/submit_form', methods=['POST'])
def submit_form():
        if request.method == "POST":
            full_name = request.form.get('name')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            moving_from = request.form.get('moving_from')
            moving_to = request.form.get('moving_to')
            type_of_house = request.form.get('type_of_house')
            state_floor_number = request.form.get('state_floor_number')
            bedroom_numbers = request.form.get('bedroom_numbers')
            tv_mounting = request.form.get('tv_mounting')
            wifi_installation = request.form.get('wifi_installation')
            cleaning = request.form.get('cleaning')
            moving_date = request.form.get('moving_date')
            message = request.form.get('message')
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO homemoverrequest (full_name, email, phone_number, moving_from, moving_to, type_of_house, state_floor_number, bedroom_numbers, tv_mounting, wifi_installation, cleaning, moving_date, message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (full_name, email, phone_number, moving_from, moving_to, type_of_house, state_floor_number, bedroom_numbers, tv_mounting, wifi_installation, cleaning, moving_date, message))
            mysql.connection.commit()

            cur.execute("SELECT id FROM homemoverrequest")
            remaining_rows = cur.fetchall()

            for index, row in enumerate(remaining_rows, start=1):
                new_id = index
                if new_id != row[0]:
                    cur.execute("UPDATE homemoverequest SET id=%s WHERE id=%s", (new_id, row[0]))
                    mysql.connection.commit()
        
            cur.close()
            flash("Your request was sent Successfully.You can also use our contacts for more enquiries")

             
             
            msg = Message('New Contact Form Submission', recipients=['bilyokwaro95@gmail.com'])
            msg.body = (
              f"Name: {full_name}\n"
              f"Email: {email}\n"
              f"Phone Number: {phone_number}\n"
              f"moving_from: {moving_from}\n"
              f"moving_to: {moving_to}\n"
              f"type of house: {type_of_house}\n"
              f"floor number: {state_floor_number}\n"
              f"number of bedrooms: {bedroom_numbers}\n"
              f"tv installations: {tv_mounting}\n"
              f"wifi installation: {wifi_installation}\n"
              f"cleaning: {cleaning}\n"
              f"moving date: {moving_date}\n"
              f"message: {message}"
              )
            mail.send(msg)
            
   
        
        
            return redirect(url_for('home', _anchor='form-section'))

    
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name']
        purchase_price = request.form['purchase_price']
        selling_price = request.form['selling_price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO toners (name, purchase_price, selling_price) VALUES (%s, %s, %s)", (name, purchase_price, selling_price))
        mysql.connection.commit()

        # Fetch all remaining rows, renumber the rows, and update the IDs...
        cur.execute("SELECT id FROM toners")
        remaining_rows = cur.fetchall()
        for index, row in enumerate(remaining_rows, start=1):
            new_id = index
            if new_id != row[0]:
                cur.execute("UPDATE toners SET id=%s WHERE id=%s", (new_id, row[0]))
                mysql.connection.commit()
        
        cur.close()
        flash("Data Inserted Successfully")
        
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    flash("Data deleted Successfully")
    cur = mysql.connection.cursor()

    # Delete the row
    cur.execute("DELETE FROM toners WHERE id=%s", (id,))
    mysql.connection.commit()

    # Fetch all remaining rows
    cur.execute("SELECT id FROM toners")
    remaining_rows = cur.fetchall()

    # Renumber the rows
    for index, row in enumerate(remaining_rows, start=1):
        new_id = index
        # Update the ID only if it's different from the new ID
        if new_id != row[0]:
            cur.execute("UPDATE toners SET id=%s WHERE id=%s", (new_id, row[0]))
            mysql.connection.commit()

    return redirect(url_for('Index'))

@app.route('/remove/<string:CustomerID>', methods=['GET'])
def remove(CustomerID):
    flash("Data deleted Successfully")
    cur = mysql.connection.cursor()

    # Delete the row
    cur.execute("DELETE FROM customerdetails WHERE CustomerID=%s", (CustomerID,))
    mysql.connection.commit()

    # Fetch all remaining rows
    cur.execute("SELECT CustomerID FROM customerdetails")
    remaining_rows = cur.fetchall()

    # Renumber the rows
    for index, row in enumerate(remaining_rows, start=1):
        new_id = index
        # Update the ID only if it's different from the new ID
        if new_id != row[0]:
            cur.execute("UPDATE customerdetails SET CustomerID=%s WHERE CustomerID=%s", (new_id, row[0]))
            mysql.connection.commit()

    return redirect(url_for('customers'))

@app.route('/updatecustomer', methods=['POST'])
def updatecustomer():
    if request.method == "POST":
        CustomerID = request.form['CustomerID']
        Name = request.form['Name']
        Email = request.form['Email']
        Phone = request.form['Phone']
        Address = request.form['Address']
        Age_group = request.form['Age_group']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE customerdetails SET Name=%s,Email=%s,Phone=%s,Address=%s,Age_group=%s
        WHERE CustomerID=%s
        """, (Name, Email, Phone, Address, Age_group, CustomerID))
        flash("Updated")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('customers'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        id = request.form['id']
        name = request.form['name']
        purchase_price = request.form['purchase_price']
        selling_price = request.form['selling_price']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE toners SET name=%s, purchase_price=%s, selling_price=%s
        WHERE id=%s
        """, (name, purchase_price, selling_price, id))
        flash("Updated")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Index'))
    

if __name__ == "__main__":
    app.run(debug=True)