# Exemples pratiques - Comprendre par la pratique

Ce guide complète FONCTIONNEMENT_TECHNIQUE.md avec des exemples concrets et des cas d'usage réels.

## Table des matières

1. [Exemple complet: Correction d'une note](#exemple-complet-correction-dune-note)
2. [Exemple: Créer un outil personnalisé](#exemple-créer-un-outil-personnalisé)
3. [Exemple: Modifier le comportement du correcteur](#exemple-modifier-le-comportement-du-correcteur)
4. [Exemple: Workflow automatisé](#exemple-workflow-automatisé)
5. [Debugging et troubleshooting](#debugging-et-troubleshooting)

---

## Exemple complet: Correction d'une note

### Scénario réel

Vous avez une note `Projets/rapport.md` avec ce contenu:

```markdown
# Rapport du projet

Aujourdhui jai travailler sur le projet. Voici les taches accomplies:

- Corriger les bug
- Ameliorer la performance
- Tester le systeme

Les resultat sont encourageant!
```

### Étape par étape du processus

#### 1. Lancement du script

```bash
source venv/bin/activate
python correct_spelling.py
```

**Ce qui se passe en mémoire:**

```python
# Python charge le script
import os
import sys
from dotenv import load_dotenv
# ...

# Charge les variables .env
load_dotenv()
# → Lit .env
# → Met OBSIDIAN_VAULT_PATH dans os.environ

VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")
# → VAULT_PATH = "/Users/moi/vault"
```

#### 2. Initialisation du correcteur

```python
corrector = SpellingCorrector(
    vault_path="/Users/moi/vault",
    model="llama3.1:8b"
)
```

**En mémoire:**

```
Heap Python:
├─ SpellingCorrector instance
│  ├─ vault_path: Path("/Users/moi/vault")
│  ├─ tools: ObsidianTools instance
│  │  └─ vault_path: Path("/Users/moi/vault")
│  └─ llm: Ollama instance
│     ├─ model: "llama3.1:8b"
│     ├─ base_url: "http://localhost:11434"
│     └─ temperature: 0.1
```

#### 3. Menu utilisateur

```
Votre choix: 2
Chemin de la note: Projets/rapport.md
```

**Code exécuté:**

```python
choice = input("Votre choix: ").strip()  # "2"

if choice == "2":
    note_path = input("Chemin de la note: ").strip()  # "Projets/rapport.md"
    result = corrector.correct_note(note_path)
```

#### 4. Lecture de la note

```python
def correct_note(self, note_path: str):
    full_path = self.vault_path / note_path
    # full_path = Path("/Users/moi/vault/Projets/rapport.md")

    with open(full_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
```

**Contenu en mémoire:**

```python
original_content = """# Rapport du projet

Aujourdhui jai travailler sur le projet. Voici les taches accomplies:

- Corriger les bug
- Ameliorer la performance
- Tester le systeme

Les resultat sont encourageant!"""
```

**Taille en mémoire:** ~200 bytes (texte ASCII/UTF-8)

#### 5. Création du backup

```python
backup_path = self.create_backup(full_path)
```

**Opérations filesystem:**

```
1. datetime.now() → "2025-11-30 15:30:45"
2. strftime("%Y%m%d_%H%M%S") → "20251130_153045"
3. backup_path = "/Users/moi/vault/.backups/rapport_20251130_153045.md"
4. shutil.copy2(original, backup)
   → Copie fichier avec métadonnées
```

**Vérification:**

```bash
ls -la /Users/moi/vault/.backups/
# -rw-r--r--  rapport_20251130_153045.md
```

#### 6. Correction via LLM

```python
corrected_content = self.correct_text(original_content)
```

**Construction du prompt:**

```python
prompt = f"""Tu es un correcteur orthographique expert en français.

RÈGLES IMPORTANTES:
1. Corrige UNIQUEMENT les fautes d'orthographe, de grammaire et de ponctuation
2. Ne modifie PAS la structure Markdown (titres ##, listes -, liens [[]], tags #)
...

TEXTE À CORRIGER:
# Rapport du projet

Aujourdhui jai travailler sur le projet. Voici les taches accomplies:
...

TEXTE CORRIGÉ:"""
```

**Longueur du prompt:** ~500 caractères = ~125 tokens

**Appel HTTP à Ollama:**

```python
# Langchain fait en arrière-plan:
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 1024
        }
    }
)

# Réponse d'Ollama (simplifié):
{
    "model": "llama3.1:8b",
    "created_at": "2025-11-30T15:30:50Z",
    "response": "# Rapport du projet\n\nAujourd'hui j'ai travaillé...",
    "done": true,
    "total_duration": 2500000000,  # 2.5 secondes en nanosecondes
    "load_duration": 100000000,     # 0.1 seconde (déjà chargé)
    "prompt_eval_count": 125,       # 125 tokens dans le prompt
    "eval_count": 85                # 85 tokens générés
}
```

**Processus dans Ollama:**

```
1. Ollama reçoit requête HTTP
   ↓
2. Modèle llama3.1:8b déjà en RAM? Oui (chargé au premier appel)
   ↓
3. Tokenize le prompt: "Tu es un correcteur..." → [tokens]
   ↓
4. Passe les tokens au modèle neural
   ↓
5. Modèle génère token par token:
   "Aujourd" → "'" → "hui" → " " → "j" → "'" → "ai" → " " → "travaillé" ...
   ↓
6. Arrêt quand:
   - Génère token de fin </s>
   - OU atteint num_predict (1024 tokens)
   ↓
7. Retourne le texte complet
```

**RAM utilisée pendant la correction:**

```
Ollama server:
├─ llama3.1:8b model: 4.7 GB
├─ Prompt context: 125 tokens × 4 bytes = 500 bytes
├─ Generation buffer: 85 tokens × 4 bytes = 340 bytes
└─ Total: ~4.7 GB

Python script:
├─ Original content: 200 bytes
├─ Corrected content: 220 bytes
├─ Prompt string: 500 bytes
└─ Total: ~1 KB (négligeable)
```

**Résultat retourné:**

```python
corrected_content = """# Rapport du projet

Aujourd'hui j'ai travaillé sur le projet. Voici les tâches accomplies:

- Corriger les bugs
- Améliorer la performance
- Tester le système

Les résultats sont encourageants!"""
```

#### 7. Comparaison et décision

```python
if corrected_content == original_content:
    return {"success": True, "changes": False}
```

**Comparaison en Python:**

```python
# Python compare caractère par caractère
original_content[0:10]  = "# Rapport "
corrected_content[0:10] = "# Rapport "
# ✓ Identiques

original_content[30:40] = "Aujourdhui"
corrected_content[30:40] = "Aujourd'hu"
# ✗ Différents → changes = True
```

#### 8. Écriture du fichier corrigé

```python
with open(full_path, 'w', encoding='utf-8') as f:
    f.write(corrected_content)
```

**Opérations filesystem:**

```
1. Ouvre /Users/moi/vault/Projets/rapport.md en mode 'w'
   → Tronque le fichier (vide tout)
2. Écrit corrected_content
   → Encode UTF-8: "Aujourd'hui" → bytes
3. Ferme le fichier
   → Flush buffer vers disque
```

**Vérification:**

```bash
cat /Users/moi/vault/Projets/rapport.md
# Rapport du projet
#
# Aujourd'hui j'ai travaillé sur le projet...
```

#### 9. Retour du résultat

```python
return {
    "success": True,
    "changes": True,
    "backup": "/Users/moi/vault/.backups/rapport_20251130_153045.md"
}
```

**Affichage à l'utilisateur:**

```
✅ Note corrigée: Projets/rapport.md
💾 Backup: .backups/rapport_20251130_153045.md
```

### Timeline complète

```
T+0ms    : Utilisateur lance script
T+100ms  : Python charge modules
T+200ms  : Charge .env
T+300ms  : Initialise SpellingCorrector
T+400ms  : Affiche menu
T+5000ms : Utilisateur entre choix
T+5100ms : Lit fichier rapport.md (200 bytes)
T+5120ms : Crée backup
T+5150ms : Construit prompt
T+5200ms : Envoie requête HTTP à Ollama
T+5250ms : Ollama reçoit requête
T+5300ms : Tokenize prompt (125 tokens)
T+5400ms : Commence génération
T+7400ms : Génération terminée (85 tokens, ~2 secondes)
T+7450ms : Retourne résultat
T+7500ms : Compare original vs corrigé
T+7520ms : Écrit fichier
T+7550ms : Affiche résultat à l'utilisateur

Total: ~7.5 secondes
```

---

## Exemple: Créer un outil personnalisé

### Besoin: Extraire tous les tags d'une note

```python
# Ajouter dans obsidian_tools.py

def extract_tags(self, note_path: str) -> str:
    """
    Extrait tous les tags (#tag) d'une note.

    Args:
        note_path: Chemin relatif de la note

    Returns:
        Liste des tags trouvés
    """
    full_path = self.vault_path / note_path

    if not full_path.exists():
        return f"Erreur: Note introuvable"

    # Lire le contenu
    content = full_path.read_text(encoding='utf-8')

    # Extraire les tags avec regex
    import re
    # Pattern: # suivi de lettres/chiffres/- mais pas d'espace
    pattern = r'#([a-zA-Z0-9_-]+)'
    tags = re.findall(pattern, content)

    # Dédupliquer (enlever doublons)
    unique_tags = sorted(set(tags))

    if not unique_tags:
        return f"Aucun tag trouvé dans {note_path}"

    return f"Tags dans {note_path}:\n" + "\n".join(f"  - #{tag}" for tag in unique_tags)
```

**Utilisation:**

```python
tools = ObsidianTools("/vault")
result = tools.extract_tags("Projets/rapport.md")
print(result)

# Output:
# Tags dans Projets/rapport.md:
#   - #important
#   - #projet
#   - #urgent
```

**Comment fonctionne la regex:**

```python
pattern = r'#([a-zA-Z0-9_-]+)'

Décomposition:
- r'...'           : Raw string (pas d'échappement \)
- #                : Caractère # littéral
- (...)            : Groupe de capture
- [a-zA-Z0-9_-]    : Un caractère alphanumérique ou _ ou -
- +                : Un ou plusieurs

Exemples:
"Voici #projet et #urgent-2025"
         ^^^^^^     ^^^^^^^^^^^
         Groupe 1   Groupe 2

re.findall() retourne: ['projet', 'urgent-2025']
```

### Besoin: Compter les mots dans une note

```python
def count_words(self, note_path: str) -> str:
    """Compte les mots dans une note."""
    full_path = self.vault_path / note_path

    if not full_path.exists():
        return f"Erreur: Note introuvable"

    content = full_path.read_text(encoding='utf-8')

    # Supprimer le code (entre ```)
    import re
    content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

    # Supprimer les titres Markdown (##)
    content_no_headers = re.sub(r'^#+\s+', '', content_no_code, flags=re.MULTILINE)

    # Compter les mots
    words = content_no_headers.split()
    word_count = len(words)

    # Compter les caractères (sans espaces)
    char_count = len(content_no_headers.replace(' ', '').replace('\n', ''))

    # Estimer temps de lecture (250 mots/minute)
    reading_time = round(word_count / 250, 1)

    return f"""Statistiques pour {note_path}:
  Mots: {word_count}
  Caractères: {char_count}
  Temps de lecture: ~{reading_time} min"""
```

**Flags regex expliqués:**

```python
re.DOTALL
# . match aussi les \n (par défaut . ne match pas \n)

re.MULTILINE
# ^ et $ matchent début/fin de ligne (pas juste début/fin de texte)

re.sub(r'```.*?```', '', content, flags=re.DOTALL)
#        ^^^
#        .*?  = non-greedy (s'arrête au premier ```)
#        .*   = greedy (irait jusqu'au dernier ```)

Exemple:
content = "Texte ```code1``` autre ```code2``` fin"

Avec .*? (non-greedy):
Supprime: ```code1``` et ```code2```
Résultat: "Texte  autre  fin"

Avec .* (greedy):
Supprime: ```code1``` autre ```code2```
Résultat: "Texte  fin"
```

---

## Exemple: Modifier le comportement du correcteur

### Cas 1: Corriger seulement certains types de fautes

```python
# Dans correct_spelling.py, méthode correct_text()

def correct_text_grammar_only(self, text: str) -> str:
    """Corrige uniquement la grammaire, pas l'orthographe."""

    prompt = f"""Tu es un correcteur grammatical expert en français.

RÈGLES STRICTES:
1. Corrige UNIQUEMENT les erreurs de grammaire et d'accord
2. NE corrige PAS l'orthographe des mots individuels
3. Corrige les accords (genre, nombre, temps)
4. Corrige les conjugaisons
5. Ne modifie PAS la structure Markdown
6. Retourne UNIQUEMENT le texte corrigé

Exemples:
- "Les chiens mange" → "Les chiens mangent" (accord)
- "Il a manger" → "Il a mangé" (participe passé)
- "ortographe" → "ortographe" (NE CHANGE PAS l'orthographe!)

TEXTE À CORRIGER:
{text}

TEXTE CORRIGÉ:"""

    return self.llm.invoke(prompt).strip()
```

**Différence avec correction complète:**

```python
# Correction complète
Entrée:  "Les chiens mange des gateau"
Sortie:  "Les chiens mangent des gâteaux"
         ^^^^^^^^        ^^^^^^^^^^^^^^
         Accord          Accord + orthographe

# Correction grammaire seulement
Entrée:  "Les chiens mange des gateau"
Sortie:  "Les chiens mangent des gateau"
         ^^^^^^^^        ^^^^^^^
         Accord          Orthographe inchangée
```

### Cas 2: Correction en plusieurs passes

```python
def correct_text_multiple_passes(self, text: str) -> str:
    """
    Corrige en plusieurs passes pour meilleure qualité.

    Pass 1: Orthographe
    Pass 2: Grammaire
    Pass 3: Ponctuation
    """

    # Pass 1: Orthographe
    prompt1 = f"""Corrige UNIQUEMENT l'orthographe des mots.
Ne touche PAS à la grammaire ou la ponctuation.

TEXTE: {text}
CORRIGÉ:"""

    text_pass1 = self.llm.invoke(prompt1).strip()

    # Pass 2: Grammaire
    prompt2 = f"""Corrige UNIQUEMENT les accords et la grammaire.
L'orthographe est déjà correcte.

TEXTE: {text_pass1}
CORRIGÉ:"""

    text_pass2 = self.llm.invoke(prompt2).strip()

    # Pass 3: Ponctuation
    prompt3 = f"""Corrige UNIQUEMENT la ponctuation.
Tout le reste est déjà correct.

TEXTE: {text_pass2}
CORRIGÉ:"""

    text_pass3 = self.llm.invoke(prompt3).strip()

    return text_pass3
```

**Avantages:**
- Plus de précision (focus sur un aspect à la fois)
- Le modèle fait moins d'erreurs

**Inconvénients:**
- 3× plus lent (3 appels LLM)
- 3× plus de RAM/CPU

**Quand l'utiliser:**
- Documents importants (articles, thèses)
- Quand la qualité prime sur la vitesse

### Cas 3: Correction avec vérification

```python
def correct_text_with_verification(self, text: str) -> str:
    """Corrige et vérifie que le Markdown est préservé."""

    # Extraire structure Markdown avant correction
    import re

    # Trouver tous les titres
    headers_before = re.findall(r'^#+\s+.+$', text, re.MULTILINE)

    # Trouver tous les liens
    links_before = re.findall(r'\[\[.+?\]\]', text)

    # Trouver tous les tags
    tags_before = re.findall(r'#[a-zA-Z0-9_-]+', text)

    # Corriger
    corrected = self.correct_text(text)

    # Vérifier structure après correction
    headers_after = re.findall(r'^#+\s+.+$', corrected, re.MULTILINE)
    links_after = re.findall(r'\[\[.+?\]\]', corrected)
    tags_after = re.findall(r'#[a-zA-Z0-9_-]+', corrected)

    # Comparer
    if len(headers_before) != len(headers_after):
        print(f"⚠️ ATTENTION: Nombre de titres changé!")
        print(f"   Avant: {len(headers_before)}, Après: {len(headers_after)}")

    if set(links_before) != set(links_after):
        print(f"⚠️ ATTENTION: Liens modifiés!")
        print(f"   Supprimés: {set(links_before) - set(links_after)}")
        print(f"   Ajoutés: {set(links_after) - set(links_before)}")

    if set(tags_before) != set(tags_after):
        print(f"⚠️ ATTENTION: Tags modifiés!")

    return corrected
```

---

## Exemple: Workflow automatisé

### Script: Correction quotidienne automatique

```python
#!/usr/bin/env python3
"""
daily_correction.py - Corrige automatiquement les notes Daily
"""
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from correct_spelling import SpellingCorrector

def correct_daily_notes():
    """Corrige les notes quotidiennes de la semaine."""

    load_dotenv()
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")

    corrector = SpellingCorrector(vault_path, model="llama3.1:8b")

    # Obtenir les 7 derniers jours
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    print("🗓️ Correction des notes quotidiennes de la semaine\n")

    for date in dates:
        note_path = f"Daily/{date}.md"

        result = corrector.correct_note(note_path, create_backup=True)

        if result["success"]:
            if result.get("changes"):
                print(f"✅ {date}: Corrigée")
            else:
                print(f"➖ {date}: Déjà correcte")
        else:
            print(f"❌ {date}: {result.get('error', 'Non trouvée')}")

    print("\n✨ Correction terminée!")

if __name__ == "__main__":
    correct_daily_notes()
```

**Automatiser avec cron (macOS/Linux):**

```bash
# Éditer crontab
crontab -e

# Ajouter cette ligne (tous les jours à 20h)
0 20 * * * cd ~/obsidian-multiagent && source venv/bin/activate && python daily_correction.py >> logs/daily.log 2>&1

# Explication:
# 0 20 * * *  → minute=0, heure=20, tous les jours
# cd ~/obsidian-multiagent  → se placer dans le dossier
# source venv/bin/activate  → activer l'environnement
# python daily_correction.py  → lancer le script
# >> logs/daily.log  → rediriger stdout vers log
# 2>&1  → rediriger stderr aussi vers log
```

### Script: Correction avant push Git

```python
#!/usr/bin/env python3
"""
pre_commit_correction.py - Corrige les notes modifiées avant commit
"""
import subprocess
from correct_spelling import SpellingCorrector
import os
from dotenv import load_dotenv

def get_modified_notes():
    """Obtient les notes .md modifiées depuis le dernier commit."""

    # Exécuter git diff
    result = subprocess.run(
        ['git', 'diff', '--name-only', '--cached'],
        capture_output=True,
        text=True
    )

    # Filtrer les fichiers .md
    files = result.stdout.strip().split('\n')
    md_files = [f for f in files if f.endswith('.md')]

    return md_files

def main():
    load_dotenv()
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")

    # Obtenir notes modifiées
    modified = get_modified_notes()

    if not modified:
        print("Aucune note modifiée")
        return

    print(f"📝 {len(modified)} note(s) modifiée(s)\n")

    corrector = SpellingCorrector(vault_path)

    for note in modified:
        print(f"Correction de {note}...")
        result = corrector.correct_note(note, create_backup=False)

        if result["success"] and result.get("changes"):
            # Re-stager le fichier corrigé
            subprocess.run(['git', 'add', note])
            print(f"  ✅ Corrigée et re-staged")
        else:
            print(f"  ➖ Aucune correction")

    print("\n✨ Prêt à commit!")

if __name__ == "__main__":
    main()
```

**Installer comme git hook:**

```bash
# Copier dans .git/hooks/pre-commit
cp pre_commit_correction.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Maintenant, à chaque git commit, vos notes seront auto-corrigées!
```

---

## Debugging et troubleshooting

### Problème: Le correcteur change trop de choses

**Solution: Augmenter la température**

```python
# Dans correct_spelling.py
self.llm = Ollama(
    model=model,
    temperature=0.01,  # Ultra bas = ultra conservateur
)
```

**Ou: Prompt plus strict**

```python
prompt = f"""RÈGLE ABSOLUE: Change UNIQUEMENT ce qui est CLAIREMENT une faute.
En cas de doute, NE CHANGE RIEN.

Exemples de ce qui doit être changé:
- "jai" → "j'ai" (apostrophe manquante)
- "aujourdhui" → "aujourd'hui" (orthographe)

Exemples de ce qui NE doit PAS être changé:
- "email" (pas "e-mail", les deux sont corrects)
- "Okay" (variante acceptable de "OK")
- Style personnel

TEXTE: {text}
CORRIGÉ:"""
```

### Problème: Le correcteur est trop lent

**Diagnostic:**

```python
import time

start = time.time()
corrected = self.correct_text(text)
duration = time.time() - start

print(f"Temps: {duration:.2f}s")
```

**Solutions:**

1. **Utiliser un modèle plus petit**
   ```python
   corrector = SpellingCorrector(vault_path, model="mistral:7b")
   # Plus rapide mais peut-être moins précis
   ```

2. **Réduire la longueur du prompt**
   ```python
   # Au lieu d'un long prompt avec règles...
   prompt = f"Corrige l'orthographe:\n{text}\nCorrigé:"
   # Moins de tokens = plus rapide
   ```

3. **Limiter num_predict**
   ```python
   self.llm = Ollama(
       model=model,
       num_predict=512,  # Au lieu de 1024
   )
   # Moins de tokens à générer = plus rapide
   ```

### Problème: Erreur "Connection refused" avec Ollama

**Diagnostic:**

```python
import requests

try:
    r = requests.get("http://localhost:11434/api/version")
    print(f"Ollama répond: {r.json()}")
except requests.exceptions.ConnectionError:
    print("Ollama ne répond pas!")
```

**Solutions:**

```bash
# 1. Vérifier si Ollama tourne
ps aux | grep ollama

# 2. Lancer Ollama
ollama serve

# 3. Vérifier le port
lsof -i :11434  # Doit montrer ollama
```

### Problème: Le backup prend trop de place

**Solution: Nettoyer les vieux backups**

```python
# cleanup_backups.py
from pathlib import Path
from datetime import datetime, timedelta
import os

def cleanup_old_backups(vault_path: str, days: int = 30):
    """Supprime les backups de plus de X jours."""

    backup_dir = Path(vault_path) / ".backups"

    if not backup_dir.exists():
        return

    cutoff = datetime.now() - timedelta(days=days)
    deleted = 0

    for backup_file in backup_dir.glob("*.md"):
        # Obtenir date de modification
        mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)

        if mtime < cutoff:
            backup_file.unlink()  # Supprimer
            deleted += 1

    print(f"🗑️ {deleted} backups supprimés (>{days} jours)")

# Utilisation
cleanup_old_backups("/vault", days=30)
```

**Automatiser le nettoyage:**

```bash
# Dans crontab (tous les lundis à 3h du matin)
0 3 * * 1 cd ~/obsidian-multiagent && source venv/bin/activate && python cleanup_backups.py
```

### Problème: Le correcteur plante sur de grosses notes

**Diagnostic:**

```python
def correct_note(self, note_path: str):
    full_path = self.vault_path / note_path

    # Vérifier la taille
    size = full_path.stat().st_size
    print(f"Taille: {size} bytes ({size/1024:.1f} KB)")

    if size > 100_000:  # 100 KB
        print("⚠️ Note très grande, risque de timeout")
```

**Solution: Découper en chunks**

```python
def correct_large_note(self, note_path: str, chunk_size: int = 10000):
    """Corrige une grande note par morceaux."""

    # Lire
    content = full_path.read_text()

    # Découper en paragraphes
    paragraphs = content.split('\n\n')

    corrected_paragraphs = []
    current_chunk = []
    current_size = 0

    for para in paragraphs:
        current_chunk.append(para)
        current_size += len(para)

        # Si chunk assez gros, corriger
        if current_size > chunk_size:
            chunk_text = '\n\n'.join(current_chunk)
            corrected = self.correct_text(chunk_text)
            corrected_paragraphs.append(corrected)

            # Reset
            current_chunk = []
            current_size = 0

    # Dernier chunk
    if current_chunk:
        chunk_text = '\n\n'.join(current_chunk)
        corrected = self.correct_text(chunk_text)
        corrected_paragraphs.append(corrected)

    # Recombiner
    return '\n\n'.join(corrected_paragraphs)
```

---

## Résumé des patterns courants

### Pattern: Lecture sécurisée

```python
def safe_read(file_path):
    """Lit un fichier avec gestion d'erreur."""
    try:
        return file_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        return None
    except UnicodeDecodeError:
        # Fichier binaire ou mauvais encodage
        return None
    except Exception as e:
        print(f"Erreur: {e}")
        return None
```

### Pattern: Opération avec rollback

```python
def safe_operation(file_path, operation_func):
    """Exécute une opération avec backup et rollback."""

    # Backup
    backup = create_backup(file_path)

    try:
        # Opération
        operation_func(file_path)
        return {"success": True}

    except Exception as e:
        # Rollback
        if backup.exists():
            shutil.copy2(backup, file_path)
        return {"success": False, "error": str(e)}
```

### Pattern: Batch processing avec statistiques

```python
def process_batch(items, process_func):
    """Traite une liste d'items avec stats."""

    stats = {"total": len(items), "success": 0, "errors": 0}

    for i, item in enumerate(items, 1):
        print(f"[{i}/{len(items)}] Processing {item}...")

        try:
            process_func(item)
            stats["success"] += 1
        except Exception as e:
            stats["errors"] += 1
            print(f"  Error: {e}")

    return stats
```

---

Voilà! Vous avez maintenant une compréhension complète et pratique du fonctionnement du système. N'hésitez pas si vous avez des questions sur un aspect spécifique!
