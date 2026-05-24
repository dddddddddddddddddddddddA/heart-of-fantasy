import json
import random

class DialogueSystem:
    def __init__(self):
        self.dialogues = self.load_dialogues()
    
    def load_dialogues(self):
        """Charger les dialogues depuis le fichier JSON"""
        try:
            with open('data/dialogues.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except:
            return {}
    
    def get_dialogue_chain(self, character_id, affinity_level):
        """Obtenir une chaîne de dialogue pour un personnage"""
        if character_id not in self.dialogues:
            return self.get_default_dialogue()
        
        char_dialogues = self.dialogues[character_id]
        
        if affinity_level in char_dialogues:
            return random.choice(char_dialogues[affinity_level])
        else:
            return random.choice(char_dialogues.get('base', [self.get_default_dialogue()]))
    
    def get_default_dialogue(self):
        """Obtenir un dialogue par défaut"""
        return {
            'text': "Je ne suis pas sûr de quoi parler en ce moment...",
            'options': [
                {'text': 'Revenir', 'affinity_change': 0},
                {'text': 'Continuer', 'affinity_change': 1}
            ]
        }
    
    def get_response(self, character_id, option_index, affinity):
        """Obtenir une réponse basée sur le choix du joueur"""
        dialogue = self.get_dialogue_chain(character_id, affinity)
        
        if option_index < len(dialogue.get('options', [])):
            option = dialogue['options'][option_index]
            return {
                'response': option.get('response', 'Ils sourient mystérieusement...'),
                'affinity_change': option.get('affinity_change', 0)
            }
        
        return {'response': 'Hmm...', 'affinity_change': 0}
