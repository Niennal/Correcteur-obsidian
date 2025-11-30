#!/usr/bin/env python3
"""
Script principal pour gérer les notes Obsidian avec CrewAI et Ollama
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from crewai import Crew, Process

from obsidian_tools import (
    ObsidianReadTool,
    ObsidianWriteTool,
    ObsidianListTool,
    ObsidianSearchTool,
)
from agents_config import (
    ObsidianAgentsConfig,
    create_research_task,
    create_analysis_task,
    create_editing_task,
)


class ObsidianMultiAgent:
    """Système multi-agent pour gérer les notes Obsidian."""

    def __init__(self, vault_path: str, main_model: str = "llama3.1:8b", tool_model: str = "llama3.1:8b"):
        """
        Initialise le système multi-agent.

        Args:
            vault_path: Chemin vers le vault Obsidian
            main_model: Modèle Ollama pour la réflexion (défaut: llama3.1:8b)
            tool_model: Modèle Ollama pour les tool calls (défaut: llama3.1:8b)
        """
        self.vault_path = Path(vault_path).resolve()

        if not self.vault_path.exists():
            raise ValueError(f"Le vault Obsidian n'existe pas: {self.vault_path}")

        print(f"📂 Vault Obsidian: {self.vault_path}")
        print(f"🧠 Modèle principal: {main_model}")
        print(f"🔧 Modèle tool calls: {tool_model}\n")

        # Initialiser les outils
        self.read_tool = ObsidianReadTool(vault_path=str(self.vault_path))
        self.write_tool = ObsidianWriteTool(vault_path=str(self.vault_path))
        self.list_tool = ObsidianListTool(vault_path=str(self.vault_path))
        self.search_tool = ObsidianSearchTool(vault_path=str(self.vault_path))

        # Configurer les agents
        self.config = ObsidianAgentsConfig(
            vault_path=str(self.vault_path),
            main_model=main_model,
            tool_model=tool_model,
        )

    def execute_simple_task(self, user_request: str):
        """
        Exécute une tâche simple avec un seul agent.
        Utile pour des actions directes comme lire une note ou chercher quelque chose.

        Args:
            user_request: La demande de l'utilisateur
        """
        print("🚀 Mode simple - Exécution avec agent unique\n")

        # Créer l'agent chercheur avec tous les outils
        all_tools = [self.read_tool, self.write_tool, self.list_tool, self.search_tool]
        researcher = self.config.create_researcher_agent(tools=all_tools)

        # Créer une tâche simple
        from crewai import Task
        task = Task(
            description=user_request,
            agent=researcher,
            expected_output="Résultat de la tâche demandée"
        )

        # Créer et exécuter le crew
        crew = Crew(
            agents=[researcher],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return result

    def execute_complex_task(self, user_request: str):
        """
        Exécute une tâche complexe avec plusieurs agents.
        Utilise le workflow complet: recherche → analyse → édition.

        Args:
            user_request: La demande de l'utilisateur
        """
        print("🚀 Mode complexe - Workflow multi-agents\n")

        # Créer les agents
        researcher = self.config.create_researcher_agent(
            tools=[self.read_tool, self.list_tool, self.search_tool]
        )
        analyst = self.config.create_analyst_agent()
        editor = self.config.create_editor_agent(
            tools=[self.write_tool, self.read_tool]
        )

        # Créer les tâches
        from crewai import Task

        # Tâche 1: Recherche
        research_task = Task(
            description=f"""Recherche toutes les informations pertinentes dans le vault Obsidian pour: {user_request}

            Utilise les outils pour:
            1. Lister les notes pertinentes
            2. Rechercher des mots-clés
            3. Lire le contenu des notes importantes

            Fournis un résumé complet de ce que tu trouves.""",
            agent=researcher,
            expected_output="Résumé des notes et informations trouvées"
        )

        # Tâche 2: Analyse
        analysis_task = Task(
            description=f"""Analyse les résultats de la recherche et détermine comment répondre à: {user_request}

            Crée un plan d'action détaillé qui spécifie:
            1. Quelles notes modifier ou créer
            2. Quel contenu ajouter ou modifier
            3. L'ordre des opérations

            Sois précis et détaillé dans tes recommandations.""",
            agent=analyst,
            expected_output="Plan d'action détaillé pour les modifications",
            context=[research_task]
        )

        # Tâche 3: Édition
        editing_task = Task(
            description="""Exécute le plan d'action pour modifier les notes.

            Utilise les outils d'écriture pour:
            1. Créer ou modifier les notes selon le plan
            2. Respecter le format Markdown
            3. Vérifier que tout fonctionne

            Rapporte chaque modification effectuée.""",
            agent=editor,
            expected_output="Rapport des modifications effectuées",
            context=[analysis_task]
        )

        # Créer et exécuter le crew
        crew = Crew(
            agents=[researcher, analyst, editor],
            tasks=[research_task, analysis_task, editing_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return result


def main():
    """Point d'entrée principal."""
    load_dotenv()

    # Configuration
    VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "")
    MAIN_MODEL = os.getenv("MAIN_MODEL", "llama3.1:8b")
    TOOL_MODEL = os.getenv("TOOL_MODEL", "llama3.1:8b")

    if not VAULT_PATH:
        print("❌ Erreur: Veuillez définir OBSIDIAN_VAULT_PATH dans le fichier .env")
        print("Exemple: OBSIDIAN_VAULT_PATH=/Users/votre-nom/Documents/MonVault")
        sys.exit(1)

    print("=" * 70)
    print("🤖 Correcteur-obsidian System")
    print("=" * 70)

    try:
        system = ObsidianMultiAgent(
            vault_path=VAULT_PATH,
            main_model=MAIN_MODEL,
            tool_model=TOOL_MODEL,
        )

        # Menu interactif
        while True:
            print("\n" + "=" * 70)
            print("Que voulez-vous faire ?")
            print("=" * 70)
            print("1. Tâche simple (recherche, lecture)")
            print("2. Tâche complexe (workflow complet avec modifications)")
            print("3. Quitter")
            print("=" * 70)

            choice = input("\nVotre choix (1-3): ").strip()

            if choice == "3":
                print("\n👋 Au revoir!")
                break

            if choice not in ["1", "2"]:
                print("❌ Choix invalide")
                continue

            user_request = input("\n📝 Décrivez votre demande: ").strip()

            if not user_request:
                print("❌ Demande vide")
                continue

            try:
                print("\n" + "=" * 70)
                if choice == "1":
                    result = system.execute_simple_task(user_request)
                else:
                    result = system.execute_complex_task(user_request)

                print("\n" + "=" * 70)
                print("✅ RÉSULTAT:")
                print("=" * 70)
                print(result)
                print("=" * 70)

            except Exception as e:
                print(f"\n❌ Erreur lors de l'exécution: {e}")
                import traceback
                traceback.print_exc()

    except Exception as e:
        print(f"\n❌ Erreur d'initialisation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
