# Contribuer au projet

Merci de votre intérêt pour contribuer au Correcteur Obsidian! 🎉

## Comment contribuer

### Rapporter un bug

Si vous trouvez un bug:

1. Vérifiez qu'il n'a pas déjà été rapporté dans les [Issues](../../issues)
2. Créez une nouvelle issue avec:
   - Description claire du problème
   - Étapes pour reproduire
   - Comportement attendu vs comportement observé
   - Votre environnement (OS, Python, versions)
   - Logs/captures d'écran si pertinent

### Suggérer une fonctionnalité

Pour proposer une nouvelle fonctionnalité:

1. Vérifiez qu'elle n'est pas déjà proposée dans les Issues
2. Créez une issue avec le tag "enhancement"
3. Décrivez:
   - Le problème que ça résout
   - Comment ça devrait fonctionner
   - Des exemples d'utilisation

### Contribuer du code

1. **Fork** le projet
2. Créez une **branche** pour votre fonctionnalité:
   ```bash
   git checkout -b feature/ma-super-fonctionnalite
   ```
3. **Codez** en suivant les conventions du projet
4. **Testez** vos modifications
5. **Committez** avec des messages clairs:
   ```bash
   git commit -m "feat: ajout de la fonctionnalité X"
   ```
6. **Push** vers votre fork:
   ```bash
   git push origin feature/ma-super-fonctionnalite
   ```
7. Créez une **Pull Request**

## Conventions de code

### Python

- Suivre PEP 8
- Docstrings pour toutes les fonctions publiques
- Type hints quand approprié
- Commentaires en français pour ce projet

### Messages de commit

Format: `type(scope): message`

Types:
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation uniquement
- `style`: Formatage, pas de changement de code
- `refactor`: Refactoring sans changement fonctionnel
- `test`: Ajout/modification de tests
- `chore`: Maintenance (dépendances, etc.)

Exemples:
```
feat(correction): ajout support des tables Markdown
fix(tools): correction lecture notes avec accents
docs(readme): mise à jour installation
```

## Structure du projet

```
Correcteur-obsidian/
├── correct_spelling.py     # Correction orthographique
├── main_simple.py          # Interface simple
├── obsidian_tools.py       # API Obsidian
├── agents_config.py        # Configuration agents
├── tests/                  # Tests (à créer)
└── docs/                   # Documentation
```

## Tests

Avant de soumettre une PR:

```bash
# Activer le venv
source venv/bin/activate

# Tester les imports
python test_simple.py

# Tester Ollama
python test_ollama.py

# Tester la démo
python demo_correction.py
```

## Documentation

Si vous ajoutez une fonctionnalité:

1. Mettez à jour README.md
2. Ajoutez des exemples
3. Créez un guide si nécessaire (dans docs/)
4. Mettez à jour INDEX.md

## Licence

En contribuant, vous acceptez que votre code soit sous licence MIT.

## Questions?

N'hésitez pas à:
- Ouvrir une issue pour discuter
- Commenter sur une issue existante
- Demander de l'aide

Merci de contribuer! 🙏
