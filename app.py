from flask import Flask, render_template, request, redirect
import oracledb

# Enable thick mode for older Oracle DB versions (like 11g)
oracledb.init_oracle_client(lib_dir=r"d:\DBMS\instantclient-basic-windows.x64-23.8.0.25.04\instantclient_23_8")
  # Change to your path

app = Flask(__name__)

# Oracle connection parameters
conn = oracledb.connect(
    user="roshan",
    password="2727",
    dsn="localhost/XE"  # Replace with your actual DSN or use EZConnect string
)

@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', cars=data)

@app.route('/add', methods=['POST'])
def add_car():
    if request.method == 'POST':
        username = request.form['username']
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        regno = request.form['regno']
        cur = conn.cursor()
        cur.execute("INSERT INTO cars (username, make, model, year, regno) VALUES (:1, :2, :3, :4, :5)",
                    (username, make, model, year, regno))
        conn.commit()
        cur.close()
        return redirect('/')

@app.route('/delete/<int:id>')
def delete_car(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM cars WHERE id = :1", (id,))
    conn.commit()
    cur.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_car(id):
    cur = conn.cursor()

    # Handle the GET request to show the current details of the car
    if request.method == 'GET':
        cur.execute("SELECT * FROM cars WHERE id = :1", (id,))
        car = cur.fetchone()
        cur.close()
        return render_template('edit_car.html', car=car)

    # Handle the POST request to update the car details
    elif request.method == 'POST':
        username = request.form['username']
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        regno = request.form['regno']

        cur.execute("""
            UPDATE cars
            SET username = :1, make = :2, model = :3, year = :4, regno = :5
            WHERE id = :6
        """, (username, make, model, year, regno, id))
        conn.commit()
        cur.close()
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
