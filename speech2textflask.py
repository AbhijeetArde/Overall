from flask import Flask, render_template, request
import speech_recognition as sr

r = sr.Recognizer()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index5.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'GET':
        with sr.Microphone() as source:
            print("Speak Anything :")
            audio = r.listen(source)
            print(audio)
            try:
                text = r.recognize_google(audio)
                print(text)
                print("You said : {}".format(text))
            except Exception as e:
                print("Sorry could not recognize what you said")
        return render_template("index5.html", result=text)


if __name__ == '__main__':
    app.run(debug=True)
