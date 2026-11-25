"use strict";
class Ciudad {
    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre;
        this.pais = pais;
        this.gentilicio = gentilicio;
        this.poblacion = 0;
        this.coordenadas = { latitud: 0, longitud: 0 };
    }

    rellenarAtributos(poblacion, latitud, longitud) {
        this.poblacion = poblacion;
        this.coordenadas = { latitud: latitud, longitud: longitud }
    }

    getCiudad() {
        return this.nombre;
    }

    getPais() {
        return this.pais;
    }

    getInformacionSecundaria() {
        return `<ul>
                <li><strong>Gentilicio:</strong> ${this.gentilicio}</li>
                <li><strong>Poblacion:</strong> ${this.poblacion.toLocaleString()} habitantes</li>
                </ul>`;
    }

    escribeCoordenadas() {
        const seccion = document.querySelector("section");
        if (seccion) {
            const parrafo = document.createElement("p");
            parrafo.textContent = `Coordenadas: Latitud ${this.coordenadas.latitud}, Longitud ${this.coordenadas.longitud}`;
            seccion.appendChild(parrafo);
        }
    }

    getMeteorologia() {
        const apiKey = "0c064cc611a00132fa58a2b0091d7947";
        const url = `https://api.openweathermap.org/data/2.5/weather?lat=${this.coordenadas.latitud}&lon=${this.coordenadas.longitud}&mode=xml&units=metric&lang=es&appid=${apiKey}`;

        $.ajax({            // peticiones http en segundo plano
            dataType: "xml",
            url: url,
            method: "GET",
            success: (datos) => {
                this.datosXml = datos;
                this.procesarXML();
            },
            error: (err) => {
                console.error("Error al obtener los datos mereorológicos:", err);
            }
        })
    }

    procesarXML() {
        var temperatura = $('temperature', this.datosXml).attr("value");
        var temperaturaUnit = $('temperature', this.datosXml).attr("unit");
        var sensacion = $('feels_like', this.datosXml).attr("value");
        var humedad = $('humidity', this.datosXml).attr("value");
        var humedadUnit = $('humidity', this.datosXml).attr("unit");
        var presion = $('pressure', this.datosXml).attr("value");
        var presionUnit = $('pressure', this.datosXml).attr("unit");

        var velocidadViento = $('speed', this.datosXml).attr("value");
        var direccionViento = $('direction', this.datosXml).attr("value");
        var nombreDireccionViento = $('direction', this.datosXml).attr("name");

        var minutosZonaHoraria = new Date().getTimezoneOffset();

        var amanecer = $('sun', this.datosXml).attr("rise");
        var amanecerMiliSeg1970 = Date.parse(amanecer);
        amanecerMiliSeg1970 -= minutosZonaHoraria * 60 * 1000;
        var amanecerLocal = (new Date(amanecerMiliSeg1970)).toLocaleTimeString("es-ES");

        var oscurecer = $('sun', this.datosXml).attr("set");
        var oscurecerMiliSeg1970 = Date.parse(oscurecer);
        oscurecerMiliSeg1970 -= minutosZonaHoraria * 60 * 1000;
        var oscurecerLocal = (new Date(oscurecerMiliSeg1970)).toLocaleTimeString("es-ES");

        var icono = $('weather', this.datosXml).attr("icon");
        var descripcion = $('weather', this.datosXml).attr("value");
        var urlIcono = "https://openweathermap.org/img/wn/" + icono + "@2x.png";

        // dd/MM/YYYY
        var hoy = new Date();
        var dia = String(hoy.getDate()).padStart(2, "0");
        var mes = String(hoy.getMonth() + 1).padStart(2, "0");
        var anio = hoy.getFullYear();
        var fecha = dia + "/" + mes + "/" + anio;

        // sección en el DOM
        var $section = $("<section></section>");
        var $h3 = $("<h3></h3>").text("El tiempo meteorológico hoy (" + fecha + ")");
        var $img = $("<img>").attr("src", urlIcono).attr("alt", descripcion);

        var stringDatos = "<ul><li>Temperatura actual: " + temperatura + " " + temperaturaUnit + "</li>";
        stringDatos += "<li>Sensación térmica: " + sensacion + " " + temperaturaUnit + "</li>";
        stringDatos += "<li>Humedad: " + humedad + " " + humedadUnit + "</li>";
        stringDatos += "<li>Presión atmosférica: " + presion + " " + presionUnit + "</li>";
        stringDatos += "<li>Velocidad del viento: " + velocidadViento + " metros/segundo</li>";
        stringDatos += "<li>Dirección del viento: " + direccionViento + " grados (" + nombreDireccionViento + ")</li>";
        stringDatos += "<li>Salida del sol: " + amanecerLocal + "</li>";
        stringDatos += "<li>Puesta del sol: " + oscurecerLocal + "</li></ul>";

        $section.append($h3);
        $section.append($img);
        $section.append(stringDatos);
        $("main").append($section);
    }
}

const ciudad = new Ciudad("Alcossebre", "España", "Gaspachero/a");
ciudad.rellenarAtributos(2326, 40.252003, 0.246447);

const seccion = document.createElement("section");

const h3 = document.createElement("h3");
h3.textContent = `${ciudad.getCiudad()}, ${ciudad.getPais()}`;
seccion.appendChild(h3);

seccion.insertAdjacentHTML("beforeend", ciudad.getInformacionSecundaria());

const h2 = document.querySelector("h2");
if (h2) {
    h2.insertAdjacentElement("afterend", seccion);
}

ciudad.escribeCoordenadas();
ciudad.getMeteorologia();
