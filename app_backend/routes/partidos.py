from flask import Blueprint, jsonify, request
from db import get_connection

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route ("/", methods=["GET"])
def lista_partidos():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        fecha = request.args.get ("fecha")
        fase = request.args.get ("fase")
        equipo = request.args.get ("equipo")
        limit = int (request.args.get("_limit", 10))
        offset = int (request.args.get("_offset", 0))

        consulta_partidos= """
        SELECT ID, equipo_local, equipo_visitante, fecha, fase
        FROM partidos
        WHERE 1=1
        """

        valores = []

        if equipo:
            consulta_partidos += " AND (equipo_local = %s OR equipo_visitante = %s)"
            valores.extend ([equipo, equipo])

        if fecha:
            consulta_partidos += " AND fecha = %s"
            valores.append (fecha)

        if fase:
            consulta_partidos += " AND fase = %s"
            valores.append (fase)

        consulta_cantidad_partidos = f"SELECT COUNT(*) as total from ({consulta_partidos}) as sub" 
        cursor.execute(consulta_cantidad_partidos, valores) 
        total = cursor.fetchone()["total"]

        consulta_partidos += " LIMIT %s OFFSET %s"
        valores.extend ([limit, offset])  

        cursor.execute (consulta_partidos, valores)
        lista_partidos = cursor.fetchall()

        partidos = []
        for partido in lista_partidos:
            cursor.execute("SELECT equipo FROM equipos WHERE ID = %s", (partido["equipo_local"],))
            equipo_local = cursor.fetchone()["equipo"]
            cursor.execute("SELECT equipo FROM equipos WHERE ID = %s", (partido["equipo_visitante"],))
            equipo_visitante = cursor.fetchone()["equipo"]

            partidos.append ({
                "ID" : partido["ID"],
                "equipo_local" : equipo_local,
                "equipo_visitante" : equipo_visitante,
                "fecha" : str(partido["fecha"]),
                "fase" : partido ["fase"]
            })

        base_url = request.base_url

        def build_url (new_offset):
            params = f"_limit={limit}&_offset={new_offset}"

            if equipo:
                params += f"&equipo={equipo}"

            if fecha:
                params += f"&fecha={fecha}"

            if fase:
                params += f"&fase={fase}"  

            return f"{base_url}?{params}"         

        links = {
            "_first" : {"href": build_url(0)},
            "_last" :  {"href": build_url(max(total - limit, 0))}
        }

        if offset > 0:
            links ["_prev"] = {"href": build_url(max(offset - limit, 0))}


        if offset + limit < total: 
            links ["_next"] = {"href": build_url(offset + limit)}

        return jsonify ({
            "partidos": partidos,
            "_links" : links,
        }), 200

    except Exception as e:
        return jsonify ({"error": str(e)}), 500
    
    finally:
       if cursor:
        cursor.close()
       if conn: 
        conn.close()
            


@partidos_bp.route("/", methods=["POST"])
def crear_partido():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        datos = request.get_json()
        campos = ['equipo_local', 'equipo_visitante', 'fecha', 'fase']
        
        if not datos:
            return jsonify({"error": "Body vacío"}), 400

        for campo in campos:
            if campo not in datos:
                return jsonify({"error": f"Falta el campo {campo}"}), 400

        equipo_local = datos.get('equipo_local')
        equipo_visitante = datos.get('equipo_visitante')
        fecha = datos.get('fecha')
        fase = datos.get('fase')
       
        if not equipo_local or not equipo_visitante:
            return jsonify({"error": "Equipos inválidos"}), 400

        if equipo_local == equipo_visitante:
            return jsonify({"error": "Un equipo no puede jugar contra sí mismo"}), 400

        if not fecha:
            return jsonify({"error": "Fecha inválida"}), 400

        from datetime import datetime
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except:
            return jsonify({"error": "Formato de fecha inválido (YYYY-MM-DD)"}), 400

        cursor.execute("SELECT ID FROM equipos WHERE equipo = %s", (equipo_local,))
        result_equipo_local = cursor.fetchone()
        if not result_equipo_local:
            return jsonify({"error": "equipo_local no existe"}), 400
        id_equipo_local = result_equipo_local["ID"]

        cursor.execute("SELECT ID FROM equipos WHERE equipo = %s", (equipo_visitante,))
        result_equipo_visitante = cursor.fetchone()
        if not result_equipo_visitante:
            return jsonify({"error": "equipo_visitante no existe"}), 400
        id_equipo_visitante = result_equipo_visitante["ID"]

        query = """
        INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (id_equipo_local, id_equipo_visitante, fecha, fase))
        conn.commit()

        partido_id = cursor.lastrowid

        response = jsonify({
            "ID": partido_id,
            "equipo_local": id_equipo_local,
            "equipo_visitante": id_equipo_visitante,
            "fecha": fecha,
            "fase": fase
        })
        response.status_code = 201
        response.headers["Location"] = f"/partidos/{partido_id}"

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
    
        
@partidos_bp.route("/<int:partido_id>", methods=["GET"])
def obtener_partido(partido_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            p.ID,
            p.equipo_local,
            p.equipo_visitante,
            p.fecha,
            p.fase,
            r.goles_local,
            r.goles_visitante
        FROM partidos p
        LEFT JOIN resultados r ON p.id = r.partido_id
        WHERE p.id = %s
        """

        cursor.execute(query, (partido_id,))
        partido = cursor.fetchone()

        if not partido:
            return jsonify({"error": "Partido no encontrado"}), 404
        
        resultado = None
        if partido["goles_local"] is not None and partido["goles_visitante"] is not None:
            resultado = {
                "goles_local": partido["goles_local"],
                "goles_visitante": partido["goles_visitante"]
            }

        cursor.execute("SELECT equipo FROM equipos WHERE ID = %s", (partido["equipo_local"],))
        equipo_local = cursor.fetchone()["equipo"]
        cursor.execute("SELECT equipo FROM equipos WHERE ID = %s", (partido["equipo_visitante"],))
        equipo_visitante = cursor.fetchone()["equipo"]
        
        response = {
            "id": partido["ID"],
            "equipo_local": equipo_local,
            "equipo_visitante": equipo_visitante,
            "fecha": str(partido["fecha"]),
            "fase": partido["fase"],
            "resultado": resultado
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@partidos_bp.route("/<int:partido_id>", methods=["DELETE"])
def eliminar_partido(partido_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        
        cursor.execute("DELETE FROM resultados WHERE partido_id = %s", (partido_id,))
        cursor.execute("DELETE FROM predicciones WHERE partido_id = %s", (partido_id,))

        
        query_eliminar = "DELETE FROM partidos WHERE id = %s"
        cursor.execute(query_eliminar, (partido_id,))

        if cursor.rowcount == 0:
            return jsonify({"error": "Partido no encontrado"}), 404

        conn.commit()

        return jsonify({"mensaje": "Partido eliminado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@partidos_bp.route ("/<int:partido_id>/resultados", methods=["PUT"])
def actualizar_partido(partido_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "Body vacío"}), 400
        goles_local = datos.get("goles_local")
        goles_visitante = datos.get("goles_visitante")
        if goles_local is None or goles_visitante is None:
            return jsonify({"error": "Faltan goles_local o goles_visitante"}), 400
        
        if goles_local < 0 or goles_visitante < 0:
            return jsonify({"error": "Los goles no pueden ser negativos"}), 400
        cursor.execute("SELECT id FROM partidos WHERE id = %s", (partido_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Partido no encontrado"}), 404
        
        if resultado_existe is not None:
            query_actualizar = """
            UPDATE resultados
            SET goles_local = %s, goles_visitante = %s
            WHERE partido_id = %s
            """
            cursor.execute(query_actualizar, (goles_local, goles_visitante, partido_id))
        else:
            query_insertar = """
            INSERT INTO resultados (partido_id, goles_local, goles_visitante)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query_insertar, (partido_id, goles_local, goles_visitante))
        conn.commit()
        return jsonify({"mensaje": "Resultado actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        

            