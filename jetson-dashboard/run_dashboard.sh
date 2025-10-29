#!/bin/bash

echo "🚀 Jetson Dashboard - Démarrage"
echo "================================"

# Aller dans le répertoire du dashboard
cd "$(dirname "$0")"

# Vérifier si le serveur est déjà en cours d'exécution
if pgrep -f "simple_server.py" > /dev/null; then
    echo "⚠️  Le dashboard est déjà en cours d'exécution!"
    echo "🌐 Accédez à: http://localhost:5000"
    echo "⏹️  Pour arrêter: pkill -f simple_server.py"
    exit 1
fi

# Vérifier les fichiers nécessaires
if [ ! -f "simple_server.py" ]; then
    echo "❌ Fichier simple_server.py non trouvé!"
    exit 1
fi

if [ ! -f "templates/dashboard.html" ]; then
    echo "❌ Fichier templates/dashboard.html non trouvé!"
    exit 1
fi

# Obtenir l'IP locale
LOCAL_IP=$(hostname -I | awk '{print $1}')

echo "✅ Fichiers trouvés"
echo "🌐 Démarrage du serveur..."
echo ""
echo "📊 Dashboard disponible à:"
echo "   • Local: http://localhost:5000"
echo "   • Réseau: http://$LOCAL_IP:5000"
echo ""
echo "⏹️  Pour arrêter: Ctrl+C ou pkill -f simple_server.py"
echo "=" * 50

# Démarrer le serveur
python3 simple_server.py
