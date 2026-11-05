import time
import RPi.GPIO as GPIO

PIN_DATA = 26  # broche à adapter au câblage (numérotation BCM)
SEUIL_BIT = 50e-6  # front haut > 50 µs => bit 1 (26-28 µs => bit 0)


def _duree_niveau(pin, niveau, timeout):
    """Mesure combien de temps la broche reste au 'niveau' donné.
    Renvoie None si le timeout est dépassé."""
    debut = time.perf_counter()
    while GPIO.input(pin) == niveau:
        if time.perf_counter() - debut > timeout:
            return None
    return time.perf_counter() - debut


def envoyer_signal_depart(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.018)  # >= 18 ms
    GPIO.output(pin, GPIO.HIGH)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # on rend la main au capteur


def attendre_reponse_capteur(pin):
    # la ligne est encore HAUTE (pull-up) jusqu'à ce que le capteur tire vers le bas
    if _duree_niveau(pin, GPIO.HIGH, 100e-6) is None:
        return False
    if _duree_niveau(pin, GPIO.LOW, 200e-6) is None:   # ~80 µs BAS
        return False
    if _duree_niveau(pin, GPIO.HIGH, 200e-6) is None:  # ~80 µs HAUT
        return False
    return True


def lire_bit(pin):
    # 1) fin du front bas (~50 µs)
    if _duree_niveau(pin, GPIO.LOW, 150e-6) is None:
        return None
    # 2) durée du front haut qui suit
    haut = _duree_niveau(pin, GPIO.HIGH, 150e-6)
    if haut is None:
        return None
    # 3) seuil
    return 1 if haut > SEUIL_BIT else 0


def lire_trame(pin):
    GPIO.setmode(GPIO.BCM)
    envoyer_signal_depart(pin)
    if not attendre_reponse_capteur(pin):
        raise TimeoutError("Pas de réponse du capteur")

    octets = [0, 0, 0, 0, 0]
    for i in range(40):
        bit = lire_bit(pin)
        if bit is None:
            raise TimeoutError(f"Bit {i} non reçu")
        octets[i // 8] = (octets[i // 8] << 1) | bit

    checksum = sum(octets[0:4]) & 0xFF
    if checksum != octets[4]:
        raise ValueError("Erreur de checksum")

    humidite = octets[0]
    temperature = octets[2]
    return temperature, humidite


def lire_avec_retry(pin, essais=5, pause=1.5):
    """Q19 : nouvelle tentative en cas d'échec (le DHT11 veut > 1-2 s entre deux lectures)."""
    derniere = None
    for _ in range(essais):
        try:
            return lire_trame(pin)
        except (TimeoutError, ValueError) as e:
            derniere = e
            time.sleep(pause)
    raise derniere


if __name__ == "__main__":
    try:
        while True:
            try:
                temp, hum = lire_trame(PIN_DATA)
                print(f"Température : {temp} °C — Humidité : {hum} %")
            except (TimeoutError, ValueError) as e:
                print(f"Erreur de lecture : {e}")
            time.sleep(2)  # datasheet : période d'échantillonnage > 2 s (5 s recommandé)
    finally:
        GPIO.cleanup()
