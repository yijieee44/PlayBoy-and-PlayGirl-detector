from flask import Flask, render_template, request
import os
from threading import Thread
from src.model.model import preprocess, predict_from_text
from src.chatbot.tinder_function import tinder_api_sms, get_message_every_1_sec

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    percent = 0
    people = [i.replace(".txt", "") for i in os.listdir("src/replies")]
    if percent <= 50:
        angle = percent*360/100
    else:
        angle = (percent-50)*360/100
    return render_template('home.html', percent=percent, angle=angle, people=people, selected="None", messages="-")


@app.route('/', methods=['POST'])
def update():
    name = request.form.get('selected_people')
    pred, messages = predict_from_text(name)
    percent = float("{:.2f}".format(pred * 100))
    people = [i.replace(".txt", "") for i in os.listdir("src/replies")]
    if percent <= 50:
        angle = percent*360/100
    else:
        angle = (percent-50)*360/100
    return render_template('home.html', percent=percent, angle=angle, people=people, selected=name, messages=messages)


def connect_tinder():
    my_id = tinder_api_sms.get_self().get("_id")
    get_message_every_1_sec(my_id)


if __name__ == "__main__":
    t1 = Thread(target=app.run)
    t2 = Thread(target=connect_tinder)
    t1.start()
    t2.start()