class AffinitySystem:
    def __init__(self):
        self.max_affinity = 100
        self.min_affinity = 0
    
    def increase_affinity(self, current_affinity, amount):
        """Augmenter l'affinité"""
        return min(self.max_affinity, current_affinity + amount)
    
    def decrease_affinity(self, current_affinity, amount):
        """Diminuer l'affinité"""
        return max(self.min_affinity, current_affinity - amount)
    
    def get_affinity_level(self, affinity):
        """Obtenir le niveau d'affinité textuel"""
        if affinity < 25:
            return 'Stranger'
        elif affinity < 50:
            return 'Acquaintance'
        elif affinity < 75:
            return 'Friend'
        elif affinity < 90:
            return 'Close Friend'
        else:
            return 'Lover'
    
    def get_affinity_color(self, affinity):
        """Obtenir une couleur pour l'affinity"""
        if affinity < 25:
            return '#808080'  # Gris
        elif affinity < 50:
            return '#0099FF'  # Bleu
        elif affinity < 75:
            return '#00FF00'  # Vert
        elif affinity < 90:
            return '#FF9900'  # Orange
        else:
            return '#FF0000'  # Rouge (amour)
    
    def should_unlock_special_quest(self, affinity):
        """Vérifier si une quête spéciale doit être débloquée"""
        return affinity >= 75
    
    def should_unlock_romantic_ending(self, affinity):
        """Vérifier si une fin romantique doit être débloquée"""
        return affinity >= 90
