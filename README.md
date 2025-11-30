# Correcteur Obsidian - Correction orthographique automatique avec IA

Système de correction orthographique intelligent pour vos notes Obsidian, utilisant CrewAI et Ollama.

## 🚀 Installation rapide

```bash
# Cloner le repo
git clone https://github.com/VOTRE-USERNAME/Correcteur-obsidian.git
cd Correcteur-obsidian

# Lancer le setup automatique
./setup.sh
```

Le script `setup.sh` va automatiquement:
- ✅ Détecter et configurer Python 3.10-3.13
- ✅ Créer l'environnement virtuel
- ✅ Installer toutes les dépendances
- ✅ Vérifier et configurer Ollama
- ✅ Configurer le fichier `.env`
- ✅ Lancer les tests

**C'est tout!** Le système sera prêt à utiliser. 🎉

## Caractéristiques

- **Architecture multi-agent** avec séparation des responsabilités:
  - 🔍 **Agent Chercheur**: Explore et recherche dans vos notes
  - 🧠 **Agent Analyste**: Analyse les informations et planifie les modifications
  - ✏️ **Agent Éditeur**: Exécute les modifications sur les notes

- **Modèles dédiés** pour améliorer la fiabilité:
  - Modèle principal pour la réflexion et la coordination
  - Modèle spécialisé pour les tool calls (appels de fonctions plus précis)

- **Outils Obsidian complets**:
  - Lecture de notes
  - Écriture et modification de notes
  - Recherche de contenu
  - Listage de fichiers
  - **✨ Correction orthographique automatique** (NOUVEAU!)

- **Correction orthographique intelligente**:
  - Corrige les fautes d'orthographe et de grammaire
  - Préserve le formatage Markdown (##, liens [[]], tags #)
  - Crée des backups automatiques avant modification
  - Traitement par dossier ou note individuelle

- **Optimisé pour MacBook Air 24GB**

## Prérequis

- Python 3.10 ou supérieur
- Ollama installé et en cours d'exécution
- Un vault Obsidian existant

## Installation

### 1. Installer Ollama

Si ce n'est pas déjà fait, installez Ollama:

```bash
# Sur macOS
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Télécharger les modèles recommandés

Pour un MacBook Air 24GB, nous recommandons:

```bash
# Modèle principal (choisissez-en un)
ollama pull llama3.1:8b          # Recommandé - Bon équilibre
ollama pull mistral:7b           # Alternative plus légère
ollama pull qwen2.5:7b           # Excellent en français

# Pour de meilleurs tool calls (optionnel mais recommandé)
ollama pull mistral-nemo:12b     # Meilleurs tool calls, un peu plus lourd
```

**Note**: Avec 24GB de RAM, vous pouvez faire tourner confortablement des modèles 8B, et même 12B pour les tool calls.

### 3. Cloner et installer les dépendances

```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur macOS/Linux

# Installer les dépendances
pip install -r requirements.txt
```

### 4. Configuration

Créez un fichier `.env` à partir de l'exemple:

```bash
cp .env.example .env
```

Éditez le fichier `.env` et configurez:

```bash
# Chemin vers votre vault Obsidian (OBLIGATOIRE)
OBSIDIAN_VAULT_PATH=/Users/votre-nom/Documents/MonVault

# Modèles Ollama
MAIN_MODEL=llama3.1:8b        # Modèle principal
TOOL_MODEL=llama3.1:8b        # Modèle pour les tool calls
```

## Utilisation

### Lancer le système

```bash
python main.py
```

### Modes d'exécution

Le système propose deux modes:

#### 1. Mode Simple (tâches directes)

Pour des actions simples comme:
- Lire une note
- Chercher un contenu
- Lister les notes

**Exemple de demandes**:
- "Liste toutes mes notes dans le dossier Projets"
- "Recherche toutes les notes qui parlent de Python"
- "Lis le contenu de ma note Idées/projet-app.md"

#### 2. Mode Complexe (workflow complet)

Pour des tâches nécessitant analyse et modifications:
- Créer de nouvelles notes
- Modifier plusieurs notes
- Réorganiser le contenu

**Exemple de demandes**:
- "Crée une note récapitulative de tous mes projets en cours"
- "Ajoute un tag #important à toutes les notes qui contiennent 'urgent'"
- "Réorganise mes notes de meeting par date"

### ✨ Correction Orthographique (NOUVEAU!)

Un outil dédié pour corriger automatiquement les fautes d'orthographe de vos notes:

```bash
python correct_spelling.py
```

**Options disponibles:**

1. **Corriger un dossier spécifique**
   ```
   Votre choix: 1
   Dossier: Projets/MonProjet
   ```
   Corrige toutes les notes du dossier avec backup automatique.

2. **Corriger une note spécifique**
   ```
   Votre choix: 2
   Note: Meetings/2025-11-30.md
   ```
   Corrige une seule note.

3. **Corriger tout le vault** (avec double confirmation)

**Fonctionnalités:**
- ✅ Préserve le formatage Markdown (##, -, *, [[]], #)
- ✅ Backup automatique avant modification
- ✅ Ne modifie PAS le code, URLs ou noms propres
- ✅ Statistiques détaillées (corrigées/inchangées/erreurs)

**Démo rapide:**
```bash
python demo_correction.py
```
Crée une note de test avec des fautes et la corrige pour voir le système en action!

**Documentation complète:** Voir [CORRECTION_GUIDE.md](CORRECTION_GUIDE.md)

## Architecture

### Agents

1. **Chercheur** (Tool Model)
   - Explore le vault
   - Recherche des informations
   - Lit les notes pertinentes
   - Outils: Read, Search, List

2. **Analyste** (Main Model)
   - Analyse les résultats de recherche
   - Planifie les modifications
   - Détermine la meilleure approche
   - Pas d'outils directs

3. **Éditeur** (Tool Model)
   - Exécute les modifications
   - Crée de nouvelles notes
   - Respecte le format Markdown
   - Outils: Write, Read

### Pourquoi deux modèles?

L'utilisation de deux modèles séparés améliore la fiabilité:

- **Tool Model** (température 0.1): Pour les appels de fonctions précis et déterministes
- **Main Model** (température 0.7): Pour la réflexion créative et la planification

Cela réduit considérablement les erreurs dans les tool calls tout en maintenant une bonne qualité de raisonnement.

## Recommandations de modèles

### Pour MacBook Air 24GB

| Modèle | Taille | Utilisation | Avantages |
|--------|--------|-------------|-----------|
| llama3.1:8b | ~4.7GB | Polyvalent | Excellents tool calls, bon équilibre |
| mistral:7b | ~4.1GB | Léger | Rapide, consomme moins de RAM |
| qwen2.5:7b | ~4.4GB | Français | Excellent en français |
| mistral-nemo:12b | ~7GB | Tool calls | Meilleurs tool calls disponibles |

### Configurations recommandées

**Équilibre performance/qualité**:
```bash
MAIN_MODEL=llama3.1:8b
TOOL_MODEL=llama3.1:8b
```

**Meilleurs tool calls**:
```bash
MAIN_MODEL=llama3.1:8b
TOOL_MODEL=mistral-nemo:12b
```

**Optimisé français**:
```bash
MAIN_MODEL=qwen2.5:7b
TOOL_MODEL=qwen2.5:7b
```

**Performance maximale** (RAM limitée):
```bash
MAIN_MODEL=mistral:7b
TOOL_MODEL=mistral:7b
```

## Exemples d'utilisation

### Recherche simple

```
Votre choix: 1
Demande: Liste toutes les notes qui contiennent le mot "deadline"
```

### Création de note récapitulative

```
Votre choix: 2
Demande: Crée une note "Résumé hebdomadaire" qui liste tous les tasks marqués comme terminés cette semaine
```

### Réorganisation

```
Votre choix: 2
Demande: Pour toutes les notes dans le dossier "Brouillons", ajoute un header avec la date de création et déplace-les dans "Archive"
```

## Dépannage

### Ollama ne répond pas

Vérifiez qu'Ollama est en cours d'exécution:

```bash
ollama list  # Liste les modèles installés
ollama ps    # Affiche les modèles en cours d'exécution
```

Redémarrez Ollama si nécessaire:

```bash
# Arrêter
pkill ollama

# Redémarrer
ollama serve
```

### Erreurs de mémoire

Si vous obtenez des erreurs de mémoire:

1. Utilisez des modèles plus légers (7B au lieu de 8B ou 12B)
2. Fermez les autres applications
3. Vérifiez la mémoire disponible: `Activity Monitor` sur macOS

### Tool calls inconsistants

Si les agents n'utilisent pas correctement les outils:

1. Essayez `mistral-nemo:12b` comme TOOL_MODEL
2. Vérifiez que la température du tool_llm est basse (0.1)
3. Redémarrez Ollama pour nettoyer le cache

### Le vault n'est pas trouvé

Assurez-vous que le chemin dans `.env` est absolu et correct:

```bash
# Trouver le chemin absolu de votre vault
cd /path/to/your/vault
pwd
# Copiez le résultat dans OBSIDIAN_VAULT_PATH
```

## Performance et optimisation

### Utilisation mémoire typique

- llama3.1:8b: ~4.7GB RAM
- mistral-nemo:12b: ~7GB RAM
- Overhead Python/CrewAI: ~1-2GB

**Total attendu**: 6-10GB avec les deux modèles chargés

### Conseils d'optimisation

1. **Un seul modèle actif**: Utilisez le même modèle pour MAIN_MODEL et TOOL_MODEL si la RAM est limitée
2. **Quantization**: Utilisez les versions quantizées (déjà par défaut avec Ollama)
3. **Batch operations**: Groupez les modifications pour réduire les appels

## Structure du projet

```
Correcteur-obsidian/
├── correct_spelling.py     # Correction orthographique
├── main_simple.py          # Interface simple
├── obsidian_tools.py       # Outils pour Obsidian
├── agents_config.py        # Configuration des agents
├── requirements.txt        # Dépendances Python
├── .env.example           # Exemple de configuration
├── .env                   # Configuration (à créer)
└── README.md              # Ce fichier
```

## Contribuer

N'hésitez pas à ouvrir des issues ou proposer des améliorations!

## Licence

MIT

## Avertissement

Ce système modifie directement vos notes Obsidian. Il est recommandé de:
1. Faire des sauvegardes régulières de votre vault
2. Utiliser un système de contrôle de version (Git) pour votre vault
3. Tester d'abord sur un vault de test

## Crédits

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Framework multi-agent
- [Ollama](https://ollama.ai/) - Modèles LLM locaux
- [Obsidian](https://obsidian.md/) - Application de notes
