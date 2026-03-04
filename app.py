from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)

# ----------------------------
# FIREBASE INITIALIZATION
# ----------------------------

firebase_key = os.environ.get("FIREBASE_KEY")

if firebase_key:
    # Production (Render)
    cred_dict = json.loads(firebase_key)
    cred = credentials.Certificate(cred_dict)
else:
    # Local testing (only if you have local json file)
    cred = credentials.Certificate("firebase-key.json")

# Prevent re-initialization error
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/open", methods=["POST"])
def open_note():
    note_name = request.form.get("note_name")
    if not note_name:
        return redirect("/")
    return redirect(f"/note/{note_name}")


@app.route("/note/<note_name>")
def note(note_name):
    doc_ref = db.collection("notes").document(note_name)
    doc = doc_ref.get()

    if doc.exists:
        content = doc.to_dict().get("content", "")
    else:
        doc_ref.set({"content": ""})
        content = ""

    return render_template(
        "editor.html",
        note_name=note_name,
        content=content
    )


@app.route("/save/<note_name>", methods=["POST"])
def save(note_name):
    content = request.form.get("content", "")
    doc_ref = db.collection("notes").document(note_name)
    doc_ref.set({"content": content})
    return "Saved"


# ----------------------------
# RUN APP
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)