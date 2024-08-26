from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    """
    Store class is a view class that represents a store in the database.
    """
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """
        Get a store by its ID.
        """
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        """
        Delete a store by its ID.
        """
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}


@blp.route("/store")
class StoreList(MethodView):
    """
    StoreList class is a view class that represents a list of stores in the database.
    """
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """
        Get a list of stores.
        """
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        """
        Create a new store.
        """
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store
