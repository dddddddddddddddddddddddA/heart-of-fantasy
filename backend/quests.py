import json

class QuestSystem:
    def __init__(self):
        self.quests = self.load_quests()
    
    def load_quests(self):
        """Charger les quêtes depuis le fichier JSON"""
        try:
            with open('data/quests.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('quests', [])
        except:
            return []
    
    def get_quests_for_character(self, character_id):
        """Obtenir les quêtes pour un personnage spécifique"""
        return [q for q in self.quests if q.get('character_id') == character_id]
    
    def get_quest(self, quest_id):
        """Obtenir une quête par son ID"""
        for quest in self.quests:
            if quest['id'] == quest_id:
                return quest
        return None
    
    def complete_quest(self, quest_id):
        """Marquer une quête comme complétée"""
        quest = self.get_quest(quest_id)
        if quest:
            return {
                'success': True,
                'reward_gold': quest.get('reward_gold', 0),
                'affinity_gain': quest.get('affinity_gain', 5),
                'message': f"Quête complétée : {quest['title']}"
            }
        return {'success': False}
