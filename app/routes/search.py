from flask import Blueprint, jsonify, request

from app.controller.qanda_controller import search_for_post_by_key

search_route = Blueprint("search", __name__)


@search_route.route("/searchbar/autocomplete", methods=["POST"])
def autocomplete():
    search_for = request.get_json().get("search_key")

    search_results = search_for_post_by_key(search_for)
    print(search_results)

    return jsonify(search_results), 200
