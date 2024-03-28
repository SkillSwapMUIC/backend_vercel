from flask import Blueprint, json, jsonify, request, url_for

from app.models.question import Question

search_route = Blueprint("search", __name__)


@search_route.route("/searchbar/autocomplete", methods=["GET"])
def autocomplete():
    search = request.args.get("search")
    questions = Question.query.filter(Question.title.contains(search)).limit(5).all()
    json_list = []
    for question in questions:
        question_link = url_for(
            "qanda.get_question", question_id=question.id, _external=True
        )
        json_list.append(
            {"title": question.title, "id": question.id, "link": question_link}
        )

    if json_list:
        json_data = json.dumps(json_list)
        return json_data
    else:
        return jsonify({"message": "Nothing was found"}), 404
