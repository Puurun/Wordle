from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from wordle import Wordle
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'whatisthekey??'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///words.sqlite"
db = SQLAlchemy(app)

class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(5), nullable=False)
    result = db.Column(db.String(10), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    db.session.query(Words).delete()
    db.session.commit()

wordle = Wordle()
wordle.ResetWordleGame()

@app.context_processor
def _AssignColor():
    def AssignColor(ch):
        if ch == '?':
            return 'box-red'
        elif ch == '@':
            return 'box-yellow'
        else:
            return 'box-green'
    return dict(AssignColor=AssignColor)

@app.route('/')
def ShowGameBoard(method=["GET"]):
    if 'status' not in session:
        session['status'] = ''
    words = Words.query.order_by(Words.date_time).all()
    return render_template('wordle_game.html', status=session['status'], words=words)

@app.route('/guess', methods=["POST", "GET"])
def GuessWord():
    session['status'] = ''
    if request.method == "POST":
        user_input = request.form["user_input"].strip()
        if wordle.isFiveLetterInput(user_input):
            result, success = wordle.TryGuess(user_input)
            new_word = Words(word=user_input, result=result)
            db.session.add(new_word)
            db.session.commit()

            if success:
                return redirect('/reset')

        else:
            session['status'] = "word isn't 5 letters or isn't a valid word!"
    return redirect('/')
    
@app.route('/reset')
def ResetGame():
    target_word = wordle.target_word
    wordle.ResetWordleGame()
    with app.app_context():
        db.session.query(Words).delete()
        db.session.commit()
    return render_template('finished.html', target_word=target_word)

if __name__ == '__main__':
    app.run(debug=True)


