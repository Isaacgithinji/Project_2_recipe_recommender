import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # change if different
        password="",       # put your MySQL password here
        database="recipe_db"
    )

    if conn.is_connected():
        print("✅ Successfully connected to MySQL database!")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        print("Tables in recipe_db:", cursor.fetchall())
        cursor.close()
        conn.close()

except mysql.connector.Error as e:
    print("❌ Error:", e)
