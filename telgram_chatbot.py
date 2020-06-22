import requests
import json
import wikipedia
import random
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

higreeting = ["नमस्ते ", "नमस्कार", "आपले स्वागत आहे"]
token = ''
base = "https://api.telegram.org/bot{}/".format(token)


def get_updates(offset=None):
    url = base + "getUpdates?timeout=100"
    if offset:
        url = url + "&offset={}".format(offset + 1)
    r = requests.get(url)
    return json.loads(r.content)


def send_message(msg, chat_id):
    url = base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
    if msg is not None:
        requests.get(url)


def tokenit(msg):
    try:
        tokens = nltk.word_tokenize(msg)
        tagged = nltk.pos_tag(tokens)
    except Exception as e:
        tagged = []
    return tagged


def make_reply(msg):
    reply = None
    tokenize = tokenit(msg)
    msg = [lis[0].lower() for lis in tokenize if lis[1] == 'NN' or lis[1] == 'NNP' or
           lis[1] == 'JJ' or lis[1] == 'NNS' or lis[1] == 'VBN']
    if len(msg) is not 0:

        msg = "_".join(msg)
        msg = msg.replace("something_", "")
        if "/start" in msg:
            reply = "Hello"
        elif msg == "hi" or msg == "hello":
            reply = random.choice(higreeting)
        elif msg is not None:
            try:
                print("searching for :", msg)
                reply = wikipedia.summary(msg, sentences=2)
            except Exception as e:
                search = wikipedia.search(str(msg), results=2)
                if search:
                    reply = ",".join(search)
                    reply = "Do you mean : " + reply
                else:
                    reply = "Hey buddy,Try again with a different word"  # wikipedia.summary(msg+ "(greeting)", sentences=2)
    return reply


update_id = None
while True:
    updates = get_updates(offset=update_id)
    updates = updates["result"]

    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
                # message = message.split(" ")[-1]
                print(message, "message received ", type(message))
            except:
                message = None
            from_ = item["message"]["from"]["id"]
            reply = make_reply(message)
            print("Replying....")
            send_message(reply, from_)
            print("repoply send... :", reply)
