from flask import Flask, request, render_template, jsonify, session, redirect, url_for
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "boggle123words"

boggle_game = Boggle()

@app.route('/')
def redirect_to_boggle():
    return redirect(url_for('show_board'))

@app.route("/boggle")
def show_board():
    """Show the current board"""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    attempts = session.get("attempts", 0)

    return render_template("board.html", board = board,
                           highscore = highscore,
                           attempts = attempts)


@app.route("/check-word")
def check_word():
    """ Check to see if word attempt is in the text file"""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Retrieve and post the score.  Update attempts"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    attempts = session.get("attempts", 0)

    session['attempts'] = attempts + 1
    session['highscore'] = max(score, highscore)

    return jsonify(newRecord=score > highscore)