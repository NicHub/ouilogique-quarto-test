
function targetBlank() {
    const _a = document.getElementsByTagName("a");
    const _siteHost = location.host.replace(/^www\./i, "");
    const internalRegex = new RegExp(_siteHost, "i");

    for (let i = 0; i < _a.length; i++) {
        let href = _a[i].href;
        let isExternal = false;

        if (/^mailto:/i.test(href)) {
            // Si le lien commence par mailto: il est forcément externe
            isExternal = true;
        } else if (location.protocol === "file:") {
            // Si on est en protocole file://
            // tous les liens http/https et protocol-relative sont externes
            isExternal = /^(https?:)?\/\//i.test(href);
        } else {
            // Logique normale pour http/https
            // Un lien est externe s’il a un host et que ce host ne correspond pas au site actuel
            let linkHost = _a[i].host;
            isExternal = linkHost && !internalRegex.test(linkHost);
        }

        if (isExternal) {
            // Attribue `_blank` à l’attribut `target`.
            _a[i].setAttribute("target", "_blank");

            // Ajoute `noopener` à l’attribut `rel`.
            const rel = (_a[i].getAttribute("rel") || "").trim();
            const relParts = rel ? rel.split(/\s+/) : [];
            if (!relParts.includes("noopener")) relParts.push("noopener");
            _a[i].setAttribute("rel", relParts.join(" ").trim());
        }
        // console.log(`${String(isExternal).padEnd(5)} ${_siteHost} ${href}`);
    }
}
targetBlank();
