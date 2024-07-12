from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.model import db, JournalEntry

entries_bp = Blueprint('entries', __name__)


@entries_bp.route('/', methods=['GET', 'POST'])
@jwt_required()
def entries():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        data = request.get_json()
        journal = JournalEntry.query.filter_by(title=data['title']).first()
        if journal:
            return jsonify({'message': 'Journal already exist'}), 409
        new_entry = JournalEntry(
            user_id=user_id,
            title=data['title'],
            content=data['content'],
            category=data['category']
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'message': 'Entry created successfully'}), 201
    entries = JournalEntry.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': e.id, 'title': e.title, 'category': e.category, 'content': e.content, 'created_at': e.created_at} for e in entries]), 200


@entries_bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def entry(id):
    user_id = get_jwt_identity()
    entry = JournalEntry.query.get_or_404(id)
    if entry.user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    if request.method == 'GET':
        return jsonify({'title': entry.title, 'content': entry.content, 'category': entry.category, 'created_at': entry.created_at}), 200
    if request.method == 'PUT':
        data = request.get_json()
        entry.title = data['title']
        entry.content = data['content']
        entry.category = data['category']
        db.session.commit()
        return jsonify({'message': 'Entry updated successfully'}), 200
    if request.method == 'DELETE':
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'message': 'Entry deleted successfully'}), 200
