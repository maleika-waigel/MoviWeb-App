import os
from flask import Flask, render_template

from data_manager import DataManager
from models import db, Movie


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def home():
    """
    Die Startseite. Zeigt eine Liste aller registrierten Nutzer
    und ein Formular zum Hinzufügen neuer Nutzer.
    (Diese Route verwendet standardmäßig GET.)
    :return:
    """
    users = data_manager.get_users()
    return render_template('users.html', users=users)


@app.route('/users', methods=['POST'])
def add_user():
    """
    Wenn der Nutzer das „Nutzer hinzufügen“-Formular abschickt, wird eine POST-Anfrage ausgelöst.
    Der Server erhält die neuen Nutzerdaten, fügt sie der Datenbank hinzu und leitet dann zurück zu /.
    :return:
    """
    pass


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    """
    Wenn du auf einen Nutzernamen klickst, ruft die App die Liste der
    Lieblingsfilme dieses Nutzers ab und zeigt sie an.
    :return:
    """
    pass


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Fügt einen neuen Film zur Favoritenliste eines Nutzers hinzu.
    :return:
    """
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """
    Den Titel eines bestimmten Films in der Liste eines Nutzers ändern, ohne sich auf OMDb für Korrekturen zu verlassen.
    :return:
    """
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Entfernt einen bestimmten Film aus der Liste der Lieblingsfilme eines Nutzers.
    :return:
    """
    pass


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run()
