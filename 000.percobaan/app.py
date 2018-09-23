from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    booking = 5
    return render_template('index.html', booking=booking)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)