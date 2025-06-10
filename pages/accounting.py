from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp_accounting.db'
db = SQLAlchemy(app)

# 모델: 거래 (Journal Entry)
class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    account = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    debit = db.Column(db.Float, default=0.0)
    credit = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "account": self.account,
            "description": self.description,
            "debit": self.debit,
            "credit": self.credit
        }

@app.route('/api/journal', methods=['GET'])
def get_entries():
    entries = JournalEntry.query.all()
    return jsonify([entry.to_dict() for entry in entries])

@app.route('/api/journal', methods=['POST'])
def add_entry():
    data = request.json
    new_entry = JournalEntry(
        date=datetime.fromisoformat(data['date']),
        account=data['account'],
        description=data['description'],
        debit=data['debit'],
        credit=data['credit']
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.to_dict()), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
