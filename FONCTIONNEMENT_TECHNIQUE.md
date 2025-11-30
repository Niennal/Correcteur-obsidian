# Comment fonctionnent les scripts - Guide technique détaillé

Ce guide explique le fonctionnement interne de chaque script du projet.

## Table des matières

1. [setup.sh - Script d'installation](#setupsh---script-dinstallation)
2. [correct_spelling.py - Correction orthographique](#correct_spellingpy---correction-orthographique)
3. [obsidian_tools.py - API Obsidian](#obsidian_toolspy---api-obsidian)
4. [agents_config.py - Configuration des agents](#agents_configpy---configuration-des-agents)
5. [main_simple.py - Interface utilisateur](#main_simplepy---interface-utilisateur)
6. [Flux de données](#flux-de-données)

---

## setup.sh - Script d'installation

### Vue d'ensemble

Script Bash qui automatise l'installation complète du projet.

### Étapes détaillées

```bash
#!/bin/bash
set -e  # Arrêter en cas d'erreur
```

**`set -e`** : Si une commande échoue, tout le script s'arrête immédiatement.

### 1. Détection de Python

```bash
for cmd in python3.12 python3.13 python3.10 python3.11 python3; do
    if command -v $cmd &> /dev/null; then
        VERSION=$($cmd --version 2>&1 | awk '{print $2}')
        MAJOR=$(echo $VERSION | cut -d. -f1)
        MINOR=$(echo $VERSION | cut -d. -f2)

        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ] && [ "$MINOR" -le 13 ]; then
            PYTHON_CMD=$cmd
            break
        fi
    fi
done
```

**Comment ça marche:**
1. Boucle sur différentes commandes Python possibles (python3.12, python3.13, etc.)
2. `command -v $cmd` vérifie si la commande existe
3. Récupère la version avec `--version`
4. `awk '{print $2}'` extrait le numéro de version (ex: "3.12.5")
5. `cut -d. -f1` et `-f2` extraient la version majeure (3) et mineure (12)
6. Vérifie que c'est Python 3.10 à 3.13 (compatible CrewAI 0.11.2)
7. Dès qu'un Python valide est trouvé, on sort de la boucle

**Pourquoi ces versions?**
- CrewAI 0.11.2 nécessite Python 3.10-3.13 maximum
- Python 3.14 est trop récent et incompatible

### 2. Création du venv

```bash
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
fi
source venv/bin/activate
```

**Comment ça marche:**
1. `[ ! -d "venv" ]` vérifie si le dossier venv n'existe PAS
2. Si absent: `python3.12 -m venv venv` crée l'environnement virtuel
3. `source venv/bin/activate` active le venv

**Pourquoi un venv?**
- Isole les dépendances Python du système
- Évite les conflits de versions
- Permet plusieurs projets Python avec différentes dépendances

### 3. Installation des dépendances

```bash
pip install --quiet --upgrade pip
pip install --quiet setuptools
pip install --quiet -r requirements.txt
```

**Comment ça marche:**
1. Met à jour pip (le gestionnaire de packages Python)
2. Installe setuptools (nécessaire pour CrewAI 0.11.2)
3. Lit requirements.txt et installe chaque package listé

**Contenu de requirements.txt:**
```
crewai==0.11.2        # Framework multi-agent
crewai-tools==0.0.1   # Outils CrewAI
langchain<0.2.0       # Framework LLM (version compatible)
langchain-community   # Extensions Langchain
ollama                # Client Python pour Ollama
python-dotenv==1.0.0  # Lecture fichiers .env
pydantic>=2.0.0       # Validation de données
```

### 4. Vérification d'Ollama

```bash
if curl -s http://localhost:11434/api/version &> /dev/null; then
    echo "Ollama en cours d'exécution"
else
    echo "Ollama n'est pas lancé"
fi
```

**Comment ça marche:**
1. `curl -s http://localhost:11434/api/version` essaie de contacter l'API Ollama
2. `-s` = mode silencieux (pas d'affichage)
3. `&> /dev/null` redirige toute sortie vers le vide
4. Le code de retour détermine si Ollama répond

**Port 11434:** Port par défaut d'Ollama pour son API HTTP

### 5. Configuration .env

```bash
if [ "$OS" == "macos" ]; then
    sed -i '' "s|^OBSIDIAN_VAULT_PATH=.*|OBSIDIAN_VAULT_PATH=$VAULT_PATH|" .env
else
    sed -i "s|^OBSIDIAN_VAULT_PATH=.*|OBSIDIAN_VAULT_PATH=$VAULT_PATH|" .env
fi
```

**Comment ça marche:**
1. `sed` = Stream EDitor, pour modifier des fichiers
2. `s|pattern|replacement|` = substitution
3. `^OBSIDIAN_VAULT_PATH=.*` = ligne commençant par OBSIDIAN_VAULT_PATH=
4. Remplace par `OBSIDIAN_VAULT_PATH=$VAULT_PATH`
5. Différence macOS/Linux: macOS nécessite `''` après `-i`

---

## correct_spelling.py - Correction orthographique

### Architecture

```
SpellingCorrector
├── __init__()      # Initialise LLM et outils
├── correct_text()  # Corrige un texte via LLM
├── correct_note()  # Corrige une note complète
└── correct_folder() # Corrige un dossier entier
```

### 1. Initialisation

```python
class SpellingCorrector:
    def __init__(self, vault_path: str, model: str = "llama3.1:8b"):
        self.tools = ObsidianTools(vault_path)
        self.vault_path = Path(vault_path)

        self.llm = Ollama(
            model=model,
            base_url="http://localhost:11434",
            temperature=0.1,  # Très bas pour précision
        )
```

**Comment ça marche:**
1. Crée une instance de `ObsidianTools` pour lire/écrire les notes
2. Initialise le modèle LLM Ollama
3. **Temperature 0.1** = mode déterministe
   - Plus la température est basse, plus les réponses sont prévisibles
   - Pour la correction, on veut de la précision, pas de la créativité

**Température expliquée:**
- 0.0 = Toujours la même réponse (déterministe)
- 0.1 = Très peu de variation (idéal pour correction)
- 0.7 = Équilibré (créativité + cohérence)
- 1.0+ = Très créatif mais imprévisible

### 2. Création de backup

```python
def create_backup(self, note_path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = self.vault_path / ".backups"
    backup_dir.mkdir(exist_ok=True)

    relative_path = note_path.relative_to(self.vault_path)
    backup_path = backup_dir / f"{relative_path.stem}_{timestamp}.md"

    shutil.copy2(note_path, backup_path)
    return backup_path
```

**Comment ça marche:**
1. `datetime.now().strftime()` génère un timestamp unique (ex: `20251130_153045`)
2. Crée le dossier `.backups/` s'il n'existe pas (`exist_ok=True` évite erreur si existe)
3. `note_path.relative_to(vault_path)` obtient le chemin relatif (ex: `Projets/note.md`)
4. `.stem` retire l'extension (ex: `note` au lieu de `note.md`)
5. `shutil.copy2()` copie le fichier en préservant les métadonnées (date de modification, etc.)

**Exemple:**
```
Original: /vault/Projets/note.md
Backup:   /vault/.backups/note_20251130_153045.md
```

### 3. Correction de texte (le coeur du système!)

```python
def correct_text(self, text: str, language: str = "français") -> str:
    prompt = f"""Tu es un correcteur orthographique expert en {language}.

RÈGLES IMPORTANTES:
1. Corrige UNIQUEMENT les fautes d'orthographe, de grammaire et de ponctuation
2. Ne modifie PAS la structure Markdown (titres ##, listes -, liens [[]], tags #)
3. Ne modifie PAS le sens ou le style du texte
4. Ne modifie PAS les noms propres, les URLs ou le code
5. Conserve EXACTEMENT la même mise en forme Markdown
6. Retourne UNIQUEMENT le texte corrigé, sans explication

TEXTE À CORRIGER:
{text}

TEXTE CORRIGÉ:"""

    corrected = self.llm.invoke(prompt)
    return corrected.strip()
```

**Comment ça marche:**

1. **Construction du prompt:**
   - Le prompt est crucial! C'est l'instruction au LLM
   - On donne des RÈGLES strictes pour limiter les modifications
   - Le format "TEXTE À CORRIGER: / TEXTE CORRIGÉ:" guide le modèle

2. **self.llm.invoke(prompt):**
   - Envoie le prompt à Ollama via HTTP (localhost:11434)
   - Ollama charge le modèle en mémoire si nécessaire
   - Le modèle génère la réponse token par token
   - Retourne le texte complet

3. **.strip():**
   - Enlève les espaces/retours à la ligne en début/fin
   - Le LLM ajoute parfois des espaces inutiles

**Pourquoi ce prompt fonctionne:**
- Instructions très précises et numérotées
- Exemples négatifs ("Ne modifie PAS...")
- Format clair d'entrée/sortie
- Contexte linguistique (français)

### 4. Correction d'une note

```python
def correct_note(self, note_path: str, create_backup: bool = True) -> dict:
    full_path = self.vault_path / note_path

    # Lire le contenu original
    with open(full_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Créer backup
    if create_backup:
        backup_path = self.create_backup(full_path)

    # Corriger
    corrected_content = self.correct_text(original_content)

    # Vérifier changements
    if corrected_content == original_content:
        return {"success": True, "changes": False}

    # Écrire
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(corrected_content)

    return {"success": True, "changes": True}
```

**Flux de données:**
```
1. Lire note.md → "Aujourdhui jai travaillé..."
2. Backup → .backups/note_20251130_153045.md
3. LLM corrige → "Aujourd'hui j'ai travaillé..."
4. Comparer original vs corrigé
5. Si différent → écrire dans note.md
6. Retourner {"success": True, "changes": True}
```

**Gestion des erreurs:**
```python
try:
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(corrected_content)
except Exception as e:
    # Restaurer backup si échec
    if backup_path and backup_path.exists():
        shutil.copy2(backup_path, full_path)
    return {"success": False, "error": str(e)}
```

Si l'écriture échoue, on restaure automatiquement le backup!

### 5. Correction d'un dossier

```python
def correct_folder(self, folder: str = "", pattern: str = "*.md") -> dict:
    search_path = self.vault_path / folder if folder else self.vault_path
    notes = list(search_path.glob(f"**/{pattern}"))

    results = {
        "total": len(notes),
        "corrected": 0,
        "unchanged": 0,
        "errors": 0
    }

    for note_path in notes:
        relative_path = str(note_path.relative_to(self.vault_path))
        result = self.correct_note(relative_path)

        if result["success"] and result.get("changes"):
            results["corrected"] += 1
        elif result["success"]:
            results["unchanged"] += 1
        else:
            results["errors"] += 1

    return results
```

**Comment ça marche:**

1. **glob(f"**/{pattern}"):**
   - `**` = recherche récursive dans tous les sous-dossiers
   - `*.md` = tous les fichiers Markdown
   - Exemple: trouve `Projets/notes/test.md`, `Daily/2025-11-30.md`, etc.

2. **Boucle sur chaque note:**
   - Appelle `correct_note()` pour chacune
   - Accumule les statistiques
   - Continue même si une note échoue (pas de `raise`)

3. **Statistiques:**
   - `total`: Nombre de notes trouvées
   - `corrected`: Notes modifiées
   - `unchanged`: Notes déjà correctes
   - `errors`: Notes en erreur

---

## obsidian_tools.py - API Obsidian

### Architecture simple

```python
class ObsidianTools:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)

    def read_note(self, note_path: str) -> str:
        # Lire une note

    def write_note(self, note_path: str, content: str) -> str:
        # Écrire une note

    def list_notes(self, folder: str = "") -> str:
        # Lister les notes

    def search_notes(self, query: str) -> str:
        # Rechercher du texte
```

### 1. Lecture de note

```python
def read_note(self, note_path: str) -> str:
    full_path = self.vault_path / note_path

    if not full_path.exists():
        return f"Erreur: La note '{note_path}' n'existe pas"

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return f"Contenu de {note_path}:\n\n{content}"
```

**Path operations:**
```python
vault_path = Path("/Users/moi/vault")
note_path = "Projets/test.md"
full_path = vault_path / note_path
# Résultat: /Users/moi/vault/Projets/test.md
```

**L'opérateur `/` avec Path:**
- Concatène intelligemment les chemins
- Gère automatiquement les séparateurs (/ sur Unix, \ sur Windows)
- Plus propre que `os.path.join()`

**encoding='utf-8':**
- Crucial pour les accents français!
- UTF-8 = encodage universel pour tous les caractères

### 2. Écriture de note

```python
def write_note(self, note_path: str, content: str, append: bool = False) -> str:
    full_path = self.vault_path / note_path

    # Créer dossiers parents si nécessaire
    full_path.parent.mkdir(parents=True, exist_ok=True)

    mode = 'a' if append else 'w'
    with open(full_path, mode, encoding='utf-8') as f:
        if append and full_path.exists():
            f.write('\n\n')  # Séparateur
        f.write(content)

    return f"Succès: Contenu écrit dans {note_path}"
```

**full_path.parent.mkdir():**
```python
# Si on veut créer: /vault/Projets/Nouveau/test.md
# Mais que /vault/Projets/Nouveau n'existe pas

full_path.parent  # = /vault/Projets/Nouveau
.mkdir(parents=True, exist_ok=True)
# parents=True: crée aussi les parents (Projets, Nouveau)
# exist_ok=True: pas d'erreur si existe déjà
```

**Modes d'ouverture de fichier:**
- `'r'` = Read (lecture seule)
- `'w'` = Write (écrase tout le contenu)
- `'a'` = Append (ajoute à la fin)
- `'r+'` = Read+Write (lecture et écriture)

### 3. Recherche dans les notes

```python
def search_notes(self, query: str, folder: str = "") -> str:
    search_path = self.vault_path / folder if folder else self.vault_path
    matches = []

    for note_path in search_path.glob("**/*.md"):
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if query.lower() in content.lower():
                # Extraire contexte
                idx = content.lower().index(query.lower())
                start = max(0, idx - 50)
                end = min(len(content), idx + len(query) + 50)
                context = content[start:end].replace('\n', ' ')

                relative_path = str(note_path.relative_to(self.vault_path))
                matches.append(f"- {relative_path}\n  Contexte: ...{context}...")

    return "\n\n".join(matches)
```

**Recherche insensible à la casse:**
```python
query.lower() in content.lower()
# "Python" trouvera "python", "PYTHON", "Python"
```

**Extraction du contexte:**
```python
content = "Voici un texte Python est génial pour les scripts"
query = "Python"
idx = content.lower().index(query.lower())  # Position de "Python" = 14

start = max(0, idx - 50)      # 0 (pas avant le début)
end = min(len(content), idx + len(query) + 50)  # idx + 6 + 50

context = content[start:end]   # "Voici un texte Python est génial pour"
context.replace('\n', ' ')     # Remplace retours ligne par espaces
```

**Résultat:**
```
- Projets/web.md
  Contexte: ...ici un texte Python est génial pour...
```

---

## agents_config.py - Configuration des agents

### Concept: Deux LLM différents

```python
class ObsidianAgentsConfig:
    def __init__(self, vault_path, main_model, tool_model):
        # LLM pour réflexion (temperature haute)
        self.main_llm = Ollama(
            model=main_model,
            temperature=0.7,  # Créatif
        )

        # LLM pour tool calls (temperature basse)
        self.tool_llm = Ollama(
            model=tool_model,
            temperature=0.1,  # Précis
        )
```

**Pourquoi deux modèles?**

1. **Main LLM (temperature 0.7):**
   - Pour analyser, planifier, réfléchir
   - Besoin de créativité et de raisonnement
   - Exemple: "Quelle est la meilleure façon d'organiser ces notes?"

2. **Tool LLM (temperature 0.1):**
   - Pour appeler des fonctions précisément
   - Besoin de déterminisme
   - Exemple: Appeler `read_note("exact/path.md")` sans variation

**Le problème des tool calls:**
```python
# Avec temperature haute (0.7):
Agent: "Je vais lire la note 'projet.md'"
→ Appelle parfois read_note("projet.md")
→ Appelle parfois read_note("Projets/projet.md")
→ Inconsistant!

# Avec temperature basse (0.1):
Agent: "Je vais lire la note 'projet.md'"
→ Appelle TOUJOURS read_note("projet.md")
→ Consistant!
```

### Création d'agents

```python
def create_researcher_agent(self, tools: List) -> Agent:
    return Agent(
        role="Chercheur de notes Obsidian",
        goal="Explorer et analyser les notes",
        backstory="Tu es un expert en recherche...",
        tools=tools,
        llm=self.tool_llm,  # LLM précis pour les tools
        verbose=True,
        allow_delegation=False,
    )
```

**Paramètres Agent:**
- `role`: Le "métier" de l'agent
- `goal`: Ce qu'il doit accomplir
- `backstory`: Contexte pour influencer le comportement
- `tools`: Liste des outils disponibles
- `llm`: Quel modèle utiliser
- `verbose=True`: Affiche ce que fait l'agent
- `allow_delegation=False`: Ne peut pas déléguer à d'autres agents

**L'importance du backstory:**
```python
# Mauvais backstory:
backstory="Tu es un agent"

# Bon backstory:
backstory="""Tu es un expert en recherche d'information dans des bases de
connaissances. Tu maîtrises parfaitement la navigation dans les notes Obsidian
et tu sais comment trouver rapidement les informations pertinentes."""
```

Le backstory influence la "personnalité" et le comportement du LLM!

---

## main_simple.py - Interface utilisateur

### Menu interactif simple

```python
while True:
    print("1. Lister toutes les notes")
    print("2. Rechercher dans les notes")
    print("3. Lire une note")
    print("4. Créer/Modifier une note")
    print("5. Quitter")

    choice = input("Votre choix: ").strip()

    if choice == "1":
        folder = input("Dossier: ").strip()
        result = tools.list_notes(folder=folder)
        print(result)
```

**`.strip()`:**
```python
input("Nom: ")  # Si user tape "  test  \n"
→ "  test  \n"

input("Nom: ").strip()  # Enlève espaces et \n
→ "test"
```

Toujours utiliser `.strip()` sur les inputs utilisateur!

---

## Flux de données - Exemple complet

### Scénario: Corriger toutes les notes du dossier "Projets"

```
1. UTILISATEUR
   └─> Lance: python correct_spelling.py
   └─> Choisit: 1 (Corriger un dossier)
   └─> Entre: "Projets"

2. correct_spelling.py
   └─> SpellingCorrector.__init__()
       ├─> ObsidianTools("/vault")
       └─> Ollama("llama3.1:8b", temp=0.1)

3. correct_folder("Projets")
   └─> glob("Projets/**/*.md")
       ├─> Trouve: Projets/web.md
       ├─> Trouve: Projets/app.md
       └─> Trouve: Projets/todo.md

4. Pour chaque note:

   correct_note("Projets/web.md")
   ├─> create_backup()
   │   └─> Copie vers .backups/web_20251130_153045.md
   │
   ├─> read()
   │   └─> "Aujourdhui jai travaillé sur le site web..."
   │
   ├─> correct_text()
   │   ├─> Construit prompt avec règles
   │   ├─> Envoie à Ollama (HTTP localhost:11434)
   │   │   ├─> Ollama charge llama3.1:8b en RAM
   │   │   ├─> Génère token par token
   │   │   └─> "Aujourd'hui j'ai travaillé sur le site web..."
   │   └─> Retourne texte corrigé
   │
   ├─> Compare original vs corrigé
   │   └─> Différent! changes=True
   │
   └─> write()
       └─> Écrit dans Projets/web.md

5. RÉSULTAT
   ├─> Total: 3 notes
   ├─> Corrigées: 2
   ├─> Inchangées: 1
   └─> Erreurs: 0
```

### Communication avec Ollama (détails techniques)

```python
# Quand on fait:
self.llm.invoke(prompt)

# En arrière-plan:
1. Client Python crée requête HTTP POST
   └─> URL: http://localhost:11434/api/generate
   └─> Body: {"model": "llama3.1:8b", "prompt": "..."}

2. Ollama reçoit requête
   └─> Charge modèle en RAM si pas déjà chargé
   └─> Tokenize le prompt
   └─> Passe les tokens au modèle neural

3. Modèle génère réponse
   └─> Token par token (pas tout d'un coup!)
   └─> "Aujourd" → "'hui" → " j" → "'" → "ai" ...

4. Ollama retourne réponse
   └─> HTTP Response: {"response": "Aujourd'hui j'ai..."}

5. Client Python parse JSON
   └─> Retourne juste le texte
```

### Mémoire et performance

**Utilisation RAM typique:**
```
llama3.1:8b chargé en RAM:
├─> Modèle: ~4.7 GB
├─> Contexte (prompt): ~100-500 MB
└─> Total: ~5-6 GB

Python + environnement:
├─> Venv: ~500 MB
├─> Imports: ~200 MB
└─> Total: ~700 MB

TOTAL: ~6-7 GB pour une correction
```

**Pourquoi c'est rapide après le premier appel?**
- Ollama garde le modèle en RAM
- Pas de rechargement nécessaire
- Premier appel: ~10 secondes (chargement)
- Appels suivants: ~2-3 secondes (juste inférence)

---

## Questions/Réponses techniques

### Q: Pourquoi Python 3.12 et pas 3.14?

**R:** CrewAI 0.11.2 a été compilé pour Python ≤3.13. Python 3.14 a changé des APIs internes que CrewAI 0.11.2 utilise.

### Q: Pourquoi langchain<0.2.0?

**R:** CrewAI 0.11.2 dépend de l'ancienne API de Langchain 0.1.x. Langchain 0.2+ a cassé la compatibilité.

### Q: Comment Ollama sait quel modèle utiliser?

**R:**
```python
Ollama(model="llama3.1:8b")
# Cherche dans ~/.ollama/models/
# Si trouvé → charge
# Si absent → erreur
```

### Q: Que fait temperature exactement?

**R:**
Temperature contrôle le "sampling" (échantillonnage):

```python
# Modèle calcule probabilités pour chaque token:
Prochain token possible:
- "le": 40%
- "la": 30%
- "les": 20%
- "un": 10%

# Temperature 0.1 (bas):
→ Prend presque toujours "le" (40%)
→ Très prévisible

# Temperature 0.7 (moyen):
→ "le" 50% du temps
→ "la" 30% du temps
→ "les" 15% du temps
→ "un" 5% du temps
→ Varié mais cohérent

# Temperature 1.5 (haut):
→ Chances quasi égales
→ Très créatif mais risque incohérence
```

### Q: Pourquoi glob("**/*.md") et pas os.listdir()?

**R:**
```python
# os.listdir() - basique
for file in os.listdir("folder"):
    if file.endswith(".md"):
        # Traiter fichier
# ❌ Ne cherche PAS dans les sous-dossiers

# glob("**/*.md") - récursif
for file in glob("**/*.md"):
    # Traiter fichier
# ✅ Cherche dans TOUS les sous-dossiers automatiquement
```

### Q: C'est quoi Path() vs str pour les chemins?

**R:**
```python
# Avec str - verbeux et fragile
import os
vault = "/Users/moi/vault"
note = "Projets/test.md"
full = os.path.join(vault, note)  # Manuellement
if os.path.exists(full):          # Vérification manuelle
    with open(full) as f:
        content = f.read()

# Avec Path - élégant et sûr
from pathlib import Path
vault = Path("/Users/moi/vault")
note = "Projets/test.md"
full = vault / note               # Opérateur /
if full.exists():                 # Méthode intégrée
    content = full.read_text()    # Lecture directe
```

Path est orienté objet et plus moderne!

---

## Diagramme d'architecture complet

```
┌─────────────────────────────────────────────────────────────┐
│                        UTILISATEUR                           │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
    ┌────▼─────┐                  ┌─────▼──────┐
    │ setup.sh │                  │ Python     │
    │          │                  │ Scripts    │
    │ • Détecte│                  └─────┬──────┘
    │   Python │                        │
    │ • Crée   │         ┌──────────────┼──────────────┐
    │   venv   │         │              │              │
    │ • Install│    ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
    │   deps   │    │correct_ │   │main_    │   │obsidian_│
    └──────────┘    │spelling │   │simple   │   │tools    │
                    └────┬────┘   └────┬────┘   └────┬────┘
                         │             │             │
                    ┌────▼─────────────▼─────────────▼────┐
                    │        ObsidianTools Class          │
                    │  • read_note()                      │
                    │  • write_note()                     │
                    │  • search_notes()                   │
                    │  • list_notes()                     │
                    └────┬────────────────────────────────┘
                         │
                         │ Lit/Écrit fichiers
                         ▼
                ┌────────────────────┐
                │  Fichiers .md      │
                │  dans vault        │
                │  Obsidian          │
                └────────────────────┘

┌────────────────────────────────────────────────────────────┐
│              CORRECTION ORTHOGRAPHIQUE                      │
└────────────────────────────────────────────────────────────┘

SpellingCorrector
      │
      ├─> read_note() ────> "Texte avec fautes"
      │
      ├─> LLM (Ollama)
      │    │
      │    ├─> HTTP POST localhost:11434
      │    │   Body: {prompt: "Corrige...", model: "llama3.1:8b"}
      │    │
      │    └─> Ollama Server
      │         │
      │         ├─> Charge modèle en RAM (~5GB)
      │         ├─> Tokenize prompt
      │         ├─> Génère tokens un par un
      │         └─> Retourne texte corrigé
      │
      └─> write_note() ────> "Texte corrigé"
```

---

## Conseils pour modifier les scripts

### Ajouter un nouveau tool Obsidian

```python
# Dans obsidian_tools.py

def create_note_template(self, note_path: str, template_name: str) -> str:
    """Crée une note depuis un template."""

    # Charger le template
    template_path = self.vault_path / "Templates" / f"{template_name}.md"
    if not template_path.exists():
        return f"Template {template_name} introuvable"

    template_content = template_path.read_text(encoding='utf-8')

    # Remplacer variables (ex: {{date}})
    from datetime import datetime
    content = template_content.replace(
        "{{date}}",
        datetime.now().strftime("%Y-%m-%d")
    )

    # Créer la note
    return self.write_note(note_path, content)
```

### Changer la température du correcteur

```python
# Dans correct_spelling.py, ligne ~35

self.llm = Ollama(
    model=model,
    base_url="http://localhost:11434",
    temperature=0.3,  # Changé de 0.1 → 0.3 pour plus de variation
)
```

### Ajouter logging

```python
# En haut du fichier
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Dans votre code
logger.info(f"Correction de {note_path}...")
logger.error(f"Erreur: {e}")
```

---

J'espère que ce guide vous aide à comprendre le fonctionnement technique! N'hésitez pas si vous avez des questions spécifiques sur une partie.
