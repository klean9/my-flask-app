from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Advice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    language = db.Column(db.String(50), nullable=False, default='kz')

@app.route('/advices', methods=['GET'])
def get_advices():
    advices = Advice.query.all()
    return jsonify([{'id': advice.id, 'text': advice.text, 'language': advice.language} for advice in advices])

@app.route('/advice', methods=['POST'])
def add_advice():
    data = request.get_json()
    new_advice = Advice(text=data['text'], language=data.get('language', 'kz'))
    db.session.add(new_advice)
    db.session.commit()
    return jsonify({'message': 'Advice added successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
