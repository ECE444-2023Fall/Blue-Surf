from app import app, db
from models import Tag
from datalayer_abstract import DataLayer
import logging

'''
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
'''

class TagDataLayer(DataLayer):
    '''
    The TagDataLayer should be accessed by the rest of the code when trying to access the Tag table in the database.
    '''
    def get_all_tags(self):
        '''
        Returns a list of strings containing all the existing tags in the database.
        '''
        with app.app_context():
            tags = Tag.query.all()
        tag_names = [tag.name for tag in tags]
        return tag_names 
    
    def add_tag(self, tag_name: str):
        '''
        Inserts the given tag name into the Tag table in the database.
        '''
        # Check if a tag with the same name already exists
        with app.app_context():
            existing_tag = Tag.query.filter_by(name=tag_name).first()

        if existing_tag is None:  # No existing tag with the same name
            tag = Tag()
            tag.name = tag_name
            with app.app_context():
                db.session.add(tag)
                db.session.commit()
        else:
            logging.warning(f"Tag {tag_name} {self.ALREADY_EXISTS}")


