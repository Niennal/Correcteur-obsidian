# Guide de démarrage rapide

## État actuel

Le système est installé avec **Python 3.12** et **CrewAI 0.11.2** (version compatible).

## Prochaines étapes

### 1. Vérifier qu'Ollama fonctionne

```bash
# Vérifier qu'Ollama est lancé
ollama list

# Si ollama n'est pas lancé, démarrez-le
ollama serve
```

### 2. Installer le modèle llama3.1:8b

```bash
ollama pull llama3.1:8b
```

### 3. Configurer votre vault Obsidian

Éditez le fichier `.env`:

```bash
nano .env
```

Modifiez cette ligne avec le chemin vers votre vault:
```
OBSIDIAN_VAULT_PATH=/Users/votre-nom/chemin/vers/votre/vault
```

### 4. Tester le système

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Tester les imports
python test_simple.py
```

### 5. Utiliser le système

```bash
# Version simplifiée (recommandée pour commencer)
python main_simple.py
```

## Fonctionnalités disponibles

La version actuelle (`main_simple.py`) vous permet de:

1. **Lister** toutes les notes de votre vault
2. **Rechercher** du texte dans vos notes
3. **Lire** le contenu d'une note
4. **Créer/Modifier** des notes

## Dépannage

### Ollama ne répond pas

```bash
# Vérifier si Ollama tourne
curl http://localhost:11434/api/version

# Si ça ne répond pas, lancez:
ollama serve
```

### Le modèle n'est pas trouvé

```bash
# Lister les modèles installés
ollama list

# Installer llama3.1:8b si absent
ollama pull llama3.1:8b
```

### Erreur "vault not found"

Vérifiez que le chemin dans `.env` est correct:
```bash
# Voir le contenu de .env
cat .env

# Vérifier que le dossier existe
ls -la /chemin/vers/votre/vault
```

## Version multi-agent (avancé)

Le fichier `main.py` contient une version plus complexe avec plusieurs agents qui collaborent.

Cette version nécessite des ajustements supplémentaires pour fonctionner avec CrewAI 0.11.2.

Pour l'instant, utilisez `main_simple.py` qui fonctionne de manière fiable.

## Architecture technique

### Versions installées:
- Python: 3.12.12
- CrewAI: 0.11.2
- Langchain: 0.1.20
- Ollama (package Python): 0.6.1

### Pourquoi ces versions?

CrewAI a changé significativement entre les versions. La version 0.11.2 est stable mais nécessite:
- Python <=3.13 (pas 3.14)
- Langchain <0.2.0
- Une approche simplifiée pour les outils personnalisés

### Améliorations futures

Pour utiliser les dernières versions de CrewAI (1.x+), il faudrait:
1. Recréer le venv avec Python 3.12 ou 3.13
2. Réinstaller CrewAI 1.x
3. Réécrire les outils Obsidian avec la nouvelle API

Pour l'instant, la version actuelle fonctionne bien pour:
- Gérer vos notes
- Rechercher du contenu
- Automatiser des tâches simples

## Exemples d'utilisation

### Rechercher toutes les notes sur un projet

1. Lancez `python main_simple.py`
2. Choisissez option 2 (Rechercher)
3. Entrez "nom-du-projet"
4. Consultez les résultats

### Créer une note quotidienne

1. Lancez `python main_simple.py`
2. Choisissez option 4 (Créer/Modifier)
3. Entrez le chemin: `Daily/2025-11-30.md`
4. Entrez votre contenu
5. Terminez par une ligne vide

### Lister toutes les notes d'un dossier

1. Lancez `python main_simple.py`
2. Choisissez option 1 (Lister)
3. Entrez le nom du dossier (ex: "Projets")
4. Consultez la liste

## Support

Si vous rencontrez des problèmes:
1. Vérifiez qu'Ollama fonctionne: `ollama list`
2. Vérifiez le fichier `.env`
3. Activez bien le venv: `source venv/bin/activate`
4. Testez avec: `python test_simple.py`
