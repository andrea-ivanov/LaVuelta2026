"use strict"

class Noticias {
    constructor() {
        this.busqueda = '"Vuelta a España" | "EF Education" | ciclismo';
        this.url = "https://api.thenewsapi.com/v1/news/all";
        this.apiKey = "Fr0tK9kJJ9J4qn0yqc6BTpTVZTU5toB4nxBNpeiQ";
    }

    async buscar() {
        const urlCompleta = `${this.url}?api_token=${this.apiKey}&search=${encodeURIComponent(this.busqueda)}&language=es`;

        try {
            const respuesta = await fetch(urlCompleta);
            if (!respuesta.ok) {
                throw new Error("Error en la petición: " + respuesta.status);
            }
            const datos = await respuesta.json();
            this.procesarInformacion(datos);
        } catch (error) {
            console.error("Error al obtener las noticias:", error);
        }
    }

    procesarInformacion(datos) {
        if (!datos || !datos.data || datos.data.length === 0) {
            return;
        }

        const $section = $("<section></section>");
        const $h2 = $("<h2></h2>").text("Noticias");
        $section.append($h2);

        datos.data.forEach((noticia) => {
            const $article = $("<article></article>");
            const $h3 = $("<h3></h3>").text(noticia.title);
            const $pEntradilla = $("<p></p>").text(noticia.description || noticia.snippet || "");
            const $a = $("<a></a>")
                .attr("href", noticia.url)
                .attr("target", "_blank")
                .attr("rel", "noopener noreferrer")
                .text("Leer noticia en " + (noticia.source || "la fuente"));
            const $pEnlace = $("<p></p>").append($a);
            $article.append($h3, $pEntradilla, $pEnlace);
            $section.append($article);
        });
        $("main").append($section);
    }
}

const noticias = new Noticias();
noticias.buscar();