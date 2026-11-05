import io
import os
import sqlite3
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temperatures.db")
MARGE_ALERTE = 2.0        # °C : au-delà de 2 °C hors plage => critique (rouge)
DELAI_DONNEE_PERIMEE = 60  # s : sonde muette => état "inconnu"


def connexion_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- Authentification (exigence 1.3.1) ----------
def authentifie(f):
    """HTTP Basic. Identifiants dans SUPERVISION_USER / SUPERVISION_PASSWORD."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        ok = (auth and auth.username == os.environ.get("SUPERVISION_USER", "chef")
              and auth.password == os.environ.get("SUPERVISION_PASSWORD", ""))
        if not os.environ.get("SUPERVISION_PASSWORD") or not ok:
            return Response("Authentification requise", 401,
                            {"WWW-Authenticate": 'Basic realm="Supervision COGIP"'})
        return f(*args, **kwargs)
    return wrapper


# ---------- Logique métier ----------
def etat(armoire, mesure):
    """Renvoie (conforme, etat) avec etat in ok / alerte / critique / inconnu."""
    if mesure is None:
        return False, "inconnu"
    age = (datetime.now() - datetime.fromisoformat(mesure["horodatage"])).total_seconds()
    if age > DELAI_DONNEE_PERIMEE:
        return False, "inconnu"
    t = mesure["temperature"]
    ecart = max(armoire["temp_min"] - t, t - armoire["temp_max"], 0)
    if ecart == 0:
        return True, "ok"
    return False, "alerte" if ecart <= MARGE_ALERTE else "critique"


def dernieres_mesures():
    conn = connexion_db()
    resultat = []
    for armoire in conn.execute("SELECT * FROM Armoire ORDER BY id").fetchall():
        mesure = conn.execute(
            "SELECT * FROM Mesure WHERE armoire_id = ? ORDER BY horodatage DESC LIMIT 1",
            (armoire["id"],)).fetchone()
        conforme, e = etat(armoire, mesure)
        resultat.append({
            "armoire_id": armoire["id"],
            "nom": armoire["nom"],
            "type_produit": armoire["type_produit"],
            "temp_min": armoire["temp_min"],
            "temp_max": armoire["temp_max"],
            "temperature": mesure["temperature"] if mesure else None,
            "horodatage": mesure["horodatage"] if mesure else None,
            "conforme": conforme,
            "etat": e,
        })
    conn.close()
    return resultat


# ---------- Routes ----------
@app.route("/")
@authentifie
def dashboard():
    return render_template("dashboard.html", donnees=dernieres_mesures())


@app.route("/api/dernieres")
def api_dernieres():
    return jsonify(dernieres_mesures())


@app.route("/historique/<int:armoire_id>")
@authentifie
def historique(armoire_id):
    conn = connexion_db()
    armoire = conn.execute("SELECT * FROM Armoire WHERE id = ?", (armoire_id,)).fetchone()
    if armoire is None:
        return "Armoire inconnue", 404
    mesures = conn.execute(
        "SELECT horodatage, temperature FROM Mesure "
        "WHERE armoire_id = ? AND horodatage >= datetime('now', 'localtime', '-7 days') "
        "ORDER BY horodatage", (armoire_id,)).fetchall()
    conn.close()
    points = [{"t": m["horodatage"], "y": m["temperature"]} for m in mesures]
    return render_template("historique.html", points=points, armoire=dict(armoire))


@app.route("/affichage")
def affichage_cuisine():
    # écran de cuisine : lecture seule, sans navigation
    return render_template("affichage_cuisine.html")


@app.route("/rapport.pdf")
@authentifie
def rapport_pdf():
    """Q41 : rapport imprimable ?debut=2026-10-01&fin=2026-10-07 (PDF via reportlab)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer

    try:
        debut = request.args.get("debut") or (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        fin = request.args.get("fin") or datetime.now().strftime("%Y-%m-%d")
        datetime.strptime(debut, "%Y-%m-%d"); datetime.strptime(fin, "%Y-%m-%d")
    except ValueError:
        return "Dates attendues au format AAAA-MM-JJ", 400

    conn = connexion_db()
    styles = getSampleStyleSheet()
    elems = [Paragraph(f"Relevé des températures — du {debut} au {fin}", styles["Title"])]
    for a in conn.execute("SELECT * FROM Armoire ORDER BY id").fetchall():
        stats = conn.execute(
            "SELECT MIN(temperature) mn, MAX(temperature) mx, AVG(temperature) moy, COUNT(*) n "
            "FROM Mesure WHERE armoire_id = ? AND date(horodatage) BETWEEN ? AND ?",
            (a["id"], debut, fin)).fetchone()
        eps = conn.execute(
            "SELECT debut, fin, temp_extreme, action_corrective FROM EpisodeNonConformite "
            "WHERE armoire_id = ? AND date(debut) BETWEEN ? AND ? ORDER BY debut",
            (a["id"], debut, fin)).fetchall()
        elems.append(Paragraph(
            f"{a['nom']} — {a['type_produit']} (plage {a['temp_min']} à {a['temp_max']} °C)",
            styles["Heading3"]))
        if stats["n"]:
            elems.append(Paragraph(
                f"{stats['n']} mesures — min {stats['mn']} °C, max {stats['mx']} °C, "
                f"moyenne {stats['moy']:.1f} °C", styles["Normal"]))
        else:
            elems.append(Paragraph("Aucune mesure sur la période.", styles["Normal"]))
        if eps:
            rows = [["Début", "Fin", "T° extrême", "Action corrective"]] + [
                [e["debut"], e["fin"] or "en cours", e["temp_extreme"], e["action_corrective"] or ""]
                for e in eps]
            elems.append(Table(rows))
        else:
            elems.append(Paragraph("Aucun épisode de non-conformité.", styles["Normal"]))
        elems.append(Spacer(1, 12))
    conn.close()

    buf = io.BytesIO()
    SimpleDocTemplate(buf, pagesize=A4).build(elems)
    return Response(buf.getvalue(), mimetype="application/pdf",
                    headers={"Content-Disposition": f"inline; filename=rapport_{debut}_{fin}.pdf"})


if __name__ == "__main__":
    app.run(host="192.168.1.216", port=5001)
