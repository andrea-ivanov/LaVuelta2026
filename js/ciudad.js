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
