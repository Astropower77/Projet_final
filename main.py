import streamlit as st
import numpy as np
import folium
import requests
from geopy.distance import geodesic
from geopy.point import Point
import math
from streamlit_folium import st_folium

# Configuration de la page Streamlit
st.set_page_config(page_title="Optimisation de Trajectoire", layout="wide")
st.title("🛫 Optimisation de trajectoire d'avion avec météo")

# Liste des aéroports disponibles avec leurs coordonnées (latitude, longitude)
aeroports = {
    "CDG - Paris Charles de Gaulle": (49.0097, 2.5479),
    "JFK - New York John F. Kennedy": (40.6413, -73.7781),
    "LHR - London Heathrow": (51.4700, -0.4543),
    "DXB - Dubai": (25.2532, 55.3657),
    "NRT - Tokyo Narita": (35.7720, 140.3929),
    "YUL - Montréal Trudeau": (45.4704, -73.7403),
    "YVR - Vancouver": (49.1937, -123.1836),
}

# Sélection dans la barre latérale (sidebar)
st.sidebar.title("Paramètres")
depart = st.sidebar.selectbox("Aéroport de départ", list(aeroports.keys()))
arrivee = st.sidebar.selectbox("Aéroport d’arrivée", list(aeroports.keys()))

# Récupération des coordonnées des aéroports sélectionnés
lat_initial, lon_initial = aeroports[depart]
lat_final, lon_final = aeroports[arrivee]

# Calcul de la distance totale entre les deux aéroports et interpolation des points de la trajectoire
distance_totale = geodesic((lat_initial, lon_initial), (lat_final, lon_final)).km
n_points = max(2, int(distance_totale / 50))  # Le nombre de points dépend de la distance
lats = np.linspace(lat_initial, lat_final, n_points)
lons = np.linspace(lon_initial, lon_final, n_points)


def get_weather_data(lat, lon):
    """
    Récupère les données météo pour un point donné à l'aide de l'API Open-Meteo.

    Args:
        lat (float): Latitude du point pour lequel obtenir les données météo.
        lon (float): Longitude du point pour lequel obtenir les données météo.

    Returns:
        tuple: vitesse du vent (m/s), direction du vent (°), précipitations (mm).
    """
    try:
        api_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current_weather=true&hourly=precipitation"
        )
        response = requests.get(api_url, timeout=5)  # Requête vers l'API avec un délai d'attente de 5 secondes
        if response.status_code == 200:
            data = response.json()
            weather = data.get("current_weather", {})
            precipitation = data.get("hourly", {}).get("precipitation", [0])[0]
            windspeed = weather.get("windspeed", 0) / 3.6  # Conversion de la vitesse du vent de km/h en m/s
            return windspeed, weather.get("winddirection", 0), precipitation
    except requests.exceptions.RequestException:
        return None, None, None
    return None, None, None


def is_point_in_circle(lat, lon, circle_lat, circle_lon, radius):
    """
    Vérifie si un point donné (lat, lon) se trouve à l'intérieur d'un cercle
    défini par un centre (circle_lat, circle_lon) et un rayon (en mètres).

    Args:
        lat (float): Latitude du point à tester.
        lon (float): Longitude du point à tester.
        circle_lat (float): Latitude du centre du cercle.
        circle_lon (float): Longitude du centre du cercle.
        radius (float): Rayon du cercle en mètres.

    Returns:
        bool: True si le point est dans le cercle, False sinon.
    """
    return geodesic((lat, lon), (circle_lat, circle_lon)).km * 1000 <= radius


def move_perpendicularly(lat1, lon1, lat2, lon2, lat, lon, distance_m):
    """
    Déplace un point perpendiculairement à la trajectoire entre deux autres points.

    Args:
        lat1, lon1: Coordonnées du point de départ de la trajectoire.
        lat2, lon2: Coordonnées du point d'arrivée de la trajectoire.
        lat, lon: Coordonnées du point à déplacer.
        distance_m (float): Distance de déplacement en mètres.

    Returns:
        tuple: Nouvelle latitude et longitude après déplacement perpendiculaire.
    """
    angle_rad = math.atan2(lat2 - lat1, lon2 - lon1)  # Calcul de l'angle entre les deux points
    angle_perp = angle_rad + math.pi / 2  # Angle perpendiculaire
    delta_lat = (distance_m / 1000) / 111 * math.sin(angle_perp)
    delta_lon = (distance_m / 1000) / (111 * math.cos(math.radians(lat))) * math.cos(angle_perp)
    return lat + delta_lat, lon + delta_lon


# Récupération des données météo sur la trajectoire entre les deux aéroports
weather_data = [get_weather_data(lat, lon) for lat, lon in zip(lats, lons)]

# Identification des zones dangereuses (pluie ou vent trop fort)
red_circles = []
for (lat, lon), (wind_speed, wind_dir, precipitation) in zip(zip(lats, lons), weather_data):
    if wind_speed is not None and precipitation is not None:
        if wind_speed > 10 or precipitation > 0.2:  # Zone dangereuse si vent > 10 m/s ou précipitations > 0.2 mm
            red_circles.append((lat, lon, 75000))  # Rayon de 75 km pour chaque zone dangereuse


# Adaptation de la trajectoire pour éviter les zones dangereuses
new_lats = []
new_lons = []
MAX_ATTEMPTS = 5  # Nombre maximum de tentatives pour déplacer le point

for i, (lat, lon) in enumerate(zip(lats, lons)):
    current_lat, current_lon = lat, lon
    moved = False

    for attempt in range(MAX_ATTEMPTS):
        # Vérification si le point est dans une zone dangereuse
        is_dangerous = any(is_point_in_circle(current_lat, current_lon, c_lat, c_lon, radius)
                           for c_lat, c_lon, radius in red_circles)

        # Si le point est trop près d'un aéroport, ne pas le déplacer
        if is_dangerous:
            for a_lat, a_lon in aeroports.values():
                if geodesic((current_lat, current_lon), (a_lat, a_lon)).meters < 100:
                    is_dangerous = False
                    break

        # Si aucune zone dangereuse n'est détectée, on sort de la boucle
        if not is_dangerous:
            break

        moved = True
        lat2, lon2 = (lats[i + 1], lons[i + 1]) if i < len(lats) - 1 else (lats[i - 1], lons[i - 1])
        # Déplacement perpendiculaire pour éviter la zone dangereuse
        current_lat, current_lon = move_perpendicularly(lat, lon, lat2, lon2, lat, lon, 75000)

    new_lats.append(current_lat)
    new_lons.append(current_lon)


# Création de la carte Folium pour visualiser la trajectoire
m = folium.Map(location=[(lat_initial + lat_final) / 2, (lon_initial + lon_final) / 2], zoom_start=4)

# Ajout des cercles rouges pour les zones dangereuses
for lat, lon, radius in red_circles:
    folium.Circle(location=[lat, lon], radius=radius, color='red', fill=True, fill_color='red').add_to(m)

# Trajectoire initiale (en gris) et modifiée (en bleu)
folium.PolyLine(list(zip(lats, lons)), color='gray', weight=1.0, dash_array="5").add_to(m)
folium.PolyLine(list(zip(new_lats, new_lons)), color='blue', weight=2.5).add_to(m)

# Marqueurs pour le départ et l'arrivée
folium.Marker([lat_initial, lon_initial], popup=f"Départ: {depart}", icon=folium.Icon(color='green')).add_to(m)
folium.Marker([lat_final, lon_final], popup=f"Arrivée: {arrivee}", icon=folium.Icon(color='red')).add_to(m)

# Calcul des distances (avant et après la modification de la trajectoire)
distance_initiale = sum(
    geodesic((lats[i], lons[i]), (lats[i+1], lons[i+1])).km
    for i in range(len(lats) - 1)
)
distance_modifiee = sum(
    geodesic((new_lats[i], new_lons[i]), (new_lats[i+1], new_lons[i+1])).km
    for i in range(len(new_lats) - 1)
)
surcout = distance_modifiee - distance_initiale

# Affichage des distances et du surcoût dans Streamlit
st.markdown(f"📏 **Distance initiale :** {distance_initiale:.2f} km")
st.markdown(f"🛣️ **Distance modifiée :** {distance_modifiee:.2f} km")
st.markdown(f"📈 **Surcoût :** {surcout:.2f} km")

# Affichage de la carte dans l'interface Streamlit
st_folium(m, width=1000, height=600)
