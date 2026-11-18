"use strict";

class Formulario {
    constructor() {
        this.puntuacion = 0;
        this.dureza = 0;
        this.descripcion = "";
        this.usuario = "";

        const boton = document.querySelector('form button[type="submit"]');
        if (boton) {
            boton.addEventListener("click", this.analizar.bind(this));
        }
    }

    analizar(event) {
        event.preventDefault();
        this.puntuacion = 0;

        const form = event.target.closest("form");
        if (!form) return;

        // Datos no puntuables para el mensaje final
        const inputDureza = form.querySelector('input[name="dureza-etapa"]');
        const inputDesc = form.querySelector('textarea[name="descripcion-etapa"]');
        const inputUsuario = form.querySelector('input[name="nombre-participante"]');

        this.dureza = inputDureza ? inputDureza.value : "";
        this.descripcion = inputDesc ? inputDesc.value : "";
        this.usuario = inputUsuario ? inputUsuario.value : "";

        // Comprobación respuestas correctas (Etapa 6: Alcossebre - Castelló)
        const numero = form.querySelector('input[name="numero-etapa"]')?.value.trim();
        if (numero === "6") this.puntuacion++;

        const fecha = form.querySelector('input[name="fecha-etapa"]')?.value;
        if (fecha === "2026-09-12") this.puntuacion++;

        const salida = form.querySelector('select[name="salida-etapa"]')?.value;
        if (salida === "alcossebre") this.puntuacion++;

        const llegada = form.querySelector('select[name="llegada-etapa"]')?.value;
        if (llegada === "castelló") this.puntuacion++;

        const tipo = form.querySelector('input[name="tipo-etapa"]:checked')?.value;
        if (tipo === "mediamontaña") this.puntuacion++;

        // Hitos de la etapa 6: tiene puerto de montaña y sprint intermedio
        const hitosSeleccionados = Array.from(form.querySelectorAll('input[name="hito"]:checked')).map(cb => cb.value);
        const tienePuerto = hitosSeleccionados.includes("puerto");
        const tieneSprint = hitosSeleccionados.includes("sprint-inter");
        const sinIncorrectos = !hitosSeleccionados.includes("esp") && !hitosSeleccionados.includes("sprint-bonif") && !hitosSeleccionados.includes("sin");

        if (tienePuerto && tieneSprint && sinIncorrectos) this.puntuacion++;

        const longitud = parseFloat(form.querySelector('input[name="longitud-etapa"]')?.value);
        if (!isNaN(longitud) && Math.abs(longitud - 195.4) < 1) this.puntuacion++;

        const desnivel = parseFloat(form.querySelector('input[name="desnivel-etapa"]')?.value);
        if (!isNaN(desnivel) && desnivel === 3094) this.puntuacion++;

        this.calificar(form);
    }

    calificar(form) {
        // eliminamos mensaje anterior de calificación si ya había uno
        const anterior = form.parentElement.querySelector("p.resultado-calificacion");
        if (anterior) anterior.remove();

        const p = document.createElement("p");
        p.classList.add("resultado-calificacion");
        p.textContent = `${this.usuario} has obtenido ${this.puntuacion} puntos, la dureza que has asignado a la etapa es ${this.dureza} y tu descripción ${this.descripcion}`;

        form.insertAdjacentElement("afterend", p);
    }
}

const formularioJuego = new Formulario();