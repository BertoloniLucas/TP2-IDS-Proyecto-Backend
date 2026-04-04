from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Esto funca joya"

if __name__ == '__main__':
    app.run(port=5001, debug=True)