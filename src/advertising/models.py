#To hold database model
from advertising import advDB

class Advertisement(advDB.Model):
    id = advDB.Column(advDB.Integer, primary_key=True, unique=True)
    tag = advDB.Column(advDB.String())
    text = advDB.Column(advDB.String())
    source_url = advDB.Column(advDB.String())
    img = advDB.Column(advDB.String())	

    def __repr__(self):
        return "<Advertisement {}, text = \"{}\" with tag {} from {}>".format(self.id, self.text, self.tag,self.source_url)

    def serialize(self):
        return {
            "id": self.id,
            "tag": self.tag,
            "text": self.text,
            "source_url": self.source_url,
            "img": self.img
        }