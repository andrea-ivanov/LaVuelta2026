import xml.etree.ElementTree as ET
import math

xml_file = 'xml/etapaEsquema.xml'
tree = ET.parse(xml_file)
root = tree.getroot()
ns = {'ns': 'http://www.uniovi.es'}

targets = [
    ("Alcalá de Xivert", 6.3),
    ("Les Coves de Vinromà", 21.4),
    ("La Torre d'en Doménec", 30.3),
    ("Puerto de La Serratella", 44.6),
    ("Albocàsser", 52.0),
    ("Coll de la Bandereta", 66.1),
    ("Benlloc", 79.0),
    ("Cabanes", 93.3),
    ("Benicàssim", 117.0),
    ("Alto del Desierto de las Palmas", 128.5),
    ("Benicàssim (2)", 141.8) # named it Benicàssim (2) to avoid duplicates but let's just use Benicàssim
]

puntos_anonimos = root.findall('.//ns:puntosAnonimos/ns:puntoAnonimo', ns)

for target_name, target_dist in targets:
    # Find the closest puntoAnonimo
    closest_punto = None
    min_diff = float('inf')
    
    for punto in puntos_anonimos:
        dist_elem = punto.find('ns:distancia', ns)
        if dist_elem is not None:
            dist = float(dist_elem.text)
            diff = abs(dist - target_dist)
            if diff < min_diff:
                min_diff = diff
                closest_punto = punto
                
    if closest_punto is not None:
        nombre_elem = closest_punto.find('ns:nombre', ns)
        if nombre_elem is not None:
            print(f"Renaming '{nombre_elem.text}' to '{target_name}' (distance: {target_dist}, actual: {closest_punto.find('ns:distancia', ns).text})")
            # If the user wanted the exact name:
            nombre_elem.text = target_name if "Benicàssim (" not in target_name else "Benicàssim"

# Also register SprintIntermedio if needed, but it's already updated.

tree.write(xml_file, encoding='utf-8', xml_declaration=True)
