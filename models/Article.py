from application import db


# Article模型

class Article(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    types = db.Column(db.String(10), nullable=False)
    img_url = db.Column(db.String(300))
    author = db.Column(db.String(20))
    view_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    is_valid = db.Column(db.Boolean, default=1)
    is_recommend = db.Column(db.Boolean, default=0)
