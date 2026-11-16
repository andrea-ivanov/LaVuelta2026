"use strict"
class Ciclista {
    constructor(nombre, apellidos, dorsal, fechaNacimiento, nacionalidad) {
        this.nombre = nombre;
        this.apellidos = apellidos;
        this.dorsal = dorsal;
        this.fechaNacimiento = fechaNacimiento;
        this.nacionalidad = nacionalidad;
    }

    getNombreCompleto() {
        return `${this.nombre} ${this.apellidos}`;
    }

    getDorsal() {
        return this.dorsal;
    }

    getInformacionAdicional() {
        return `${this.fechaNacimiento} - ${this.nacionalidad}`;
    }
}

class Equipo {
    constructor(nombre, codigoUCI, pais) {
        this.nombre = nombre;
        this.codigoUCI = codigoUCI;
        this.pais = pais;
        this.director = "";
        this.categoria = "";
        this.web = "";
        this.alineacion = [];
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
                </ul> `;
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

    async leerEquipo() {
        const response = await fetch("js/lavuelta.json");
        const data = await response.json();
        const equipoData = this.equipos.find(eq => eq.codigoUci === this.codigoUCI);
        if (equipoData && equipoData.corredores) {
            this.alinearCiclistas(equipoData.corredores);
            this.mostrarAlineacion();
        }
    }

    alinearCiclistas(corredores) {
        corredores.forEach(c => {
            const ciclista = new Ciclista(c.nombre,
                c.apellidos,
                c.dorsal,
                c.fecha_nacimiento,
                c.nacionalidad)
            this.alineacion.push(ciclista);
        });
    }

    mostrarAlineacion() {
        this.alineacion.sort((a, b) => a.getDorsal() - b.getDorsal());  // ordeno por dorsal

        const sectionAlineacion = document.querySelectorAll("main > section")[1];
        if (!sectionAlineacion) return;

        // limpio los artículos estáticos y deno solo el h3
        const h3 = sectionAlineacion.querySelector("h3");
        sectionAlineacion.innerHTML = "";
        if (h3) {
            sectionAlineacion.appendChild(h3);
        }
        else {
            const nuevoH3 = document.createElement("h3");
            nuevoH3.textContent = "Alineación de corredores";
            sectionAlineacion.appendChild(nuevoH3);
        }

        // creao cada tarjeta article dinámicamente
        this.alineacion.forEach(ciclista => {
            const article = document.createElement("article");
            const h4 = document.createElement("h4");
            h4.textContent = ciclista.getNombreCompleto();

            const img = document.createElement("img");
            img.src = "multimedia/icono-ciclista.png";
            img.alt = `Icono de ciclista ${ciclista.getNombreCompleto()}`;
            img.width = 128;
            img.height = 128;

            const pDorsal = document.createElement("p");
            pDorsal.textContent = `Dorsal ${ciclista.getDorsal()}`;

            const pInfo = document.createElement("p");
            pInfo.textContent = ciclista.getInformacionAdicional();

            article.appendChild(h4);
            article.appendChild(img);
            article.appendChild(pDorsal);
            article.append(pInfo);

            sectionAlineacion.appendChild(article);
        });
    }
}

const equipo = new Equipo("EF EDUCATION - EASYPOST", "EFE", "Estados Unidos");
equipo.rellenarAtributos("Juan Manuel Garate / Ken Vanmarcke", "UCI WorldTeam", "https://www.lavuelta.es/es/equipo/EFE/ef-education-easypost");

const section = document.createElement("section");
const h3 = document.createElement("h3");

h3.textContent = `${equipo.datosBasicos()} - ${equipo.getPais()} `;
section.appendChild(h3);
section.insertAdjacentHTML("beforeend", equipo.getInformacionSecundaria());

const h2 = document.querySelector("h2");
if (h2) {
    h2.insertAdjacentElement("afterend", section);
}

equipo.getPaginaWeb();
equipo.leerEquipo();