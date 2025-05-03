from flask import Flask, render_template, request

app = Flask(_name_)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/spiel', methods=['POST'])
def spiel():
    spieler = request.form.get("spieler")
    return render_template("spiel.html", spieler=spieler)

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=10000)
