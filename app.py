from flask import Flask, render_template, request, redirect, session
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)
app.secret_key = "secret123"

# ----------------------------
# FIREBASE INIT
# ----------------------------
firebase_key = os.environ.get("FIREBASE_KEY")

if firebase_key:
    cred_dict = json.loads(firebase_key)
    cred = credentials.Certificate(cred_dict)
else:
    cred = credentials.Certificate("firebase-key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ----------------------------
# LOGIN PAGE
# ----------------------------
@app.route("/")
def login():
    return render_template("login.html", message="")

# ----------------------------
# OPEN / CREATE NOTE
# ----------------------------
@app.route("/open", methods=["POST"])
def open_note():
    note_name = request.form.get("note_name")
    password = request.form.get("password")

    if not note_name or not password:
        return render_template("login.html", message="All fields required ❗")

    doc_ref = db.collection("notes").document(note_name)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()

        if data.get("password") == password:
            session["note"] = note_name
            return redirect(f"/note/{note_name}")
        else:
            return render_template("login.html", message="Wrong password ❌")

    else:
        doc_ref.set({
            "content": "",
            "password": password
        })
        session["note"] = note_name
        return redirect(f"/note/{note_name}")

# ----------------------------
# VIEW NOTE
# ----------------------------
@app.route("/note/<note_name>")
def note(note_name):

    if session.get("note") != note_name:
        return redirect("/")

    doc_ref = db.collection("notes").document(note_name)
    doc = doc_ref.get()

    if not doc.exists:
        return "Note not found ❌"

    content = doc.to_dict().get("content", "")

    return render_template(
        "editor.html",
        note_name=note_name,
        content=content
    )

# ----------------------------
# SAVE NOTE (ONLY ONE!)
# ----------------------------
@app.route("/save/<note_name>", methods=["POST"])
def save(note_name):

    if session.get("note") != note_name:
        return "Unauthorized ❌"

    content = request.form.get("content", "")

    doc_ref = db.collection("notes").document(note_name)

    doc = doc_ref.get()
    password = ""
    if doc.exists:
        password = doc.to_dict().get("password", "")

    doc_ref.set({
        "content": content,
        "password": password
    })

    return "Saved"

# ----------------------------
# LOGOUT
# ----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
