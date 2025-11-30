# Comment pousser ce projet sur GitHub

## Étape 1: Créer un repo sur GitHub

1. Allez sur https://github.com
2. Cliquez sur le bouton **"+"** en haut à droite
3. Sélectionnez **"New repository"**
4. Configurez:
   - **Repository name**: `obsidian-multiagent` (ou un autre nom)
   - **Description**: `Système multi-agent intelligent pour gérer et corriger vos notes Obsidian avec CrewAI et Ollama`
   - **Public** ou **Private** (à votre choix)
   - ⚠️ **NE cochez PAS** "Initialize with README" (on a déjà tout!)
5. Cliquez sur **"Create repository"**

## Étape 2: Connecter votre repo local à GitHub

GitHub va vous afficher une page avec des instructions. Copiez l'URL de votre repo (qui ressemble à `https://github.com/VOTRE-USERNAME/obsidian-multiagent.git`).

Puis dans votre terminal:

```bash
# Ajouter le remote
git remote add origin https://github.com/VOTRE-USERNAME/obsidian-multiagent.git

# Vérifier que c'est bon
git remote -v
```

Vous devriez voir:
```
origin  https://github.com/VOTRE-USERNAME/obsidian-multiagent.git (fetch)
origin  https://github.com/VOTRE-USERNAME/obsidian-multiagent.git (push)
```

## Étape 3: Pousser le code

```bash
# Pousser la branche main
git push -u origin main
```

Si c'est la première fois, Git peut vous demander de vous authentifier:
- Utilisez votre **username GitHub**
- Pour le mot de passe, utilisez un **Personal Access Token** (pas votre mot de passe!)

### Comment créer un Personal Access Token (si nécessaire)

1. Allez sur GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Cliquez sur **"Generate new token"** → **"Generate new token (classic)"**
3. Donnez-lui un nom: `obsidian-multiagent`
4. Cochez la case **"repo"** (full control of private repositories)
5. Cliquez sur **"Generate token"**
6. **COPIEZ LE TOKEN** (vous ne le reverrez jamais!)
7. Utilisez ce token comme mot de passe quand Git le demande

## Étape 4: Vérifier sur GitHub

Allez sur `https://github.com/VOTRE-USERNAME/obsidian-multiagent` et vous devriez voir tous vos fichiers!

## Étape 5: Mettre à jour le README (optionnel)

Maintenant que vous connaissez votre URL GitHub, vous pouvez mettre à jour le lien dans README.md:

```bash
# Ouvrir le README
nano README.md

# Chercher cette ligne:
git clone https://github.com/VOTRE-USERNAME/obsidian-multiagent.git

# Remplacer VOTRE-USERNAME par votre vrai username

# Sauvegarder et quitter (Ctrl+O, Enter, Ctrl+X)

# Commiter le changement
git add README.md
git commit -m "docs: update GitHub username in README"
git push
```

## Commandes Git utiles pour la suite

```bash
# Voir l'état de vos fichiers
git status

# Ajouter tous les fichiers modifiés
git add .

# Commiter avec un message
git commit -m "feat: description de votre modification"

# Pousser vers GitHub
git push

# Voir l'historique
git log --oneline

# Voir les différences
git diff
```

## Structure des messages de commit

Utilisez ces préfixes pour des commits clairs:

- `feat:` - Nouvelle fonctionnalité
- `fix:` - Correction de bug
- `docs:` - Documentation
- `style:` - Formatage (pas de changement de code)
- `refactor:` - Refactoring
- `test:` - Ajout de tests
- `chore:` - Maintenance

Exemples:
```bash
git commit -m "feat: ajout support des tables Markdown dans correction"
git commit -m "fix: correction bug lecture notes avec accents"
git commit -m "docs: mise à jour guide correction orthographique"
```

## Ignorer des fichiers

Le fichier `.gitignore` est déjà configuré pour ignorer:
- `venv/` - Environnement virtuel
- `.env` - Configuration locale (avec vos chemins)
- `__pycache__/` - Cache Python
- `.DS_Store` - Fichiers macOS
- `.backups/` - Backups de notes

Ces fichiers ne seront **jamais** poussés sur GitHub, ce qui est voulu!

## Cloner sur un autre ordinateur

Pour utiliser ce projet sur un autre ordinateur:

```bash
# Cloner le repo
git clone https://github.com/VOTRE-USERNAME/obsidian-multiagent.git
cd obsidian-multiagent

# Lancer le setup (qui fait tout!)
./setup.sh
```

C'est tout! Le script `setup.sh` configurera automatiquement tout l'environnement.

## Ajouter un badge au README (optionnel)

Éditez `README.md` et ajoutez en haut (après le titre):

```markdown
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/Ollama-Required-green.svg)](https://ollama.ai/)
```

Puis commitez:
```bash
git add README.md
git commit -m "docs: add badges to README"
git push
```

## Collaborer

Si d'autres personnes veulent contribuer:

1. Ils font un **Fork** de votre repo
2. Ils clonent leur fork
3. Ils créent une branche pour leur feature
4. Ils poussent vers leur fork
5. Ils créent une **Pull Request** vers votre repo

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

## Aide

Si vous avez des problèmes:

- Vérifiez que Git est installé: `git --version`
- Vérifiez votre remote: `git remote -v`
- Assurez-vous d'être sur la branche main: `git branch`
- Consultez les logs: `git log --oneline`

Bon courage! 🚀
