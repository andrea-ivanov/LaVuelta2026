"use strict"
class Equipo {
    constructor(nombre, codigoUCI, pais) {
        this.nombre = nombre;
        this.codigoUCI = codigoUCI;
        this.pais = pais;
        this.director = "";
        this.categoria = "";
        this.web = "";
    }

    rellenarAtributos(director, categoria, web) {
        this.director = director;
        this.categoria = categoria;
        this.web = web;
    }

    datosBasicos() {
        return this.nombre + " " + this.codigoUCI;
    }

    getPais() {
        return this.pais;
    }

    getInformacionSecundaria() {
        return `<ul>
                <li><strong>Director: </strong> ${this.director}</li>
                <li><strong>Categoría: </strong> ${this.categoria}</li>
                </ul>`;
    }

    getPaginaWeb() {
        const section = document.querySelector("main > section");
        if (section) {
            const parrafo = document.createElement("p");
            const enlace = document.createElement("a");
            enlace.href = this.web;
            enlace.textContent = "Ficha oficial del equipo en La Vuelta 2026";
            enlace.title = "Ficha oficial del equipo en La Vuelta 2026";
            parrafo.appendChild(enlace);
            section.appendChild(parrafo)
        }
    }
}

const equipo = new Equipo("EF EDUCATION - EASYPOST", "EFE", "Estados Unidos");
equipo.rellenarAtributos("Juan Manuel Garate / Ken Vanmarcke", "UCI WorldTeam", "https://www.lavuelta.es/es/equipo/EFE/ef-education-easypost");

const section = document.createElement("section");
const h3 = document.createElement("h3");

h3.textContent = `${equipo.datosBasicos()} - ${equipo.getPais()}`;
section.appendChild(h3);
section.insertAdjacentHTML("beforeend", equipo.getInformacionSecundaria());

const h2 = document.querySelector("h2");
if (h2) {
    h2.insertAdjacentElement("afterend", section);
}

equipo.getPaginaWeb();