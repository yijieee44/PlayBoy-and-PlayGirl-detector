from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    percent = 37.5
    if percent<=50:
        angle = percent*360/100
    else:
        angle = (percent-50)*360/100
    return render_template('home.html', percent=percent, angle=angle)

if __name__ == "__main__":
    app.run()