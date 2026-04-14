from flask import Blueprint, jsonify, request
from db import get_connection

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route ("/", methods=["GET"])
def lista_partidos():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor (dictionary=True)    
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
            partidos.append ({
                "ID" : partido["ID"],
                "equipo_local" : partido ["equipo_local"],
                "equipo_visitante" : partido ["equipo_visitante"],
                "fecha" : str(partido["fecha"]),
                "fase" : partido ["fase"]
            })

        base_url = request.base_url

        def build_url (new_offset):
            return f"{base_url}?_limit={limit}&_offset={new_offset}"

        links = {
            "_first" : {"href": build_url(0)},
            "_last" :  {"href": build_url(max(total - limit, 0))}
        }

        if offset > 0:
            links ["_prev"] = {"href": build_url(max(total - limit, 0))}


        if offset + limit < total: 
            links ["_next"] = {"href": build_url(offset + limit)}

        return jsonify ({
            "partidos": partidos,
            "_links" : links,
        }), 200

    except Exception as e:
        return jsonify ({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()
            


@partidos_bp.route("/", methods=["POST"])
def crear_partido():
    conn = None
    cursor = None
    try:
        conn = get_connection() #coneccion con la db
        cursor = conn.cursor (dictionary=True) #El cursor me permite realizar consultas SQL, devuelve diccionarios en vez de tuplas.
        datos = request.get_json() #obtengo los datos del body solicitado
        campos = ['equipo_local', 'equipo_visitante', 'fecha', 'fase']
        
        if not datos:
            return (jsonify({'error': 'campos incompletos'}), 400)
        for campo in campos:
            if campo not in datos:
                return (jsonify({'error': '%s no especificado' %campo}), 400)
        
        equipo_local = datos.get('equipo_local')
        equipo_visitante = datos.get('equipo_visitante')
        fecha = datos.get('fecha')
        fase = datos.get('fase')

        query = """
        INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (equipo_local, equipo_visitante, fecha, fase))
        conn.commit()

        return jsonify({'mensaje':'Partido agregado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': '%s' %e}), 500 
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    
        
@partidos_bp.route("/<int:partido_id>", methods=["GET"])
def obtener_partido(partido_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM partidos WHERE ID = %s"
        cursor.execute(query, (partido_id,))
        partido = cursor.fetchone()

        if not partido:
            return jsonify({'error': 'Partido no encontrado'}), 404
        else:
            return jsonify(partido), 200
    except Exception as e:
        return jsonify({'error':'%s' %e}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    
@partidos_bp.route("/<int:partido_id>", methods=["DELETE"])
def eliminar_partido(partido_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query_eliminar = "DELETE FROM partidos WHERE ID = %s"
        cursor.execute(query_eliminar, (partido_id,))

        filas_afectadas = cursor.rowcount #verifico si el execute devolvio alguna fila.
        if filas_afectadas == 0:
            return jsonify({'error': 'Partido no encontrado'}), 404
        else:
            conn.commit()
            return jsonify({'mensaje': 'Partido eliminado'}), 200
    except Exception as e:
        return jsonify({'error': '%s' %e}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
