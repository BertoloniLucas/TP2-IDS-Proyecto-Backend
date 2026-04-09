from flask import Flask
from flask_cors import CORS
#aca deberiamos importar cosas del blueprint


app = Flask(__name__)
CORS(app)

#aca el register del blueprint


if __name__ == '__main__':
    app.run(port=5000, debug=True)