import mysql.connector 
with open("init_db.sql") as f:
    sql_script = f.read()
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = conn.cursor()
    for statement in sql_script.split(";"):
        if statement.strip():
            print(statement)
            cursor.execute(statement)
    conn.commit()
    print("statement executed")
    cursor.close()
    conn.close()
    