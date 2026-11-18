"use strict";

class Buscador {
    constructor() {
        const lupa = document.querySelector('search label img');
        const input = document.querySelector('search input[type="search"]');

        if (lupa) {
            lupa.addEventListener("click", (event) => {
                event.preventDefault();
                this.buscar();
            });
        }

        if (input) {
            // Escuchamos keydown y keypress para asegurar que Enter funcione en cualquier navegador
            input.addEventListener("keydown", (event) => {
                if (event.key === "Enter") {
                    this.buscar();
                }
            });
            input.addEventListener("keypress", (event) => {
                if (event.key === "Enter") {
                    this.buscar();
                }
            });
        }
    }

    limpiar_busqueda() {
        const marks = document.querySelectorAll("mark");
        marks.forEach(mark => {
            const textNode = document.createTextNode(mark.textContent);
            mark.replaceWith(textNode);
        });
        document.body.normalize();
    }

    buscar() {
        this.limpiar_busqueda();

        const input = document.querySelector('search input[type="search"]');
        if (!input) return;

        const texto = input.value.trim();
        if (texto === "") return;

        const regexp = new RegExp(texto, "gi");
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        const resultados = [];

        let node = walker.nextNode();
        while (node) {
            // Evitamos buscar dentro de search, script o style
            const dentroDeSearch = node.parentElement && node.parentElement.closest("search");
            const esScriptOStyle = node.parentElement && (node.parentElement.tagName === "SCRIPT" || node.parentElement.tagName === "STYLE");

            if (!dentroDeSearch && !esScriptOStyle) {
                regexp.lastIndex = 0;
                if (regexp.test(node.textContent)) {
                    resultados.push(node);
                }
            }
            node = walker.nextNode();
        }

        resultados.forEach(n => {
            if (!n.isConnected || !n.parentElement) return;
            regexp.lastIndex = 0;
            const new_text = n.textContent.replaceAll(regexp, "<mark>$&</mark>");
            if (n.parentElement.childNodes.length === 1) {
                n.parentElement.innerHTML = new_text;
            } else {
                const span = document.createElement("span");
                span.innerHTML = new_text;
                n.replaceWith(...span.childNodes);
            }
        });
    }
}

const buscador = new Buscador();