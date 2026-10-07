import xml.etree.ElementTree as ET
import math
from collections import defaultdict

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371 
    return c * r

def parse_route(kml_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    ls = root.find('.//kml:LineString/kml:coordinates', ns)
    coords_text = ls.text.strip().split()
    route = []
    cum_dist = 0.0
    prev_lon, prev_lat = None, None
    for ct in coords_text:
        parts = ct.split(',')
        lon, lat, alt = float(parts[0]), float(parts[1]), float(parts[2])
        if prev_lon is not None:
            dist = haversine(prev_lon, prev_lat, lon, lat)
            cum_dist += dist
        route.append({'lon': lon, 'lat': lat, 'alt': alt, 'dist': cum_dist})
        prev_lon, prev_lat = lon, lat
    return route

def parse_points(kml_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    placemarks = root.findall('.//kml:Placemark', ns)
    points = []
    for p in placemarks:
        name = p.find('kml:name', ns).text
        coords_text = p.find('.//kml:coordinates', ns).text.strip()
        parts = coords_text.split(',')
        lon, lat, alt = float(parts[0]), float(parts[1]), float(parts[2])
        points.append({'name': name, 'lon': lon, 'lat': lat, 'alt': alt})
    return points

def find_passes(point, route):
    # Find all local minima distance < 0.2 km
    passes = []
    n = len(route)
    distances = [haversine(point['lon'], point['lat'], r['lon'], r['lat']) for r in route]
    
    for i in range(1, n - 1):
        if distances[i] < distances[i-1] and distances[i] < distances[i+1] and distances[i] < 0.2:
            passes.append(route[i]['dist'])
            
    # Handle edges
    if distances[0] < distances[1] and distances[0] < 0.2:
        passes.append(route[0]['dist'])
    if distances[-1] < distances[-2] and distances[-1] < 0.2:
        passes.append(route[-1]['dist'])
        
    # Deduplicate very close passes (e.g., within 2km of each other)
    passes.sort()
    merged_passes = []
    for p in passes:
        if not merged_passes or (p - merged_passes[-1]) > 2.0:
            merged_passes.append(p)
            
    return merged_passes

route = parse_route("../20260925023450-25072-map.kml")
points = parse_points("puntos_usuario.kml")

# Group points by coordinate key
grouped_points = defaultdict(list)
for p in points:
    key = f"{p['lon']:.5f}_{p['lat']:.5f}"
    grouped_points[key].append(p)

for key, pts in grouped_points.items():
    # Find passes for this coordinate
    passes = find_passes(pts[0], route)
    
    if len(passes) == 0:
        # Fallback to absolute minimum if no local minimum < 0.2km is found
        min_dist = float('inf')
        closest = 0
        for r in route:
            d = haversine(pts[0]['lon'], pts[0]['lat'], r['lon'], r['lat'])
            if d < min_dist:
                min_dist = d
                closest = r['dist']
        passes = [closest]
        
    # Assign passes to the identical points
    # If there are more points than passes, we'll just repeat the last pass or just distribute them
    for i, p in enumerate(pts):
        if i < len(passes):
            p['dist'] = passes[i]
        else:
            p['dist'] = passes[-1]

points.sort(key=lambda x: x['dist'])

# Now inject into etapaEsquema.xml
ET.register_namespace('', "http://www.uniovi.es")
ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
tree = ET.parse('etapaEsquema.xml')
root = tree.getroot()
ns = {'ns': 'http://www.uniovi.es'}

hitos = root.find('ns:hitosImportantes', ns)
if hitos is not None:
    hitos.clear()
    tipos = {
        "Serratella": "segunda",
        "Bandereta": "tercera",
        "Desierto": "segunda",
        "Bartolo": "primera"
    }
    
    for p in points:
        name = p['name']
        if "puerto" in name.lower() or "sprint" in name.lower():
            if "puerto" in name.lower():
                tipo = "primera"
                for k, v in tipos.items():
                    if k in name:
                        tipo = v
                
                puerto_el = ET.SubElement(hitos, 'puerto', {'tipo': tipo})
                nombre_el = ET.SubElement(puerto_el, 'nombre')
                nombre_el.text = name.replace("Puerto: ", "")
                coord_el = ET.SubElement(puerto_el, 'coordenadas', {
                    'longitud': f"{p['lon']:.6f}", 'longitudUnidad': 'grados',
                    'latitud': f"{p['lat']:.6f}", 'latitudUnidad': 'grados',
                    'altitud': f"{p['alt']:.1f}", 'altitudUnidad': 'm'
                })
                dist_el = ET.SubElement(puerto_el, 'distancia', {'unidad': 'km'})
                dist_el.text = f"{p['dist']:.1f}"
                
            elif "sprint" in name.lower():
                sprint_el = ET.SubElement(hitos, 'sprintIntermedio')
                coord_el = ET.SubElement(sprint_el, 'coordenadas', {
                    'longitud': f"{p['lon']:.6f}", 'longitudUnidad': 'grados',
                    'latitud': f"{p['lat']:.6f}", 'latitudUnidad': 'grados',
                    'altitud': f"{p['alt']:.1f}", 'altitudUnidad': 'm'
                })
                dist_el = ET.SubElement(sprint_el, 'distancia', {'unidad': 'km'})
                dist_el.text = f"{p['dist']:.1f}"

puntos_anon = root.find('ns:puntosAnonimos', ns)
if puntos_anon is not None:
    puntos_anon.clear()
    for p in points:
        name = p['name']
        if "anonimo" in name.lower() or "anónimo" in name.lower():
            pa_el = ET.SubElement(puntos_anon, 'puntoAnonimo')
            nombre_el = ET.SubElement(pa_el, 'nombre')
            nombre_el.text = name
            coord_el = ET.SubElement(pa_el, 'coordenadas', {
                'longitud': f"{p['lon']:.6f}", 'longitudUnidad': 'grados',
                'latitud': f"{p['lat']:.6f}", 'latitudUnidad': 'grados',
                'altitud': f"{p['alt']:.1f}", 'altitudUnidad': 'm'
            })
            dist_el = ET.SubElement(pa_el, 'distancia', {'unidad': 'km'})
            dist_el.text = f"{p['dist']:.1f}"

def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

indent(root)

tree.write('etapaEsquema.xml', encoding='utf-8', xml_declaration=True)
print("etapaEsquema.xml updated with duplicates correctly mapped!")
