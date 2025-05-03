from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "geheim"

kategorien = [
    "1er", "2er", "3er", "4er", "5er", "6er", "Bonus",
    "Dreierpasch", "Viererpasch", "Full House", "Kleine Straße",
    "Große Straße", "Kniffel", "Chance"
]

max_punkte = {
    "1er": 5, "2er": 10, "3er": 15, "4er": 20,
    "5er": 25, "6er": 30, "Bonus": 35,
    "Dreierpasch": 30, "Viererpasch": 40,
    "Full House": 25, "Kleine Straße": 30,
    "Große Straße": 40, "Kniffel": 50, "Chance": 30
}

fixpunkte = {
    "Full House": 25,
    "Kleine Straße": 30,
    "Große Straße": 40,
    "Kniffel": 50
}

@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        # Spieler von der Startseite erhalten
        namen = request.form.getlist("spielername")
        namen = [name.strip() for name in namen if name.strip()]  # Leere Felder ignorieren
        if not namen:
            return redirect(url_for("start"))  # Keine gültigen Spieler
        session["spieler"] = namen
        session["punkte"] = {
            name: {k: "" for k in kategorien} for name in namen
        }
        return redirect(url_for("spiel"))
    return render_template("start.html")

@app.route("/spiel", methods=["GET", "POST"])
def spiel():
    spieler_punkte = session.get("punkte", {})
    if not spieler_punkte:
        return redirect(url_for("start"))

    if request.method == "POST":
        # Punkte aktualisieren
        for spieler in spieler_punkte:
            for kategorie in kategorien:
                feldname = f"{spieler}_{kategorie}"
                wert = request.form.get(feldname)
                if wert is not None and wert.isdigit():
                    spieler_punkte[spieler][kategorie] = int(wert)

        # Bonus automatisch berechnen
        for spieler in spieler_punkte:
            obere_summe = sum(
                spieler_punkte[spieler].get(k, 0) for k in kategorien[:6]
                if isinstance(spieler_punkte[spieler].get(k), int)
            )
            spieler_punkte[spieler]["Bonus"] = 35 if obere_summe >= 63 else 0

        session["punkte"] = spieler_punkte

    gesamtsumme = {}
    for spieler, punkte in spieler_punkte.items():
        obere = sum(punkte.get(k, 0) for k in kategorien[:7] if isinstance(punkte.get(k), int))
        untere = sum(punkte.get(k, 0) for k in kategorien[7:] if isinstance(punkte.get(k), int))
        gesamtsumme[spieler] = obere + untere

    return render_template("spiel.html",
                           spieler_punkte=spieler_punkte,
                           kategorien=kategorien,
                           punkte=spieler_punkte,
                           max_punkte=max_punkte,
                           gesamtsumme=gesamtsumme,
                           fixpunkte=fixpunkte)
