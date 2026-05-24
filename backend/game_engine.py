import json
import os
from datetime import datetime
from .characters import CharacterManager
from .dialogue_system import DialogueSystem
from .affinity_system import AffinitySystem
from .quests import QuestSystem

class GameEngine:
    def __init__(self):
        self.character_manager = CharacterManager()
        self.dialogue_system = DialogueSystem()
        self.affinity_system = AffinitySystem()
        self.quest_system = QuestSystem()
        self.load_data()
    
    def load_data(self):
        """Charger les données du jeu"""
        with open('data/characters.json', 'r', encoding='utf-8') as f:
            self.characters_data = json.load(f)
        
        with open('data/dialogues.json', 'r', encoding='utf-8') as f:
            self.dialogues_data = json.load(f)
        
        with open('data/quests.json', 'r', encoding='utf-8') as f:
            self.quests_data = json.load(f)
    
    def create_new_game(self, player_name):
        """Créer une nouvelle partie"""
        game_state = {
            'player': {
                'name': player_name,
                'level': 1,
                'experience': 0,
                'health': 100,
                'max_health': 100,
                'gold': 100,
                'location': 'village_center'
            },
            'affinities': {char['id']: 10 for char in self.characters_data['characters']},
            'completed_quests': [],
            'active_quests': [],
            'inventory': [],
            'time': {'day': 1, 'hour': 12},
            'created_at': datetime.now().isoformat(),
            'last_saved': datetime.now().isoformat()
        }
        return game_state
    
    def process_action(self, game_state, action, target=None):
        """Traiter une action du joueur"""
        result = {
            'success': True,
            'message': '',
            'new_state': game_state
        }
        
        if action == 'explore':
            result['message'] = f"Vous explorez {target}..."
            game_state['player']['location'] = target
            game_state['time']['hour'] += 1
        
        elif action == 'rest':
            result['message'] = "Vous vous reposez..."
            game_state['player']['health'] = game_state['player']['max_health']
            game_state['time']['hour'] += 8
        
        elif action == 'speak':
            result['message'] = f"Vous parlez à {target}..."
            result['dialogue'] = self.get_dialogue(game_state, target)
        
        game_state['last_saved'] = datetime.now().isoformat()
        result['new_state'] = game_state
        
        return result
    
    def get_dialogue(self, game_state, character_name, choice=0):
        """Obtenir un dialogue avec un personnage"""
        affinity = game_state['affinities'].get(character_name, 10)
        
        # Trouver le personnage
        character = None
        for char in self.characters_data['characters']:
            if char['id'] == character_name or char['name'].lower() == character_name.lower():
                character = char
                break
        
        if not character:
            return {
                'success': False,
                'message': 'Personnage non trouvé'
            }
        
        # Obtenir le dialogue approprié selon l'affinité
        dialogue_level = self.get_affinity_level(affinity)
        dialogues = self.dialogues_data.get(character_name, {}).get(dialogue_level, [])
        
        if not dialogues:
            dialogues = self.dialogues_data.get(character_name, {}).get('base', [])
        
        if choice >= len(dialogues):
            choice = 0
        
        selected_dialogue = dialogues[choice] if dialogues else {'text': 'Hmm...', 'options': []}
        
        return {
            'success': True,
            'character': character['name'],
            'affinity': affinity,
            'dialogue': selected_dialogue,
            'character_info': {
                'name': character['name'],
                'description': character['description'],
                'personality': character['personality']
            }
        }
    
    def get_affinity_level(self, affinity):
        """Obtenir le niveau d'affinité"""
        if affinity < 25:
            return 'stranger'
        elif affinity < 50:
            return 'acquaintance'
        elif affinity < 75:
            return 'friend'
        else:
            return 'lover'
    
    def modify_affinity(self, game_state, character_name, amount):
        """Modifier l'affinité avec un personnage"""
        if character_name in game_state['affinities']:
            game_state['affinities'][character_name] = max(0, min(100, 
                game_state['affinities'][character_name] + amount))
        return game_state
    
    def get_player_stats(self, game_state):
        """Obtenir les statistiques du joueur"""
        return {
            'player': game_state['player'],
            'total_affinities': sum(game_state['affinities'].values()) / len(game_state['affinities']),
            'quests_completed': len(game_state['completed_quests']),
            'time': game_state['time']
        }
    
    def get_all_affinities(self, game_state):
        """Obtenir toutes les affinités"""
        affinities = []
        for char in self.characters_data['characters']:
            affinity_value = game_state['affinities'].get(char['id'], 10)
            affinities.append({
                'character': char['name'],
                'affinity': affinity_value,
                'level': self.get_affinity_level(affinity_value)
            })
        
        return sorted(affinities, key=lambda x: x['affinity'], reverse=True)
    
    def get_available_quests(self, game_state):
        """Obtenir les quêtes disponibles"""
        quests = []
        for quest in self.quests_data['quests']:
            if quest['id'] not in game_state['completed_quests']:
                quests.append(quest)
        return quests
