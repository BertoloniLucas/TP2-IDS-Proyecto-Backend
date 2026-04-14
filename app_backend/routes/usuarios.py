from flask import Blueprint, jsonify, request
from db import get_connection

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/", methods=["GET"])
def lista_usuarios():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        limit = int(request.args.get("_limit", 10))
        offset = int(request.args.get("_offset", 0))

        
        limit = max(1, min(limit, 100))
        offset = max(0, offset)

        
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total = cursor.fetchone()["total"]

        
        query = """
        SELECT id, nombre, email
        FROM usuarios
        LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, offset))
        lista = cursor.fetchall()

        usuarios = []
        for u in lista:
            usuarios.append({
                "id": u["id"],
                "nombre": u["nombre"],
                "email": u["email"]
            })

        base_url = request.base_url

        def build_url(new_offset):
            return f"{base_url}?_limit={limit}&_offset={new_offset}"

        links = {
            "_first": {"href": build_url(0)},
            "_last": {"href": build_url(max(total - limit, 0))}
        }

        if offset > 0:
            links["_prev"] = {"href": build_url(max(offset - limit, 0))}

        if offset + limit < total:
            links["_next"] = {"href": build_url(offset + limit)}

        return jsonify({
            "usuarios": usuarios,
            "_links": links
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@usuarios_bp.route("/", methods=["POST"])
def crear_usuario():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        datos = request.get_json()

       
        if not datos:
            return jsonify({"error": "Body vacío"}), 400

        campos = ["nombre", "email"]
        for campo in campos:
            if campo not in datos:
                return jsonify({"error": f"Falta el campo {campo}"}), 400

        nombre = datos.get("nombre")
        email = datos.get("email")

        
        if not nombre:
            return jsonify({"error": "Nombre inválido"}), 400

        if not email or "@" not in email:
            return jsonify({"error": "Email inválido"}), 400

        
        query_buscar = "SELECT id FROM usuarios WHERE email = %s"
        cursor.execute(query_buscar, (email,))
        if cursor.fetchone():
            return jsonify({"error": "Ya existe un usuario con ese email"}), 400

        
        query = """
        INSERT INTO usuarios (nombre, email)
        VALUES (%s, %s)
        """
        cursor.execute(query, (nombre, email))
        conn.commit()

        usuario_id = cursor.lastrowid

        
        response = jsonify({
            "id": usuario_id,
            "nombre": nombre,
            "email": email
        })
        response.status_code = 201
        response.headers["Location"] = f"/usuarios/{usuario_id}"

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



            #santi 1 -- lastrowid es el id del ultimo registro de la bd
            #santi 1 -- corregi algunas cosas de los ends y d la bd 14/04