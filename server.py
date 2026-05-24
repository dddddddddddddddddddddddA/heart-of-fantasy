from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import os
from datetime import datetime
from backend.game_engine import GameEngine
from backend.save_system import SaveSystem

app = Flask(__name__)
app.secret_key = 'heart_of_fantasy_secret_key_2024'
CORS(app)

# Initialiser le moteur de jeu
game_engine = GameEngine()
save_system = SaveSystem()

# Stocker les sessions de jeu
game_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/new-game', methods=['POST'])
def new_game():
    data = request.json
    player_name = data.get('name', 'Héros')
    player_id = data.get('id', f"player_{datetime.now().timestamp()}")
    
    # Créer une nouvelle session de jeu
    game_state = game_engine.create_new_game(player_name)
    game_sessions[player_id] = game_state
    
    return jsonify({
        'success': True,
        'player_id': player_id,
        'game_state': game_state
    })

@app.route('/api/action', methods=['POST'])
def perform_action():
    data = request.json
    player_id = data.get('player_id')
    action = data.get('action')
    target = data.get('target')
    
    if player_id not in game_sessions:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    game_state = game_sessions[player_id]
    result = game_engine.process_action(game_state, action, target)
    
    game_sessions[player_id] = result['new_state']
    
    return jsonify(result)

@app.route('/api/dialogue', methods=['POST'])
def dialogue():
    data = request.json
    player_id = data.get('player_id')
    character_name = data.get('character')
    choice = data.get('choice', 0)
    
    if player_id not in game_sessions:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    game_state = game_sessions[player_id]
    result = game_engine.get_dialogue(game_state, character_name, choice)
    
    return jsonify(result)

@app.route('/api/stats/<player_id>', methods=['GET'])
def get_stats(player_id):
    if player_id not in game_sessions:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    game_state = game_sessions[player_id]
    stats = game_engine.get_player_stats(game_state)
    
    return jsonify(stats)

@app.route('/api/affinity/<player_id>', methods=['GET'])
def get_affinity(player_id):
    if player_id not in game_sessions:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    game_state = game_sessions[player_id]
    affinities = game_engine.get_all_affinities(game_state)
    
    return jsonify(affinities)

@app.route('/api/save', methods=['POST'])
def save_game():
    data = request.json
    player_id = data.get('player_id')
    save_name = data.get('save_name', f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    if player_id not in game_sessions:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    game_state = game_sessions[player_id]
    success = save_system.save_game(player_id, game_state, save_name)
    
    return jsonify({'success': success, 'save_name': save_name})

@app.route('/api/load', methods=['POST'])
def load_game():
    data = request.json
    player_id = data.get('player_id')
    save_name = data.get('save_name')
    
    game_state = save_system.load_game(save_name)
    
    if game_state:
        game_sessions[player_id] = game_state
        return jsonify({'success': True, 'game_state': game_state})
    else:
        return jsonify({'success': False, 'error': 'Save not found'}), 404

@app.route('/api/characters', methods=['GET'])
def get_characters():
    with open('data/characters.json', 'r', encoding='utf-8') as f:
        characters = json.load(f)
    return jsonify(characters)

@app.route('/api/quests/<player_id>', methods=['GET'])
def get_quests(player_id):
    if player_id not in game_sessions:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    game_state = game_sessions[player_id]
    quests = game_engine.get_available_quests(game_state)
    
    return jsonify(quests)

if __name__ == '__main__':
    os.makedirs('saves', exist_ok=True)
    app.run(debug=True, port=5000)
