"""
Configuration des agents CrewAI pour la gestion des notes Obsidian
"""
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
from typing import List


class ObsidianAgentsConfig:
    """Configuration des agents pour Obsidian."""

    def __init__(self, vault_path: str, main_model: str = "llama3.1:8b", tool_model: str = "llama3.1:8b"):
        """
        Initialise la configuration des agents.

        Args:
            vault_path: Chemin vers le vault Obsidian
            main_model: Modèle Ollama principal pour la réflexion et la planification
            tool_model: Modèle Ollama spécialisé pour les tool calls (plus fiable)
        """
        self.vault_path = vault_path
        self.main_model = main_model
        self.tool_model = tool_model

        # LLM principal pour la réflexion et la coordination
        self.main_llm = Ollama(
            model=main_model,
            base_url="http://localhost:11434",
            temperature=0.7,
        )

        # LLM spécialisé pour les tool calls (température basse pour plus de précision)
        self.tool_llm = Ollama(
            model=tool_model,
            base_url="http://localhost:11434",
            temperature=0.1,  # Très bas pour des tool calls précis
            num_predict=1024,
        )

    def create_researcher_agent(self, tools: List) -> Agent:
        """
        Crée l'agent chercheur qui explore les notes.
        Utilise le modèle spécialisé pour les tool calls.
        """
        return Agent(
            role="Chercheur de notes Obsidian",
            goal="Explorer et analyser les notes Obsidian pour trouver les informations pertinentes",
            backstory="""Tu es un expert en recherche d'information dans des bases de connaissances.
            Tu maîtrises parfaitement la navigation dans les notes Obsidian et tu sais comment
            trouver rapidement les informations pertinentes. Tu utilises efficacement les outils
            de recherche et de lecture pour comprendre le contenu du vault.""",
            tools=tools,
            llm=self.tool_llm,  # Utilise le modèle optimisé pour les tool calls
            verbose=True,
            allow_delegation=False,
        )

    def create_analyst_agent(self) -> Agent:
        """
        Crée l'agent analyste qui réfléchit sur les informations.
        Utilise le modèle principal pour la réflexion.
        """
        return Agent(
            role="Analyste de contenu",
            goal="Analyser les informations trouvées et déterminer les modifications nécessaires",
            backstory="""Tu es un analyste expert qui comprend la structure et le contenu des notes.
            Tu sais identifier les patterns, les connexions entre les notes, et déterminer
            quelles modifications seraient les plus pertinentes. Tu ne fais pas d'actions directes,
            tu analyses et recommandes.""",
            tools=[],  # Pas d'outils, seulement de la réflexion
            llm=self.main_llm,
            verbose=True,
            allow_delegation=True,
        )

    def create_editor_agent(self, tools: List) -> Agent:
        """
        Crée l'agent éditeur qui modifie les notes.
        Utilise le modèle spécialisé pour les tool calls.
        """
        return Agent(
            role="Éditeur de notes Obsidian",
            goal="Modifier et créer des notes Obsidian selon les recommandations de l'analyste",
            backstory="""Tu es un éditeur expert en Markdown et en format Obsidian.
            Tu sais comment structurer des notes, utiliser les liens internes [[]], les tags,
            et maintenir une cohérence dans le vault. Tu exécutes précisément les modifications
            demandées tout en respectant les bonnes pratiques de formatage.""",
            tools=tools,
            llm=self.tool_llm,  # Utilise le modèle optimisé pour les tool calls
            verbose=True,
            allow_delegation=False,
        )

    def create_coordinator_agent(self) -> Agent:
        """
        Crée l'agent coordinateur qui orchestre le travail.
        Utilise le modèle principal.
        """
        return Agent(
            role="Coordinateur",
            goal="Coordonner les agents pour accomplir les tâches demandées par l'utilisateur",
            backstory="""Tu es un coordinateur expert qui sait comment orchestrer une équipe
            d'agents pour accomplir des tâches complexes. Tu délègues efficacement le travail
            au chercheur, à l'analyste et à l'éditeur selon les besoins.""",
            tools=[],
            llm=self.main_llm,
            verbose=True,
            allow_delegation=True,
        )


def create_research_task(agent: Agent, query: str) -> Task:
    """Crée une tâche de recherche."""
    return Task(
        description=f"""Recherche des informations dans le vault Obsidian concernant: {query}

        Utilise les outils de recherche et de lecture pour:
        1. Trouver les notes pertinentes
        2. Lire leur contenu
        3. Résumer les informations trouvées

        Sois précis et complet dans tes recherches.""",
        agent=agent,
        expected_output="Un résumé détaillé des informations trouvées avec les chemins des notes concernées."
    )


def create_analysis_task(agent: Agent, research_context: str, user_request: str) -> Task:
    """Crée une tâche d'analyse."""
    return Task(
        description=f"""Analyse les informations suivantes et détermine les modifications nécessaires:

        Demande de l'utilisateur: {user_request}

        Contexte de recherche: {research_context}

        Détermine:
        1. Quelles notes doivent être modifiées
        2. Quelles modifications précises doivent être faites
        3. Si de nouvelles notes doivent être créées

        Fournis un plan d'action clair et détaillé.""",
        agent=agent,
        expected_output="Un plan d'action détaillé avec les modifications à effectuer sur chaque note."
    )


def create_editing_task(agent: Agent, action_plan: str) -> Task:
    """Crée une tâche d'édition."""
    return Task(
        description=f"""Exécute le plan d'action suivant pour modifier les notes Obsidian:

        {action_plan}

        Utilise les outils d'écriture pour:
        1. Créer ou modifier les notes selon le plan
        2. Respecter le format Markdown et les conventions Obsidian
        3. Vérifier que les modifications sont correctes

        Documente chaque modification effectuée.""",
        agent=agent,
        expected_output="Un rapport des modifications effectuées avec succès."
    )
