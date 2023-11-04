from app import app, db
from models import Tag
from datalayer_abstract import DataLayer
import logging

'''
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
'''

class TagDataLayer(DataLayer):
    '''
    The TagDataLayer should be accessed by the rest of the code when trying to access the Tag table in the database.
    '''
    @staticmethod
    def get_all_tags():
        '''
        Returns a list of strings containing all the existing tags in the database.
        '''
        with app.app_context():
            tags = Tag.query.all()
        tag_names = [tag.name for tag in tags]
        return tag_names 
  

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     tag_data = TagDataLayer.get_all_tags()

#     # Use a format string with a placeholder (%s) and provide tag_data as a tuple
#     logging.info("Here are some tags: %s", tag_data)



