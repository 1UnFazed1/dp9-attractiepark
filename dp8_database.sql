USE attractiepark;

DROP TABLE IF EXISTS bezoeker;
DROP TABLE IF EXISTS voorziening;

CREATE TABLE voorziening (
    id INT AUTO_INCREMENT PRIMARY KEY,
    naam VARCHAR(100),
    soort VARCHAR(100),
    overdekt TINYINT(1),
    geschatte_wachttijd INT,
    doorlooptijd INT,
    actief TINYINT(1)
);

CREATE TABLE bezoeker (
    id INT AUTO_INCREMENT PRIMARY KEY,
    naam VARCHAR(45),
    leeftijd INT,
    lengte INT,
    gewicht INT
);
INSERT INTO voorziening (naam, soort, overdekt, geschatte_wachttijd, doorlooptijd, actief)
VALUES
('Sky Coaster', 'achtbaan', 0, 25, 2, 1),
('Food Corner', 'horeca', 1, 10, 45, 1),
('Gift Shop', 'winkel', 1, 5, 15, 1),
('Water Splash', 'attractie', 0, 20, 3, 1),
('Snack Bar', 'horeca', 1, 8, 20, 1);

INSERT INTO bezoeker (naam, leeftijd, lengte, gewicht)
VALUES
('Daan', 21, 182, 78),
('Lina', 19, 168, 60),
('Omar', 25, 175, 82),
('Emma', 17, 160, 55);

/*

-- Alle voorzieningen ophalen
SELECT * FROM voorziening;

-- Alle bezoekers ophalen
SELECT * FROM bezoeker;

-- Alleen achtbanen tonen
SELECT * FROM voorziening WHERE soort = 'achtbaan';

-- Voorzieningen sorteren op wachttijd (oplopend)
SELECT * FROM voorziening ORDER BY geschatte_wachttijd;

-- Voorzieningen sorteren op wachttijd (aflopend)
SELECT * FROM voorziening ORDER BY geschatte_wachttijd DESC;

-- Bezoekers sorteren op naam (A-Z)
SELECT * FROM bezoeker ORDER BY naam;

-- Actieve voorzieningen tonen en sorteren op wachttijd
SELECT * FROM voorziening WHERE actief = 1 ORDER BY geschatte_wachttijd DESC;

-- Bezoekers sorteren op leeftijd en naam
SELECT * FROM bezoeker ORDER BY leeftijd DESC, naam;

*/
