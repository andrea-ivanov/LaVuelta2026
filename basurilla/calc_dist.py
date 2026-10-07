import xml.etree.ElementTree as ET
import math

def haversine(lon1, lat1, lon2, lat2):
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371 # Radius of earth in kilometers
    return c * r

def parse_route(kml_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    ls = root.find('.//kml:LineString/kml:coordinates', ns)
    if ls is None:
        raise Exception("No LineString found")
    
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
        route.append({
            'lon': lon, 'lat': lat, 'alt': alt, 'dist': cum_dist
        })
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
        points.append({
            'name': name, 'lon': lon, 'lat': lat, 'alt': alt
        })
    return points

def find_closest_distance(point, route):
    min_dist = float('inf')
    closest_cum_dist = 0.0
    for r in route:
        dist = haversine(point['lon'], point['lat'], r['lon'], r['lat'])
        if dist < min_dist:
            min_dist = dist
            closest_cum_dist = r['dist']
    return closest_cum_dist

if __name__ == "__main__":
    import sys
    route = parse_route("../20260925023450-25072-map.kml")
    points = parse_points("puntos_usuario.kml")
    
    for p in points:
        p['dist'] = find_closest_distance(p, route)
    
    points.sort(key=lambda x: x['dist'])
    
    # Generate XML
    print("<puntosAnonimos>")
    for p in points:
        if "anonimo" in p['name'].lower():
            print("    <puntoAnonimo>")
            print(f"        <nombre>{p['name']}</nombre>")
            print(f"        <coordenadas longitud=\"{p['lon']:.6f}\" longitudUnidad=\"grados\" latitud=\"{p['lat']:.6f}\" latitudUnidad=\"grados\" altitud=\"{p['alt']:.1f}\" altitudUnidad=\"m\" />")
            print(f"        <distancia unidad=\"km\">{p['dist']:.1f}</distancia>")
            print("    </puntoAnonimo>")
    print("</puntosAnonimos>")
    
    print("\n<hitosImportantes>")
    for p in points:
        if "puerto" in p['name'].lower() or "sprint" in p['name'].lower() or "salida" in p['name'].lower() or "meta" in p['name'].lower():
            if "puerto" in p['name'].lower():
                print("    <puerto tipo=\"primera\">") # Placeholder tipo
                print(f"        <nombre>{p['name']}</nombre>")
                print(f"        <coordenadas longitud=\"{p['lon']:.6f}\" longitudUnidad=\"grados\" latitud=\"{p['lat']:.6f}\" latitudUnidad=\"grados\" altitud=\"{p['alt']:.1f}\" altitudUnidad=\"m\" />")
                print(f"        <distancia unidad=\"km\">{p['dist']:.1f}</distancia>")
                print("    </puerto>")
            elif "sprint" in p['name'].lower():
                print("    <sprintIntermedio>")
                print(f"        <coordenadas longitud=\"{p['lon']:.6f}\" longitudUnidad=\"grados\" latitud=\"{p['lat']:.6f}\" latitudUnidad=\"grados\" altitud=\"{p['alt']:.1f}\" altitudUnidad=\"m\" />")
                print(f"        <distancia unidad=\"km\">{p['dist']:.1f}</distancia>")
                print("    </sprintIntermedio>")
            else: # Salida or Meta
                print(f"    <!-- {p['name']} -->")
                print(f"    <coordenadas longitud=\"{p['lon']:.6f}\" longitudUnidad=\"grados\" latitud=\"{p['lat']:.6f}\" latitudUnidad=\"grados\" altitud=\"{p['alt']:.1f}\" altitudUnidad=\"m\" />")
                print(f"    <distancia unidad=\"km\">{p['dist']:.1f}</distancia>")
    print("</hitosImportantes>")
