from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Page d'accueil
@app.route('/')
def home():
    return 'Bienvenue sur la page d\'accueil'

# Page d'inscription
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Enregistrer les données dans une base de données ou effectuer d'autres actions nécessaires
        # Dans cet exemple, nous redirigeons simplement vers la page de connexion
        return redirect(url_for('connexion'))
    return render_template('inscription.html')

# Page de connexion
@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Vérification des informations d'identification
        # Dans cet exemple, nous redirigeons simplement vers une page de succès
        return 'Connecté avec succès'
    return render_template('connexion.html')

if __name__ == '__main__':
    app.run(debug=True)
