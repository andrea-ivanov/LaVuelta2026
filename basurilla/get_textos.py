import xml.etree.ElementTree as ET
xml_file = 'xml/etapaEsquema.xml'
tree = ET.parse(xml_file)
root = tree.getroot()
ns = {'ns': 'http://www.uniovi.es'}

textos = []
# Salida
salida_nombre = root.find('.//ns:salida', ns).text
textos.append((0.0, salida_nombre))
# Puntos anonimos
for punto in root.findall('.//ns:puntosAnonimos/ns:puntoAnonimo', ns):
    dist_node = punto.find('ns:distancia', ns)
    nombre_elem = punto.find('ns:nombre', ns)
    if nombre_elem is not None and "Punto anonimo" not in nombre_elem.text:
        textos.append((float(dist_node.text), nombre_elem.text))
# Hitos importantes
for hito in root.findall('.//ns:hitosImportantes/*', ns):
    dist_node = hito.find('ns:distancia', ns)
    nombre_elem = hito.find('ns:nombre', ns)
    if dist_node is not None:
        nombre = nombre_elem.text if nombre_elem is not None else hito.tag.split('}')[-1]
        textos.append((float(dist_node.text), nombre))
# Llegada
llegada_nombre = root.find('.//ns:llegada', ns).text
textos.append((195.4, llegada_nombre))

textos.sort(key=lambda x: x[0])
for t in textos:
    print(t)
