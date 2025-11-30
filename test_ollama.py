#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion à Ollama
"""
import sys
from langchain_ollama import ChatOllama


def test_ollama_connection(model: str = "llama3.1:8b"):
    """Teste la connexion à Ollama."""
    print(f"🧪 Test de connexion à Ollama avec le modèle: {model}")
    print("=" * 70)

    try:
        # Initialiser le modèle
        print(f"\n1️⃣ Initialisation du modèle {model}...")
        llm = ChatOllama(
            model=model,
            base_url="http://localhost:11434",
            temperature=0.7,
        )
        print("✅ Modèle initialisé")

        # Test simple
        print(f"\n2️⃣ Envoi d'un message de test...")
        from langchain_core.messages import HumanMessage

        messages = [
            HumanMessage(content="Réponds juste 'OK' si tu me reçois bien.")
        ]

        response = llm.invoke(messages)
        print(f"✅ Réponse reçue: {response.content}")

        # Test avec tool call
        print(f"\n3️⃣ Test des tool calls...")

        from langchain_core.tools import tool

        @tool
        def get_weather(location: str) -> str:
            """Obtenir la météo pour un lieu donné."""
            return f"Il fait beau à {location}"

        llm_with_tools = llm.bind_tools([get_weather])

        messages = [
            HumanMessage(content="Quelle est la météo à Paris?")
        ]

        response = llm_with_tools.invoke(messages)

        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"✅ Tool call détecté: {response.tool_calls[0]['name']}")
        else:
            print(f"⚠️ Pas de tool call détecté (normal pour certains modèles)")
            print(f"   Réponse: {response.content[:100]}...")

        print("\n" + "=" * 70)
        print("✅ Tous les tests ont réussi!")
        print("=" * 70)
        print("\n💡 Conseils:")
        print("  - Si les tool calls ne fonctionnent pas bien, essayez: mistral-nemo:12b")
        print("  - Vérifiez que vous avez assez de RAM disponible")
        print("  - Utilisez 'ollama ps' pour voir les modèles chargés en mémoire")

        return True

    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ Erreur: {e}")
        print("=" * 70)
        print("\n🔧 Solutions possibles:")
        print("  1. Vérifiez qu'Ollama est lancé: 'ollama serve'")
        print("  2. Vérifiez que le modèle est installé: 'ollama list'")
        print(f"  3. Si besoin, installez le modèle: 'ollama pull {model}'")
        print("  4. Vérifiez la connexion: 'curl http://localhost:11434/api/version'")
        return False


def list_available_models():
    """Liste les modèles disponibles."""
    import subprocess

    print("\n📋 Modèles Ollama installés:")
    print("=" * 70)
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except Exception as e:
        print(f"❌ Impossible de lister les modèles: {e}")


if __name__ == "__main__":
    print("🤖 Test de connexion Ollama pour Obsidian Multi-Agent")
    print()

    # Lister les modèles disponibles
    list_available_models()

    # Test avec le modèle par défaut
    model = sys.argv[1] if len(sys.argv) > 1 else "llama3.1:8b"

    success = test_ollama_connection(model)

    sys.exit(0 if success else 1)
