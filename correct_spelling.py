#!/usr/bin/env python3
"""
Script de correction orthographique pour les notes Obsidian
Corrige automatiquement toutes les notes d'un dossier spécifié
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from obsidian_tools import ObsidianTools
from langchain_community.llms import Ollama
from datetime import datetime
import shutil


class SpellingCorrector:
    """Correcteur orthographique pour notes Obsidian."""

    def __init__(self, vault_path: str, model: str = "llama3.1:8b"):
        """
        Initialise le correcteur.

        Args:
            vault_path: Chemin vers le vault Obsidian
            model: Modèle Ollama à utiliser
        """
        self.tools = ObsidianTools(vault_path)
        self.vault_path = Path(vault_path)

        # LLM optimisé pour la correction orthographique
        self.llm = Ollama(
            model=model,
            base_url="http://localhost:11434",
            temperature=0.1,  # Température basse pour corrections précises
        )

    def create_backup(self, note_path: Path) -> Path:
        """
        Crée une sauvegarde de la note avant modification.

        Args:
            note_path: Chemin de la note

        Returns:
            Chemin du fichier de backup
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.vault_path / ".backups"
        backup_dir.mkdir(exist_ok=True)

        relative_path = note_path.relative_to(self.vault_path)
        backup_path = backup_dir / f"{relative_path.stem}_{timestamp}.md"
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(note_path, backup_path)
        return backup_path

    def correct_text(self, text: str, language: str = "français") -> str:
        """
        Corrige l'orthographe d'un texte.

        Args:
            text: Texte à corriger
            language: Langue du texte

        Returns:
            Texte corrigé
        """
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

        try:
            corrected = self.llm.invoke(prompt)
            # Nettoyer la réponse au cas où le modèle ajoute des explications
            return corrected.strip()
        except Exception as e:
            print(f"⚠️  Erreur lors de la correction: {e}")
            return text  # Retourner le texte original en cas d'erreur

    def correct_note(self, note_path: str, create_backup: bool = True) -> dict:
        """
        Corrige l'orthographe d'une note.

        Args:
            note_path: Chemin relatif de la note
            create_backup: Si True, crée une sauvegarde avant modification

        Returns:
            Dict avec le résultat de la correction
        """
        full_path = self.vault_path / note_path

        if not full_path.exists():
            return {
                "success": False,
                "note": note_path,
                "error": "Note introuvable"
            }

        # Lire le contenu
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "note": note_path,
                "error": f"Erreur de lecture: {e}"
            }

        # Créer un backup si demandé
        backup_path = None
        if create_backup:
            backup_path = self.create_backup(full_path)

        # Corriger le texte
        print(f"  🔍 Correction de {note_path}...")
        corrected_content = self.correct_text(original_content)

        # Vérifier s'il y a des changements
        if corrected_content == original_content:
            print(f"  ✓ Aucune correction nécessaire")
            return {
                "success": True,
                "note": note_path,
                "changes": False,
                "backup": str(backup_path) if backup_path else None
            }

        # Écrire le contenu corrigé
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(corrected_content)

            print(f"  ✓ Corrigé et sauvegardé")
            return {
                "success": True,
                "note": note_path,
                "changes": True,
                "backup": str(backup_path) if backup_path else None
            }
        except Exception as e:
            # Restaurer le backup en cas d'erreur
            if backup_path and backup_path.exists():
                shutil.copy2(backup_path, full_path)

            return {
                "success": False,
                "note": note_path,
                "error": f"Erreur d'écriture: {e}"
            }

    def correct_folder(self, folder: str = "", pattern: str = "*.md",
                       create_backups: bool = True, confirm: bool = True) -> dict:
        """
        Corrige toutes les notes d'un dossier.

        Args:
            folder: Dossier à traiter (vide = racine)
            pattern: Pattern de fichiers (ex: '*.md')
            create_backups: Si True, crée des backups
            confirm: Si True, demande confirmation avant de commencer

        Returns:
            Dict avec les statistiques de correction
        """
        search_path = self.vault_path / folder if folder else self.vault_path

        if not search_path.exists():
            return {
                "success": False,
                "error": f"Dossier introuvable: {folder}"
            }

        # Lister les notes
        notes = list(search_path.glob(f"**/{pattern}"))

        if not notes:
            return {
                "success": False,
                "error": f"Aucune note trouvée dans {folder or 'le vault'}"
            }

        # Afficher le résumé
        print("=" * 70)
        print(f"📂 Dossier: {folder or 'Racine du vault'}")
        print(f"📝 Notes trouvées: {len(notes)}")
        print(f"💾 Backups: {'Oui' if create_backups else 'Non'}")
        print("=" * 70)

        # Demander confirmation
        if confirm:
            response = input(f"\n⚠️  Corriger {len(notes)} note(s) ? (o/n): ").strip().lower()
            if response != 'o':
                print("❌ Annulé")
                return {"success": False, "error": "Annulé par l'utilisateur"}

        # Traiter chaque note
        results = {
            "total": len(notes),
            "corrected": 0,
            "unchanged": 0,
            "errors": 0,
            "details": []
        }

        print(f"\n🚀 Début de la correction...\n")

        for i, note_path in enumerate(notes, 1):
            relative_path = str(note_path.relative_to(self.vault_path))
            print(f"[{i}/{len(notes)}] {relative_path}")

            result = self.correct_note(relative_path, create_backup=create_backups)
            results["details"].append(result)

            if result["success"]:
                if result.get("changes"):
                    results["corrected"] += 1
                else:
                    results["unchanged"] += 1
            else:
                results["errors"] += 1
                print(f"  ❌ {result.get('error', 'Erreur inconnue')}")

            print()  # Ligne vide entre les notes

        # Afficher le résumé final
        print("=" * 70)
        print("📊 RÉSUMÉ")
        print("=" * 70)
        print(f"Total: {results['total']} notes")
        print(f"✅ Corrigées: {results['corrected']}")
        print(f"➖ Inchangées: {results['unchanged']}")
        print(f"❌ Erreurs: {results['errors']}")

        if create_backups and results['corrected'] > 0:
            backup_dir = self.vault_path / ".backups"
            print(f"\n💾 Backups sauvegardés dans: {backup_dir}")

        print("=" * 70)

        results["success"] = True
        return results


def main():
    """Point d'entrée principal."""
    load_dotenv()

    # Configuration
    VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "")
    MODEL = os.getenv("TOOL_MODEL", os.getenv("MAIN_MODEL", "llama3.1:8b"))

    if not VAULT_PATH:
        print("❌ Erreur: Définissez OBSIDIAN_VAULT_PATH dans .env")
        sys.exit(1)

    vault_path = Path(VAULT_PATH).resolve()
    if not vault_path.exists():
        print(f"❌ Erreur: Le vault n'existe pas: {vault_path}")
        sys.exit(1)

    print("=" * 70)
    print("📝 Correcteur Orthographique Obsidian")
    print("=" * 70)
    print(f"📂 Vault: {vault_path}")
    print(f"🧠 Modèle: {MODEL}")
    print("=" * 70)

    # Créer le correcteur
    corrector = SpellingCorrector(str(vault_path), model=MODEL)

    # Menu
    print("\nOptions:")
    print("1. Corriger un dossier spécifique")
    print("2. Corriger une note spécifique")
    print("3. Corriger tout le vault (ATTENTION!)")
    print("4. Quitter")

    choice = input("\nVotre choix (1-4): ").strip()

    try:
        if choice == "1":
            folder = input("\nDossier à corriger (ex: 'Projets'): ").strip()
            results = corrector.correct_folder(folder=folder)

        elif choice == "2":
            note_path = input("\nChemin de la note (ex: 'Projets/ma-note.md'): ").strip()
            if not note_path:
                print("❌ Chemin vide")
                sys.exit(1)

            result = corrector.correct_note(note_path)
            if result["success"]:
                if result.get("changes"):
                    print(f"\n✅ Note corrigée: {note_path}")
                else:
                    print(f"\n✓ Aucune correction nécessaire: {note_path}")
            else:
                print(f"\n❌ Erreur: {result.get('error')}")

        elif choice == "3":
            print("\n⚠️  ATTENTION: Ceci va corriger TOUTES les notes du vault!")
            confirm = input("Êtes-vous VRAIMENT sûr? (tapez 'OUI' en majuscules): ").strip()
            if confirm != "OUI":
                print("❌ Annulé")
                sys.exit(0)

            results = corrector.correct_folder(folder="", confirm=False)

        elif choice == "4":
            print("\n👋 Au revoir!")
            sys.exit(0)

        else:
            print("❌ Choix invalide")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n❌ Interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
