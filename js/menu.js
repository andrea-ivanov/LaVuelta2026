"use strict"

class Menu {
    constructor() {
        this.button = document.querySelector("header > button");
        this.menu = document.querySelector("header nav");

        if (this.button)
            this.button.addEventListener("click", this.desplegar.bind(this));
    }

    desplegar() {
        const nav = document.querySelector("nav");
        if (!nav || !this.button) return;

        nav.classList.toggle("abierto");

        const isOpen = nav.classList.contains("abierto");
        this.button.textContent = isOpen ? "x" : "☰";
        this.button.setAttribute("aria-expanded", isOpen ? "true" : "false");
    }
}

const menu = new Menu();