# How to run: From Powershell (the env needs to be there) run: python app.py. Then copy the adress shown in the terminal to the browser.

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # Bare en reference til denne fil
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Viser hvor vores database er. Hvis det bruges //// (4 slahes), så er det en absolut path
db = SQLAlchemy(app)  # db initialised, med indstillingerne fra vores app.

class Todo(db.Model):  # Vi laver en class, vi kalder todo. Database relateret.
    id = db.Column(db.Integer, primary_key=True)  # Her laver vi en kolonne der hedder id. Det er Primary key i databasen.
    content = db.Column(db.Integer, nullable=False)  # Her laver vi en string kolonne. Max 200 ckarakterer. Den må ikke være tom.
    date_created = db.Column(db.DateTime, default=datetime.now())  # En kolonne hvor der bliver lavet et timestamp år der bliver alvet et todo. Dette ser brugeren ikke.
    # Nu skal man gå tilbage i Powershell (se at der står env), og skrive: from app import db
    # Dernæst skal man skrive db.create_all()
    # Dernæst exit()
    # Nu er databasen lavet, og der er blevet lavet en test.db

    def __repr__(self):  # Lav en funktion der laver en string, hver gang der bliver lavet et nyt element. F.eks. Som "Task: " + id.
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])  # Her skriver vi at vi både skal Get (hente) og post(skrive i vores database.)
def index():  # Funktion for hvad der skal ske når siden bliver åbnet. Hvis man skriver: return "Hello World", bliver det skrevet.
    if request.method == 'POST':
        task_content = request.form['content']  # 'content' er det ovre i html'en i input feltet.
        new_task = Todo(content=task_content)  # Der laves altså et nyt task, fra inputtet.

        try:
            db.session.add(new_task)  # Det prøves at lægge det nye task i vores database
            db.session.commit()  # Der comittes
            return redirect('/')  # Der redirectes tilbage til vores index.html.
        except:
            return 'Din indtastning kunne ikke oprettes. Oupsi.'  # Hvis det ikke var muligt, så skriv denne fejlmeddelelse.

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  # Querying database, ordering by date created.
        return render_template('index.html', tasks=tasks)  # Returnerer det til vores template.


@app.route('/delete/<int:id>')  # Vores primary key er ID, så denne vælges i denne linje til at identificerer den task vi vil delete.
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete) 
        db.session.commit()
        return redirect('/')
    except:
        return 'Din indtastning kunne ikke slettes. Oupsi.'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Din indtastning kunne ikke opdateres. Oupsi.'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":  # Dette sætter siden igang, og det øverste funktion bliver kaldt. Før denne linje har det kun været funktioner.
    app.run(debug=True)  # Dette er slutningen, og der sættes debug = true hvis man vil se fejl der sker på siden.
