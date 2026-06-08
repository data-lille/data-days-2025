// Rendu des slides PDF via pdf.js (fonctionne dans tous les navigateurs,
// indépendamment du réglage d'affichage PDF du navigateur).
(function () {
  "use strict";
  if (typeof pdfjsLib === "undefined") return;

  if (window.PDFJS_WORKER_SRC) {
    pdfjsLib.GlobalWorkerOptions.workerSrc = window.PDFJS_WORKER_SRC;
  }

  function renderPage(pdf, pageNum, holder, width) {
    pdf.getPage(pageNum).then(function (page) {
      var ratio = window.devicePixelRatio || 1;
      var unscaled = page.getViewport({ scale: 1 });
      var scale = width / unscaled.width;
      var viewport = page.getViewport({ scale: scale * ratio });

      var canvas = document.createElement("canvas");
      canvas.className = "slides-canvas";
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      canvas.style.width = "100%";
      canvas.style.height = "auto";

      holder.innerHTML = "";
      holder.appendChild(canvas);
      page.render({
        canvasContext: canvas.getContext("2d"),
        viewport: viewport,
      });
    });
  }

  function initViewer(viewer) {
    var url = viewer.getAttribute("data-pdf");
    var pagesWrap = viewer.querySelector(".slides-pages");
    if (!url || !pagesWrap) return;

    viewer.classList.add("is-loading");

    pdfjsLib
      .getDocument(url)
      .promise.then(function (pdf) {
        viewer.classList.remove("is-loading");
        var width = pagesWrap.clientWidth || 800;

        var section = viewer.closest(".talk-slides");
        var counter = section && section.querySelector(".slides-count");
        if (counter) {
          counter.textContent =
            " · " + pdf.numPages + " slide" + (pdf.numPages > 1 ? "s" : "");
        }

        // Crée un emplacement par page, au bon ratio, puis rend à la demande.
        var observer = new IntersectionObserver(
          function (entries) {
            entries.forEach(function (entry) {
              if (!entry.isIntersecting) return;
              var holder = entry.target;
              observer.unobserve(holder);
              renderPage(pdf, parseInt(holder.dataset.page, 10), holder, width);
            });
          },
          { root: pagesWrap, rootMargin: "300px 0px" }
        );

        var chain = Promise.resolve();
        for (var i = 1; i <= pdf.numPages; i++) {
          (function (pageNum) {
            chain = chain.then(function () {
              return pdf.getPage(pageNum).then(function (page) {
                var vp = page.getViewport({ scale: 1 });
                var holder = document.createElement("div");
                holder.className = "slides-page";
                holder.dataset.page = pageNum;
                // réserve la hauteur pour éviter les sauts de scroll
                holder.style.aspectRatio = vp.width + " / " + vp.height;
                pagesWrap.appendChild(holder);
                observer.observe(holder);
              });
            });
          })(i);
        }
      })
      .catch(function () {
        viewer.classList.remove("is-loading");
        viewer.classList.add("has-error");
        var msg = document.createElement("p");
        msg.className = "slides-error";
        msg.innerHTML =
          'Impossible d\'afficher l\'aperçu. <a href="' +
          url +
          '" target="_blank" rel="noopener">Ouvrir le PDF</a>.';
        viewer.appendChild(msg);
      });
  }

  document.querySelectorAll(".slides-viewer").forEach(initViewer);
})();
