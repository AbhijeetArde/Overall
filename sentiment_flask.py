from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)


@app.route('/')
def func1():
    result = ""
    return render_template('index.html', result=result)


@app.route('/result', methods=['POST', 'GET'])
def func2():
    if request.method == 'POST':
        result = request.form['Name']
        blob = TextBlob(result)
        for sentence in blob.sentences:
            result = sentence.sentiment.polarity
            ok = sentence.sentiment.polarity
            print(result)
            if 0 < result < 1:
                result = "Positive"
            elif result == 0:
                result = "Neutral"
            else:
                result = "Negative"
        return render_template('index.html', result=result+ "   "+str(ok))
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
