from ..app import app, db
from ..models import User, Event, Like
from .abstract import DataLayer
import logging

"""
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
"""


class LikeDataLayer(DataLayer):
    """
    The UserDataLayer should be accessed by the rest of the code when trying to access the User table in the database.
    """

    def like_by_id(self, user_id, event_id):
        with app.app_context():
            event_exists = Event.query.filter_by(id=event_id).first()
            if event_exists is None:
                logging.info(f"Event {self.DOES_NOT_EXIST}")
                raise ValueError(f"Event {self.DOES_NOT_EXIST}")
            user_exists = User.query.filter_by(id=user_id).first()
            if user_exists is None:
                logging.info(f"User {self.DOES_NOT_EXIST}")
                raise ValueError(f"User {self.DOES_NOT_EXIST}")
            like_exists = Like.query.filter_by(
                user_id=user_id, event_id=event_id
            ).first()
            if like_exists is not None:
                logging.info(f"User-event pair {self.ALREADY_EXISTS}")
                raise ValueError(f"User-event pair {self.ALREADY_EXISTS}")
            liked = Like(user_id=user_id, event_id=event_id)

            db.session.add(liked)
            event_exists.like_count += 1
            db.session.commit()

    def unlike_by_id(self, user_id, event_id):
        with app.app_context():
            event_exists = Event.query.filter_by(id=event_id).first()
            if event_exists is None:
                logging.info(f"Event {self.DOES_NOT_EXIST}")
                raise ValueError(f"Event {self.DOES_NOT_EXIST}")
            like_exists = Like.query.filter_by(
                user_id=user_id, event_id=event_id
            ).first()
            if like_exists is None:
                logging.info(f"User-event pair {self.DOES_NOT_EXIST}")
            else:
                db.session.delete(like_exists)
                event_exists.like_count -= 1
                db.session.commit()

    def get_liked_events(self, user_id):
        """
        Returns all the events that the user has liked
        """
        with app.app_context():
            user_exists = User.query.filter_by(id=user_id).first()
            if user_exists is None:
                logging.info(f"User {self.DOES_NOT_EXIST}")
                raise ValueError(f"User {self.DOES_NOT_EXIST}")
            likes = Like.query.filter_by(user_id=user_id).all()

            liked_events = Event.query.filter(
                Event.id.in_([like.event_id for like in likes])
            ).all()

            return liked_events
