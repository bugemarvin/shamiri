from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.model import db, JournalEntry
from datetime import datetime

summaries_bp = Blueprint('summaries', __name__)

@summaries_bp.route('/daily', methods=['GET'])
@jwt_required()
def daily_summary():
    user_id = get_jwt_identity()
    today = datetime.now().date()
    entries = JournalEntry.query.filter(
        JournalEntry.user_id == user_id,
        db.func.date(JournalEntry.created_at) == today
    ).all()
    return jsonify({'count': len(entries), 'entries': [{'id': e.id, 'title': e.title} for e in entries]}), 200

@summaries_bp.route('/monthly', methods=['GET'])
@jwt_required()
def monthly_summary():
    user_id = get_jwt_identity()
    first_day_of_month = datetime.now().replace(day=1)
    entries = JournalEntry.query.filter(
        JournalEntry.user_id == user_id,
        JournalEntry.created_at >= first_day_of_month
    ).all()
    return jsonify({'count': len(entries), 'entries': [{'id': e.id, 'title': e.title} for e in entries]}), 200
