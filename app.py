from flask import Flask, jsonify, request

# Create Flask app instance
app = Flask(__name__)

# Sample data (in real apps, this would be a database)
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

# GET endpoint - retrieve all users
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET endpoint - retrieve specific user by ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# POST endpoint - create new user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Basic validation
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400
    
    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    
    return jsonify(new_user), 201

# PUT endpoint - update existing user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Update user fields
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    
    return jsonify(user)

# DELETE endpoint - remove user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    users.remove(user)
    return jsonify({"message": "User deleted successfully"})

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

# Error handler for 500
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)