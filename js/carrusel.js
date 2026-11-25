"use strict";

class Carrusel {
    constructor() {
        this.busqueda = "la vuelta ciclista";
        this.actual = 0;
        this.maximo = 4;

        this.getFotografias();
    }

    getFotografias() {
        var flickrAPI = "https://api.flickr.com/services/feeds/photos_public.gne?jsoncallback=?";

        $.getJSON(flickrAPI, {
            tags: this.busqueda,
            tagmode: "any",
            format: "json"
        })
            .done((data) => {
                this.procesarJSONFotografias(data);
            })
            .fail((error) => {
                console.error("Error al obtener fotos")
            });
    }

    procesarJSONFotografias(data) {
        if (!data || !data.items || data.items.length === 0) return;

        var items = data.items.slice(0, 5);

        this.fotos = items.map(item => {
            const url640 = item.media.m.replace("_m.jpg", "_z.jpg");
            return {
                titulo: item.title || "Fotografía de La Vuelta",
                url: url640
            }
        });

        if (this.fotos.length > 0) {
            this.mostrarFotografias();
        }
    }

    mostrarFotografias() {
        const primeraFoto = this.fotos[0];

        // creación de elementos JQuery
        const $article = $("<article></article>");
        const $h2 = $("<h2></h2>").text("Instantáneas de LaVuelta");
        const $img = $("<img>").attr("src", primeraFoto.url).attr("alt", primeraFoto.titulo);

        $article.append($h2);
        $article.append($img);

        $("main").append($article);

        // cambia la foto cada 3 segundos
        setInterval(this.cambiarFotografia.bind(this), 3000);
    }

    cambiarFotografia() {
        this.actual++;
        if (this.actual > this.maximo || this.actual >= this.fotos.length) {
            this.actual = 0;
        }
        const foto = this.fotos[this.actual];
        $("article h2 + img")
            .attr("src", foto.url)
            .attr("alt", foto.titulo);
    }
}

const carrusel = new Carrusel();