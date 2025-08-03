from flask import Blueprint

card_bp = Blueprint("card_bp", __name__, url_prefix="/deck/<deck_id>/card")

@card_bp.route("/<card_id>")
def get_card(card_id):
    return card_id
