#To hold database model
from garden import db


class Garden(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    item_type=db.Column(db.String(20))
    item_name=db.Column(db.String(120))

    def __repr__(self):
        return f"garden('{self.item_type}','{self.item_name}')"





