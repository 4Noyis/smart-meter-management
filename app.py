from flask import Flask, request, render_template, redirect
import sqlite3
import os

currentDirectory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect(os.path.join(currentDirectory, "database.db"))
    connection.row_factory = sqlite3.Row
    return connection

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            form_type=request.form["form_type"]
            
            connection = get_db_connection()
            cursor = connection.cursor()

            id_search = request.form["id_search"]
            if form_type=="search":
        
                cursor.execute("SELECT id FROM Binalar WHERE id=?", 
                           (id_search))
                result_search = cursor.fetchone()

                if result_search:
                    print(id_search)
                    cursor.execute("SELECT su, dogalgaz, elektrik, date FROM Daireler WHERE building_id = ? ORDER BY date DESC LIMIT 5", (result_search[0],))
                    rows = cursor.fetchall()
                    return render_template("index.html", rows=rows , id_search=id_search)
                else:
                    print("No building found with the provided details.")
                    return render_template("index.html", message="No building found")
                    
            elif form_type == "add":
                
                su_add = float(request.form["su"])
                dogalgaz_add = float(request.form["dogalgaz"])
                elektrik_add = float(request.form["elektrik"])

                cursor.execute("SELECT id FROM Binalar WHERE id=?", 
                           (id_search,))
                result_add = cursor.fetchone()

                if result_add:
                    building_id = result_add[0]
                    query2 = "INSERT INTO Daireler (building_id, su, dogalgaz, elektrik) VALUES (?, ?, ?, ?)"
                    cursor.execute(query2, (building_id, su_add, dogalgaz_add, elektrik_add))
                    connection.commit()

                    cursor.execute("SELECT su, dogalgaz, elektrik, date FROM Daireler WHERE building_id = ? ORDER BY date DESC LIMIT 5", (building_id,))
                    rows = cursor.fetchall()
                    return render_template("index.html", rows=rows)
                else:
                    print("No building found with the provided details for adding data.")
                    return render_template("index.html", message="No building found for adding data")
            


            connection.close()  # Always close the connection after use
        except Exception as e:
            print(f"Error: {e}")
            # Optionally return an error message to the user
            return "An error occurred. Please check the server logs for more details."
    
    return render_template("index.html")


@app.route("/add", methods=["POST", "GET"])
def add_new():
    if request.method=="POST":
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            ilce_add = request.form["ilce_add"]
            apt_add = request.form["apt_add"]
            blok_add = request.form["blok_add"]
            daire_add = request.form["daire_add"]

            query = "INSERT INTO Binalar (ilce, apartman, blok, daire) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (ilce_add, apt_add, blok_add, daire_add))
            connection.commit()

            connection.close()
            return redirect("/")
        
        except Exception as e:

            print(f"Error: {e}")
            return "An error occurred. Please check the server logs for more details."
    
    return render_template("add.html")


@app.route("/remove", methods=["POST", "GET"])
def remove():
    if request.method=="POST":
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            ilce_remove=request.form["ilce_remove"]
            apt_remove=request.form["apt_remove"]
            blok_remove=request.form["blok_remove"]
            daire_remove=request.form["daire_remove"]

            cursor.execute("SELECT id FROM Binalar WHERE ilce = ? AND apartman =? AND blok = ? AND daire = ?", 
                           (ilce_remove, apt_remove, blok_remove, daire_remove))
            result_remove = cursor.fetchone()
            

            if result_remove:
                building_id = result_remove[0]
                cursor.execute("DELETE FROM Daireler WHERE building_id = ?", (building_id,))
                cursor.execute("DELETE FROM Binalar WHERE ilce = ? AND apartman =? AND blok = ? AND daire = ?", 
                           (ilce_remove, apt_remove, blok_remove, daire_remove))
                connection.commit()
            connection.close()

    
        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred. Please check the server logs for more details."
        
    return render_template("remove.html")
