[link text]([https://]([https://]([https://]([https://](https://)))))## Compte rendu de l'Act01a-temperatures-dht11

### Exigences client

#### **Q1 : Diagramme de cas d'utilisation compléter** 

![Diagramme-de-cas-d'utilisation-(Question-n°1).png](https://share.jotbird.com/images/901ee673-7596-4d73-8c0c-1263f52bca31.png)

### Capteur de température

#### **Q2 : Identification des éléments du capteur DHT11**

    1.Résistance de pull-up : Le composant physique sur la carte qui garantit l'état HAUT sur la ligne de données.
    2.Broche DATA (Signal) : Marquée `S`, c'est la broche de transmission des données.
    3.Broche Vcc (Alimentation) : C'est la broche d'alimentation `+` (3.3V).
    4.Broche GND (Masse) : Marquée `-`, c'est la broche de référence 0V.
    
#### **Q3 : Rôle d'une résistance de pull-up**

La résistance de pull-up est essentielle au bon fonctionnement de la communication avec le capteur DHT11. Son rôle est de **garantir un état logique stable sur la ligne de données (DATA)**.

La communication avec ce capteur utilise un principe de "collecteur ouvert", où les dispositifs peuvent uniquement forcer la ligne à un état BAS (0V). Sans rien, lorsque aucun dispositif n'agit, la ligne serait dans un état indéfini dit "flottant".

La résistance de pull-up, connectée entre la ligne DATA et l'alimentation (Vcc), **"tire" la tension de la ligne vers le niveau HAUT (3.3V) par défaut**.

#### **Elle assure ainsi que :**
- L'état HAUT est l'état de repos de la ligne.
- La communication peut se faire de manière fiable, les dispositifs n'ayant qu'à tirer la ligne vers le BAS pour transmettre l'information.

### Micro-contrôleur

#### **Q4 : Explication de l'acronyme GPIO**

L'acronyme **GPIO** signifie **G**eneral **P**urpose **I**nput **O**utput (Entrée/Sortie à Usage Général).

Il s'agit des broches physiques sur le Raspberry Pi qui permettent au nano-ordinateur d'interagir avec des circuits électroniques externes. Leur particularité est d'être programmables :

*   **Input (Entrée)** : La broche est configurée pour lire un signal électrique externe. Elle peut ainsi détecter l'état d'un capteur, d'un interrupteur ou d'un bouton.
*   **Output (Sortie)** : La broche est configurée pour générer un signal électrique. Elle peut ainsi commander un composant externe, comme allumer une LED, activer un relais ou faire tourner un moteur.

Les GPIO sont donc le pont entre le monde logiciel (le code Python) et le monde physique (les composants électroniques).

#### **Q5 : Compatibilité des exécutables entre une VM Linux et un Raspberry Pi**

**Non**, un fichier exécutable compilé sur une VM Linux standard ne peut pas être directement exécuté sur un Raspberry Pi.

**Justification :**

La raison principale est la **différence d'architecture du processeur**.

1.  Une machine virtuelle (VM) Linux sur un ordinateur personnel utilise l'architecture du processeur hôte, qui est quasi-systématiquement **x86_64** (Intel/AMD).
2.  Le Raspberry Pi utilise un processeur basé sur l'architecture **ARM**.

Un fichier exécutable est une suite d'instructions machines spécifiques à une architecture. Tenter d'exécuter un binaire x86_64 sur un processeur ARM (ou l'inverse) échouera avec une erreur de format. Pour qu'un programme compilé fonctionne sur le Raspberry Pi, il doit être soit compilé directement sur le Pi, soit compilé sur une autre machine via un processus appelé "cross-compilation" (compilation croisée) qui cible spécifiquement l'architecture ARM.

#### **Q6 : Découverte du Raspberry Pi avec Nmap**

Pour découvrir les hôtes actifs sur le réseau local, nous utilisons la commande `nmap` avec l'option `-sn`. Cette option effectue un "ping scan" pour lister les machines qui répondent sans effectuer de scan de ports, ce qui est plus rapide.

La commande est la suivante (en adaptant l'adresse du sous-réseau) :

```bash
nmap -sn 192.168.1.0/24
```
####  Captures d'écran:

Scan AVANT branchement du Raspberry Pi :
![Scan-Nmap-avant](https://share.jotbird.com/images/e8623b6d-c60c-46e2-9e54-b0d29f0024a6.png)

**Scan APRÈS branchement du Raspberry Pi :**
![Scan-Nmap-après](https://share.jotbird.com/images/2caf1aff-f8aa-416c-8c68-62190c8dd362.png)

En comparant les deux résultats, on constate l'apparition d'un nouvel hôte à l'adresse **"192.168.1.19"**. Il s'agit de l'adresse IP de notre Raspberry Pi.

#### **Q7 : Connexion SSH au Raspberry Pi**

Pour se connecter au terminal du Raspberry Pi à distance, nous utilisons le protocole SSH (Secure Shell). La commande `ssh` est utilisée depuis le terminal de notre machine locale (la VM Linux).

La syntaxe est `ssh <utilisateur>@<adresse_ip>`. En utilisant les informations du projet :
- L'utilisateur par défaut sur Raspberry Pi OS est `pi`.
- L'adresse IP a été identifiée à la question précédente.

La commande pour se connecter est donc (en remplaçant XXX.XXX.XXX.XXX par l'IP réelle) :

```bash
ssh pi@XXX.XXX.XXX.XXX
```
####  Captures d'écran:

![Connexion SSH au Raspberry](https://share.jotbird.com/images/2074f437-f42c-4878-aa17-085750627e0c.png)

#### **Q8 : Obtention d'informations système sur le Raspberry Pi**
-
**1. Nom de la machine :**
La commande `hostname` permet d'afficher le nom réseau de la machine.
```bash
pi@raspberrypi:~ $ hostname
raspberrypi
```
![Capture-d'écran-2026-10-07-143154.png](https://share.jotbird.com/images/177f2927-93b0-4de5-af29-67ec530d233e.png)
**2. Version du noyau Linux :**
La commande `uname -r` affiche la version du kernel (noyau) actuellement en cours d'exécution.
```bash
pi@raspberrypi:~ $ uname -r
```
![Capture-d'écran-2026-10-07-143332.png](https://share.jotbird.com/images/4960f02c-8647-4f81-bce6-4438bf9c0c45.png)
**3. Adresses IP des interfaces réseau :**
La commande `ip a` (ou `ip address`) liste toutes les interfaces réseau et leurs configurations IP.
```bash
pi@raspberrypi:~ $ ip a
```
![Capture-d'écran-2026-10-07-143430.png](https://share.jotbird.com/images/1e1e8e1f-1fb7-488d-bf82-c2e8b87b4218.png)

### Protocole de communication du DHT11

#### **Q9 : Chronogramme de l'octet 00100101 (valeur 37)**

Le protocole du DHT11 code la valeur d'un bit par la durée de l'impulsion à l'état HAUT qui suit une impulsion BAS de 50µs :
- **Bit 0 :** Impulsion HAUT courte (~26-28µs).
- **Bit 1 :** Impulsion HAUT longue (~70µs).

Voici la représentation schématique (chronogramme) de la transmission de l'octet `00100101` :

![Chronogramme de l'octet 37](https://share.jotbird.com/images/23adc871-d222-4b62-9adc-f157ee90dd06.png)

*(Explication du schéma ci-dessus)*
Le signal est une succession de 8 séquences "BAS puis HAUT". On peut y voir :
- Deux impulsions courtes (bits 0, 0).
- Une impulsion longue (bit 1).
- Deux impulsions courtes (bits 0, 0).
- Une impulsion longue (bit 1).
- Une impulsion courte (bit 0).
- Une impulsion longue (bit 1).

#### **Q10 : Utilité de la vérification du checksum**

Le checksum, ou octet de contrôle, est un mécanisme simple mais crucial pour **garantir l'intégrité des données** transmises par le capteur DHT11.

La communication entre le Raspberry Pi et le capteur est basée sur la mesure de durées d'impulsions très courtes (en microsecondes). Ce processus est sensible aux erreurs qui peuvent être causées par des parasites électriques, des problèmes de timing de lecture ou des mauvais contacts. Une seule erreur peut transformer un bit '0' en '1' (ou inversement), faussant ainsi complètement la valeur de température ou d'humidité.

Le principe de la vérification est le suivant :
1.  Le capteur additionne les 4 premiers octets de données (humidité et température) et envoie le résultat sous la forme d'un 5ème octet : le checksum.
2.  Notre programme sur le Raspberry Pi, après avoir reçu les 5 octets, effectue lui-même l'addition des 4 premiers.
3.  Il compare ensuite son propre résultat avec le checksum reçu.

Si les deux valeurs ne correspondent pas, cela signifie qu'une **erreur de transmission** s'est produite. Les données sont alors considérées comme corrompues et doivent être ignorées. La vérification du checksum est donc un **mécanisme de détection d'erreur** indispensable pour assurer la fiabilité des mesures enregistrées.

### Contraintes liées à l'utilisation de Raspberry Pi OS

#### **Q11 : Conséquence du système non-temps-réel**

Le Raspberry Pi OS est un système d'exploitation multitâche et non-temps-réel. Cela signifie que le noyau du système peut interrompre l'exécution de n'importe quel programme à tout moment pour allouer du temps processeur à d'autres tâches. Ces interruptions sont imprévisibles et peuvent durer de quelques microsecondes à plusieurs millisecondes.

La lecture du capteur DHT11 repose sur la mesure de la durée d'impulsions électriques très courtes (26µs à 70µs). Si le système d'exploitation interrompt notre script Python pendant qu'il est en train de mesurer la durée d'une impulsion, le temps mesuré par le script sera artificiellement allongé (temps réel de l'impulsion + durée de l'interruption).

**Conséquence concrète :**

Cette imprécision dans la mesure du temps mènera inévitablement à des erreurs de lecture. Un bit '0' (impulsion courte) pourra être interprété à tort comme un bit '1' (impulsion longue). Par conséquent, la trame de 40 bits lue sera erronée.

La conséquence la plus directe et observable est donc un **taux d'échec de lecture significatif**. Un certain pourcentage de tentatives de lecture du capteur échouera à la vérification du checksum, non pas à cause d'un problème matériel, mais à cause des limitations logicielles inhérentes à un système non-temps-réel.

### Écriture du programme de lecture

#### **Q12 : Création de la structure du projet**

Connecté en SSH sur le Raspberry Pi, nous avons créé le répertoire du projet et son fichier `README.md` initial avec les commandes suivantes :

```bash
# Se placer dans le répertoire personnel de l'utilisateur pi
cd ~

# Créer le répertoire du projet
mkdir supervision

# Se déplacer dans le nouveau répertoire
cd supervision

# Créer le fichier README.md avec son contenu initial
echo "# Supervision." > README.md
```
#### **Q13 : Initialisation du dépôt Git local**

Pour que Git puisse commencer à suivre les modifications de notre projet, nous devons initialiser un dépôt. En nous plaçant à l'intérieur du répertoire `supervision`, nous avons exécuté la commande suivante :

```bash
pi@raspberrypi:~/supervision $ git init
```
#### **Q14 : Réalisation du premier commit**

Après avoir initialisé le dépôt, nous avons effectué notre premier commit pour sauvegarder l'état initial du projet (le fichier `README.md`).

**1. Configuration de l'identité Git :**
Nous avons d'abord configuré notre nom et notre e-mail pour signer les commits.
```bash
git config user.name "Mon Nom"
git config user.email "mon.email@domaine.com"
```
**2. Ajout du fichier à l'index (staging area) :**
Nous avons utilisé `git add`pour indiquer à Git que nous voulions inclure le fichier `README.md` dans notre prochain commit.
```bash
git add README.md
```
**3. Création du commit :**
Enfin, nous avons créé le commit avec un message descriptif à l'aide de la commande `git commit -m`.
```bash
git commit -m "Création projet supervision des températures"
```
#### **Q15 : Création du script de lecture `lecture_dht11.py`**

Nous avons créé le fichier principal pour la lecture du capteur DHT11. En utilisant l'éditeur de texte `nano` directement sur le Raspberry Pi, nous avons créé le fichier `lecture_dht11.py` dans le répertoire `supervision` et y avons inséré le squelette de code fourni dans le sujet.

La commande utilisée pour ouvrir l'éditeur était :
```bash
nano lecture_dht11.py
```
#### **Q16 : Ajout et commit du script `lecture_dht11.py`**

Suite à la création du fichier `lecture_dht11.py`, nous l'avons ajouté à notre dépôt Git pour en suivre l'évolution.

**1. Vérification de l'état du dépôt :**
La commande `git status` nous a montré que le fichier `lecture_dht11.py` était présent mais non suivi ("Untracked file").

**2. Ajout du fichier à l'index :**
Nous avons utilisé `git add` pour l'inclure dans la préparation du prochain commit.
```bash
git add lecture_dht11.py
```
**3. Création du commit :**

Enfin, nous avons créé le commit en respectant la consigne de nommage du sujet.
```bash
git commit -m "Q16: Ajout squelette script lecture DHT11"
```

#### **Q17 : Implémentation des fonctions bas niveau**

Nous avons complété les trois fonctions essentielles à la communication avec le capteur DHT11 en manipulant directement les GPIO (`bit-banging`).

**1. `envoyer_signal_depart(pin)`**
Cette fonction a été complétée pour envoyer la séquence de démarrage : un signal BAS de 18ms, suivi d'un bref signal HAUT de 30µs, avant de passer la broche en mode entrée pour écouter la réponse du capteur.

**2. `attendre_reponse_capteur(pin)`**
La fonction vérifie la présence de la séquence de réponse du capteur (BAS puis HAUT). Elle utilise des boucles d'attente active pour détecter les changements d'état sur la broche et des compteurs de sécurité pour éviter un blocage infini.

**3. `lire_bit(pin)`**
C'est la fonction la plus critique. Elle attend le début de l'impulsion HAUT, mesure sa durée à l'aide de `time.perf_counter()`, et retourne `1` si la durée est longue (supérieure à 40µs, caractéristique d'un bit '1') ou `0` si elle est courte.

Voici un extrait du code implémenté pour `lire_bit` :
```python
def lire_bit(pin):
    # Attendre la fin du front BAS de 50µs (la ligne passe à HAUT)
    while GPIO.input(pin) == GPIO.LOW:
        pass
    
    # Mesurer la durée du front HAUT
    start_time = time.perf_counter()
    while GPIO.input(pin) == GPIO.HIGH:
        pass
    end_time = time.perf_counter()
    
    # Si la durée est supérieure à un seuil, c'est un '1'
    if (end_time - start_time) > 0.00004:
        return 1
    else:
        return 0
```

#### **Q18 : Commit de l'implémentation du script**

Après avoir complété les fonctions de lecture bas niveau dans `lecture_dht11.py`, nous avons sauvegardé cette version de travail dans notre dépôt Git.

La commande `git status` a confirmé que le fichier avait été modifié. Nous avons ensuite suivi le processus habituel pour créer un commit :

**1. Ajout des modifications à l'index :**
```bash
git add lecture_dht11.py
```
**2. Création du commit :**
```bash
git commit -m "Q18: Implémentation des fonctions de lecture bas niveau du DHT11"
```

#### **Q19 : Tester la lecture, comparer à un étalon, calculer le taux d'échec**

![image.png](https://share.jotbird.com/images/a67d41cf-3394-4a4a-9894-c4b6679ca1d6.png)

#### **Q20 : Le DHT11 répond-il aux exigences du client ?**

pour une installation réelle, il faut une sonde couvrant le
froid négatif avec une incertitude adaptée aux seuils (par exemple chaîne
Pt100 ou sonde numérique qualifiée, incertitude ≤ ±0,5 °C), avec vérification
métrologique dans les conditions réelles. Le logiciel supervise ; il ne
remplace ni la régulation frigorifique ni les contrôles des aliments.

### Choix du système de gestion de base de données

#### **Q21 : Comparer SQLite, MariaDB et PostgreSQL**

![image.png](https://share.jotbird.com/images/183f73a7-d982-4cd9-8deb-b015a0dcbe7b.png)

Choix : SQLite, conformément au sujet. Une acquisition toutes les 10 s pour cinq armoires est compatible avec un unique processus écrivain ; chaque requête web ouvre sa propre connexion de lecture. Le mode WAL améliore la coexistence lecture/écriture, sans autoriser plusieurs écrivains simultanés.

### Modèle de données

#### **Q22 : Dessiner le schéma relationnel**

![image.png](https://share.jotbird.com/images/c284014e-ea7d-4024-a5cb-bc53be2e5798.png)

#### **Q23 : Justifier l'index (armoire_id, horodatage)**
```SQL
CREATE INDEX idx_mesure_armoire_date ON Mesure(armoire_id, horodatage);
```
Cet index correspond aux deux critères combinés des requêtes fréquentes : l'armoire concernée puis la période. Il limite les lignes parcourues pour l'historique des sept derniers jours et la recherche de la dernière mesure.

#### **Q24 : Volume hebdomadaire et purge**

Durée d'une semaine         = 7 × 24 × 60 × 60 = 604 800 s
Mesures par armoire         = 604 800 / 10    = 60 480
Mesures pour cinq armoires  = 60 480 × 5      = 302 400 lignes
Taille estimée              = 302 400 × 40    = 12 096 000 octets
                             ≈ 12,1 Mo (décimaux) ≈ 11,54 Mio

Démarche : nombre de cycles sur une semaine × cinq armoires, avec l'hypothèse du sujet de 40 octets par ligne et des lectures valides à tous les cycles. La taille réelle du fichier dépend des pages SQLite, index, en-têtes et fichiers WAL/SHM : c'est une estimation demandée par le sujet, pas une mesure.

Purge proposée : rétention glissante de 14 jours (marge par rapport au minimum de 7 jours de l'exigence 1.2) :
```SQL
DELETE FROM Mesure WHERE horodatage < datetime('now', '-14 days');
```
Exécutée par un job de maintenance contrôlé, après sauvegarde, horloge correcte ; les épisodes d'anomalie peuvent nécessiter une conservation plus longue.

### Script d'enregistrement périodique

#### **Q25 : Créer et versionner mesures.py**

![image.png](images/img_1793807585523_04e83c6c376e58.png)

#### **Q26 : Respect de la période de 10 secondes**

![image.png](images/img_1793869825454_088fa01e47659.png)

#### **Q27 : Ajout et commit de `mesures.py`**

![image.png](images/img_1794469945457_4f618068dc359.png)

#### **Q28 : Fiabilisation du service avec systemd**

![image.png](images/img_1794470461919_88047b1b93d2c8.png)

![image.png](images/img_1794470670382_f43569f6d1e53.png)

![image.png](images/img_1794470933336_f5eaeb35fd53d.png)

![image.png](images/img_1794471387224_066276ea91691.png)

#### **Q29 : Champs Restart et WantedBy, activation et journaux**

![image.png](images/img_1794472707007_0e58fe7f8d0c7.png)

![image.png](images/img_1794472917977_00fa13b79b9a1.png)

![image.png](images/img_1794472633961_b376a073cf863.png)

#### **Q30 / Q31 : Arborescence des fichiers web / Ajout et commit des fichiers web**

![image.png](images/img_1794473434248_b0d5e71b6c67a.png)

#### **Q32 / Q33 : Ajout du serveur web Flask (`app.py`) / Ajout et commit de `app.py`**

![image.png](images/img_1794474023728_ca6a1327f32c3.png)


![image.png](images/img_1794475596490_e2e9c3b265a5b8.png)

#### **Q34 : Route `/api/dernieres` au format JSON**
 

![image.png](images/img_1795009758790_a91d2d195edb48.png)

![image.png](images/img_1795009946915_673b9384eaa3e8.png)

#### **Q35 : Rafraîchissement automatique du tableau de bord**

![image.png](images/img_1795010692843_0fefa03d8be89.png)

![image.png](images/img_1795010844508_e31ed47430122.png)

![image.png](images/img_1795010964773_f26d505ca4d9e8.png)

#### **Q36 : Graphique de l'évolution de la température sur 7 jours**

![image.png](images/img_1795011656579_4e361eb5634e68.png)

![image.png](images/img_1795011763883_c95a7efb1ee4a.png)

#### **Q37 : Codage visuel de la conformité (vert / orange / rouge)**

![image.png](images/img_1795012290532_d0eadb4cc47d18.png)

#### **Q38 : Écran d'affichage en cuisine (mode kiosque)**

![image.png](images/img_1795014159333_2d1fb882ffb6f8.png)

![image.png](images/img_1795015922385_fe13145cb480c.png)

![image.png](images/img_1795018285627_937219848105e8.png)

#### **Q39 : Enregistrement automatique des épisodes de non-conformité**

![image.png](images/img_1795019099641_3fe93e81362078.png)

#### **Q40 : Pertinence d'une notification (courriel, SMS) au chef de cuisine**

**Discussion.** Ajouter une notification (courriel, SMS) me semble pertinent, à
condition de bien cadrer son déclenchement.

**Pour** : la réactivité — une non-conformité peut survenir la nuit ou pendant
un service, et la notification pousse l'information vers le chef au lieu
d'attendre qu'il consulte le tableau de bord. C'est aussi un élément de
traçabilité HACCP : une alerte horodatée, conservée avec l'épisode de
non-conformité, prouve que l'anomalie a été signalée puis traitée.

**Limites** : le DHT11 (±2 °C, mesures parfois aberrantes) risque de générer
des fausses alertes et une lassitude du chef — il faut donc n'alerter qu'à
l'ouverture d'un épisode de non-conformité, pas à chaque mesure. Le courriel
est gratuit depuis le Pi (SMTP) ; le SMS exige une passerelle payante : je le
réserverais aux non-conformités critiques prolongées. Il faudrait aussi alerter
sur le silence de la sonde (état « inconnu »).

**Conclusion** : la notification est un complément utile de l'affichage, pas un
substitut — déclenchée à l'ouverture d'un épisode, par courriel d'abord, le SMS
seulement pour le critique.

#### **Q41 : Rapport PDF imprimable pour le contrôle HACCP**

![image.png](images/img_1795019721201_6a38d8f9fc223.png)

![image.png](images/img_1795019779358_e9a46a7d7c5188.png)

![image.png](images/img_1795019844027_fa659acca09be8.png)

#### **Q42 : Vérification du diagramme d'exigences**

**Synthèse.** Je reprends le diagramme d'exigences fourni en début de sujet et
je vérifie chaque exigence par rapport à la réalisation, appuis à l'appui.

![image.png](images/img_1795020085705_cbf74019820748.png)

**Exigences non totalement couvertes :**

1. **Cinq capteurs** : la phase de test n'utilise qu'un seul capteur branché
   (armoire 1) ; le logiciel est prêt pour cinq (`CONNEXIONS` documentée) mais
   les armoires 2 à 5 restent à équiper.
2. **Armoire négative (surgelés, −18 °C max)** : le DHT11 mesure de 0 à 50 °C
   et ne renvoie pas de températures négatives — il est donc inadapté à
   l'armoire 5, qui exigera un capteur différent (ex. DHT22 ou sonde Pt100).
3. **Précision** : ±2 °C pour des plages parfois étroites (poissons : 0-2 °C) —
   limite déjà discutée en Q20 ; une mise en production imposerait une sonde
   plus précise.
4. **Écran kiosque** : la solution logicielle est complète mais n'a pas pu être
   testée visuellement, aucun écran n'étant relié au Raspberry Pi pendant le TP.

**Conclusion.** Le système satisfait les exigences fonctionnelles, avec des
preuves à l'appui de chacune ; les manques identifiés sont d'ordre matériel
(capteurs supplémentaires, capteur négatif, écran) et non logiciel.