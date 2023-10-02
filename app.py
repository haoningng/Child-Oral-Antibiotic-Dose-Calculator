from cs50 import SQL
from flask import Flask, render_template, request


# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///antibiotic.db")

# Define a function that checks if an entry is a float type
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "GET":
        antibiotic = db.execute("SELECT antibiotic FROM antibiotic GROUP BY antibiotic;")
        return render_template("index.html", antibiotic=antibiotic)

@app.route("/input", methods=["GET","POST"])
def input():
    if request.method == "POST":
        antibiotic = request.form.get("antibiotic")
        strength = db.execute("SELECT strength FROM antibiotic WHERE antibiotic = ?;", antibiotic)
        return render_template("input.html", antibiotic=antibiotic, strength=strength)


@app.route("/dose", methods=["GET", "POST"])
def strength():
    if request.method == "POST":
        # Retrieve information given by user
        antibiotic = request.form.get("antibiotic")
        strength = request.form.get("strength")

        # Check if user enter volume correctly
        if not (isfloat(request.form.get("volume"))):
            return "<h1>Volume has to be numbers</h1>"
        volume = float(request.form.get("volume"))
        if (volume<0):
            return "<h1>Volume has to be positive!</h1>"

        # Check if user enter frequency correctly
        if not (isfloat(request.form.get("frequency"))):
            return "<h1>Frequency has to be numbers</h1>"
        frequency = float(request.form.get("frequency"))
        if (frequency<0):
            return "<h1>frequency has to be positive!</h1>"

        # Check if user enter weight correctly
        if not (isfloat(request.form.get("weight"))):
            return "<h1>Weight has to be numbers</h1>"
        weight = float(request.form.get("weight"))
        if (weight<0):
            return "<h1>weight has to be positive!</h1>"

        # Work out the prescribed daily dose = absolute strength(mg/ml) * prescribed volume (ml) * frequency (times/day)
        abstrength = db.execute("SELECT abstrength FROM antibiotic WHERE strength = ? AND antibiotic = ?;", strength, antibiotic)
        if (abstrength==None):
            return "<h1>Data error try again</h1>"
        abstrength = float(abstrength[0]["abstrength"])
        prescribed_dose = round(abstrength * volume * frequency)

        # If the patient is a child (i.e. weight less than around 41kg)
        if (weight <= 41):
            minimum = db.execute("SELECT minimum FROM antibiotic WHERE strength = ? AND antibiotic = ?;", strength, antibiotic)
            minimum = float(minimum[0]["minimum"])
            minimum = round(minimum * weight * frequency)
            maximum = db.execute("SELECT maximum FROM antibiotic WHERE strength = ? AND antibiotic = ?;", strength, antibiotic)
            maximum = float(maximum[0]["maximum"])
            maximum = round(maximum * weight * frequency)

        # If the patient is an adult
        else:
            minimum = db.execute("SELECT absmin FROM antibiotic WHERE strength = ? AND antibiotic = ?;", strength, antibiotic)
            minimum = float(minimum[0]["absmin"])
            minimum = round(minimum)
            maximum = db.execute("SELECT absmax FROM antibiotic WHERE strength = ? AND antibiotic = ?;", strength, antibiotic)
            maximum = float(maximum[0]["absmax"])
            maximum = round(maximum)

        # Check if the prescribed daily dose is within range (i.e. between min and max)
        if (minimum <= prescribed_dose <= maximum):
            result = "Prescribed dose is in range"
        elif (prescribed_dose < minimum):
            result = "Prescribed dose is too low"
        else:
            result = "Prescribed dose is too high"

        return render_template("dose.html", antibiotic=antibiotic, strength=strength, volume=volume, frequency=frequency, weight=weight, prescribed_dose=prescribed_dose, minimum=minimum, maximum=maximum, result=result)