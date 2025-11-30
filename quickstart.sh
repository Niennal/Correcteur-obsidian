#!/bin/bash
# Script de démarrage rapide pour Obsidian Multi-Agent

echo "🚀 Obsidian Multi-Agent - Démarrage rapide"
echo "=========================================="

# Vérifier si Ollama est installé
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama n'est pas installé"
    echo "   Installez-le avec: curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

echo "✅ Ollama est installé"

# Vérifier si Ollama est en cours d'exécution
if ! curl -s http://localhost:11434/api/version &> /dev/null; then
    echo "⚠️  Ollama n'est pas en cours d'exécution"
    echo "   Lancez-le avec: ollama serve"
    echo "   Ou utilisez un nouveau terminal et relancez ce script"
    exit 1
fi

echo "✅ Ollama est en cours d'exécution"

# Vérifier les modèles installés
echo ""
echo "📋 Modèles installés:"
ollama list

# Vérifier si llama3.1:8b est installé
if ! ollama list | grep -q "llama3.1:8b"; then
    echo ""
    echo "⚠️  Le modèle llama3.1:8b n'est pas installé"
    echo "   Voulez-vous l'installer maintenant? (o/n)"
    read -r response
    if [[ "$response" =~ ^[Oo]$ ]]; then
        echo "📥 Installation de llama3.1:8b..."
        ollama pull llama3.1:8b
    fi
fi

# Vérifier le fichier .env
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  Fichier .env non trouvé"
    echo "   Voulez-vous le créer maintenant? (o/n)"
    read -r response
    if [[ "$response" =~ ^[Oo]$ ]]; then
        cp .env.example .env
        echo "✅ Fichier .env créé"
        echo "   ⚠️  N'oubliez pas de configurer OBSIDIAN_VAULT_PATH dans .env"
        echo "   Éditez le fichier avec: nano .env"
        exit 0
    fi
else
    echo "✅ Fichier .env trouvé"

    # Vérifier si OBSIDIAN_VAULT_PATH est configuré
    if ! grep -q "^OBSIDIAN_VAULT_PATH=/" .env; then
        echo "⚠️  OBSIDIAN_VAULT_PATH n'est pas configuré dans .env"
        echo "   Éditez le fichier avec: nano .env"
        exit 1
    fi
fi

# Vérifier l'environnement virtuel
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo ""
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -q -r requirements.txt

# Test de connexion Ollama
echo ""
echo "🧪 Test de connexion à Ollama..."
python test_ollama.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Tout est prêt!"
    echo "=========================================="
    echo ""
    echo "Lancez le système avec:"
    echo "  python main.py"
    echo ""
    echo "Ou utilisez directement:"
    echo "  source venv/bin/activate"
    echo "  python main.py"
else
    echo ""
    echo "❌ Le test a échoué"
    echo "   Vérifiez les messages d'erreur ci-dessus"
fi
