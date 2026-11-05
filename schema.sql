CREATE TABLE IF NOT EXISTS Armoire (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    type_produit TEXT NOT NULL,
    temp_min REAL NOT NULL,
    temp_max REAL NOT NULL,
    pin_gpio INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Mesure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    armoire_id INTEGER NOT NULL,
    horodatage DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    temperature REAL NOT NULL,
    humidite REAL,
    FOREIGN KEY (armoire_id) REFERENCES Armoire(id)
);

CREATE INDEX IF NOT EXISTS idx_mesure_armoire_date ON Mesure(armoire_id, horodatage);

-- Q39 : épisodes de non-conformité (HACCP)
CREATE TABLE IF NOT EXISTS EpisodeNonConformite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    armoire_id INTEGER NOT NULL,
    debut DATETIME NOT NULL,
    fin DATETIME,                 -- NULL tant que l'épisode est en cours
    temp_extreme REAL NOT NULL,   -- température la plus éloignée de la plage
    action_corrective TEXT,       -- renseignée par le chef (traçabilité)
    FOREIGN KEY (armoire_id) REFERENCES Armoire(id)
);
CREATE INDEX IF NOT EXISTS idx_episode_armoire ON EpisodeNonConformite(armoire_id, debut);

INSERT INTO Armoire (nom, type_produit, temp_min, temp_max, pin_gpio)
SELECT * FROM (
  SELECT 'Armoire 1','Produits carnés frais',0,3,26 UNION ALL
  SELECT 'Armoire 2','Poissons et fruits de mer',0,2,17 UNION ALL
  SELECT 'Armoire 3','Produits laitiers',0,4,27 UNION ALL
  SELECT 'Armoire 4','Plats préparés',0,3,22 UNION ALL
  SELECT 'Armoire 5','Surgelés',-25,-18,23
) WHERE NOT EXISTS (SELECT 1 FROM Armoire);
