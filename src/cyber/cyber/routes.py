from cyber import app
from flask import render_template, request
import string

@app.route("/profanity", methods=['GET', 'POST'])
def about():
    text = request.args.get('text')

    f = open('cyber/Eng_bad_word.txt', "r")
    eng_bad_words = f.read().splitlines()
    m = open('cyber/dutch_bad_word.txt', "r")
    dutch_bad_word = m.read().splitlines()

    brokenStr1 = text.translate(str.maketrans('', '', string.punctuation)).split()
    print(brokenStr1)
    
    badWordMask = '!@#$%!@#$%^~!@%^~@#$%!@#$%^~!'
    new = ''
    for word in brokenStr1:
        if word in eng_bad_words:
            print(word + ' <--Bad word!')
            # print("delete the post coz it contains english bad words")
            # text = text.replace(word, badWordMask[:len(word)])
            text = "delete the post coz it contains english bad words"
            return "BAD"
        elif word in dutch_bad_word:
            print(word + ' <--Bad word!')
            # text = text.replace(word, badWordMask[:len(word)])
            text = "delete the post coz it contains dutch bad words"
            # print("delete the post coz it contains dutch bad words")
            return "BAD"
    
    print("okay fine")
    text = "Ok, Fine"
    return "GOOD"

    with app.app_context():
        return render_template('about.html', title="about", text=text)