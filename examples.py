#!/usr/bin/env python3
"""
Exemples d'utilisation programmatique du système Correcteur-obsidian
"""
import os
from dotenv import load_dotenv
from main import ObsidianMultiAgent


def example_1_simple_search():
    """Exemple 1: Recherche simple dans le vault."""
    print("\n" + "=" * 70)
    print("EXEMPLE 1: Recherche simple")
    print("=" * 70)

    load_dotenv()
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")

    system = ObsidianMultiAgent(
        vault_path=vault_path,
        main_model="llama3.1:8b",
        tool_model="llama3.1:8b"
    )

    result = system.execute_simple_task(
        "Liste toutes les notes qui contiennent le mot 'projet'"
    )

    print("\n📊 Résultat:")
    print(result)


def example_2_create_summary():
    """Exemple 2: Créer une note de synthèse."""
    print("\n" + "=" * 70)
    print("EXEMPLE 2: Création d'une note de synthèse")
    print("=" * 70)

    load_dotenv()
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")

    system = ObsidianMultiAgent(
        vault_path=vault_path,
        main_model="llama3.1:8b",
        tool_model="llama3.1:8b"
    )

    result = system.execute_complex_task(
        """Crée une note 'Synthèse Projets.md' qui contient:
        1. Une liste de tous les fichiers dans le dossier Projets
        2. Un résumé de chaque projet
        3. Les tags appropriés
        """
    )

    print("\n📊 Résultat:")
    print(result)


def example_3_reorganize_notes():
    """Exemple 3: Réorganiser des notes avec des tags."""
    print("\n" + "=" * 70)
    print("EXEMPLE 3: Ajout de tags automatique")
    print("=" * 70)

    load_dotenv()
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")

    system = ObsidianMultiAgent(
        vault_path=vault_path,
        main_model="llama3.1:8b",
        tool_model="llama3.1:8b"
    )

    result = system.execute_complex_task(
        """Pour chaque note qui contient les mots 'urgent' ou 'important':
        1. Ajoute le tag #priorité en haut de la note
        2. Ajoute une section '## Actions requises' si elle n'existe pas
        3. Liste ces notes dans une note 'Priorités.md'
        """
    )

    print("\n📊 Résultat:")
    print(result)


def example_4_custom_models():
    """Exemple 4: Utiliser des modèles différents."""
    print("\n" + "=" * 70)
    print("EXEMPLE 4: Configuration avec modèles différents")
    print("=" * 70)

    load_dotenv()
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")

    # Utiliser mistral-nemo pour les tool calls (meilleur)
    # et llama3.1 pour la réflexion
    system = ObsidianMultiAgent(
        vault_path=vault_path,
        main_model="llama3.1:8b",        # Réflexion
        tool_model="mistral-nemo:12b"    # Tool calls précis
    )

    result = system.execute_complex_task(
        "Crée une table des matières de mon vault avec tous les dossiers et fichiers"
    )

    print("\n📊 Résultat:")
    print(result)


def example_5_batch_processing():
    """Exemple 5: Traitement par lot."""
    print("\n" + "=" * 70)
    print("EXEMPLE 5: Traitement par lot")
    print("=" * 70)

    load_dotenv()
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")

    system = ObsidianMultiAgent(
        vault_path=vault_path,
        main_model="llama3.1:8b",
        tool_model="llama3.1:8b"
    )

    tasks = [
        "Liste toutes les notes sans tags",
        "Trouve toutes les notes créées cette semaine",
        "Identifie les notes qui contiennent des TODO"
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n🔄 Tâche {i}/{len(tasks)}: {task}")
        result = system.execute_simple_task(task)
        print(f"✅ Terminé")


def example_6_daily_note_template():
    """Exemple 6: Créer une note quotidienne avec template."""
    print("\n" + "=" * 70)
    print("EXEMPLE 6: Note quotidienne automatique")
    print("=" * 70)

    load_dotenv()
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")

    system = ObsidianMultiAgent(
        vault_path=vault_path,
        main_model="llama3.1:8b",
        tool_model="llama3.1:8b"
    )

    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    result = system.execute_complex_task(
        f"""Crée une note quotidienne 'Daily/{today}.md' avec:
        1. Un titre avec la date
        2. Une section ## Objectifs du jour (vide pour que je la remplisse)
        3. Une section ## Notes rapides
        4. Une section ## Liens avec les 5 dernières notes que j'ai modifiées
        5. Les tags #daily et #journal
        """
    )

    print("\n📊 Résultat:")
    print(result)


if __name__ == "__main__":
    print("🤖 Exemples d'utilisation Correcteur-obsidian")
    print("=" * 70)
    print("\nChoisissez un exemple à exécuter:")
    print("1. Recherche simple")
    print("2. Créer une note de synthèse")
    print("3. Ajouter des tags automatiquement")
    print("4. Utiliser des modèles différents")
    print("5. Traitement par lot")
    print("6. Créer une note quotidienne")
    print("0. Quitter")

    choice = input("\nVotre choix (0-6): ").strip()

    examples = {
        "1": example_1_simple_search,
        "2": example_2_create_summary,
        "3": example_3_reorganize_notes,
        "4": example_4_custom_models,
        "5": example_5_batch_processing,
        "6": example_6_daily_note_template,
    }

    if choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
    elif choice == "0":
        print("\n👋 Au revoir!")
    else:
        print("\n❌ Choix invalide")
