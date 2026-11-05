import os
import requests

from dotenv import load_dotenv

from models import db, User, Movie

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

API_URL = "https://www.omdbapi.com/"


class DataManager:
    def create_user(self, name):
        """
        Fügt einen neuen Nutzer zu der Datenbank hinzu.
        :param name: Name des Nutzers
        :return:
        """
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

        return new_user

    def get_users(self):
        """
        :return: Liste aller Nutzer in der Datenbank
        """
        users = User.query.all()

        return users

    def get_movies(self, user_id):
        """
        :param user_id: ID des Nutzers, dessen Filme aufgelistet werden sollen
        :return: eine Liste aller Filme eines bestimmten Nutzers
        """
        movies = Movie.query.filter_by(user_id=user_id).all()

        return movies

    def add_movie(self, title, user_id, year=None):
        """
        Fügt einen neuen Film zu der Favoriten-Datenbank des Nutzers hinzu.
        :param:
            title: Titel des Films, der hinzugefügt werden soll
            user_id: die ID des Nutzers, zu dessen Favoriten der Film hinzugefügt wird
            year: Optionales Erscheinungsjahr zur genaueren Filmsuche
        :return: Erstelltes Filmobjekt oder None, falls kein Film gefunden wurde
        """
        params = {
            "apikey": OMDB_API_KEY,
            "t": title
        }

        if year:
            params["y"] = year

        try:
            response = requests.get(API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

        except requests.exceptions.RequestException:
            return None

        if data.get("Response") == "False":
            return None

        movie = Movie(
            name=data['Title'],
            director=data['Director'],
            year=data['Year'],
            poster_url=data['Poster'],
            user_id=user_id
        )

        db.session.add(movie)
        db.session.commit()

        return movie

    def update_movie(self, movie_id, new_title):
        """
        Aktualisiere die Details eines bestimmten Films in der Datenbank.
        :param movie_id: ID des bestehenden Films
        :param new_title: neuer Titel des Films
        :return: aktualisierter Film oder None, falls nicht gefunden
        """
        movie = db.session.get(Movie, movie_id)

        if movie is None:
            return None

        movie.name = new_title
        db.session.commit()

        return movie

    def delete_movie(self, movie_id):
        """
        Entferne den Film aus der Favoritenliste des Nutzers.
        :param movie_id: ID des Films
        :return: True bei Erfolg, False, falls nicht gefunden
        """
        movie = db.session.get(Movie, movie_id)

        if movie is None:
            return False

        db.session.delete(movie)
        db.session.commit()

        return True
