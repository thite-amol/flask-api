from flask import jsonify, request

from app import db
from app.api import bp
from app.api.errors import bad_request
from app.models import ModelConfig


@bp.route("/train/config/<int:config_id>", methods=["GET"])
def get_config(config_id):
    return jsonify(ModelConfig.query.get_or_404(config_id).to_dict())


@bp.route("/train/config", methods=["GET"])
def get_configs():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 100)
    data = ModelConfig.to_collection_dict(ModelConfig.query, page, per_page, "api.get_configs")

    return jsonify(data)


@bp.route("/train/config", methods=["POST"])
def create_config():
    data = request.get_json() or {}

    if "payment_type" not in data or "segment" not in data:
        return bad_request("Must include payment type and segment fields")

    config = ModelConfig()

    try:
        config.bind(data)
    except Exception as ex:
        return bad_request(str(ex))

    try:
        db.session.add(config)
        db.session.commit()
    except Exception as ex:
        return bad_request("Unable to process request")

    response = jsonify(config.to_dict())
    response.status_code = 201

    return response


@bp.route("/train/config/<int:config_id>", methods=["DELETE"])
def delete_config(config_id):
    record = db.session.get(ModelConfig, config_id)

    if record is None:
        response = jsonify("Record is not present")
        response.status_code = 400
    else:
        db.session.delete(record)
        db.session.commit()

        response = jsonify(True)
        response.status_code = 200

    return response
