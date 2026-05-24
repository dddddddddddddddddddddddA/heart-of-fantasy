// Configuration API
const API_BASE = 'http://localhost:5000/api';

class GameAPI {
  static async newGame(playerName) {
    const response = await fetch(`${API_BASE}/new-game`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: playerName, id: `player_${Date.now()}` })
    });
    return response.json();
  }

  static async performAction(playerId, action, target = null) {
    const response = await fetch(`${API_BASE}/action`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ player_id: playerId, action, target })
    });
    return response.json();
  }

  static async getDialogue(playerId, character, choice = 0) {
    const response = await fetch(`${API_BASE}/dialogue`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ player_id: playerId, character, choice })
    });
    return response.json();
  }

  static async getStats(playerId) {
    const response = await fetch(`${API_BASE}/stats/${playerId}`);
    return response.json();
  }

  static async getAffinity(playerId) {
    const response = await fetch(`${API_BASE}/affinity/${playerId}`);
    return response.json();
  }

  static async saveGame(playerId, saveName) {
    const response = await fetch(`${API_BASE}/save`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ player_id: playerId, save_name: saveName })
    });
    return response.json();
  }

  static async loadGame(playerId, saveName) {
    const response = await fetch(`${API_BASE}/load`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ player_id: playerId, save_name: saveName })
    });
    return response.json();
  }

  static async getCharacters() {
    const response = await fetch(`${API_BASE}/characters`);
    return response.json();
  }

  static async getQuests(playerId) {
    const response = await fetch(`${API_BASE}/quests/${playerId}`);
    return response.json();
  }
}
