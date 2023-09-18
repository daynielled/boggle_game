from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "daniboggle"

debug = DebugToolbarExtension

boggle_game = Boggle()



@app.route('/')
def display_board():
    """Display Game Board"""
    board = boggle_game.make_board()
    session["board"] = board
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    return render_template('board.html', board=board, highscore=highscore, numplays=numplays)

@app.route('/check-word')
def check_word():
    """Check if guess is in dictionary"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route('/post-score', methods=["POST"])
def post_score():
        """Recieve scores and update number of plays"""

        score = request.json["score"]
        highscore = session.get("highscore", 0)
        numplays = session.get("numplays", 0)

        session['numplays'] = numplays+1
        session['highscore'] = max(score, highscore)

        return jsonify(brokeRecord=score > highscore)