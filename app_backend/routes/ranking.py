from flask import Blueprint, jsonify, request
from db import get_connection
rankng_bp = Blueprint("ranking", __name__)

@rankng_bp.route ("/", methods=["GET"])
def obtener_partido():
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        limit = int(request.args.get("_limit", 10))
        offset = int(request.args.get("_offset", 0))

        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total_usuarios = cursor.fetchone()['total']

        query = """ 
                SELECT
                u.id,
                u.nombre,
                SUM(
                    CASE    
                            WHEN p.prediccion_local = r.goles_local
                            AND p.prediccion_visitante = r.goles_visitante THEN 3

                            WHEN (p.prediccion_local > p.prediccion_visitante AND r.goles_local > r.goles_visitante)
                            OR (p.prediccion_local < p.prediccion_visitante AND r.goles_local < r.goles_visitante)
                            OR (p.prediccion_local = p.prediccion_visitante AND r.goles_local = r.goles_visitante) THEN 1
                            ELSE 0
                    END
                ) AS puntos
                FROM usuarios u
                LEFT JOIN predicciones p ON u.id = p.usuario_id
                LEFT JOIN resultados r ON p.partido_id = r.partido_id
                GROUP BY u.id
                ORDER BY puntos DESC
                LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, offset))
        lista = cursor.fetchall()

        base_url = request.base_url
        def build_url(new_offset):
            return f"{base_url}?_limit={limit}&_offset={new_offset}"
        
        links = {
            "_first": {"href": build_url(0)},
            "_last": {"href": build_url(max(total_usuarios - limit, 0))}
        }
        if offset > 0:
            links["_prev"] = {"href": build_url(max(offset - limit, 0))}
        if offset + limit < total_usuarios:
            links["_next"] = {"href": build_url(offset + limit)}
        response = {
            "ranking": lista,
            "_links": links
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    

