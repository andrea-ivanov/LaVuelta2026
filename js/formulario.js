"use strict"
class Formulario {
    constructor() {
        this.puntuacion = 0;
        this.dureza = 0;
        this.descripcion = "";
        this.usuario = "";

        const boton = document.querySelector('form button[type="submit"]');
        if (buton) {
            boton.addEventListener("click", this.analizar.bind(this));
        }

        const checkboxes = document.querySelectorAll('input[type="checkbox"] [name="hito"]');
        checkboxes.forEach(cb => {
            cb.addEventListener("change", (e) => {
                if (e.target.checked) {
                    checkboxes.forEach(otro => {
                        if (otro != e.target) otro.checked = false;
                    })
                }
            })
        })
    }

    analiza(event) {
        event.preventDefault();
        this.puntuacion = 0;

        const form = event.target.closest("form");
        if (!form) return;

        
    }
}