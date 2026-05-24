import json
import os
from datetime import datetime

class SaveSystem:
    def __init__(self):
        self.save_dir = 'saves'
        os.makedirs(self.save_dir, exist_ok=True)
    
    def save_game(self, player_id, game_state, save_name):
        """Sauvegarder l'état du jeu"""
        try:
            save_file = os.path.join(self.save_dir, f"{save_name}.json")
            save_data = {
                'player_id': player_id,
                'game_state': game_state,
                'saved_at': datetime.now().isoformat()
            }
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur de sauvegarde: {e}")
            return False
    
    def load_game(self, save_name):
        """Charger une sauvegarde"""
        try:
            save_file = os.path.join(self.save_dir, f"{save_name}.json")
            if not os.path.exists(save_file):
                return None
            
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            return save_data['game_state']
        except Exception as e:
            print(f"Erreur de chargement: {e}")
            return None
    
    def list_saves(self, player_id=None):
        """Lister toutes les sauvegardes"""
        saves = []
        for filename in os.listdir(self.save_dir):
            if filename.endswith('.json'):
                save_name = filename[:-5]
                saves.append(save_name)
        return saves
    
    def delete_save(self, save_name):
        """Supprimer une sauvegarde"""
        try:
            save_file = os.path.join(self.save_dir, f"{save_name}.json")
            if os.path.exists(save_file):
                os.remove(save_file)
                return True
        except Exception as e:
            print(f"Erreur de suppression: {e}")
        return False
