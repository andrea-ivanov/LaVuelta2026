import xml.etree.ElementTree as ET

class Xml2Kml:
    def __init__(self, archivo_xml, archivo_kml):
        """
        Constructor de la clase. Recibe las rutas de los archivos de entrada (XML) y salida (KML).
        """
        self.archivo_xml = archivo_xml
        self.archivo_kml = archivo_kml
        self.ns = {'ns': 'http://www.uniovi.es'}

    def generar_kml(self):
        """
        Método principal que coordina la lectura del XML y la escritura del KML.
        """
        try:
            # Leer el archivo XML y generar el árbol DOM en memoria
            arbol = ET.parse(self.archivo_xml)
            raiz = arbol.getroot()

            # Extraer los datos mediante expresiones XPath
            puntos = self._extraer_puntos(raiz)

            # Ordenamos los puntos por su distancia desde la salida.
            # Esto es vital para que la "planimetría" (la línea de la ruta) se trace en el orden correcto.
            puntos.sort(key=lambda x: x['distancia'])

            # Escribir el archivo KML
            self._escribir_kml(puntos)
            
            print(f"Archivo '.kml' generado: {self.archivo_kml}")

        except Exception as e:
            print(f"Ha ocurrido un error: {e}")

    def _extraer_puntos(self, raiz):
        """
        Usa XPath para buscar las coordenadas de salida, meta, puertos, sprints y anónimos.
        """
        puntos = []

        # A. Salida (Rojo). Distancia 0.0
        salida = raiz.find('.//ns:coordenadasSalida', self.ns)
        if salida is not None:
            puntos.append(self._crear_diccionario(0.0, salida, "Salida de la Etapa", "rojo"))

        # B. Meta / Llegada (Rojo). Le ponemos distancia infinita para que siempre sea el último punto.
        llegada = raiz.find('.//ns:coordenadasLlegada', self.ns)
        if llegada is not None:
            puntos.append(self._crear_diccionario(float('inf'), llegada, "Meta (Llegada)", "rojo"))

        # C. Puertos de montaña (Verde)
        puertos = raiz.findall('.//ns:puerto', self.ns)
        for p in puertos:
            dist = float(p.find('ns:distancia', self.ns).text)
            nombre = p.find('ns:nombre', self.ns).text
            coords = p.find('ns:coordenadas', self.ns)
            puntos.append(self._crear_diccionario(dist, coords, f"Puerto: {nombre}", "verde"))

        # D. Sprints Intermedios (Azul)
        sprints = raiz.findall('.//ns:sprintIntermedio', self.ns)
        for s in sprints:
            dist = float(s.find('ns:distancia', self.ns).text)
            coords = s.find('ns:coordenadas', self.ns)
            puntos.append(self._crear_diccionario(dist, coords, "Sprint Intermedio", "azul"))

        # E. Puntos Anónimos (Amarillo). Limitado a los que haya (se recomiendan 20-30).
        anonimos = raiz.findall('.//ns:puntoAnonimo', self.ns)
        for i, a in enumerate(anonimos):
            dist = float(a.find('ns:distancia', self.ns).text)
            coords = a.find('ns:coordenadas', self.ns)
            puntos.append(self._crear_diccionario(dist, coords, f"Punto Anónimo {i+1}", "amarillo"))

        return puntos

    def _crear_diccionario(self, distancia, nodo_coordenadas, nombre, color):
        """
        Empaqueta la información de un punto en un diccionario fácil de usar.
        """
        return {
            'distancia': distancia,
            'nombre': nombre,
            'color': color,
            'lon': nodo_coordenadas.attrib['longitud'],
            'lat': nodo_coordenadas.attrib['latitud'],
            'alt': nodo_coordenadas.attrib['altitud']
        }

    def _escribir_kml(self, puntos):
        """
        Escribe físicamente el archivo KML cumpliendo con la estructura estándar.
        """
        with open(self.archivo_kml, 'w', encoding='utf-8') as f:
            # 1. Prólogo
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            f.write('<Document>\n')
            f.write('<name>Planimetria Etapa KML</name>\n\n')

            # Definición de colores
            self._definir_estilos(f)

            # 2. Línea de la ruta (Planimetría)
            f.write('\n<!-- Línea que une todos los puntos -->\n')
            f.write('<Placemark>\n')
            f.write('  <name>Ruta</name>\n')
            f.write('  <styleUrl>#lineaRuta</styleUrl>\n')
            f.write('  <LineString>\n')
            f.write('    <extrude>1</extrude>\n')
            f.write('    <tessellate>1</tessellate>\n')
            f.write('    <coordinates>\n')
            for p in puntos:
                f.write(f"      {p['lon']},{p['lat']},{p['alt']}\n")
            f.write('    </coordinates>\n')
            f.write('  </LineString>\n')
            f.write('</Placemark>\n\n')

            # 3. Puntos de interés (Pines con colores)
            f.write('<!-- Puntos individuales -->\n')
            for p in puntos:
                f.write('<Placemark>\n')
                f.write(f"  <name>{p['nombre']}</name>\n")
                f.write(f'  <styleUrl>#{p["color"]}</styleUrl>\n')
                f.write('  <Point>\n')
                f.write(f"    <coordinates>{p['lon']},{p['lat']},{p['alt']}</coordinates>\n")
                f.write('  </Point>\n')
                f.write('</Placemark>\n')

            # 4. Epílogo
            f.write('</Document>\n')
            f.write('</kml>\n')

    def _definir_estilos(self, f):
        """
        Declara los iconos y el grosor de línea en el archivo KML.
        """
        colores = {
            "rojo": "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
            "verde": "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
            "azul": "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
            "amarillo": "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png"
        }
        
        # Estilos para los iconos
        for nombre, url in colores.items():
            f.write(f'<Style id="{nombre}">\n')
            f.write('  <IconStyle>\n    <Icon>\n')
            f.write(f'      <href>{url}</href>\n')
            f.write('    </Icon>\n  </IconStyle>\n')
            f.write('</Style>\n')

        # Estilo para la línea (azul y gruesa)
        f.write('<Style id="lineaRuta">\n')
        f.write('  <LineStyle>\n')
        f.write('    <color>ffff0000</color>\n') # El KML usa AABBGGRR
        f.write('    <width>4</width>\n')
        f.write('  </LineStyle>\n')
        f.write('</Style>\n')

# Ejecución principal
if __name__ == "__main__":
    mi_conversor = Xml2Kml("etapaEsquema.xml", "etapa.kml")
    mi_conversor.generar_kml()
