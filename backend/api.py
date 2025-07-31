from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


# --- Dummy store HP & players data ---
players = {
    "player1": {"name": "Alice", "hp": 100},
    "player2": {"name": "Bob", "hp": 100},
    "player3": {"name": "Charlie", "hp": 100}
}


viewed_players = {}  # Global variable to store viewed players


@app.route('/players')
def get_players():
    address = request.args.get('address')
    if address in players:
        viewed_players[address] = players[address]  # Store in dictionary
        return jsonify(viewed_players)
    else:
        return jsonify({"error": "Player not found"}), 404


@app.route('/allPlayers', methods=['GET'])
def get_all_players():
    return jsonify(players)


@app.route('/viewedPlayers', methods=['GET'])
def get_viewed_players():
    return jsonify(viewed_players.get('viewed_players', {}))


@app.route('/resetViewedPlayers', methods=['POST'])
def reset_viewed_players():
    global viewed_players
    viewed_players = {}
    return jsonify({"message": "Viewed players reset successfully"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
