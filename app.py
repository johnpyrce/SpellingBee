from flask import Flask, render_template, request
import spellingbee

app = Flask(__name__)

@app.route("/")
def hello():
    ''' Prompt for target letters. '''
    return render_template("start.html")

@app.route('/', methods=['POST'])
def hello_post():
    letters = request.form['letters'].lower()
    if len(letters) != 7:
        return render_template("start_error.html")
    else:
        return results(letters)

@app.route("/letters/<letters>")
def results(letters = None):
    ''' Target letters passed with URL. '''
    bee = spellingbee.SpellingBee(letters)
    names = bee.names
    words = bee.words
    suffixes = bee.candidate_suffixes
    max_words = bee.all_letter_words
    inflections = bee.inflections
    return render_template("results.html", 
        target_letters=letters, names=names, words=words, suffixes=suffixes, max_words=max_words, inflections=inflections, score=bee.score())
