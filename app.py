from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

KATEGORIEN = [
    "Einser", "Zweier", "Dreier", "Vierer", "Fünfer", "Sechser",
    "Bonus", "Dreierpasch", "Viererpasch", "Full House",
    "Kleine Straße", "Große Straße", "Kniffel", "Chance"
]

spieler_punkte = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        namen_input = request.form.get("spielernamen")
        if namen_input:
            namen = [n.strip() for n in namen_input.split(",") if n.strip()]
            for name in namen:
                if name not in spieler_punkte:
                    spieler_punkte[name] = {k: "" for k in KATEGORIEN}
            return redirect(url_for("spiel"))
    return render_template("index.html")

@app.route("/spiel", methods=["GET", "POST"])
def spiel():
    if request.method == "POST":
        for spieler in spieler_punkte:
            for kategorie in KATEGORIEN:
                wert = request.form.get(f"{spieler}_{kategorie}")
                if wert is not None:
                    spieler_punkte[spieler][kategorie] = wert

    gesamtsumme = {}
    for spieler, punkte in spieler_punkte.items():
        try:
            obere = sum(int(punkte[k]) for k in KATEGORIEN[:6] if punkte[k].isdigit())
            bonus = 35 if obere >= 63 else 0
            spieler_punkte[spieler]["Bonus"] = str(bonus)
            gesamtsumme[spieler] = sum(int(punkte[k]) for k in KATEGORIEN if punkte[k].isdigit())
        except ValueError:
            gesamtsumme[spieler] = 0

    return render_template("spiel.html", spieler_punkte=spieler_punkte, kategorien=KATEGORIEN, gesamtsumme=gesamtsumme)
