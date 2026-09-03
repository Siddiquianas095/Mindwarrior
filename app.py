from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "mind-warrior-secret-key"

UPLOAD_FOLDER = "static/pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Mind123"


@app.route("/")
def home():
    pdfs = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", pdfs=pdfs)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))

        return render_template(
            "login.html",
            error="Wrong username or password!"
        )

    return render_template("login.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))

    if request.method == "POST":
        pdf = request.files.get("pdf")

        if pdf and pdf.filename.lower().endswith(".pdf"):
            pdf.save(os.path.join(UPLOAD_FOLDER, pdf.filename))

        return redirect(url_for("admin"))

    pdfs = os.listdir(UPLOAD_FOLDER)

    return render_template("admin.html", pdfs=pdfs)


@app.route("/pdf/<filename>")
def open_pdf(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)