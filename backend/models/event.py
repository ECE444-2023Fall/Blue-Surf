from app import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    like_count = db.Column(db.Integer, default=0)