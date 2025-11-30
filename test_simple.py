#!/usr/bin/env python3
"""
Test simple du système
"""
import os
from dotenv import load_dotenv

# Test d'import
print("Test des imports...")
try:
    from crewai import Agent, Task, Crew
    print("✅ CrewAI importé")
except Exception as e:
    print(f"❌ Erreur CrewAI: {e}")
    exit(1)

try:
    from langchain_community.llms import Ollama
    print("✅ Langchain Community importé")
except Exception as e:
    print(f"❌ Erreur Langchain: {e}")
    exit(1)

try:
    from obsidian_tools import ObsidianReadTool, ObsidianWriteTool
    print("✅ Obsidian Tools importé")
except Exception as e:
    print(f"❌ Erreur Obsidian Tools: {e}")
    exit(1)

# Test de connexion Ollama
print("\nTest de connexion à Ollama...")
try:
    llm = Ollama(
        model="llama3.1:8b",
        base_url="http://localhost:11434",
        temperature=0.7,
    )

    response = llm.invoke("Réponds juste 'OK'")
    print(f"✅ Ollama fonctionne: {response[:50]}...")
except Exception as e:
    print(f"❌ Erreur Ollama: {e}")
    print("   Assurez-vous qu'Ollama est lancé et que le modèle llama3.1:8b est installé")
    exit(1)

print("\n✅ Tous les tests passent! Le système est prêt.")
print("\nVous pouvez maintenant:")
print("  1. Configurer votre OBSIDIAN_VAULT_PATH dans .env")
print("  2. Lancer: python main.py")
