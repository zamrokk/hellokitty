#!/bin/bash

echo "🚀 Démarrage du Jetson Dashboard..."
echo "=================================="

# Vérifier si Python3 est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Installation en cours..."
    sudo apt update && sudo apt install -y python3 python3-pip
fi

# Vérifier si pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé. Installation en cours..."
    sudo apt install -y python3-pip
fi

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip3 install -r requirements.txt

# Rendre les scripts exécutables
chmod +x data_collector.py
chmod +x server.py

# Vérifier si tegrastats est disponible
if ! command -v tegrastats &> /dev/null; then
    echo "⚠️  tegrastats n'est pas trouvé. Le dashboard utilisera des données de fallback."
fi

echo "✅ Installation terminée!"
echo ""
echo "🌐 Pour démarrer le dashboard:"
echo "   python3 server.py"
echo ""
echo "📊 Le dashboard sera disponible à l'adresse:"
echo "   http://localhost:5000"
echo "   http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "⏹️  Pour arrêter le dashboard, appuyez sur Ctrl+C"
