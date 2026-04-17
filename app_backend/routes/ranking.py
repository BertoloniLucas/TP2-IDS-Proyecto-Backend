from flask import Blueprint, jsonify, request

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

        query = """ 
                SELECT
                u.id,
                u,nombre,
                SUM(
                    CASE    
                            WHEN p.prediccion_local == r.goles_local
                            AND p.prediccion_visitante == r.goles_visitante THEN 3

                            WHEN (p.prediccion_local > p.prediccion_visitante AND r.goles_local > r.goles_visitante)
                                (p.prediccion_local < p.prediccion_visitante AND r.goles_local < r.goles_visitante)
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

        return jsonify(ranking), 200
        

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    

