#!/usr/bin/env python3
"""
Version simplifiée compatible avec CrewAI 0.11.2
Système multi-agent pour gérer les notes Obsidian
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
from obsidian_tools import ObsidianTools


def main():
    """Point d'entrée principal."""
    load_dotenv()

    # Configuration
    VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "")
    MODEL = os.getenv("MAIN_MODEL", "llama3.1:8b")

    if not VAULT_PATH:
        print("❌ Erreur: Définissez OBSIDIAN_VAULT_PATH dans .env")
        print("Exemple: OBSIDIAN_VAULT_PATH=/Users/votre-nom/Documents/MonVault")
        sys.exit(1)

    vault_path = Path(VAULT_PATH).resolve()
    if not vault_path.exists():
        print(f"❌ Erreur: Le vault n'existe pas: {vault_path}")
        sys.exit(1)

    print("=" * 70)
    print("🤖 Correcteur-obsidian System (Version Simplifiée)")
    print("=" * 70)
    print(f"📂 Vault: {vault_path}")
    print(f"🧠 Modèle: {MODEL}")
    print("=" * 70)

    # Initialiser les outils
    tools = ObsidianTools(str(vault_path))

    # Initialiser le LLM
    llm = Ollama(
        model=MODEL,
        base_url="http://localhost:11434",
        temperature=0.7,
    )

    # Menu interactif
    while True:
        print("\nQue voulez-vous faire ?")
        print("1. Lister toutes les notes")
        print("2. Rechercher dans les notes")
        print("3. Lire une note")
        print("4. Créer/Modifier une note")
        print("5. Quitter")
        print("=" * 70)

        choice = input("\nVotre choix (1-5): ").strip()

        if choice == "5":
            print("\n👋 Au revoir!")
            break

        try:
            if choice == "1":
                folder = input("Dossier (vide pour tout): ").strip()
                result = tools.list_notes(folder=folder)
                print("\n" + "=" * 70)
                print(result)
                print("=" * 70)

            elif choice == "2":
                query = input("Rechercher: ").strip()
                if not query:
                    print("❌ Recherche vide")
                    continue
                result = tools.search_notes(query=query)
                print("\n" + "=" * 70)
                print(result)
                print("=" * 70)

            elif choice == "3":
                note_path = input("Chemin de la note: ").strip()
                if not note_path:
                    print("❌ Chemin vide")
                    continue
                result = tools.read_note(note_path=note_path)
                print("\n" + "=" * 70)
                print(result)
                print("=" * 70)

            elif choice == "4":
                note_path = input("Chemin de la note: ").strip()
                if not note_path:
                    print("❌ Chemin vide")
                    continue

                print("Contenu (terminez par une ligne vide):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                content = "\n".join(lines)

                append = input("Ajouter au contenu existant? (o/n): ").strip().lower() == 'o'
                result = tools.write_note(note_path=note_path, content=content, append=append)
                print("\n" + "=" * 70)
                print(result)
                print("=" * 70)

            else:
                print("❌ Choix invalide")

        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
