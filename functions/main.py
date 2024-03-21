# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import firestore_fn, https_fn

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
import google.cloud.firestore
from openai import OpenAI

# Initialize your OpenAI API key
client = OpenAI(api_key='API KEY GOES HERE')
app = initialize_app()


#http://127.0.0.1:5001/hack2024-2530e/us-central1/addmessage?text=%22TestText%22
@https_fn.on_request()
def addmessage(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Grab the text parameter.
    original = req.args.get("text")
    if original is None:
        return https_fn.Response("No text parameter provided", status=400)

    firestore_client: google.cloud.firestore.Client = firestore.client()

    # Push the new message into Cloud Firestore using the Firebase Admin SDK.
    _, doc_ref = firestore_client.collection("messages").add({"original": original})

    # Send back a message that we've successfully written the message
    return https_fn.Response(f"Message with ID {doc_ref.id} added.")

'''
@firestore_fn.on_document_created(document="messages/{pushId}")
def makeuppercase(event: firestore_fn.Event[firestore_fn.DocumentSnapshot | None]) -> None:
    """Listens for new documents to be added to /messages. If the document has
    an "original" field, creates an "uppercase" field containg the contents of
    "original" in upper case."""

    # Get the value of "original" if it exists.
    if event.data is None:
        return
    try:
        original = event.data.get("original")
    except KeyError:
        # No "original" field, so do nothing.
        return

    # Set the "uppercase" field.
    print(f"Uppercasing {event.params['pushId']}: {original}")
    upper = original.upper()
    event.data.reference.update({"uppercase": upper})

'''

#sample request: 
#http://127.0.0.1:5001/hack2024-2530e/us-central1/addmessage?text=Ich kann Subtraktionen, Additionen und Multiplikationen von Brüchen anhand von Modellen darstellen. 
#3) Ich kann Additionen, Subtraktionen und Multiplikationen mit Brüchen ausführen.
# Ich kann Brüche mit verschiedenen Faktoren erweitern, kürzen und miteinander vergleichen, indem ich sie gleichnamig mache.

@firestore_fn.on_document_created(document="messages/{pushId}")
def analyze_text_with_openai(event: firestore_fn.Event[firestore_fn.DocumentSnapshot | None]) -> None:
    if event.data is None:
        return

    original_text = event.data.get("original")
    if not original_text:
        return  # Exit if there's no text to analyze

    try:
        # Updated API call using the corrected approach
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du hilfts einem St. Galler lehere seinen Lernziele den forgegebenen kompetenzbereichen aus dem Lehrplan zuzuordnen."},
                {"role": "user", "content": f'''Hier Lernziele aus einer Prüfunng. Bitte überprüfe welche dieser Lernziele am besten zu welchen kompetenzen passen. Gib die kompetenz ID zurück (ZAHL AM ANFANG, INDICIES). Die lernziele sind {original_text}. Die kompetenzen aus denen du eines pro lernziel auswählen sollst, sind die folgenden:0	verstehen und verwenden die Begriffe Bruch, Prozent, Teiler, Vielfache, Zähler, Nenner, überschlagen, runden.
                1	verstehen und verwenden die Begriffe Addition, Subtraktion, Multiplikation, Division, Rest, Zahlenstrahl, Quadratzahl,  Hunderter, Tausender, Stellenwerte.
                2	verstehen und verwenden die Begriffe Summand, Summe, Differenz, Faktor, Produkt, Quotient.
                3	können im Zahlenraum bis 1'000 von beliebigen Zahlen aus in 1er-, 2er-, 10er- und 100er-Schritten vorwärts und rückwärts zählen.
                4	können von beliebigen Dezimalzahlen aus in angemessenen Schritten vorwärts und rückwärts zählen (z.B. von 0.725 in 0.005er-Schritten).
                5	können im Zahlenraum bis 1 Million von beliebigen Zahlen aus in angemessenen Schritten vorwärts und rückwärts zählen (z.B. von 320'000 in 20'000er-Schritten).
                6	können Dezimalzahlen  bis 5 Wertziffern addieren und subtrahieren (im Kopf oder mit Notieren eigener Rechenwege, z.B. 30.8 + 5.6).
                7	können bis 4 Wertziffern im Kopf addieren und subtrahieren (z.B. 320'000 + 38'000; 402 + 90).
                8	können beim Addieren und Subtrahieren Rechenwege notieren und Ergebnisse überprüfen.
                9	erkennen Zahlen, die durch 2, 5, 10, 100, 1'000 teilbar sind.
                10	können Produkte durch Verdoppeln und Halbieren umformen (z.B. 8 · 26 = 4 · 52 = 2 · 104).
                11	lassen sich auf offene Aufgaben ein, erforschen Beziehungen, formulieren Vermutungen und suchen Lösungsalternativen.
                12	können heuristische Strategien verwenden: ausprobieren, Beispiele suchen, Analogien bilden, Regelmässigkeiten untersuchen, Annahmen treffen,  Vermutungen formulieren.
                13	können operative Beziehungen zwischen natürlichen Zahlen erforschen und beschreiben (z.B. die Differenz von 2 Umkehrzahlen ist ein Vielfaches von 9: 41 - 14 = 27; 83 - 38 = 45).
                14	können Ergebnisse mit Überschlagsrechnungen überprüfen.
                15	können Divisionen mit Rest mit der Umkehroperation begründen (z.B. 32 : 6 gibt Rest, weil 32 keine Zahl aus der 6er-Reihe ist).
                16	können Ergebnisse zu Grundoperationen durch Vereinfachen (z.B. 8 · 13 = 4 · 26 = 2 · 52), Zerlegen (z.B. 17.8 + 23.5 = 17 + 3 + 20 + 1.3) und Umkehroperationen überprüfen.
                17	können Stellenwerttafel beim Erforschen arithmetischer Strukturen nutzen (z.B. Plättchen in die Stellenwerttafel legen und verschieben).
                18	können Anweisungen zu Handlungssequenzen (z.B. in Flussdiagrammen) befolgen und beim Erforschen arithmetischer Strukturen nutzen (z.B. 1. Starte mit einer zweistelligen Zahl / 2. Wenn die Zahl gerade ist: Dividiere durch 2, sonst: Multipliziere mit 3 und addiere 1 / 3. Wiederhole 2.).
                19	können Rechenwege zu Grundoperationen mit Dezimalzahlen darstellen, austauschen und nachvollziehen (z.B. 35.7 + 67.8 in mehrere Summanden zerlegen und auf dem Rechenstrich darstellen).
                20	können die Bedeutung der Ziffern im Stellenwertsystem darstellen (z.B. 2 100er-Platten, 5 10-er-Stäbe und 7 1er-Würfel stellen 257 dar).
                21	können Zahlenfolgen und Produkte veranschaulichen (z.B. 14 · 14 mit dem Malkreuz; die Zahlenfolge 1, 3, 6, 10, ... mit Punkten).
                22	verstehen und verwenden die Begriffe Punkt, Ecke, Kante, Seitenfläche, Würfel, Quader.
                23	erkennen und benennen geometrische Körper (Würfel, Quader, Kugel, Zylinder, Pyramide) und Figuren in der Umwelt und auf Bildern.
                24	verstehen und verwenden die Begriffe Seite, Diagonale, Durchmesser, Radius, Flächeninhalt, Mittelpunkt, Parallele, Linie, Gerade, Strecke, Raster, Schnittpunkt, schneiden, Senkrechte, Symmetrie, Achsenspiegelung, Umfang, Winkel, rechtwinklig, Verschiebung, Geodreieck.
                25	können mit Grundfiguren verschieden parkettieren (z.B. mit Dreiecken oder Pentominos).
                26	können Figuren in Rastern vergrössern, verkleinern und verschieben.
                27	können reale Körper verschieben, kippen, drehen und erkennen entsprechende Abbildungen (z.B. einen Würfel zwei Mal kippen).
                28	können den Umfang von Vielecken messen und berechnen.
                29	können Flächen mit Einheitsquadraten auszählen (z.B. das Schulzimmer mit Meterquadraten).
                30	können Strecken an Figuren systematisch variieren, Auswirkungen erforschen, Vermutungen formulieren und austauschen (z.B. Flächeninhalt eines Rechtecks bei gegebenem Umfang mit einem Raster).
                31	können Beziehungen zwischen Seitenlängen und Flächeninhalt bei Rechtecken in einem Raster erforschen.
                32	können Figuren mit gegebenem Umfang bilden (z.B. Dreiecke mit 5, 6, oder 7 Streichhölzern legen).
                33	können heuristische Strategien verwenden: Linien und Winkel verändern, Beispiele skizzieren, Figuren und Körper vergleichen.
                34	können Aussagen zu geometrischen Beziehungen im Dreieck, Viereck und Kreis überprüfen (z.B. ein Kreis und ein Viereck können sich in mehr als 4 Punkten schneiden).
                35	können Würfel und Quader im Schrägbild skizzieren.
                36	können die Aufsicht, Vorderansicht und Seitenansicht von Quadern und Würfelgebäuden skizzieren.
                37	können aus Quadraten und Rechtecken  Würfel und Quader herstellen und umgekehrt das Netz von Würfeln und Quadern durch Abwickeln zeichnen.
                38	können mit Rastern, Zirkel und Geodreieck zeichnen (z.B. parallele Linien, rechte Winkel, rechtwinklige Dreiecke, Quadrate und Rechtecke).
                39	können Rechtecke mit gegebenen Seitenlängen zeichnen.
                40	können Körper in der Vorstellung zerlegen und zusammenfügen (z.B. eine vorgegebene Figur aus zwei Teilen des Somawürfels nachbauen).
                41	können die Lage einer Figur oder eines Quaders in der Vorstellung verändern sowie Veränderungen beschreiben (z.B. ein Pult im Kopf um 180° drehen).
                42	können Figuren in einem Koordinatensystem zeichnen, horizontal und vertikal verschieben sowie die Koordinaten der Eckpunkte angeben.
                43	können zu Koordinaten Figuren zeichnen sowie die Koordinaten von Punkten bestimmen (z.B. Figuren auf dem Geobrett nach Koordinaten aufspannen und zeichnen).
                44	können Pläne und Fotografien zur Orientierung im Raum lesen und nutzen.
                45	verstehen und verwenden die Begriffe  (un)wahrscheinlich, (un)möglich, sicher.
                46	verstehen und verwenden die Begriffe Gewicht, Inhalt, Zeitpunkt, Zeitdauer, Sekunde.
                47	können Masseinheiten und deren Abkürzungen benennen und verwenden: Hohlmasse (l, dl, cl, ml), Gewichte (t, kg, g, mg), Zeit (h, min, s).
                48	verstehen und verwenden die Begriffe Proportionalität, Flächeninhalt, Volumen, Inhalt, Mittelwert, Kreisdiagramm, Säulendiagramm, Liniendiagramm, Daten, Häufigkeit, Zufall, Speicher.
                49	können Grössen schätzen, messen und in benachbarte Masseinheiten umwandeln: l, dl; m, cm, mm; kg, g (z.B. 2'000 g = 2 kg).
                50	können Längen, Gewichte, Inhalte, Zeitpunkte und Zeitdauern schätzen und messen sowie mit einer geeigneten Masseinheit angeben.
                51	können mit Längen, Gewichten, Volumen und Zeitangaben rechnen sowie entsprechende Grössen in benachbarte Masseinheiten umwandeln.
                52	können Grössen (Geld, Längen, Gewicht bzw. Masse, Zeit, Volumen [l]) schätzen, bestimmen, vergleichen, runden, mit ihnen rechnen, in benachbarte Masseinheiten umwandeln und in zweifach benannten Einheiten schreiben.
                53	können lineare und nichtlineare Zahlenfolgen weiterführen (z.B. 90, 81, 70, 57, ...; 1, 4, 9, 16, ...; 1, 3, 6, 10, 15, ...).
                54	können funktionale Zusammenhänge in Wertetabellen erfassen (z.B. zurückgelegte Distanzen bei einer Geschwindigkeit von 4.5 km/h nach 10 min, 20 min, 30 min, ...).
                55	können zu Beziehungen zwischen Grössen Fragen formulieren, erforschen,  und funktionale Zusammenhänge überprüfen (z.B. die Füllhöhe von ½ Liter, 1 Liter, 2 Liter in verschiedenen Gefässen; das Verhältnis zwischen Preis und Gewicht eines Produkts; das Gewicht eines Lightgetränks und einer Limonade).
                56	können systematisch kombinieren und variieren (z.B. Paarbildungen mit 6 Kindern).
                57	können auszählbare Kombinationen und Permutationen erforschen, Beobachtungen festhalten und Aussagen überprüfen (z.B. Kombinationen von Zahlen beim Veloschloss; Permutationen mit Buchstaben ADEN, ADNE, AEDN, ...).
                58	können Daten zu Längen, Inhalten, Gewichten, Zeitdauern, Anzahlen und Preisen in Tabellen und Diagrammen darstellen und interpretieren (z.B. zu Haustieren).
                59	können Daten statistisch erfassen, ordnen, darstellen und interpretieren (z.B. Schulwege: Distanz, Transportmittel, Zeitdauer).
                60	können Datensätze nach Kriterien auswerten und in Datensätzen Mittelwert, Maximum und Minimum bestimmen.
                61	können zu Texten, Tabellen und Diagrammen Fragen stellen, eigene Berechnungen ausführen sowie Ergebnisse interpretieren und überprüfen.
                62	erkennen in Sachsituationen Proportionalitäten (z.B.  zwischen Anzahl Schritten und Distanz).
                63	können zu einer proportionalen Wertetabelle Zusammenhänge beschreiben (z.B. die Anzahl min je zurückgelegtem km).
            '''}
            ]
        )

        analysis_result = response.choices[0].message.content

        # Update Firestore document with the analysis result
        print(f"Saving analysis for {event.params['pushId']}")
        event.data.reference.update({"analysis": analysis_result})
    except Exception as e:
        print(f"Error processing OpenAI API request: {e}")
