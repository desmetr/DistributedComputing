from cyber import app
from flask import render_template


@app.route("/profanity/<text>", methods=['GET', 'POST'])
def about(text):
    f = open('Eng_bad_word.txt', "r")
    eng_bad_words = f.read().splitlines()
    m = open('dutch_bad_word.txt', "r")
    dutch_bad_word = m.read().splitlines()

    brokenStr1 = text.split()

    badWordMask = '!@#$%!@#$%^~!@%^~@#$%!@#$%^~!'
    new = ''
    for word in brokenStr1:
        if word in eng_bad_words:
            print(word + ' <--Bad word!')
            # print("delete the post coz it contains english bad words")
            # text = text.replace(word, badWordMask[:len(word)])
            text = "delete the post coz it contains english bad words"
        elif word in dutch_bad_word:
            print(word + ' <--Bad word!')
            # text = text.replace(word, badWordMask[:len(word)])
            text = "delete the post coz it contains dutch bad words"
            # print("delete the post coz it contains dutch bad words")

        else:
            # print("okay fine")
            text = "Ok, Fine"
        # print new

    with app.app_context():
        return render_template('about.html', title="about", text=text)
