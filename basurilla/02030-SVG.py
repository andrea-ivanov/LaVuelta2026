# 02030-SVG.py
# # -*- coding: utf-8 -*-
""""
Crea archivos SVG con rectángulos, círculos, líneas, polilíneas y texto

@version 1.0 18/Octubre/2024
@author: Juan Manuel Cueva Lovelle. Universidad de Oviedo
"""

import xml.etree.ElementTree as ET

class Svg(object):
    """
    Genera archivos SVG con rectángulos, círculos, líneas, polilíneas y texto
    @version 1.0 18/Octubre/2024
    @author: Juan Manuel Cueva Lovelle. Universidad de Oviedo
    """
    def __init__(self):
        """
        Crea el elemento raíz, el espacio de nombres y la versión
        """
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="2.0")

    
    def addRect(self,x,y,width,height,fill, strokeWidth,stroke):
        """
        Añade un elemento rect
        """
        ET.SubElement(self.raiz,'rect',
                      x=x,
                      y=y,
                      width=width,
                      height=height,
                      fill=fill, 
                      strokeWidth=strokeWidth,
                      stroke=stroke)
        
    def addCircle(self,cx,cy,r,fill):
        """
        Añade un elemento circle
        """
        ET.SubElement(self.raiz,'circle',
                      cx=cx,
                      cy=cy,
                      r=r,
                      fill=fill)
        
    def addLine(self,x1,y1,x2,y2,stroke,strokeWith):
        """
        Añade un elemento line
        """
        ET.SubElement(self.raiz,'line',
                      x1=x1,
                      y1=y1,
                      x2=x2,
                      y2=y2,
                      stroke=stroke,
                      strokeWith=strokeWith)

    def addPolyline(self,points,stroke,strokeWith,fill):
        """
        Añade un elemento polyline
        """
        ET.SubElement(self.raiz,'polyline',
                      points=points,
                      stroke=stroke,
                      strokeWith=strokeWith,
                      fill=fill)
        
    def addText(self,texto,x,y,fontFamily,fontSize,style):
        """
        Añade un elemento texto
        """
        ET.SubElement(self.raiz,'text',
                      x=x,
                      y=y,
                      fontFamily=fontFamily,
                      fontSize=fontSize,
                      style=style).text=texto

    def escribir(self,nombreArchivoSVG):
        """ de
        Escribe el archivo SVG con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        
        """
        Introduce indentacióon y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)
        
        arbol.write(nombreArchivoSVG, 
                    encoding='utf-8', 
                    xml_declaration=True
                    )
    
    def ver(self):
        """
        Muestra el archivo SVG. Se utiliza para depurar
        """
        print("\nElemento raiz = ", self.raiz.tag)

        if self.raiz.text != None:
            print("Contenido = "    , self.raiz.text.strip('\n')) #strip() elimina los '\n' del string
        else:
            print("Contenido = "    , self.raiz.text)
        
        print("Atributos = "    , self.raiz.attrib)

        # Recorrido de los elementos del árbol
        for hijo in self.raiz.findall('.//'): # Expresión XPath
            print("\nElemento = " , hijo.tag)
            if hijo.text != None:
                print("Contenido = ", hijo.text.strip('\n')) #strip() elimina los '\n' del string
            else:
                print("Contenido = ", hijo.text)    
            print("Atributos = ", hijo.attrib)

def main():
    
    print(Svg.__doc__)

    """Prueba unitaria de la clase Svg"""
    
    """ nombreSVG = input('Introduzca el nombre del archivo SVG = ') """

    nombreSVG = "demo.svg"

    nuevoSVG = Svg()
    
    nuevoSVG.addRect('25','25','200','200','lime','4','pink')

    nuevoSVG.addCircle('125','125','75','orange')

    nuevoSVG.addLine('50','50','200','200','blue','4')
    
    puntos="50,150 50,200 200,200 200,100"

    nuevoSVG.addPolyline(puntos,'red','4','none') 

    nuevoSVG.addText('texto vertical','220','25','Verdana','55',
                     "writing-mode: tb; glyph-orientation-vertical: 0;")
    
    nuevoSVG.addText('texto horizontal','30','35','Verdana','55',
                     "none")

    """Visualización del SVG creado"""
    nuevoSVG.ver()
    
    """Creación del archivo en formato SVG"""
    nuevoSVG.escribir(nombreSVG)
    print("Creado el archivo: ", nombreSVG)
    
if __name__ == "__main__":
    main()    
