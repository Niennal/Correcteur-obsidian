"""
Outils pour interagir avec les notes Obsidian
Version simplifiée compatible avec CrewAI 0.11.2
"""
import os
from pathlib import Path
from typing import Optional


class ObsidianTools:
    """Classe contenant tous les outils Obsidian."""

    def __init__(self, vault_path: str):
        """
        Initialise les outils Obsidian.

        Args:
            vault_path: Chemin absolu vers le vault Obsidian
        """
        self.vault_path = Path(vault_path)

    def read_note(self, note_path: str) -> str:
        """
        Lit le contenu d'une note Obsidian.

        Args:
            note_path: Chemin relatif de la note depuis le vault

        Returns:
            Contenu de la note ou message d'erreur
        """
        full_path = self.vault_path / note_path

        if not full_path.exists():
            return f"Erreur: La note '{note_path}' n'existe pas dans le vault."

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"Contenu de {note_path}:\n\n{content}"
        except Exception as e:
            return f"Erreur lors de la lecture de {note_path}: {str(e)}"

    def write_note(self, note_path: str, content: str, append: bool = False) -> str:
        """
        Écrit ou modifie le contenu d'une note Obsidian.

        Args:
            note_path: Chemin relatif de la note depuis le vault
            content: Contenu à écrire
            append: Si True, ajoute le contenu. Si False, remplace tout

        Returns:
            Message de confirmation ou d'erreur
        """
        full_path = self.vault_path / note_path

        # Créer les dossiers parents si nécessaire
        full_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            mode = 'a' if append else 'w'
            with open(full_path, mode, encoding='utf-8') as f:
                if append and full_path.exists():
                    f.write('\n\n')
                f.write(content)

            action = "ajouté à" if append else "écrit dans"
            return f"Succès: Contenu {action} {note_path}"
        except Exception as e:
            return f"Erreur lors de l'écriture dans {note_path}: {str(e)}"

    def list_notes(self, folder: str = "", pattern: str = "*.md") -> str:
        """
        Liste toutes les notes dans le vault ou un dossier spécifique.

        Args:
            folder: Sous-dossier à lister (vide pour la racine)
            pattern: Pattern de fichiers (ex: '*.md')

        Returns:
            Liste des notes trouvées
        """
        search_path = self.vault_path / folder if folder else self.vault_path

        if not search_path.exists():
            return f"Erreur: Le dossier '{folder}' n'existe pas dans le vault."

        try:
            notes = list(search_path.glob(f"**/{pattern}"))

            if not notes:
                return f"Aucune note trouvée dans {folder if folder else 'le vault'}."

            relative_notes = [str(note.relative_to(self.vault_path)) for note in notes]
            relative_notes.sort()

            result = f"Notes trouvées ({len(relative_notes)}):\n\n"
            result += "\n".join(f"- {note}" for note in relative_notes)
            return result
        except Exception as e:
            return f"Erreur lors du listage: {str(e)}"

    def search_notes(self, query: str, folder: str = "") -> str:
        """
        Recherche un texte dans toutes les notes Obsidian.

        Args:
            query: Texte à rechercher
            folder: Limiter la recherche à un dossier spécifique

        Returns:
            Notes contenant le texte recherché
        """
        search_path = self.vault_path / folder if folder else self.vault_path

        if not search_path.exists():
            return f"Erreur: Le dossier '{folder}' n'existe pas dans le vault."

        try:
            matches = []
            for note_path in search_path.glob("**/*.md"):
                try:
                    with open(note_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            relative_path = str(note_path.relative_to(self.vault_path))
                            # Extraire un contexte autour de la première occurrence
                            idx = content.lower().index(query.lower())
                            start = max(0, idx - 50)
                            end = min(len(content), idx + len(query) + 50)
                            context = content[start:end].replace('\n', ' ')
                            matches.append(f"- {relative_path}\n  Contexte: ...{context}...")
                except Exception:
                    continue

            if not matches:
                return f"Aucune note ne contient '{query}'."

            result = f"Notes contenant '{query}' ({len(matches)}):\n\n"
            result += "\n\n".join(matches)
            return result
        except Exception as e:
            return f"Erreur lors de la recherche: {str(e)}"


# Fonctions helper pour créer des tools compatibles avec CrewAI 0.11.2
def create_obsidian_tools(vault_path: str):
    """
    Crée une instance des outils Obsidian.

    Args:
        vault_path: Chemin vers le vault Obsidian

    Returns:
        Instance de ObsidianTools
    """
    return ObsidianTools(vault_path)
