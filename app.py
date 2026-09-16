from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)

next_queue_number = 1


def get_db_connection():
    connection = sqlite3.connect("database/queueless.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            queue_number INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/shops")
def shops():
    return render_template("shops.html")


@app.route("/join", methods=["GET", "POST"])
def join_queue():

    global next_queue_number

    if request.method == "POST":

        name = request.form["name"]

        queue_number = next_queue_number

        next_queue_number = next_queue_number + 1

        connection = get_db_connection()

        connection.execute(
            "INSERT INTO customers (name, queue_number) VALUES (?, ?)",
            (name, queue_number)
        )

        connection.commit()
        connection.close()

        return f"You're in the queue, {name}! Your queue number is #{queue_number}."

    return render_template("join_queue.html")


@app.route("/queue")
def queue():

    connection = get_db_connection()

    customers = connection.execute(
        "SELECT * FROM customers"
    ).fetchall()

    connection.close()

    return render_template("queue.html", customers=customers)


if __name__ == "__main__":
    create_database()
    app.run(debug=True)