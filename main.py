from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Esto funca joya"

if __name__ == '__main__':
    app.run(port=5001, debug=True)

# Hay que hacer 15 endpoints totales
# Ver tema de paginación y filtro
# Agregar el Swagger
# README indicando el funcionamiento de cada endpoint + ejecución, etc 
