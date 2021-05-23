from flask import Flask, render_template
from src import chatbot

dict__ = {'60aa02ecb9ea4101007575f7': '', '60a3c99c3286bd01007eb94d': 'How you doing?', '60a3b30a06eb39010021aaa9': 'How’s ur day?'}
chatbot_1 = chatbot.Chatbot()
print(chatbot_1.get_responses(dict__))

# app = Flask(__name__)
#
# @app.route('/')
# def home():
#     percent = 37.5
#     if percent<=50:
#         angle = percent*360/100
#     else:
#         angle = (percent-50)*360/100
#     return render_template('home.html', percent=percent, angle=angle)
#
# if __name__ == "__main__":
#     app.run()