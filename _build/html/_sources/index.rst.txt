.. Optimisation de Trajectoire d’Avion avec Données Météo documentation master file, created by
   sphinx-quickstart on Sun Apr 20 18:49:29 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Optimisation de Trajectoire d’Avion avec Données Météo documentation
====================================================================

---

### **Module : Optimisation de trajectoire d'avion avec météo**

#### **But du module**
Ce script optimise la trajectoire d'un avion entre deux aéroports en tenant compte des conditions météorologiques. Il ajuste la trajectoire pour éviter les zones dangereuses (vents forts et précipitations) et affiche les résultats sur une carte interactive.

---

### **Fonctions**

#### `get_weather_data(lat, lon)`
**But** : Récupère les données météorologiques pour un point donné à l'aide de l'API Open-Meteo.

**Paramètres** :
- `lat` (float) : Latitude du point.
- `lon` (float) : Longitude du point.

**Retour** :
- Tuple `(windspeed, winddirection, precipitation)` où :
  - `windspeed` (float) : Vitesse du vent en m/s.
  - `winddirection` (float) : Direction du vent en degrés.
  - `precipitation` (float) : Précipitations en mm.

**Exemple** :
```python
windspeed, winddirection, precipitation = get_weather_data(48.8566, 2.3522)
```

---

#### `is_point_in_circle(lat, lon, circle_lat, circle_lon, radius)`
**But** : Vérifie si un point se trouve dans un cercle défini par un centre et un rayon.

**Paramètres** :
- `lat` (float) : Latitude du point à tester.
- `lon` (float) : Longitude du point à tester.
- `circle_lat` (float) : Latitude du centre du cercle.
- `circle_lon` (float) : Longitude du centre du cercle.
- `radius` (float) : Rayon du cercle en mètres.

**Retour** :
- `True` si le point est dans le cercle, `False` sinon.

**Exemple** :
```python
is_in_zone = is_point_in_circle(48.8566, 2.3522, 48.8584, 2.2945, 1000)
```

---

#### `move_perpendicularly(lat1, lon1, lat2, lon2, lat, lon, distance_m)`
**But** : Déplace un point perpendiculairement à la trajectoire entre deux autres points.

**Paramètres** :
- `lat1`, `lon1` (float) : Coordonnées du point de départ de la trajectoire.
- `lat2`, `lon2` (float) : Coordonnées du point d'arrivée de la trajectoire.
- `lat`, `lon` (float) : Coordonnées du point à déplacer.
- `distance_m` (float) : Distance de déplacement en mètres.

**Retour** :
- Tuple `(new_lat, new_lon)` : Nouvelle position après le déplacement.

**Exemple** :
```python
new_lat, new_lon = move_perpendicularly(48.8566, 2.3522, 48.8584, 2.2945, 48.8600, 2.3500, 500)
```

---

### **Comportement du Script**

1. **Sélection des aéroports** : L'utilisateur choisit les aéroports de départ et d'arrivée via une interface Streamlit.
2. **Calcul de la trajectoire** : Le script calcule la trajectoire linéaire entre les deux aéroports.
3. **Données météorologiques** : Il récupère les conditions météo sur la trajectoire via l'API **Open-Meteo**.
4. **Identification des zones dangereuses** : Les zones avec un vent supérieur à 10 m/s ou des précipitations supérieures à 0.2 mm sont marquées comme dangereuses.
5. **Modification de la trajectoire** : La trajectoire est modifiée pour éviter ces zones, en déplaçant les points perpendiculairement.
6. **Affichage sur une carte** : La trajectoire originale et modifiée est affichée sur une carte interactive avec **Folium**.

---

### **Exemple d'utilisation**

Lancer le script dans **Streamlit** pour visualiser l'optimisation de trajectoire.

1. **Sélectionner un aéroport de départ et d'arrivée** dans la barre latérale.
2. Le script calcule la trajectoire initiale et ajuste la trajectoire pour éviter les zones dangereuses.
3. **Visualiser** la carte avec la trajectoire initiale (en gris) et modifiée (en bleu), ainsi que les zones dangereuses (cercles rouges).

---

### **Notes supplémentaires**
- Ce module nécessite les bibliothèques **streamlit**, **folium**, **requests**, **geopy** et **numpy**.
- Assurez-vous que votre environnement dispose d'une connexion internet pour récupérer les données météo.

---


.. toctree::
   :maxdepth: 2
   :caption: Contents:


