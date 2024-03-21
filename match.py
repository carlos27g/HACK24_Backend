import sys
from openai import OpenAI
import json

STRING_LERNZIELE_MATHEMATIK = { '''0	verstehen und verwenden die Begriffe Bruch, Prozent, Teiler, Vielfache, Zähler, Nenner, überschlagen, runden.
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
                63	können zu einer proportionalen Wertetabelle Zusammenhänge beschreiben (z.B. die Anzahl min je zurückgelegtem km).'''
}

STRING_LERNZIELE_DEUTSCH = {'''0	können unter Anleitung wichtige, auch implizite Informationen eines Hörtextes verstehen und wiedergeben (z.B. Bericht, Vortrag, Hörspiel).
1	können einen längeren geübten Text flüssig vorlesen.
2	können das Zusammenspiel von Verbalem, Paraverbalem und Nonverbalem gestalten.
3	können die Buchstabenabläufe in einer teilverbundenen oder verbundenen Schrift schreiben.
4	können die Leserperspektive ansatzweise einnehmen (z.B. mit Leitfragen, Denkmuster).
5	können sprachliches Material aus einer vorgegebenen Sammlung auswählen oder dieses aus einer oder mehreren Sprachen selber erstellen (z.B. Laute, Klangbild anderer Sprachen, Wörter, Sätze, Piktogramme, Geheimschriften und andere Schriftarten, Redewendungen, Texte) und ihr Vorgehen nachvollziehbar beschreiben.
6	können die Sichtweise einzelner Figuren erkennen und sich in sie hineinversetzen (z.B. indem sie die Figuren darstellend spielen).
7	können mit Unterstützung aufgrund von Cover, Klappentext, Illustrationen und Textausschnitten, (Hör-)Bücher und andere Medien auswählen.
8	können unter Anleitung beschreiben, welche Lesestrategien sie angewendet haben (z.B. überblicken, markieren, Randnotizen).
9	können ein Buch (Kinder-/Jugendliteratur, Sachbuch) oder einen Film in Standardsprache präsentieren.
10	können sich in längeren Gesprächen angemessen einbringen und thematisch passende Beiträge beisteuern.
11	können eine angenehme und wertschätzende Gesprächsatmosphäre als Bereicherung erfahren und dies in eigenen Worten ausdrücken.
12	können untersuchen, in welchen Situationen Mundart und Standardsprache verwendet werden. Sie denken dabei auch über Funktion und Wirkung dieser beiden Sprachformen nach.
13	können Lautung, Wort- und Satzbau in verschiedenen Sprachen (der Klasse) vergleichen (z.B. unterschiedliche Laute, Wortübersetzung, unterschiedliche Wortstellung).
14	können typische Nomen, Verben und Adjektive mithilfe inhaltlicher Proben bestimmen.
15	können Nomen, Verb und Adjektiv mithilfe formaler Proben bestimmen.
16	können Wörter in ihre Morpheme zerlegen. Sie nutzen dies für die Stammregel.
17	können im Gespräch unter Anleitung ihre eigene Leseart des literarischen Textes formulieren.
18	können eine inhaltliche und grammatische Leseerwartung aufbauen.
19	können die Struktur eines Textes erkennen und explizite Informationen entnehmen.
20	kennen Erzählmuster wie Erzählperspektive, Perspektivenwechsel, um sie für das eigene Schreiben nutzen zu können (z.B. Erlebniserzählung aus Sicht von zwei oder mehr Figuren, Parallelgeschichte).
21	können verschiedene Vorgehensweisen zur Ideenfindung bei Geschichten und Gedichten selbstständig einsetzen.
22	können am Computer durch gezieltes Ausprobieren falsche Wortschreibungen korrigieren, wenn der Computer eine Falschschreibung anzeigt.
23	können mithilfe von Kriterien über Textqualitäten sprechen, um damit ein Gefühl für gelungene Textstellen zu entwickeln  (z.B. einzelne Wörter oder Sätze, die ihnen besonders gut oder nicht gefallen).
24	kennen einzelne Autor/innen der Kinderliteratur und einzelne Aspekte aus deren Leben.
25	kennen einzelne bedeutende Vertreter/innen von Kinderliteratur auch aus anderen Kulturen und können ihr Wissen über die Autor/innen in Bezug zu einzelnen Texten setzen und schriftlich festhalten (z.B. Lesetagebuch, Plakat).
26	können in anforderungsreichen Situationen (z.B. Zeitdruck, Nebengeräusche) Emotionen der sprechenden Person einschätzen.
27	können mit Unterstützung eine Hörerwartung aufbauen (z.B. Vorwissen aktivieren, durch vorheriges Lesen der Hörverständnis-Fragen).
28	können ihre Aufmerksamkeit in einem längeren Gespräch aufrecht erhalten und sich passend einbringen.
29	können verschiedenen, längeren Gesprächen folgen und dabei ihre aktive Beteiligung nonverbal, paraverbal und verbal zeigen (aktives Zuhören).
30	können mithilfe von Leitfragen beschreiben, welche Hörstrategien sie beim Zuhören anwenden, um das Gehörte zu verstehen (z.B. einen Hörtext in Portionen abspielen, Fragen vor dem Zuhören lesen).
31	können übersichtliche Sachtexte mit Fotos und Abbildungen überblicken.
32	können ein Buch auswählen, indem sie in verschiedenen Büchern schnuppern (z.B. durchblättern, Anfang oder Schluss lesen).
33	können ihren Beitrag mit nonverbalen (z.B. Handzeichen) und verbalen Signalen rechtzeitig ankündigen.
34	entwickeln Elemente einer persönlichen Handschrift.
35	kennen das Muster eines Dialogs, um es für das eigene Schreiben nutzen zu können.
36	können allein oder in Gruppen verschiedene Schreibideen entwickeln, diese strukturieren und ihren Schreibprozess unter Anleitung planen (z.B. Mindmap, Stichwortliste).
37	können Wörter, Begriffe und Wendungen zum Thema aufbauen und angemessen verwenden.
38	können in einem Wort den Stamm erkennen.
39	können wesentliche Eigenschaften der Figuren, Orte und Handlungen in altersgerechten Geschichten oder einzelnen Szenen erkennen und auf folgende Arten damit umgehen: gestaltend vorlesen (z.B. Lesetheater), szenisch darstellen (z.B. Standbild, Pantomime, Stegreiftheater), schreibend umsetzen (z.B. Textanfang/-schluss ergänzen, aus der Sicht einer Figur schreiben), zeichnerisch umsetzen (z.B. Figurengalerie).
40	können einfache formale und sprachliche Merkmale von literarischen Texten v.a. bei sprachspielerischen Elementen selbstständig erkennen (z.B. Reim, Vers, Strophe, Wortwahl).
41	können sich Störfaktoren einer Gesprächssituation bewusst machen und sie beim Zuhören berücksichtigen (z.B. Lärmpegel, undeutliche Aussprache).
42	können Strukturierungshilfen für eine Kurzpräsentation nutzen (z.B. Mindmap, Gliederung, Stichworte).
43	können über Sinn und Funktion von Gesprächsregeln nachdenken.
44	können einzelne vorher besprochene Punkte in ihren Texten mithilfe von Kriterien am Computer oder auf Papier überarbeiten.
45	zeigen die Bereitschaft, ihren Text auf Fehler hin durchzulesen und entwickeln dabei auch eine Fehlersensibilität.
46	können im Austausch mit anderen eine Distanz zum eigenen Text aufbauen und ihn mithilfe von Kriterien einschätzen (z.B. in einer Schreibkonferenz).
47	entwickeln Interesse am Austausch unterschiedlicher Lese-, Seh- oder Hörerfahrungen eines literarischen Textes und vergleichen ihr Textverstehen.
48	kennen einzelne typische inhaltliche, formale oder sprachliche Merkmale von Erzähltexten (z.B. Märchen, Sage, Fabel, Kurzgeschichte), lyrischen Texten (z.B. Reim) und Theaterstücken/Filmen (z.B. Dialog).'''
}


def read_in_lernziele(file_path):
    """Reads in the provided CSV file line for line, skipping the first line (header),
    and separates the data by the delimiter ','. It then saves the first part as a string list
    and the second part as a score list."""
    lernziele = []
    scores = []
    with open(file_path, 'r') as file:
        next(file)  # Skip the first line (header)
        for line in file:  # Process the rest of the lines
            parts = line.strip().split(',')  # strip() removes any leading/trailing whitespace, including the newline character
            if len(parts) >= 2:  # Ensure there are at least two parts
                lernziele.append(parts[0])
                scores.append(parts[1])
    return lernziele, scores


def analyze_text_with_openai(subject_string):
    """Analyzes the provided text with OpenAI and prints the result."""
    
    #get api key from config file
    with open('config.json') as f:
        config = json.load(f)
    api_key = config['openai_api_key']
    # Initialize your OpenAI API key
    client = OpenAI(api_key=api_key)
    
    input_lernziele, input_scores = read_in_lernziele("competences_scores_manual.csv")
    
    match_kompetenzen = ""

    if (subject_string == "math"):
        match_kompetenzen = STRING_LERNZIELE_MATHEMATIK
    elif (subject_string == "german"):
        match_kompetenzen = STRING_LERNZIELE_DEUTSCH
    else:
        print("Subject not found")
        return

    for lernziel in input_lernziele:
        try:
            # Call to OpenAI's API with the text to analyze
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Du musst einene gegebenen text mit einer gegebenen database von texten verbinden und die ID zurückgeben, vom database text, welcher am besten zum gebene text passt."},
                    {"role": "user", "content": f"Hier ein lernziel von einer Prüfung. Welche kompetenz wird mit diesem Lernziel überprüft'{lernziel}'?: GIB NUR DIE ID ZURÜCK!! ALSO NUR DIE ZAHL AM ANFANG.{match_kompetenzen}"}
                ]
            )
            
            analysis_result = response.choices[0].message.content
            print(f"{analysis_result}")
            
        except Exception as e:
            print(f"Error processing OpenAI API request: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the text to analyze as an argument.")
    else:
        text_to_analyze = " ".join(sys.argv[1:])
        analyze_text_with_openai(text_to_analyze)

