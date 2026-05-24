"""
Heart of Fantasy - Game Engine
Moteur principal du jeu RPG textuel romantique
"""

import json
from typing import Dict, List, Any
from datetime import datetime
from characters import Character, CharacterManager
from dialogue_system import DialogueSystem
from affinity_system import AffinitySystem
from quests import QuestManager
from save_system import SaveSystem


class GameEngine:
    """Moteur principal du jeu"""
    
    def __init__(self):
        self.player = None
        self.character_manager = CharacterManager()
        self.dialogue_system = DialogueSystem()
        self.affinity_system = AffinitySystem()
        self.quest_manager = QuestManager()
        self.save_system = SaveSystem()
        self.current_location = "tavern_of_stars"
        self.game_state = "menu"
        self.turn_count = 0
        self.playtime = 0
        
    def initialize_game(self, player_name: str) -> Dict[str, Any]:
        """Initialise une nouvelle partie"""
        self.player = {
            "name": player_name,
            "level": 1,
            "exp": 0,
            "health": 100,
            "max_health": 100,
            "gold": 50,
            "inventory": []
        }
        
        self.character_manager.load_characters()
        self.affinity_system.initialize_affinities()
        self.quest_manager.initialize_quests()
        
        self.game_state = "playing"
        return self.get_game_state()
    
    def get_game_state(self) -> Dict[str, Any]:
        """Retourne l'état actuel du jeu"""
        return {
            "player": self.player,
            "location": self.current_location,
            "turn": self.turn_count,
            "game_state": self.game_state,
            "available_characters": self.get_available_characters(),
            "current_quest": self.quest_manager.get_current_quest(),
            "affinities": self.affinity_system.get_all_affinities() if self.player else None
        }
    
    def move_to_location(self, location: str) -> Dict[str, Any]:
        """Déplace le joueur à un nouveau lieu"""
        valid_locations = [
            "tavern_of_stars",
            "crystal_forest",
            "dragon_mountains",
            "moonlight_harbor",
            "shadow_castle",
            "enchanted_library",
            "sacred_temple",
            "mystic_grove"
        ]
        
        if location not in valid_locations:
            return {"error": "Location invalide"}
        
        self.current_location = location
        self.turn_count += 1
        
        return {
            "success": True,
            "location": location,
            "description": self._get_location_description(location),
            "characters_here": self.character_manager.get_characters_in_location(location)
        }
    
    def _get_location_description(self, location: str) -> str:
        """Retourne la description d'un lieu"""
        descriptions = {
            "tavern_of_stars": "Une taverne chaleureuse où les aventuriers se réunissent. Les rires résonnent, des histoires de quêtes légendaires se racontent.",
            "crystal_forest": "Une forêt scintillante où les arbres brillent de mille couleurs. La magie flotte dans l'air.",
            "dragon_mountains": "Les pics enneigés des montagnes du dragon. Un endroit où règne la puissance et le danger.",
            "moonlight_harbor": "Un port mystérieux éclairé par la lueur de la lune. Les navires anciens y racontent des histoires oubliées.",
            "shadow_castle": "Un château ancien et énigmatique, enveloppé de mystère et de secrets.",
            "enchanted_library": "Une bibliothèque magique contenant les savoirs anciens du monde.",
            "sacred_temple": "Un temple sacré où règne la paix et la spiritualité.",
            "mystic_grove": "Un bosquet mystique où la nature et la magie s'entrelacent."
        }
        return descriptions.get(location, "Un lieu inconnu")
    
    def get_available_characters(self) -> List[str]:
        """Retourne les personnages disponibles au lieu actuel"""
        return self.character_manager.get_characters_in_location(self.current_location)
    
    def talk_to_character(self, character_id: str) -> Dict[str, Any]:
        """Lance une conversation avec un personnage"""
        character = self.character_manager.get_character(character_id)
        if not character:
            return {"error": "Personnage non trouvé"}
        
        # Récupère le dialogue basé sur l'affinité
        affinity = self.affinity_system.get_affinity(character_id)
        dialogue_options = self.dialogue_system.get_dialogue_options(
            character_id, 
            affinity
        )
        
        return {
            "character": character.to_dict(),
            "affinity": affinity,
            "dialogue_options": dialogue_options,
            "current_dialogue": self.dialogue_system.get_greeting(character_id, affinity)
        }
    
    def choose_dialogue(self, character_id: str, dialogue_id: str) -> Dict[str, Any]:
        """Le joueur choisit une option de dialogue"""
        response = self.dialogue_system.get_dialogue_response(character_id, dialogue_id)
        affinity_change = response.get("affinity_change", 0)
        
        # Mets à jour l'affinité
        self.affinity_system.add_affinity(character_id, affinity_change)
        
        self.turn_count += 1
        
        return {
            "response": response.get("text"),
            "affinity_change": affinity_change,
            "new_affinity": self.affinity_system.get_affinity(character_id),
            "unlocked_quest": response.get("unlocked_quest"),
            "romantic_scene": response.get("romantic_scene")
        }
    
    def save_game(self, save_name: str) -> Dict[str, Any]:
        """Sauvegarde la partie"""
        save_data = {
            "player": self.player,
            "location": self.current_location,
            "turn_count": self.turn_count,
            "timestamp": datetime.now().isoformat(),
            "affinities": self.affinity_system.get_all_affinities(),
            "quests": self.quest_manager.get_all_quests()
        }
        
        self.save_system.save(save_name, save_data)
        return {"success": True, "save_name": save_name}
    
    def load_game(self, save_name: str) -> Dict[str, Any]:
        """Charge une partie sauvegardée"""
        save_data = self.save_system.load(save_name)
        
        if not save_data:
            return {"error": "Sauvegarde non trouvée"}
        
        self.player = save_data["player"]
        self.current_location = save_data["location"]
        self.turn_count = save_data["turn_count"]
        self.affinity_system.load_affinities(save_data["affinities"])
        self.quest_manager.load_quests(save_data["quests"])
        
        return {"success": True, "game_state": self.get_game_state()}
    
    def end_game(self) -> Dict[str, Any]:
        """Termine la partie et calcule les résultats"""
        affinities = self.affinity_system.get_all_affinities()
        
        # Trie par affinité décroissante
        sorted_affinities = sorted(
            affinities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        romance_endings = []
        for char_id, affinity in sorted_affinities:
            if affinity >= 75:
                romance_endings.append({
                    "character": self.character_manager.get_character(char_id),
                    "affinity": affinity,
                    "ending_type": "True Love" if affinity >= 90 else "Romance"
                })
        
        return {
            "game_over": True,
            "playtime": self.turn_count,
            "romance_endings": romance_endings,
            "total_affinities": dict(sorted_affinities)
        }