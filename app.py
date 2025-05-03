from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'dein_geheimer_schluessel'

kategorien = ['1er', '2er', '3er', '4er', '5er', '6er', 'Bonus',
              'Dreier', 'Vierer', 'Full House', 'Kleine Straße',
              'Große Straße', 'Kniffel', 'Chance']

max_punkte = {
    '1er': 5, '2er': 10, '3er': 15, '4er': 20, '5er': 25, '6er': 30,
    'Bonus': 35, 'Dreier': 30, 'Vierer': 40, 'Full House': 25,
    'Kleine Straße': 30, 'Große Straße': 40, 'Kniffel': 50, 'Chance': 50
}

def init_spielstand(spieler_liste):
    session['spieler_punkte'] = spieler_liste
    session['punkte'] = {spieler: {k: '' for k in kategorien} for spieler in spieler_liste}
    session['gesamtsumme'] = {spieler: 0 for spieler in spieler_liste}

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        spieler_eingabe = request.form.get('spieler')
        spieler_liste = [s.strip() for s in spieler_eingabe.split(',') if s.strip()]
        if not spieler_liste:
            return "Bitte mindestens einen Spielernamen eingeben."
        init_spielstand(spieler_liste)
        return redirect(url_for('spiel'))
    return render_template('start.html')

@app.route('/spiel', methods=['GET', 'POST'])
def spiel():
    if 'spieler_punkte' not in session:
        return redirect(url_for('start'))

    spieler_punkte = session['spieler_punkte']
    punkte = session['punkte']

    if request.method == 'POST':
        for spieler in spieler_punkte:
            for kategorie in kategorien:
                name = f"{spieler}_{kategorie}"
                wert = request.form.get(name)
                if wert:
                    try:
                        punkt = int(wert)
                        if punkt <= max_punkte.get(kategorie, 100):  # großzügiges Limit für freie Felder
                            session['punkte'][spieler][kategorie] = punkt
                    except ValueError:
                        pass

        # Bonus automatisch setzen
        for spieler in spieler_punkte:
            ober_summe = sum(
                session['punkte'][spieler][k] for k in ['1er', '2er', '3er', '4er', '5er', '6er']
                if isinstance(session['punkte'][spieler][k], int)
            )
            if ober_summe >= 63:
                session['punkte'][spieler]['Bonus'] = 35
            else:
                session['punkte'][spieler]['Bonus'] = ''

        # Gesamtsumme berechnen
        session['gesamtsumme'] = {
            spieler: sum(v for v in session['punkte'][spieler].values() if isinstance(v, int))
            for spieler in spieler_punkte
        }
        session.modified = True

    return render_template('spiel.html',
                           spieler_punkte=spieler_punkte,
                           kategorien=kategorien,
                           punkte=session['punkte'],
                           gesamtsumme=session['gesamtsumme'],
                           max_punkte=max_punkte)
