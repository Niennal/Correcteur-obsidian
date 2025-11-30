# Index des Fichiers - Correcteur-obsidian

Guide complet de tous les fichiers du projet et leur utilité.

## 📚 Documentation

| Fichier | Description | Quand l'utiliser |
|---------|-------------|------------------|
| **README.md** | Documentation principale du projet | Premier fichier à lire |
| **QUICKSTART.md** | Guide de démarrage rapide | Pour l'installation initiale |
| **CORRECTION_GUIDE.md** | Guide complet de correction orthographique | Pour comprendre en détail la correction |
| **GUIDE_RAPIDE_CORRECTION.md** | Guide rapide de correction | Pour démarrer rapidement avec la correction |
| **FONCTIONNEMENT_TECHNIQUE.md** | Explication détaillée du code | Pour comprendre comment ça marche |
| **EXEMPLES_PRATIQUES.md** | Cas d'usage et exemples concrets | Pour apprendre par la pratique |
| **GITHUB_SETUP.md** | Instructions pour pousser sur GitHub | Pour publier le projet |
| **INDEX.md** | Ce fichier - index de tous les fichiers | Pour s'y retrouver dans le projet |

## 🚀 Scripts Principaux

### Scripts utilisateur (à exécuter)

| Script | Usage | Commande |
|--------|-------|----------|
| **correct_spelling.py** | ✨ Corriger l'orthographe des notes | `python correct_spelling.py` |
| **main_simple.py** | Interface simple pour gérer les notes | `python main_simple.py` |
| **demo_correction.py** | Démonstration de la correction | `python demo_correction.py` |
| **test_simple.py** | Tester l'installation | `python test_simple.py` |
| **test_ollama.py** | Tester la connexion à Ollama | `python test_ollama.py` |

### Scripts avancés (pour développeurs)

| Script | Usage | Note |
|--------|-------|------|
| **main.py** | Version multi-agent complète | Nécessite adaptation pour CrewAI 0.11.2 |
| **examples.py** | Exemples d'utilisation programmatique | Pour créer vos propres scripts |

## 🔧 Fichiers Techniques

### Bibliothèques Python

| Fichier | Description | Utilisé par |
|---------|-------------|-------------|
| **obsidian_tools.py** | Outils pour interagir avec Obsidian | Tous les scripts |
| **agents_config.py** | Configuration des agents CrewAI | main.py, main_simple.py |

### Configuration

| Fichier | Description | Action requise |
|---------|-------------|----------------|
| **.env** | Configuration (vault path, modèles) | ⚠️ À CONFIGURER |
| **.env.example** | Template de configuration | Pour référence |
| **requirements.txt** | Dépendances Python | Déjà installé |
| **.gitignore** | Fichiers à ignorer par Git | Aucune |

### Utilitaires

| Fichier | Description | Usage |
|---------|-------------|-------|
| **quickstart.sh** | Script de setup automatique | `./quickstart.sh` |

## 📋 Guide d'utilisation par tâche

### Je veux corriger l'orthographe

1. **Démarrage rapide**: Lisez [GUIDE_RAPIDE_CORRECTION.md](GUIDE_RAPIDE_CORRECTION.md)
2. **Documentation complète**: Consultez [CORRECTION_GUIDE.md](CORRECTION_GUIDE.md)
3. **Lancer**: `python correct_spelling.py`
4. **Tester**: `python demo_correction.py`

**Fichiers concernés:**
- ✅ `correct_spelling.py` - Le script principal
- ✅ `demo_correction.py` - Pour tester
- ✅ `GUIDE_RAPIDE_CORRECTION.md` - Guide rapide
- ✅ `CORRECTION_GUIDE.md` - Documentation complète

### Je veux gérer mes notes

1. **Lancer**: `python main_simple.py`
2. **Lire la doc**: Section "Utilisation" dans [README.md](README.md)

**Fichiers concernés:**
- ✅ `main_simple.py` - Interface simple
- ✅ `obsidian_tools.py` - Les outils Obsidian

### Je veux installer le système

1. **Lire**: [QUICKSTART.md](QUICKSTART.md)
2. **Exécuter**: `./quickstart.sh`
3. **Tester**: `python test_simple.py`

**Fichiers concernés:**
- ✅ `QUICKSTART.md` - Guide d'installation
- ✅ `quickstart.sh` - Script automatique
- ✅ `test_simple.py` - Tests
- ✅ `.env.example` - Template config

### Je veux développer mes propres scripts

1. **Exemples**: Consultez `examples.py`
2. **API**: Étudiez `obsidian_tools.py`
3. **Agents**: Regardez `agents_config.py`

**Fichiers concernés:**
- ✅ `examples.py` - 6 exemples
- ✅ `obsidian_tools.py` - API des outils
- ✅ `agents_config.py` - Configuration agents

## 🎯 Workflows recommandés

### Workflow 1: Installation initiale

```bash
# 1. Lire la documentation
cat QUICKSTART.md

# 2. Configurer .env
nano .env

# 3. Tester l'installation
python test_simple.py

# 4. Tester Ollama
python test_ollama.py

# 5. Tester avec une démo
python demo_correction.py
```

### Workflow 2: Correction hebdomadaire

```bash
# Tous les dimanches
source venv/bin/activate
python correct_spelling.py
# Choix: 1
# Dossier: Daily
```

### Workflow 3: Gestion quotidienne des notes

```bash
source venv/bin/activate
python main_simple.py
# Chercher, lire, créer des notes
```

## 📁 Structure du projet

```
Correcteur-obsidian/
├── 📚 Documentation
│   ├── README.md                      # Doc principale
│   ├── QUICKSTART.md                  # Installation
│   ├── CORRECTION_GUIDE.md            # Guide correction complet
│   ├── GUIDE_RAPIDE_CORRECTION.md     # Guide correction rapide
│   └── INDEX.md                       # Ce fichier
│
├── 🚀 Scripts utilisateur
│   ├── correct_spelling.py            # ✨ Correction orthographique
│   ├── main_simple.py                 # Interface simple
│   ├── demo_correction.py             # Démo correction
│   ├── test_simple.py                 # Test installation
│   └── test_ollama.py                 # Test Ollama
│
├── 🔧 Scripts avancés
│   ├── main.py                        # Version multi-agent
│   └── examples.py                    # Exemples d'utilisation
│
├── 📚 Bibliothèques
│   ├── obsidian_tools.py              # Outils Obsidian
│   └── agents_config.py               # Config agents
│
├── ⚙️ Configuration
│   ├── .env                           # Config (à configurer!)
│   ├── .env.example                   # Template
│   ├── requirements.txt               # Dépendances
│   └── .gitignore                     # Git ignore
│
├── 🛠️ Utilitaires
│   └── quickstart.sh                  # Setup auto
│
└── 📦 Environnement
    └── venv/                          # Env virtuel Python
```

## 🎓 Apprentissage progressif

### Niveau 1: Débutant

Fichiers à lire dans l'ordre:
1. ✅ README.md (vue d'ensemble)
2. ✅ QUICKSTART.md (installation)
3. ✅ GUIDE_RAPIDE_CORRECTION.md (première fonctionnalité)

Scripts à exécuter:
1. ✅ `python test_simple.py`
2. ✅ `python demo_correction.py`
3. ✅ `python correct_spelling.py`

### Niveau 2: Intermédiaire

Fichiers à explorer:
1. ✅ CORRECTION_GUIDE.md (détails)
2. ✅ obsidian_tools.py (code source)
3. ✅ main_simple.py (interface)

À essayer:
1. ✅ Corriger différents dossiers
2. ✅ Utiliser `main_simple.py`
3. ✅ Restaurer des backups

### Niveau 3: Avancé

Fichiers à étudier:
1. ✅ agents_config.py (architecture)
2. ✅ examples.py (patterns)
3. ✅ main.py (multi-agent)

À créer:
1. ✅ Vos propres scripts Python
2. ✅ Automatisations (cron)
3. ✅ Extensions personnalisées

## 💡 Conseils

### Pour trouver rapidement un fichier

Utilisez ce tableau selon votre besoin:

| Je veux... | Fichier à utiliser |
|------------|-------------------|
| Corriger l'orthographe | `correct_spelling.py` |
| Voir une démo | `demo_correction.py` |
| Gérer mes notes | `main_simple.py` |
| Comprendre le code | `obsidian_tools.py` |
| Installer | `QUICKSTART.md` |
| Configurer | `.env` |
| Apprendre la correction | `GUIDE_RAPIDE_CORRECTION.md` |
| Détails techniques | `CORRECTION_GUIDE.md` |
| Créer mes scripts | `examples.py` |

### Organisation recommandée

Gardez ces fichiers sous la main (favoris):
1. 📌 `.env` - Configuration
2. 📌 `correct_spelling.py` - Usage quotidien
3. 📌 `main_simple.py` - Usage quotidien
4. 📌 `GUIDE_RAPIDE_CORRECTION.md` - Référence rapide

### Fichiers à ne PAS modifier

⚠️ Ne modifiez pas (sauf si vous savez ce que vous faites):
- `requirements.txt`
- `.gitignore`
- `obsidian_tools.py`
- `agents_config.py`

✅ Vous pouvez modifier:
- `.env` (DOIT être modifié!)
- Vos propres scripts basés sur `examples.py`

## 🆘 Dépannage

### "Je ne sais pas par où commencer"

Lisez dans l'ordre:
1. README.md
2. QUICKSTART.md
3. Lancez `python test_simple.py`

### "Je veux juste corriger l'orthographe"

Allez directement à:
1. GUIDE_RAPIDE_CORRECTION.md
2. `python demo_correction.py`
3. `python correct_spelling.py`

### "Aucun fichier ne fonctionne"

Vérifiez:
1. `.env` est configuré? `cat .env`
2. Venv est activé? `source venv/bin/activate`
3. Ollama fonctionne? `python test_ollama.py`

## 📞 Aide rapide

```bash
# État du système
source venv/bin/activate
python test_simple.py

# Test Ollama
python test_ollama.py

# Voir la config
cat .env

# Démo complète
python demo_correction.py
```

---

**Navigation rapide:**
- 🏠 [README.md](README.md) - Accueil
- 🚀 [QUICKSTART.md](QUICKSTART.md) - Démarrage
- ✨ [GUIDE_RAPIDE_CORRECTION.md](GUIDE_RAPIDE_CORRECTION.md) - Correction rapide
- 📖 [CORRECTION_GUIDE.md](CORRECTION_GUIDE.md) - Correction complète
