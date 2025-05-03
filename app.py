from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'dein_geheimer_schluessel'  # Stelle sicher, dass dies sicher ist!

# Definiere die maximalen Punkte für jede Kategorie
max_punkte = {
    '1er': 5,
    '2er': 10,
    '3er': 15,
    '4er': 20,
    '5er': 25,
    '6er': 30,
    'Bonus': 35,
    'Dreier': 30,
    'Vierer': 40,
    'Full House': 25,
    'Kleine Straße': 30,
    'Große Straße': 40,
    'Kniffel': 50,
    'Chance': 50
}

# Funktion, um den Spielstand zu initialisieren
def init_spielstand(spieler_punkte):
    if 'punkte' not in session:
        session['punkte'] = {spieler: {kategorie: '' for kategorie in max_punkte} for spieler in spieler_punkte}
        session['gesamtsumme'] = {spieler: 0 for spieler in spieler_punkte}
        session['spieler_punkte'] = spieler_punkte

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        spieler_punkte = request.form.getlist('spieler')  # Spieler werden hier eingegeben

        # Initialisieren, falls der Spielstand noch nicht in der Session gespeichert wurde
        init_spielstand(spieler_punkte)

        # Verarbeite die Punkte
        for spieler in spieler_punkte:
            for kategorie in max_punkte:
                punkt_name = f"{spieler}_{kategorie}"
                punkt_wert = request.form.get(punkt_name)

                if punkt_wert:
                    try:
                        punkt_int = int(punkt_wert)
                        if punkt_int <= max_punkte.get(kategorie, 0):  # Überprüfen, ob der Wert im erlaubten Bereich liegt
                            session['punkte'][spieler][kategorie] = punkt_int
                    except ValueError:
                        session['punkte'][spieler][kategorie] = ''

        # Gesamtsummen neu berechnen
        session['gesamtsumme'] = {spieler: sum(
            v for v in session['punkte'][spieler].values() if isinstance(v, int)) for spieler in spieler_punkte}

        # Bonus berechnen, wenn der Bonus erfüllt ist
        for spieler in spieler_punkte:
            if sum(session['punkte'][spieler][kategorie] for kategorie in ['1er', '2er', '3er', '4er', '5er', '6er']) >= 63:
                session['punkte'][spieler]['Bonus'] = 35

        # Speichern der Session
        session.modified = True

    try:
        return render_template('index.html', max_punkte=max_punkte, spieler_punkte=session['spieler_punkte'],
                               punkte=session['punkte'], gesamtsumme=session['gesamtsumme'])
    except Exception as e:
        return f"Es gab einen Fehler: {e}"

if __name__ == '__main__':
    app.run(debug=True)
