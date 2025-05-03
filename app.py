from flask import Flask, render_template, request, session, redirect, url_for
from flask.sessions import SecureCookieSession

app = Flask(__name__)
app.secret_key = 'dein_geheimer_schluessel'  # Ändere diesen Schlüssel für mehr Sicherheit

# Beispiel-Daten
spieler_punkte = ['Spieler 1', 'Spieler 2', 'Spieler 3']
kategorien = ['1er', '2er', '3er', '4er', '5er', '6er', 'Bonus', 'Dreier', 'Vierer', 'Full House', 'Kleine Straße', 'Große Straße', 'Kniffel', 'Chance']

# Funktion, um die Spielstände zu initialisieren, falls sie noch nicht in der Session gespeichert sind
def init_spielstand():
    if 'punkte' not in session:
        session['punkte'] = {spieler: {kategorie: '' for kategorie in kategorien} for spieler in spieler_punkte}
        session['gesamtsumme'] = {spieler: 0 for spieler in spieler_punkte}

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialisieren, falls der Spielstand noch nicht in der Session gespeichert wurde
    init_spielstand()

    if request.method == 'POST':
        # Fehlerbehandlung: Überprüfen, ob die Eingabewerte gültige Zahlen sind
        for spieler in spieler_punkte:
            for kategorie in kategorien:
                punkt_name = f"{spieler}_{kategorie}"
                punkt_wert = request.form.get(punkt_name)

                if punkt_wert:
                    try:
                        punkt_int = int(punkt_wert)
                        session['punkte'][spieler][kategorie] = punkt_int
                    except ValueError:
                        # Falls die Eingabe keine gültige Zahl war, überspringen
                        session['punkte'][spieler][kategorie] = ''
                else:
                    session['punkte'][spieler][kategorie] = ''

        # Gesamtsummen neu berechnen
        session['gesamtsumme'] = {spieler: sum(
            v for v in session['punkte'][spieler].values() if isinstance(v, int)) for spieler in spieler_punkte}

        # Speichern der Session
        session.modified = True

    return render_template('index.html', spieler_punkte=spieler_punkte, kategorien=kategorien,
                           punkte=session['punkte'], gesamtsumme=session['gesamtsumme'])

if __name__ == '__main__':
    app.run(debug=True)
