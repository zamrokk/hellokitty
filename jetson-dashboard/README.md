# 🚀 Jetson Dashboard

Un dashboard web simple et élégant pour surveiller votre appareil NVIDIA Jetson en temps réel.

## ✨ Fonctionnalités

- **💾 Mémoire RAM** : Utilisation, totale, pourcentage avec barre de progression
- **⚡ Processeur** : Utilisation moyenne et par cœur avec visualisation
- **🎮 GPU** : Utilisation et fréquence
- **🌡️ Températures** : CPU, GPU et capteurs SOC
- **⚡ Consommation** : VDD_IN, VDD_CPU_GPU_CV, VDD_SOC
- **🔄 Swap** : Utilisation et pourcentage
- **📊 Rafraîchissement automatique** : Toutes les 2 secondes
- **📱 Interface responsive** : Compatible mobile et desktop

## 🚀 Installation et Démarrage

### Méthode 1 : Script automatique
```bash
cd jetson-dashboard
./start.sh
python3 server.py
```

### Méthode 2 : Installation manuelle
```bash
# Installer les dépendances
pip3 install -r requirements.txt

# Démarrer le serveur
python3 server.py
```

## 🌐 Accès au Dashboard

Une fois démarré, le dashboard est accessible à :
- **Local** : http://localhost:5000
- **Réseau** : http://[IP_DE_VOTRE_JETSON]:5000

## 🔧 Configuration

### Sources de données
Le dashboard utilise plusieurs sources de données :

1. **tegrastats** (priorité) : Données complètes du système Jetson
2. **Fallback** : `/proc/meminfo`, `/proc/loadavg`, `/sys/class/thermal/`

### Personnalisation
- **Intervalle de rafraîchissement** : Modifiez `time.sleep(2)` dans `server.py`
- **Port** : Changez `port=5000` dans `server.py`
- **Interface** : Modifiez `templates/dashboard.html`

## 📁 Structure du Projet

```
jetson-dashboard/
├── data_collector.py    # Collecteur de données système
├── server.py           # Serveur Flask
├── requirements.txt    # Dépendances Python
├── start.sh           # Script d'installation
├── README.md          # Documentation
└── templates/
    └── dashboard.html # Interface web
```

## 🛠️ Dépannage

### Problème : tegrastats non trouvé
```bash
# Vérifier l'installation
which tegrastats

# Le dashboard fonctionne en mode fallback
```

### Problème : Port déjà utilisé
```bash
# Changer le port dans server.py
app.run(host='0.0.0.0', port=5001, debug=False)
```

### Problème : Permissions
```bash
# Rendre les scripts exécutables
chmod +x *.py
chmod +x start.sh
```

## 🎨 Personnalisation de l'Interface

L'interface est entièrement personnalisable via CSS dans `templates/dashboard.html` :

- **Couleurs** : Modifiez les gradients dans `<style>`
- **Mise en page** : Ajustez la grille CSS
- **Métriques** : Ajoutez de nouveaux éléments dans le HTML

## 📊 API Endpoints

- `GET /` : Interface principale
- `GET /api/data` : Données système complètes (JSON)
- `GET /api/status` : Statut basique du serveur

## 🔄 Mise à jour automatique

Le dashboard se met à jour automatiquement toutes les 2 secondes. Pour modifier cette fréquence :

1. Ouvrez `server.py`
2. Changez `time.sleep(2)` par la valeur souhaitée (en secondes)
3. Redémarrez le serveur

## 🐛 Problèmes Connus

- Certains capteurs thermiques peuvent être indisponibles
- Les données GPU peuvent être limitées selon le modèle Jetson
- Le mode fallback est moins précis que tegrastats

## 📝 Licence

Ce projet est open source et libre d'utilisation.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités
