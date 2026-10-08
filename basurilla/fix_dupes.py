import xml.etree.ElementTree as ET

xml_file = 'xml/etapaEsquema.xml'
tree = ET.parse(xml_file)
root = tree.getroot()
ns = {'ns': 'http://www.uniovi.es'}

# Reset mistakenly named puntos anonimos
puntos_anonimos = root.findall('.//ns:puntosAnonimos/ns:puntoAnonimo', ns)
for p in puntos_anonimos:
    nombre_elem = p.find('ns:nombre', ns)
    if nombre_elem is not None and nombre_elem.text in ["Puerto de La Serratella", "Coll de la Bandereta", "Alto del Desierto de las Palmas"]:
        nombre_elem.text = "Punto anonimo corregido"

# Update hitos importantes to user's specified values
hitos = root.findall('.//ns:hitosImportantes/*', ns)
for h in hitos:
    nombre_elem = h.find('ns:nombre', ns)
    if nombre_elem is not None:
        name = nombre_elem.text
        dist_elem = h.find('ns:distancia', ns)
        coord_elem = h.find('ns:coordenadas', ns)
        
        if "Serratella" in name:
            dist_elem.text = "44.6"
            coord_elem.set('altitud', "839.0")
        elif "Bandereta" in name:
            dist_elem.text = "66.1"
            coord_elem.set('altitud', "790.0")
        elif "Desierto de las Palmas" in name and dist_elem.text == "128.6":
            dist_elem.text = "128.5"
            coord_elem.set('altitud', "422.0")

tree.write(xml_file, encoding='utf-8', xml_declaration=True)
