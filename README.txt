# ✈️ Optimisation de Trajectoire d’Avion avec Données Météo

Ce projet Streamlit permet de visualiser et d’optimiser une trajectoire d’avion entre deux aéroports, en tenant compte des conditions météorologiques dangereuses telles que le vent fort et la précipitation. L'application affiche une carte avec :
- La trajectoire initiale (en gris),
- Les zones météo dangereuses (en rouge),
- Une trajectoire modifiée automatiquement pour éviter les zones à risque (en bleu).

La documentation du code se situe dans le dossier build/html/index.

---

## 📦 Fonctionnalités

- Sélection de deux aéroports (départ et arrivée) parmi une liste prédéfinie.
- Récupération automatique des données météo le long de la trajectoire.
- Détection des zones dangereuses (vent > 10 m/s ou précipitation > 0.2 mm).
- Génération d'une trajectoire alternative pour les contourner.
- Visualisation sur une carte interactive avec `folium`.
- Affichage du surcoût en distance dû au contournement.

---

## ▶️ Lancer l'application

### 1. Cloner le dépôt et se placer dans le dossier du projet
```bash
cd ton_dossier/Projet_final


### 2. Installer les dépendances
bash
Copier
Modifier
pip install -r requirements.txt

Si tu n’as pas encore de fichier requirements.txt, voici un exemple :

text
Copier
Modifier
streamlit
folium
numpy
geopy
requests
streamlit-folium

### 3. Lancer l'application Streamlit
bash
Copier
Modifier
streamlit run main.py
💡 Si tu es dans PyCharm, ouvre un terminal en bas de l’interface et lance la commande ci-dessus dans le terminal (et non dans la console Python interactive).

---

## 🧠 À propos du code

Les coordonnées sont générées entre deux aéroports avec np.linspace.

À chaque point, une requête est faite à l'API Open-Meteo.

Si une zone météo dangereuse est détectée, une nouvelle trajectoire est générée en la contournant latéralement.

Les distances initiales et modifiées sont calculées avec la librairie geopy.

---

## 📜 Licence

Projet réalisé dans le cadre du cours MGA802 à l’ÉTS.







