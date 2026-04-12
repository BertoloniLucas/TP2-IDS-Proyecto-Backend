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

        consulta_usuarios = """
        SELECT padron, nombre, apellido
        FROM usuarios
        WHERE 1=1
        """

        consulta_cantidad = f"SELECT COUNT(*) as total from ({consulta_usuarios}) as sub"
        cursor.execute(consulta_cantidad)
        total = cursor.fetchone()["total"]

        consulta_usuarios += " LIMIT %s OFFSET %s"
        cursor.execute(consulta_usuarios, (limit, offset))
        lista_usuarios = cursor.fetchall()

        usuarios = []
        for usuario in lista_usuarios:
            usuarios.append({
                "padron": usuario["padron"],
                "nombre": usuario["nombre"],
                "apellido": usuario["apellido"]
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
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


@usuarios_bp.route("/", methods=["POST"])
def crear_usuario():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        datos = request.get_json()
        campos = ["padron", "nombre", "apellido"]

        if not datos:
            return jsonify({"error": "campos incompletos"}), 400
        for campo in campos:
            if campo not in datos:
                return jsonify({"error": f"{campo} no especificado"}), 400

        padron = datos.get("padron")
        nombre = datos.get("nombre")
        apellido = datos.get("apellido")

        query_buscar = "SELECT * FROM usuarios WHERE padron = %s"
        cursor.execute(query_buscar, (padron))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            return jsonify({"error": "Ya existe un usuario con ese padron"}), 400

        query = """
        INSERT INTO usuarios (padron, nombre, apellido)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (padron, nombre, apellido))
        conn.commit()

        return jsonify({"mensaje": "Usuario agregado correctamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()