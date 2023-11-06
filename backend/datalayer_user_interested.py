from app import app, db
from models import User, Event, UserInterestedEvent
from datalayer_abstract import DataLayer
import logging

'''
class UserInterestedEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
'''

class UserInterestedLayer(DataLayer):
    '''
    The UserDataLayer should be accessed by the rest of the code when trying to access the User table in the database.
    '''
    def create_user_interested_by_id(self, user_id, event_id):
        with app.app_context():
            event_exists = Event.query.filter_by(id=event_id).first()
            if event_exists is None:  
                logging.info(f"Event {self.DOES_NOT_EXIST}")
                raise ValueError(f"Event {self.DOES_NOT_EXIST}")      
            user_exists = User.query.filter_by(id=user_id).first()
            if user_exists is None:
                logging.info(f"User {self.DOES_NOT_EXIST}")
                raise ValueError(f"User {self.DOES_NOT_EXIST}") 
            user_interested_exists = UserInterestedEvent.query.filter_by(user_id=user_id, event_id=event_id).first()  
            if user_interested_exists is not None:
                logging.info(f"User-event pair {self.ALREADY_EXISTS}")
                raise ValueError(f"User-event pair {self.ALREADY_EXISTS}") 
            user_interested = UserInterestedEvent(user_id=user_id, event_id=event_id)
    
            db.session.add(user_interested)
            event_exists.like_count += 1 
            db.session.commit() 
            
    def delete_user_interested_by_id(self, user_id, event_id):
        with app.app_context():
            event_exists = Event.query.filter_by(id=event_id).first()
            if event_exists is None:  
                logging.info(f"Event {self.DOES_NOT_EXIST}")
                raise ValueError(f"Event {self.DOES_NOT_EXIST}")      
            user_interested_exists = UserInterestedEvent.query.filter_by(user_id=user_id, event_id=event_id).first()  
            if user_interested_exists is None:
                logging.info(f"User-event pair {self.DOES_NOT_EXIST}")
            else:
                db.session.delete(user_interested_exists)
                event_exists.like_count -= 1
                db.session.commit()
                
            
            
        
      



    

            

