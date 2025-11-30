# Guide de Correction Orthographique

## Fonctionnalité

Le script `correct_spelling.py` corrige automatiquement les fautes d'orthographe dans vos notes Obsidian tout en:
- ✅ Préservant le formatage Markdown (titres ##, listes -, liens [[]], tags #)
- ✅ Créant des backups automatiques avant modification
- ✅ Ne modifiant PAS le sens ou le style du texte
- ✅ Conservant les noms propres, URLs et code

## Utilisation

### Lancer le correcteur

```bash
source venv/bin/activate
python correct_spelling.py
```

### Options disponibles

#### 1. Corriger un dossier spécifique

Corrige toutes les notes d'un dossier:

```
Votre choix: 1
Dossier à corriger: Projets
```

Le script va:
1. Lister toutes les notes du dossier
2. Demander confirmation
3. Créer un backup de chaque note
4. Corriger l'orthographe
5. Afficher un résumé

#### 2. Corriger une note spécifique

Pour corriger une seule note:

```
Votre choix: 2
Chemin de la note: Projets/ma-note.md
```

#### 3. Corriger tout le vault

**⚠️ ATTENTION**: Corrige TOUTES les notes du vault!

```
Votre choix: 3
Êtes-vous VRAIMENT sûr?: OUI
```

## Exemples d'utilisation

### Exemple 1: Corriger les notes d'un projet

```bash
python correct_spelling.py
# Choix: 1
# Dossier: Projets/MonProjet
# Confirmer: o
```

Résultat:
```
📂 Dossier: Projets/MonProjet
📝 Notes trouvées: 5
💾 Backups: Oui

⚠️  Corriger 5 note(s) ? (o/n): o

🚀 Début de la correction...

[1/5] Projets/MonProjet/README.md
  🔍 Correction de Projets/MonProjet/README.md...
  ✓ Corrigé et sauvegardé

[2/5] Projets/MonProjet/todo.md
  🔍 Correction de Projets/MonProjet/todo.md...
  ✓ Aucune correction nécessaire

...

📊 RÉSUMÉ
Total: 5 notes
✅ Corrigées: 3
➖ Inchangées: 2
❌ Erreurs: 0

💾 Backups sauvegardés dans: /vault/.backups
```

### Exemple 2: Corriger une note de meeting

```bash
python correct_spelling.py
# Choix: 2
# Note: Meetings/2025-11-30.md
```

## Sécurité des données

### Backups automatiques

Chaque note modifiée est automatiquement sauvegardée dans `.backups/` avec un timestamp:

```
.backups/
  ├── README_20251130_153045.md
  ├── todo_20251130_153047.md
  └── ...
```

### Restaurer une note

Si une correction ne vous plaît pas:

```bash
# Trouver le backup
ls .backups/

# Restaurer
cp .backups/ma-note_20251130_153045.md ma-note.md
```

## Configuration avancée

### Changer le modèle utilisé

Éditez `.env`:

```bash
# Pour une meilleure correction orthographique
TOOL_MODEL=mistral-nemo:12b
```

Modèles recommandés pour la correction:
- `llama3.1:8b` - Bon équilibre (défaut)
- `mistral-nemo:12b` - Excellente qualité
- `qwen2.5:7b` - Très bon en français

### Désactiver les backups (non recommandé)

Modifier le code dans `correct_spelling.py`:

```python
results = corrector.correct_folder(folder="Projets", create_backups=False)
```

## Ce que le correcteur fait

### ✅ Corrections appliquées:

- Fautes d'orthographe
- Fautes de grammaire
- Ponctuation incorrecte
- Accords (genre, nombre, temps)
- Apostrophes et guillemets

### ❌ Ce qui n'est PAS modifié:

- Structure Markdown (##, -, *, [])
- Liens internes [[]]
- Tags #
- Code `code` ou ```blocs```
- URLs
- Noms propres
- Style d'écriture
- Sens du texte

## Exemple de correction

**Avant:**
```markdown
# Mon Projet

Aujourdhui jai travailler sur le projets. Voici les taches:
- Corriger les faute
- Ameliorer la documentation

[[lien-vers-autre-note]] #projet #urgent
```

**Après:**
```markdown
# Mon Projet

Aujourd'hui j'ai travaillé sur le projet. Voici les tâches:
- Corriger les fautes
- Améliorer la documentation

[[lien-vers-autre-note]] #projet #urgent
```

## Performances

### Vitesse de correction

Dépend du modèle et de la taille des notes:

- **llama3.1:8b**: ~5-10 secondes par note
- **mistral-nemo:12b**: ~8-15 secondes par note

Pour un dossier de 20 notes:
- Temps estimé: 2-5 minutes
- RAM utilisée: 5-8GB

### Optimisation

Pour de grandes quantités de notes:

1. Utilisez un modèle plus léger:
   ```bash
   TOOL_MODEL=llama3.1:8b
   ```

2. Traitez par dossiers plutôt que tout le vault d'un coup

3. Fermez les autres applications pour libérer de la RAM

## Dépannage

### Erreur: "Note introuvable"

Vérifiez le chemin (relatif depuis le vault):
```bash
# ❌ Mauvais
/Users/moi/Documents/Vault/Projets/note.md

# ✅ Correct
Projets/note.md
```

### Les corrections ne sont pas bonnes

1. Essayez un autre modèle (mistral-nemo:12b est excellent)
2. Vérifiez que le modèle supporte bien le français
3. Restaurez depuis les backups si nécessaire

### Processus trop lent

1. Utilisez llama3.1:8b (plus rapide)
2. Corrigez dossier par dossier
3. Vérifiez qu'aucun autre programme n'utilise Ollama

### Backups prennent trop de place

Nettoyez périodiquement:
```bash
# Supprimer les backups de plus de 7 jours
find .backups -name "*.md" -mtime +7 -delete
```

## Intégration dans un workflow

### Script automatique hebdomadaire

Créez `weekly_correction.sh`:

```bash
#!/bin/bash
source venv/bin/activate

# Corriger automatiquement les notes de la semaine
python -c "
from correct_spelling import SpellingCorrector
from dotenv import load_dotenv
import os

load_dotenv()
corrector = SpellingCorrector(os.getenv('OBSIDIAN_VAULT_PATH'))
corrector.correct_folder('Weekly', confirm=False)
"
```

### Ajout à cron (macOS/Linux)

```bash
# Éditer crontab
crontab -e

# Ajouter (tous les dimanches à 20h)
0 20 * * 0 cd /path/to/Correcteur-obsidian && ./weekly_correction.sh
```

## Limites

### Ce que le script ne peut PAS faire:

1. Corriger le style d'écriture (c'est voulu!)
2. Reformuler vos phrases
3. Corriger les erreurs de logique ou de sens
4. Traduire du contenu
5. Générer du nouveau contenu

### Notes volumineuses

Pour les notes >10,000 caractères:
- Le traitement sera plus lent
- Envisagez de découper la note

## Questions fréquentes

**Q: Les backups sont-ils obligatoires?**
R: Fortement recommandés! Vous pouvez les désactiver mais à vos risques.

**Q: Puis-je corriger pendant que Obsidian est ouvert?**
R: Oui, mais rechargez le vault après (Cmd+R sur macOS).

**Q: Le formatage Markdown est vraiment préservé?**
R: Oui, le prompt demande explicitement au modèle de ne pas toucher au Markdown.

**Q: Combien de temps garder les backups?**
R: Suggéré: 30 jours minimum, puis nettoyage manuel.

**Q: Puis-je annuler une correction?**
R: Oui, via les backups dans `.backups/` avec le timestamp.
