#!/bin/bash

echo "🚀 Jetson Dashboard - Démarrage"
echo "================================"

# Aller dans le répertoire du dashboard
cd "$(dirname "$0")"

# Vérifier si le serveur est déjà en cours d'exécution
if pgrep -f "simple_server.py" > /dev/null; then
    echo "⚠️  Le dashboard est déjà en cours d'exécution!"
    echo "🌐 Accédez à: http://localhost:8081"
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

# Démarrer le serveur en arrière-plan
echo "🚀 Démarrage du serveur web..."
python3 -c "
from simple_server import start_server
start_server(8081)
" &

# Attendre que le serveur démarre
echo "⏳ Attente du démarrage du serveur..."
sleep 3

# Vérifier que le serveur répond
if curl -s http://localhost:8081/api/data > /dev/null; then
    echo "✅ Serveur démarré avec succès!"
    echo ""
    echo "📊 Dashboard disponible à:"
    echo "   • Local: http://localhost:8081"
    echo "   • Réseau: http://$LOCAL_IP:8081"
    echo ""
    
    # Ouvrir Firefox automatiquement
    echo "🌐 Ouverture de Firefox..."
    firefox http://localhost:8081 &
    
    echo "🎀 Dashboard Hello Kitty ouvert dans Firefox!"
    echo "⏹️  Pour arrêter: pkill -f simple_server.py"
    echo "=" * 50
    
    # Garder le script en vie pour pouvoir l'arrêter avec Ctrl+C
    wait
else
    echo "❌ Erreur: Le serveur n'a pas pu démarrer!"
    echo "🔧 Vérifiez les logs pour plus d'informations"
    exit 1
fi
