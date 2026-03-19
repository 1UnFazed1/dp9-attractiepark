# Datapunt 9 uitbreiding: dagprogramma + API temperatuur

# Imports
import mysql.connector
import json
import requests


# ---------------- VERBINDING ----------------
def maak_verbinding():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="attractiepark"
    )


# ---------------- BEZOEKER OPHALEN ----------------
def haal_bezoeker_op(cursor):
    query = "SELECT * FROM bezoeker WHERE id = %s"
    cursor.execute(query, (1,))
    return cursor.fetchone()


# ---------------- ATTRACTIES OPHALEN ----------------
def haal_attracties_op(cursor):
    query = """
    SELECT * FROM voorziening
    WHERE actief = 1
    AND (soort = 'attractie' OR soort = 'achtbaan')
    AND geschatte_wachttijd <= 25
    """
    cursor.execute(query)
    return cursor.fetchall()


# ---------------- HORECA OPHALEN ----------------
def haal_horeca_op(cursor):
    query = """
    SELECT * FROM voorziening
    WHERE actief = 1
    AND soort = 'horeca'
    ORDER BY geschatte_wachttijd ASC
    LIMIT 1
    """
    cursor.execute(query)
    return cursor.fetchone()


# ---------------- WINKEL OPHALEN ----------------
def haal_souvenirwinkel_op(cursor):
    query = """
    SELECT * FROM voorziening
    WHERE actief = 1
    AND soort = 'winkel'
    LIMIT 1
    """
    cursor.execute(query)
    return cursor.fetchone()


# ---------------- TEMPERATUUR OPHALEN ----------------
def haal_temperatuur_op():
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.37&longitude=4.90&current=temperature_2m"

    response = requests.get(url)
    data = response.json()

    temperatuur = data["current"]["temperature_2m"]
    return temperatuur


# ---------------- DAGPROGRAMMA MAKEN ----------------
def maak_dagprogramma(attracties, horeca, souvenirwinkel, max_tijd):
    dagprogramma = []
    totale_tijd = 0

    # FR6: eerste attractie 2x toevoegen als favoriet
    if len(attracties) > 0:
        favoriete_attractie = attracties[0]

        tijd_favoriet = (
            favoriete_attractie["geschatte_wachttijd"] +
            favoriete_attractie["doorlooptijd"]
        )

        if totale_tijd + tijd_favoriet <= max_tijd:
            dagprogramma.append(favoriete_attractie)
            totale_tijd += tijd_favoriet

        if totale_tijd + tijd_favoriet <= max_tijd:
            dagprogramma.append(favoriete_attractie)
            totale_tijd += tijd_favoriet

    # overige attracties toevoegen
    for attractie in attracties[1:]:
        tijd_attractie = (
            attractie["geschatte_wachttijd"] +
            attractie["doorlooptijd"]
        )

        if totale_tijd + tijd_attractie <= max_tijd:
            dagprogramma.append(attractie)
            totale_tijd += tijd_attractie

    # FR10: horeca toevoegen
    if horeca:
        tijd_horeca = horeca["geschatte_wachttijd"] + horeca["doorlooptijd"]

        if totale_tijd + tijd_horeca <= max_tijd:
            dagprogramma.append(horeca)
            totale_tijd += tijd_horeca

    # FR13: souvenirwinkel ALTIJD toevoegen (zonder check)
    if souvenirwinkel:
        tijd_winkel = (
            souvenirwinkel["geschatte_wachttijd"] +
            souvenirwinkel["doorlooptijd"]
        )

        dagprogramma.append(souvenirwinkel)
        totale_tijd += tijd_winkel

    return dagprogramma, totale_tijd


# ---------------- JSON SCHRIJVEN ----------------
def schrijf_json(data):
    with open("output.json", "w") as bestand:
        json.dump(data, bestand, indent=4)


# ---------------- MAIN PROGRAMMA ----------------
def main():
    verbinding = maak_verbinding()
    cursor = verbinding.cursor(dictionary=True)

    bezoeker = haal_bezoeker_op(cursor)
    attracties = haal_attracties_op(cursor)
    horeca = haal_horeca_op(cursor)
    souvenirwinkel = haal_souvenirwinkel_op(cursor)
    temperatuur = haal_temperatuur_op()

    max_tijd = 120

    dagprogramma, totale_tijd = maak_dagprogramma(
        attracties,
        horeca,
        souvenirwinkel,
        max_tijd
    )

    output_data = {
        "bezoeker": bezoeker,
        "temperatuur": temperatuur,
        "dagprogramma": dagprogramma,
        "totale_tijd": totale_tijd
    }

    schrijf_json(output_data)

    print("output.json is gemaakt.")

    cursor.close()
    verbinding.close()


# Start het programma
main()