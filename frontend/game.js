// État global du jeu
let gameState = {
  playerId: null,
  playerName: null,
  currentLocation: 'village_center',
  gameData: null,
  characters: []
};

// Démarrer le jeu
async function startGame() {
  const playerNameInput = document.getElementById('player-name');
  const playerName = playerNameInput.value.trim();

  if (!playerName) {
    alert('Veuillez entrer votre nom!');
    return;
  }

  try {
    const result = await GameAPI.newGame(playerName);
    gameState.playerId = result.player_id;
    gameState.playerName = playerName;
    gameState.gameData = result.game_state;

    // Charger les personnages
    const charactersResult = await GameAPI.getCharacters();
    gameState.characters = charactersResult.characters || [];

    showScreen('game-screen');
    updateGameUI();
  } catch (error) {
    console.error('Erreur:', error);
    alert('Erreur lors du démarrage du jeu');
  }
}

// Afficher un écran
function showScreen(screenId) {
  document.querySelectorAll('.screen').forEach(screen => {
    screen.classList.remove('active');
  });
  document.getElementById(screenId).classList.add('active');
}

// Mettre à jour l'interface du jeu
async function updateGameUI() {
  // Mettre à jour les infos du joueur
  document.getElementById('player-name-display').textContent = gameState.playerName;
  document.getElementById('player-level').textContent = gameState.gameData.player.level;
  document.getElementById('player-gold').textContent = gameState.gameData.player.gold;
  document.getElementById('day').textContent = gameState.gameData.time.day;
  document.getElementById('hour').textContent = gameState.gameData.time.hour;

  // Mettre à jour les affinités
  await updateAffinities();

  // Afficher les personnages
  displayCharacters();
}

// Mettre à jour les affinités
async function updateAffinities() {
  try {
    const affinities = await GameAPI.getAffinity(gameState.playerId);
    const panel = document.getElementById('affinities-panel');
    panel.innerHTML = '';

    affinities.slice(0, 10).forEach(aff => {
      const item = document.createElement('div');
      item.className = 'affinity-item';
      item.innerHTML = `
        <span class="affinity-name">${aff.character}</span>
        <span class="affinity-value">${aff.affinity}/100</span>
      `;
      panel.appendChild(item);
    });
  } catch (error) {
    console.error('Erreur affinity:', error);
  }
}

// Afficher les personnages disponibles
function displayCharacters() {
  const charactersList = document.getElementById('characters-list');
  charactersList.innerHTML = '';

  gameState.characters.slice(0, 8).forEach(character => {
    const card = document.createElement('div');
    card.className = 'character-card';
    card.onclick = () => openDialogue(character.id);
    card.innerHTML = `
      <h4>${character.name}</h4>
      <p>${character.title}</p>
    `;
    charactersList.appendChild(card);
  });
}

// Ouvrir le dialogue avec un personnage
async function openDialogue(characterId) {
  try {
    const result = await GameAPI.getDialogue(gameState.playerId, characterId);
    if (result.success) {
      showScreen('dialogue-screen');
      displayDialogue(result);
    }
  } catch (error) {
    console.error('Erreur dialogue:', error);
  }
}

// Afficher le dialogue
function displayDialogue(dialogueData) {
  document.getElementById('character-name-display').textContent = dialogueData.character;
  document.getElementById('main-dialogue-text').innerHTML = dialogueData.dialogue.text;

  // Afficher la barre d'affinité
  const affinity = dialogueData.affinity;
  const affinityBar = document.getElementById('affinity-bar');
  const percentage = (affinity / 100) * 100;
  affinityBar.innerHTML = `<div class="affinity-bar-fill" style="width: ${percentage}%"></div>`;

  // Afficher les options de dialogue
  const optionsContainer = document.getElementById('main-dialogue-options');
  optionsContainer.innerHTML = '';
  dialogueData.dialogue.options.forEach((option, index) => {
    const button = document.createElement('button');
    button.textContent = option.text;
    button.onclick = () => selectDialogueOption(index);
    optionsContainer.appendChild(button);
  });
}

// Sélectionner une option de dialogue
function selectDialogueOption(optionIndex) {
  // Fermer le dialogue et mettre à jour l'affinité
  closeDialogue();
}

// Fermer le dialogue
function closeDialogue() {
  showScreen('game-screen');
}

// Explorer un lieu
async function explore(location) {
  try {
    const result = await GameAPI.performAction(gameState.playerId, 'explore', location);
    gameState.gameData = result.new_state;
    updateGameUI();
  } catch (error) {
    console.error('Erreur exploration:', error);
  }
}

// Voir les quêtes
async function viewQuests() {
  try {
    const quests = await GameAPI.getQuests(gameState.playerId);
    const questsList = document.getElementById('quests-list');
    questsList.innerHTML = '';

    quests.forEach(quest => {
      const card = document.createElement('div');
      card.className = 'quest-card';
      card.innerHTML = `
        <h4>${quest.title}</h4>
        <p>${quest.description}</p>
        <span class="quest-reward">Récompense: ${quest.reward_gold} or, +${quest.affinity_gain} affinité</span>
      `;
      questsList.appendChild(card);
    });

    showScreen('quests-screen');
  } catch (error) {
    console.error('Erreur quêtes:', error);
  }
}

// Fermer les quêtes
function closeQuests() {
  showScreen('game-screen');
}

// Sauvegarder le jeu
async function saveGame() {
  const saveName = prompt('Nom de la sauvegarde:');
  if (!saveName) return;

  try {
    const result = await GameAPI.saveGame(gameState.playerId, saveName);
    if (result.success) {
      alert(`Jeu sauvegardé: ${saveName}`);
    }
  } catch (error) {
    console.error('Erreur sauvegarde:', error);
    alert('Erreur lors de la sauvegarde');
  }
}

// Charger le jeu
async function loadGame() {
  const saveName = prompt('Nom de la sauvegarde à charger:');
  if (!saveName) return;

  try {
    const result = await GameAPI.loadGame(gameState.playerId, saveName);
    if (result.success) {
      gameState.gameData = result.game_state;
      updateGameUI();
      alert('Jeu chargé!');
    }
  } catch (error) {
    console.error('Erreur chargement:', error);
    alert('Erreur lors du chargement');
  }
}

// Retour au menu
function mainMenu() {
  if (confirm('Êtes-vous sûr? Votre progression actuelle sera perdue.')) {
    showScreen('welcome-screen');
    gameState = { playerId: null, playerName: null, currentLocation: 'village_center', gameData: null, characters: [] };
  }
}

// Initialiser au chargement
document.addEventListener('DOMContentLoaded', () => {
  showScreen('welcome-screen');
});
