from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # Students table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT
    )
    ''')

    # Doubts table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS doubts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        question TEXT,
        answer TEXT
    )
    ''')

    # Faculty table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS faculty(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        experience TEXT,
        status TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# ================= PAGES =================
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/doubts')
def doubts_page():
    return render_template("doubts.html")

@app.route('/mentor')
def mentor_page():
    return render_template("mentor.html")

@app.route('/faculty')
def faculty_page():
    return render_template("faculty.html")

# ================= STUDENT =================
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO students(email,password) VALUES(?,?)",
                (data['email'], data['password']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE email=? AND password=?",
                (data['email'], data['password']))

    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

# ================= DOUBTS =================
@app.route('/add_doubt', methods=['POST'])
def add_doubt():
    data = request.json

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO doubts(email,question,answer) VALUES(?,?,?)",
                (data['email'], data['question'], ""))

    conn.commit()
    conn.close()

    return jsonify({"message": "Doubt added"})

@app.route('/get_doubts/<email>')
def get_doubts(email):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute("SELECT id,question,answer FROM doubts WHERE email=?", (email,))
    data = cur.fetchall()

    conn.close()
    return jsonify(data)

# ================= MENTOR =================
@app.route('/all_doubts')
def all_doubts():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute("SELECT id,question,answer FROM doubts")
    data = cur.fetchall()

    conn.close()
    return jsonify(data)

@app.route('/answer', methods=['POST'])
def answer():
    data = request.json

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute("UPDATE doubts SET answer=? WHERE id=?",
                (data['answer'], data['id']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Answer submitted"})

# ================= FACULTY =================
@app.route('/add_experience', methods=['POST'])
def add_experience():
    data = request.json

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO faculty(name,email,experience,status) VALUES(?,?,?,?)",
                (data['name'], data['email'], data['experience'], "Pending"))

    conn.commit()
    conn.close()

    return jsonify({"message": "Experience submitted"})

@app.route('/get_faculty/<email>')
def get_faculty(email):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute("SELECT status FROM faculty WHERE email=?", (email,))
    data = cur.fetchone()

    conn.close()

    if data:
        return jsonify({"status": data[0]})
    else:
        return jsonify({"status": "No record found"})

@app.route('/all_faculty')
def all_faculty():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute("SELECT id,name,email,experience,status FROM faculty")
    data = cur.fetchall()

    conn.close()
    return jsonify(data)

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute("UPDATE faculty SET status=? WHERE id=?",
                (data['status'], data['id']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Status updated"})

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)