import json

class CharacterManager:
    def __init__(self):
        self.characters = self.load_characters()
    
    def load_characters(self):
        """Charger les personnages depuis le fichier JSON"""
        try:
            with open('data/characters.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('characters', [])
        except:
            return []
    
    def get_character(self, character_id):
        """Obtenir un personnage par son ID"""
        for char in self.characters:
            if char['id'] == character_id:
                return char
        return None
    
    def get_all_characters(self):
        """Obtenir tous les personnages"""
        return self.characters
    
    def get_character_description(self, character_id):
        """Obtenir la description détaillée d'un personnage"""
        char = self.get_character(character_id)
        if char:
            return {
                'name': char['name'],
                'description': char['description'],
                'personality': char['personality'],
                'backstory': char.get('backstory', ''),
                'likes': char.get('likes', []),
                'dislikes': char.get('dislikes', [])
            }
        return None
    
    def get_characters_by_location(self, location):
        """Obtenir les personnages à un lieu spécifique"""
        return [char for char in self.characters if char.get('location') == location]
