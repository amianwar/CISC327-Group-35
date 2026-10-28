from flask import Blueprint, jsonify, request

from app import store
from app.models.rental import Rental

search_bp = Blueprint("search", __name__, url_prefix="/search")

@search_bp.route("", methods=["GET"])
def search():
    search_query = request.args.get("q", "").strip()
    if search_query:
        results = Rental.search_query.filter((Rental.renter_id(f"%{search_query}%")) | (Rental.equipment_id(f"%{search_query}%"))).all()
    else:
        results = []

    return jsonify(results)
    