# Guide Rapide - Correction Orthographique

## 🚀 Démarrage en 3 étapes

### 1. Configurer (une seule fois)

Vérifiez que `.env` contient le chemin de votre vault:

```bash
cat .env | grep OBSIDIAN_VAULT_PATH
```

Si vide ou incorrect:
```bash
nano .env
# Modifiez: OBSIDIAN_VAULT_PATH=/chemin/vers/votre/vault
```

### 2. Activer l'environnement

```bash
source venv/bin/activate
```

### 3. Lancer la correction

```bash
python correct_spelling.py
```

## 📖 Exemples d'utilisation

### Cas 1: Corriger les notes d'un projet

```bash
python correct_spelling.py
```

```
Votre choix: 1
Dossier: Projets/SiteWeb
```

Le script va:
- Lister toutes les notes du dossier
- Vous demander confirmation
- Créer un backup de chaque note
- Corriger les fautes
- Afficher un résumé

**Résultat exemple:**
```
📊 RÉSUMÉ
Total: 12 notes
✅ Corrigées: 8
➖ Inchangées: 4
❌ Erreurs: 0

💾 Backups sauvegardés dans: /vault/.backups
```

### Cas 2: Corriger une note de meeting

```bash
python correct_spelling.py
```

```
Votre choix: 2
Note: Meetings/2025-11-30-reunion-equipe.md
```

**Avant:**
```markdown
# Réunion Equipe

Aujourdhui nous avons discuter de:
- Les nouveau objectif
- Le plannification des tache
```

**Après:**
```markdown
# Réunion Équipe

Aujourd'hui nous avons discuté de:
- Les nouveaux objectifs
- La planification des tâches
```

### Cas 3: Test rapide (démo)

Pour voir le système en action:

```bash
python demo_correction.py
```

Cette démo:
1. Crée une note avec des fautes
2. Affiche le contenu avant
3. Corrige automatiquement
4. Affiche le contenu après
5. Montre que le Markdown est préservé

## 🎯 Cas d'usage typiques

### Corriger vos notes quotidiennes

```bash
python correct_spelling.py
# Choix: 1
# Dossier: Daily
```

### Corriger avant de partager

```bash
python correct_spelling.py
# Choix: 2
# Note: Projets/Documentation/README.md
```

### Nettoyer un dossier entier

```bash
python correct_spelling.py
# Choix: 1
# Dossier: Archive/2024
```

## 💡 Astuces

### Astuce 1: Workflow hebdomadaire

Créez une routine chaque dimanche:

```bash
cd ~/obsidian-multiagent
source venv/bin/activate
python correct_spelling.py
# Corrigez vos notes de la semaine
```

### Astuce 2: Vérification avant présentation

Avant de présenter ou partager:

```bash
python correct_spelling.py
# Corrigez le dossier concerné
```

### Astuce 3: Test sur une note d'abord

Testez d'abord sur une seule note:

```bash
python correct_spelling.py
# Choix: 2
# Note: test.md
```

Vérifiez le résultat, puis lancez sur le dossier complet.

## ⚠️ Points importants

### ✅ Ce qui est préservé:

- Formatage Markdown (##, -, *, etc.)
- Liens internes [[note]]
- Tags #tag
- Blocs de code ```
- URLs et liens
- Noms propres (généralement)

### ❌ Ce qui est corrigé:

- Fautes d'orthographe
- Fautes de grammaire
- Ponctuation
- Accords
- Accents

### 💾 Sécurité:

- **Backups automatiques** dans `.backups/`
- Nommés avec timestamp: `note_20251130_153045.md`
- Restauration facile si besoin

## 🔧 Dépannage rapide

### "Note introuvable"

Le chemin doit être **relatif** au vault:

```
❌ Mauvais: /Users/moi/Vault/Projets/note.md
✅ Correct: Projets/note.md
```

### Corrections bizarres

Essayez un autre modèle dans `.env`:

```bash
nano .env
# Changez: TOOL_MODEL=mistral-nemo:12b
```

### Processus lent

Normal! Compter ~5-10 secondes par note.

Pour 20 notes = ~2-5 minutes.

### Restaurer une note

```bash
# Trouver le backup
ls .backups/

# Restaurer
cp .backups/ma-note_20251130_153045.md Projets/ma-note.md
```

## 📊 Performances attendues

| Modèle | Vitesse | Qualité | RAM |
|--------|---------|---------|-----|
| llama3.1:8b | ⚡⚡⚡ Rapide | ✅ Bonne | 5GB |
| mistral-nemo:12b | ⚡⚡ Moyen | ✅✅ Excellente | 7GB |
| qwen2.5:7b | ⚡⚡⚡ Rapide | ✅✅ Très bonne (FR) | 5GB |

## 🎓 Pour aller plus loin

### Documentation complète

Voir [CORRECTION_GUIDE.md](CORRECTION_GUIDE.md) pour:
- Configuration avancée
- Automatisation (cron)
- Intégration dans workflows
- Toutes les options

### Scripts Python personnalisés

Vous pouvez importer et utiliser directement:

```python
from correct_spelling import SpellingCorrector
from dotenv import load_dotenv
import os

load_dotenv()
corrector = SpellingCorrector(os.getenv('OBSIDIAN_VAULT_PATH'))

# Corriger un dossier sans confirmation
corrector.correct_folder('Projets', confirm=False)
```

## ❓ Questions fréquentes

**Q: Est-ce que ça fonctionne en français?**
✅ Oui! Utilisez llama3.1:8b ou qwen2.5:7b (excellent en FR)

**Q: Puis-je annuler une correction?**
✅ Oui, via les backups dans `.backups/`

**Q: Le formatage Markdown est-il vraiment préservé?**
✅ Oui, testé et vérifié. Le prompt demande explicitement au modèle de ne pas toucher au Markdown.

**Q: Combien de temps ça prend?**
⏱️ ~5-10 secondes par note (selon le modèle)

**Q: Puis-je corriger pendant qu'Obsidian est ouvert?**
✅ Oui, mais rechargez le vault après (Cmd+R)

## 📞 Besoin d'aide?

1. Testez d'abord avec `python demo_correction.py`
2. Consultez [CORRECTION_GUIDE.md](CORRECTION_GUIDE.md)
3. Vérifiez qu'Ollama fonctionne: `ollama list`
4. Vérifiez votre `.env`

---

**Prêt à commencer?**

```bash
source venv/bin/activate
python correct_spelling.py
```

🎉 Bon courage avec vos corrections!
