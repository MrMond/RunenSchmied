# RunenSchmied

Abgabe für WWI22DSA / Grundlagen der KI 

# Ursprüngliche Idee

## Aufgabenstellung

__Lernziel 2__: AI Verfahren (Regelungstechnik, computer vision, genetische Algorithmen) im Bereich Robotik / autonomes Fahren / Computerspiele

## Pitch

Kleines Proof of Concept Spiel, in dem man sein Schwert selbst mit "Runen" beschmieden kann, in dem ein ML-Modell die Runen interpretiert und man dann stats bekommt. (In Rot sind die vom Spieler gezeichneten Runen markiert; mit Orange ist markiert, was das Modell finden soll)

![visual concept](etc\documentation_images\pitch1.png)

Der Spieler bekommt nur kleine "Stempel" und muss sich die Runen selbst zusammenstellen.

![Stempel](etc\documentation_images\pitch2.png)

Ein Modell interpretiert die Runen und gibt dem Spielercharakter die dementsprechenden Angriffe. ZB. Schlägt man mit dem Schwert, bis man 50 Feuerschaden hat, dnach schießt man Feuerbälle, usw. Das kann dann deterministisch passieren.

## Herangehensweise

1) Es werden einige Stempel (training\data\templates) definiert
1) Es werden Bilder (mit verschiedenen graden der Komplexität) und dazugeförige Masken erstellt
1) Es wird ein (mehrere) Modell trainiert
1) Es wird ein kleiner Prototyp zur Visualisierung der Ergebnisse erstellt
