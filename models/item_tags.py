from db import db


class ItemTags(db.Model):
    """
    ItemTags class is a model class that represents the relationship between items and tags in the database.
    """
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))

