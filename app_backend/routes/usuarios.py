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


@usuarios_bp.route("/<int:usuario_id>", methods=["GET"])
def obtener_usuario(usuario_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT id, nombre, email
        FROM usuarios
        WHERE id = %s
        """
        cursor.execute(query, (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        return jsonify(usuario), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
@usuarios_bp.route("/<int:usuario_id>", methods=["PUT"])
def actualizar_usuario(usuario_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "Body vacío"}), 400
        if "nombre" not in datos and "email" not in datos:
            return jsonify({"error": "Faltan campos obligatorios"}), 400
        nombre = datos.get("nombre")
        email = datos.get("email")
        if not nombre:
            return jsonify({"error": "Nombre inválido"}), 400
        if not email or "@" not in email:
            return jsonify({"error": "Email inválido"}), 400
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Usuario no encontrado"}), 404
        cursor.execute("SELECT id FROM usuarios WHERE email = %s AND id != %s", (email, usuario_id))
        if cursor.fetchone():
            return jsonify({"error": "Ya existe un usuario con ese email"}), 400
        query = """
        UPDATE usuarios
        SET nombre = %s, email = %s
        WHERE id = %s
        """
        cursor.execute(query, (nombre, email, usuario_id))
        conn.commit()
        return jsonify({"message": "Usuario actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()    

@usuarios_bp.route("/<int:usuario_id>", methods=["DELETE"])
def eliminar_usuario(usuario_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        if not cursor.fetchone():   
            return jsonify({"error": "Usuario no encontrado"}), 404
        cursor.execute("DELETE FROM predicciones WHERE usuario_id = %s", (usuario_id,))
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        conn.commit()
        return jsonify({"message": "Usuario eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()    
           
        
        


