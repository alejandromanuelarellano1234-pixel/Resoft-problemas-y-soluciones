from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de ejemplo para guardar clientes en memoria
clientes = [
    {"id": 1, "nombre": "Juan Pérez", "email": "juan@example.com"},
    {"id": 2, "nombre": "María Gómez", "email": "maria@example.com"}
]

# Endpoint para ver todos los clientes
@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    return jsonify(clientes)

# Endpoint para agregar un cliente nuevo
@app.route('/clientes', methods=['POST'])
def agregar_cliente():
    nuevo_cliente = request.get_json()
    clientes.append(nuevo_cliente)
    return jsonify({"mensaje": "Cliente agregado con éxito", "cliente": nuevo_cliente}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
