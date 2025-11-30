#!/bin/bash
#
# Script de setup automatique pour Obsidian Multi-Agent
# Usage: ./setup.sh
#

set -e  # Arrêter en cas d'erreur

echo "=========================================================================="
echo "🚀 Setup Obsidian Multi-Agent - CrewAI + Ollama"
echo "=========================================================================="
echo ""

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher des messages
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Détection de l'OS
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
else
    error "OS non supporté: $OSTYPE"
    exit 1
fi

success "OS détecté: $OS"

# Étape 1: Vérifier Python
echo ""
echo "=========================================================================="
echo "📦 Étape 1/6: Vérification de Python"
echo "=========================================================================="

PYTHON_CMD=""
PYTHON_VERSION=""

# Chercher Python 3.12 ou 3.13 (compatible avec CrewAI 0.11.2)
for cmd in python3.12 python3.13 python3.10 python3.11 python3; do
    if command -v $cmd &> /dev/null; then
        VERSION=$($cmd --version 2>&1 | awk '{print $2}')
        MAJOR=$(echo $VERSION | cut -d. -f1)
        MINOR=$(echo $VERSION | cut -d. -f2)

        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ] && [ "$MINOR" -le 13 ]; then
            PYTHON_CMD=$cmd
            PYTHON_VERSION=$VERSION
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    error "Python 3.10-3.13 requis mais non trouvé"
    echo ""
    echo "Installation recommandée:"
    if [ "$OS" == "macos" ]; then
        echo "  brew install python@3.12"
    else
        echo "  sudo apt-get install python3.12"
    fi
    exit 1
fi

success "Python trouvé: $PYTHON_CMD ($PYTHON_VERSION)"

# Étape 2: Créer l'environnement virtuel
echo ""
echo "=========================================================================="
echo "📦 Étape 2/6: Création de l'environnement virtuel"
echo "=========================================================================="

if [ -d "venv" ]; then
    warning "L'environnement virtuel existe déjà"
    read -p "Voulez-vous le recréer? (o/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        info "Suppression de l'ancien venv..."
        rm -rf venv
    else
        info "Conservation de l'environnement existant"
    fi
fi

if [ ! -d "venv" ]; then
    info "Création du venv avec $PYTHON_CMD..."
    $PYTHON_CMD -m venv venv
    success "Environnement virtuel créé"
else
    success "Environnement virtuel déjà présent"
fi

# Activer le venv
source venv/bin/activate

# Étape 3: Installer les dépendances
echo ""
echo "=========================================================================="
echo "📦 Étape 3/6: Installation des dépendances Python"
echo "=========================================================================="

info "Mise à jour de pip..."
pip install --quiet --upgrade pip

info "Installation de setuptools..."
pip install --quiet setuptools

info "Installation des dépendances (cela peut prendre quelques minutes)..."
pip install --quiet -r requirements.txt

success "Dépendances installées"

# Étape 4: Vérifier Ollama
echo ""
echo "=========================================================================="
echo "📦 Étape 4/6: Vérification d'Ollama"
echo "=========================================================================="

if ! command -v ollama &> /dev/null; then
    warning "Ollama n'est pas installé"
    echo ""
    echo "Installation recommandée:"
    if [ "$OS" == "macos" ]; then
        echo "  curl -fsSL https://ollama.com/install.sh | sh"
    else
        echo "  curl -fsSL https://ollama.com/install.sh | sh"
    fi
    echo ""
    read -p "Voulez-vous installer Ollama maintenant? (o/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        info "Installation d'Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
        success "Ollama installé"
    else
        warning "Ollama doit être installé manuellement plus tard"
    fi
else
    success "Ollama est installé"
fi

# Vérifier si Ollama est en cours d'exécution
if curl -s http://localhost:11434/api/version &> /dev/null; then
    success "Ollama est en cours d'exécution"

    # Lister les modèles installés
    echo ""
    info "Modèles Ollama installés:"
    ollama list

    # Vérifier si llama3.1:8b est installé
    if ! ollama list | grep -q "llama3.1:8b"; then
        echo ""
        warning "Le modèle llama3.1:8b n'est pas installé"
        read -p "Voulez-vous l'installer maintenant? (recommandé) (o/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Oo]$ ]]; then
            info "Installation de llama3.1:8b (cela peut prendre quelques minutes)..."
            ollama pull llama3.1:8b
            success "Modèle llama3.1:8b installé"
        else
            warning "Vous devrez installer llama3.1:8b plus tard avec: ollama pull llama3.1:8b"
        fi
    else
        success "Modèle llama3.1:8b déjà installé"
    fi
else
    warning "Ollama n'est pas en cours d'exécution"
    echo ""
    echo "Démarrez Ollama avec:"
    echo "  ollama serve"
    echo ""
    echo "Dans un autre terminal, puis installez le modèle:"
    echo "  ollama pull llama3.1:8b"
fi

# Étape 5: Configurer .env
echo ""
echo "=========================================================================="
echo "📦 Étape 5/6: Configuration du fichier .env"
echo "=========================================================================="

if [ ! -f ".env" ]; then
    info "Création du fichier .env depuis le template..."
    cp .env.example .env
    success "Fichier .env créé"
else
    success "Fichier .env existe déjà"
fi

# Vérifier si OBSIDIAN_VAULT_PATH est configuré
if ! grep -q "^OBSIDIAN_VAULT_PATH=/" .env; then
    echo ""
    warning "OBSIDIAN_VAULT_PATH n'est pas configuré dans .env"
    echo ""
    echo "Veuillez entrer le chemin absolu vers votre vault Obsidian"
    echo "Exemple: /Users/votre-nom/Documents/MonVault"
    echo ""
    read -p "Chemin du vault (ou appuyez sur Entrée pour configurer plus tard): " VAULT_PATH

    if [ ! -z "$VAULT_PATH" ]; then
        # Vérifier que le chemin existe
        if [ -d "$VAULT_PATH" ]; then
            info "Configuration de OBSIDIAN_VAULT_PATH dans .env..."
            # Utiliser sed de manière compatible macOS/Linux
            if [ "$OS" == "macos" ]; then
                sed -i '' "s|^OBSIDIAN_VAULT_PATH=.*|OBSIDIAN_VAULT_PATH=$VAULT_PATH|" .env
            else
                sed -i "s|^OBSIDIAN_VAULT_PATH=.*|OBSIDIAN_VAULT_PATH=$VAULT_PATH|" .env
            fi
            success "OBSIDIAN_VAULT_PATH configuré: $VAULT_PATH"
        else
            warning "Le chemin n'existe pas: $VAULT_PATH"
            warning "Vous devrez configurer .env manuellement"
        fi
    else
        warning "Configuration .env à faire manuellement"
        echo "  nano .env"
    fi
else
    VAULT_PATH=$(grep "^OBSIDIAN_VAULT_PATH=" .env | cut -d'=' -f2)
    success "OBSIDIAN_VAULT_PATH déjà configuré: $VAULT_PATH"
fi

# Étape 6: Tests
echo ""
echo "=========================================================================="
echo "📦 Étape 6/6: Tests du système"
echo "=========================================================================="

info "Test des imports Python..."
if python test_simple.py 2>&1 | grep -q "Tous les tests passent"; then
    success "Imports Python OK"
else
    warning "Problème avec les imports Python"
    echo "Exécutez manuellement: python test_simple.py"
fi

# Résumé final
echo ""
echo "=========================================================================="
echo "🎉 Installation terminée!"
echo "=========================================================================="
echo ""

if curl -s http://localhost:11434/api/version &> /dev/null && ollama list | grep -q "llama3.1:8b"; then
    OLLAMA_STATUS="${GREEN}✅ OK${NC}"
else
    OLLAMA_STATUS="${YELLOW}⚠️  À configurer${NC}"
fi

if grep -q "^OBSIDIAN_VAULT_PATH=/" .env 2>/dev/null; then
    ENV_STATUS="${GREEN}✅ Configuré${NC}"
else
    ENV_STATUS="${YELLOW}⚠️  À configurer${NC}"
fi

echo -e "État du système:"
echo -e "  • Python: ${GREEN}✅ $PYTHON_VERSION${NC}"
echo -e "  • Environnement virtuel: ${GREEN}✅ Créé${NC}"
echo -e "  • Dépendances: ${GREEN}✅ Installées${NC}"
echo -e "  • Ollama: $OLLAMA_STATUS"
echo -e "  • Configuration .env: $ENV_STATUS"
echo ""

echo "Prochaines étapes:"
echo ""

if ! curl -s http://localhost:11434/api/version &> /dev/null; then
    echo "1. Démarrer Ollama:"
    echo "   ollama serve"
    echo ""
fi

if ! ollama list 2>/dev/null | grep -q "llama3.1:8b"; then
    echo "2. Installer le modèle llama3.1:8b:"
    echo "   ollama pull llama3.1:8b"
    echo ""
fi

if ! grep -q "^OBSIDIAN_VAULT_PATH=/" .env 2>/dev/null; then
    echo "3. Configurer le vault Obsidian:"
    echo "   nano .env"
    echo "   (Modifier OBSIDIAN_VAULT_PATH)"
    echo ""
fi

echo "Pour utiliser le système:"
echo ""
echo "  # Activer l'environnement virtuel"
echo "  source venv/bin/activate"
echo ""
echo "  # Tester avec une démo"
echo "  python demo_correction.py"
echo ""
echo "  # Corriger l'orthographe"
echo "  python correct_spelling.py"
echo ""
echo "  # Gérer vos notes"
echo "  python main_simple.py"
echo ""

echo "=========================================================================="
echo "📚 Documentation:"
echo "=========================================================================="
echo "  • README.md - Documentation principale"
echo "  • QUICKSTART.md - Guide de démarrage"
echo "  • GUIDE_RAPIDE_CORRECTION.md - Guide correction orthographique"
echo "  • INDEX.md - Index de tous les fichiers"
echo ""

success "Setup terminé avec succès! 🎉"
