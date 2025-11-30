#!/usr/bin/env python3
"""
Démonstration de la correction orthographique
Crée une note de test avec des fautes et la corrige
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from obsidian_tools import ObsidianTools
from correct_spelling import SpellingCorrector


def main():
    """Démonstration de la correction."""
    load_dotenv()

    VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "")

    if not VAULT_PATH:
        print("❌ Erreur: Définissez OBSIDIAN_VAULT_PATH dans .env")
        sys.exit(1)

    vault_path = Path(VAULT_PATH).resolve()
    if not vault_path.exists():
        print(f"❌ Erreur: Le vault n'existe pas: {vault_path}")
        sys.exit(1)

    print("=" * 70)
    print("🧪 Démonstration de Correction Orthographique")
    print("=" * 70)

    # Créer un dossier de test
    test_folder = "Demo_Correction"
    test_note = f"{test_folder}/test.md"

    tools = ObsidianTools(str(vault_path))

    # Contenu avec des fautes intentionnelles
    faulty_content = """# Mon Projet de Démonstration

Aujourdhui jai travailler sur mon projet Obsidian. Voici les taches que jai accomplie:

## Objectifs

- Corriger les faute d'orthographe
- Ameliorer la documentation
- Tester le systeme de correction

## Notes

Le projet avance bien. Jai rencontrer quelque difficulté, mais rien de grave.
Les resultat sont encourageant!

[[lien-vers-autre-note]] #projet #demo #urgent

## Code

```python
# Ce code ne doit PAS être modifié
def exemple():
    print("Hello World")
```

## Conclusion

Cest un bon debut. Jai hate de voir les amelioration!
"""

    print(f"\n📝 Création de la note de test: {test_note}")
    result = tools.write_note(test_note, faulty_content)
    print(f"   {result}")

    print(f"\n📖 Contenu AVANT correction:")
    print("=" * 70)
    print(faulty_content)
    print("=" * 70)

    input("\n⏸️  Appuyez sur Entrée pour lancer la correction...")

    # Corriger la note
    print(f"\n🔧 Correction en cours...")
    MODEL = os.getenv("TOOL_MODEL", os.getenv("MAIN_MODEL", "llama3.1:8b"))
    corrector = SpellingCorrector(str(vault_path), model=MODEL)

    correction_result = corrector.correct_note(test_note, create_backup=True)

    if correction_result["success"]:
        print(f"\n✅ Correction terminée!")

        if correction_result.get("changes"):
            print(f"   ✓ Des corrections ont été appliquées")

            # Afficher le contenu corrigé
            corrected_content = tools.read_note(test_note)
            print(f"\n📖 Contenu APRÈS correction:")
            print("=" * 70)
            print(corrected_content.replace(f"Contenu de {test_note}:\n\n", ""))
            print("=" * 70)

            if correction_result.get("backup"):
                print(f"\n💾 Backup créé: {correction_result['backup']}")

            print("\n📊 Vérifications:")
            print("   ✓ Le formatage Markdown est-il préservé?")
            print("   ✓ Les liens [[]] et tags # sont-ils intacts?")
            print("   ✓ Le code est-il inchangé?")
            print("   ✓ Les fautes sont-elles corrigées?")

        else:
            print(f"   ➖ Aucune correction nécessaire (déjà parfait!)")

    else:
        print(f"\n❌ Erreur: {correction_result.get('error')}")

    print("\n" + "=" * 70)
    print("🎬 Démonstration terminée!")
    print("=" * 70)
    print(f"\nLa note de test se trouve dans: {test_folder}/")
    print(f"Vous pouvez la supprimer ou la conserver pour vos tests.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrompu")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
