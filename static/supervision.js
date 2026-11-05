// Q35 : rafraîchissement sans rechargement, toutes les 10 s
const LIBELLES = { ok: "Conforme", alerte: "Alerte", critique: "Critique", inconnu: "Pas de mesure récente" };

function carte(a) {
  const t = a.temperature === null ? "—" : a.temperature.toFixed(0) + " °C";
  const heure = a.horodatage ? a.horodatage.slice(11, 19) : "";
  return `<article class="armoire ${a.etat}" data-id="${a.armoire_id}">
    <h2>${a.nom}</h2>
    <div class="produit">${a.type_produit}</div>
    <div class="temp">${t}</div>
    <div class="plage">Plage : ${a.temp_min} à ${a.temp_max} °C</div>
    <div class="statut">${LIBELLES[a.etat]}</div>
    <div class="heure">${heure}</div>
  </article>`;
}

async function rafraichir() {
  try {
    const r = await fetch("/api/dernieres");
    const donnees = await r.json();
    document.getElementById("grille").innerHTML = donnees.map(carte).join("");
    document.getElementById("maj").textContent = new Date().toLocaleTimeString("fr-FR");
  } catch (e) {
    document.getElementById("maj").textContent = "connexion perdue";
  }
}
setInterval(rafraichir, 10000);
rafraichir();
