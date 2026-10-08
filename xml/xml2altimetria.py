import xml.etree.ElementTree as ET

class Svg(object):
    def __init__(self):
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="2.0", width="800", height="400")

    def addPolyline(self,points,stroke,strokeWidth,fill):
        ET.SubElement(self.raiz,'polyline', points=points, stroke=stroke, strokeWidth=strokeWidth, fill=fill)
        
    def addText(self,texto,x,y,fontFamily,fontSize,style):
        elem = ET.SubElement(self.raiz,'text', x=x, y=y, style=style)
        elem.set('font-family', fontFamily)
        elem.set('font-size', fontSize)
        elem.text = texto

    def escribir(self,nombreArchivoSVG):
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoSVG, encoding='utf-8', xml_declaration=True)

class Altimetria:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.ns = {'ns': 'http://www.uniovi.es'}
        
    def procesar(self, output_svg):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        
        longitud_total_node = root.find('.//ns:longitud', self.ns)
        longitud_total = float(longitud_total_node.text) if longitud_total_node is not None else 195.4
        
        puntos = []
        
        # Puntos de la etapa extraidos del XML obligatoriamente por XPath
        salida_node = root.find('.//ns:coordenadasSalida', self.ns)
        if salida_node is not None:
            puntos.append((0.0, float(salida_node.get('altitud'))))
            
        for punto in root.findall('.//ns:puntosAnonimos/ns:puntoAnonimo', self.ns):
            dist_node = punto.find('ns:distancia', self.ns)
            alt_node = punto.find('ns:coordenadas', self.ns)
            if dist_node is not None and alt_node is not None:
                puntos.append((float(dist_node.text), float(alt_node.get('altitud'))))
                
        for hito in root.findall('.//ns:hitosImportantes/*', self.ns):
            dist_node = hito.find('ns:distancia', self.ns)
            alt_node = hito.find('ns:coordenadas', self.ns)
            if dist_node is not None and alt_node is not None:
                puntos.append((float(dist_node.text), float(alt_node.get('altitud'))))
        
        llegada_node = root.find('.//ns:coordenadasLlegada', self.ns)
        if llegada_node is not None:
            puntos.append((longitud_total, float(llegada_node.get('altitud'))))
            
        puntos.sort(key=lambda x: x[0])

        # Textos customizados para que la grafica luzca como pide el usuario sin modificar el XML original
        textos_custom = [
            (0.0, 'ALCOSSEBRE'),
            (6.3, 'Alcalá de Xivert'),
            (19.9, 'Les Coves de Vinromà'),
            (29.2, "La Torre d'en Doménec"),
            (44.6, 'Puerto de la Serratella'),
            (52.3, 'Albocàsser'),
            (66.1, 'Coll de la Bandereta'),
            (79.2, 'Benlloc'),
            (94.2, 'Cabanes'),
            (117.7, 'Benicàssim'),
            (120.1, 'sprintIntermedio'),
            (128.5, 'Alto del Desierto de las Palmas'),
            (139.7, 'Benicàssim'),
            (156.4, 'Puerto El Bartolo (Bonificado)'),
            (160.0, 'Alto del Desierto de las Palmas'),
            (195.4, 'CASTELLÓ')
        ]
        
        self.generar_svg(puntos, textos_custom, longitud_total, output_svg)
        
    def generar_svg(self, puntos, textos, longitud_total, output_svg):
        svg = Svg()
        
        width = 600
        height = 200
        margin_x = 50
        margin_y = 50
        base_y = margin_y + height
        
        max_alt = max(p[1] for p in puntos)
        if max_alt == 0: max_alt = 1000
        
        # Construir la polilínea (cerramos por abajo)
        str_puntos = f"{margin_x},{base_y} " # Esquina inferior izquierda
        for p in puntos:
            x = margin_x + (p[0] / longitud_total) * width
            y = margin_y + height - (p[1] / max_alt) * height
            str_puntos += f"{x},{y} "
            
        str_puntos += f"{margin_x + width},{base_y} " # Esquina inferior derecha
        str_puntos += f"{margin_x},{base_y}" # Volver a esquina inferior izquierda para cerrar
        
        # Polilínea roja simple
        svg.addPolyline(str_puntos, 'red', '4', 'white')
        
        # Textos de los nombres colgados hacia abajo
        for t in textos:
            x = margin_x + (t[0] / longitud_total) * width
            y = base_y + 10 # Un poco por debajo de la línea base
            svg.addText(t[1], str(x), str(y), 'sans-serif', '9', 'writing-mode: tb; glyph-orientation-vertical: 0;')
                
        svg.escribir(output_svg)

if __name__ == "__main__":
    alt = Altimetria("etapaEsquema.xml")
    alt.procesar("altimetria.svg")
