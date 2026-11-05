import sqlite3
import time
from datetime import datetime

from lecture_dht11 import lire_avec_retry

PERIODE = 10  # secondes

# Q26 : un seul capteur en TP. Pour les 5 armoires :
# CONNEXIONS = {1: 4, 2: 17, 3: 27, 4: 22, 5: 23}
CONNEXIONS = {1: 26}  # armoire_id -> broche GPIO


def maintenant():
    # format "YYYY-MM-DD HH:MM:SS" : comparable avec datetime() de SQLite
    return datetime.now().isoformat(sep=" ", timespec="seconds")


def maj_episode(connexion, armoire_id, temperature, horodatage):
    """Q39 : ouvre / met à jour / ferme les épisodes de non-conformité."""
    a = connexion.execute(
        "SELECT temp_min, temp_max FROM Armoire WHERE id = ?", (armoire_id,)
    ).fetchone()
    hors_plage = temperature < a[0] or temperature > a[1]
    ouvert = connexion.execute(
        "SELECT id, temp_extreme FROM EpisodeNonConformite "
        "WHERE armoire_id = ? AND fin IS NULL", (armoire_id,)
    ).fetchone()
    milieu = (a[0] + a[1]) / 2
    if hors_plage and ouvert is None:
        connexion.execute(
            "INSERT INTO EpisodeNonConformite (armoire_id, debut, temp_extreme) "
            "VALUES (?, ?, ?)", (armoire_id, horodatage, temperature))
    elif hors_plage and ouvert is not None:
        if abs(temperature - milieu) > abs(ouvert[1] - milieu):
            connexion.execute(
                "UPDATE EpisodeNonConformite SET temp_extreme = ? WHERE id = ?",
                (temperature, ouvert[0]))
    elif not hors_plage and ouvert is not None:
        connexion.execute(
            "UPDATE EpisodeNonConformite SET fin = ? WHERE id = ?",
            (horodatage, ouvert[0]))


def enregistrer_mesure(connexion, armoire_id, temperature, humidite):
    ts = maintenant()
    connexion.execute(
        "INSERT INTO Mesure (armoire_id, horodatage, temperature, humidite) "
        "VALUES (?, ?, ?, ?)",
        (armoire_id, ts, temperature, humidite)
    )
    maj_episode(connexion, armoire_id, temperature, ts)
    connexion.commit()


def boucle_mesure():
    connexion = sqlite3.connect("temperatures.db")
    while True:
        debut = time.time()
        for armoire_id, pin in CONNEXIONS.items():
            try:
                temperature, humidite = lire_avec_retry(pin)
                enregistrer_mesure(connexion, armoire_id, temperature, humidite)
            except (TimeoutError, ValueError) as e:
                print(f"Armoire {armoire_id} : erreur de lecture ({e})", flush=True)
        # Q26 : on attend uniquement le temps restant
        duree_ecoulee = time.time() - debut
        time.sleep(max(0, PERIODE - duree_ecoulee))


if __name__ == "__main__":
    boucle_mesure()
