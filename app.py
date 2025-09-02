from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # change if your MySQL username is different
        password="",       # add your MySQL password if set
        database="recipe_db"
    )

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM recipes ORDER BY created_at DESC")
    recipes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", recipes=recipes)

@app.route("/add", methods=["POST"])
def add_recipe():
    name = request.form["name"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recipes (name, ingredients, instructions) VALUES (%s, %s, %s)",
        (name, ingredients, instructions),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("index"))

@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        # Update recipe
        name = request.form["name"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]

        cursor.execute(
            "UPDATE recipes SET name=%s, ingredients=%s, instructions=%s WHERE id=%s",
            (name, ingredients, instructions, recipe_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("index"))

    # Load recipe for editing
    cursor.execute("SELECT * FROM recipes WHERE id = %s", (recipe_id,))
    recipe = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("edit.html", recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True)
