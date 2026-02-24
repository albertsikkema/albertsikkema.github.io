---
layout: post
title: "Bijna de helft van alle bushaltes in Nederland is ontoegankelijk, dus bouwde ik een tool om er wat aan te doen"
date: 2026-02-24
categories: accessibility open-source civic-tech
description: "Een open-source tool die alle 20.277 ontoegankelijke bushaltes in Nederland zichtbaar maakt en burgers helpt actie te ondernemen."
keywords: "bushaltes, toegankelijkheid, OV, open data, civic tech, VN-verdrag handicap, CROW, gemeenten, open source"
image: /assets/images/busstop-fail.jpg
---

<figure>
  <img src="/assets/images/busstop-fail.jpg" alt="Een ontoegankelijke bushalte in Nederland: geen verhoogd perron, geen geleidelijnen">
  <figcaption>Een bushalte een paar kilometer van mijn huis. Geen verhoogd perron, geen geleidelijnen — ontoegankelijk voor veel reizigers.</figcaption>
</figure>

*This post is in Dutch — a first for this blog. It covers a topic specific to the Netherlands: I built an open-source tool that maps all 20,277 inaccessible bus stops in the country and lets citizens email the responsible authority with a legally grounded request for improvements. Apologies to my English-speaking readers; normal service will resume next post.*

---

Vandaag publiceerde de [NOS](https://nos.nl/artikel/2603791-veel-bushaltes-niet-toegankelijk-voor-mensen-met-een-beperking) dat voor veel mensen als een verrassing kwam: ongeveer de helft van de Nederlandse bushaltes is niet of nauwelijks toegankelijk voor mensen met een beperking. Zes op de tien haltes missen goede voorzieningen voor blinden en slechtzienden. Bijna de helft is slecht ingericht voor rolstoelgebruikers. In sommige gemeenten ligt het percentage ontoegankelijke haltes boven de 90%.

Afgelopen jaren ben ik intensief bezig geweest met toegankelijkheid, onder andere als developer van de [Beter Bereikbaar Applicatie - BBA](https://bba.nl/), en dit bevestigt alle verhalen die ik hoorde. De data is openbaar beschikbaar, maar dat meer dan de helft van de bushaltes in Nederland slecht bereikbaar zijn is hoger dan ik zelf had verwacht. Dus heb ik de mooie kaarten bekeken, en toen dacht ik: wat nu? De gemiddelde persoon zal het getalletje zien, en of zijn schouders ophalen of het voor kennis geving aannemen. Wat moet je er immers mee? Dus toen dacht ik: wat kan ik er mee? Zou het niet mooi zijn als je een kaart zou hebben waar je deze data op ziet en die je in staat stelt om dit onder de aandacht te brengen bij de desbetreffende instantie (vaak een gemeente, soms een provincie en heel soms een waterschap) Dus bouwde ik er iets voor.

## De onzichtbare data

Het [Centraal Haltebestand](https://dova.nu) — beheerd door DOVA, het samenwerkingsverband van OV-autoriteiten — bevat gedetailleerde informatie over elke bushalte in Nederland. Van elke halte is bekend hoe hoog de stoeprand is, hoe breed het perron, of er geleidelijnen liggen, of de halte obstakels heeft. Al die data is openbaar.

Maar "openbaar" is niet hetzelfde als "zichtbaar". De data zit in de [Halteviewer](https://halteviewer.ov-data.nl), een tool voor professionals. Je moet weten dat die bestaat, je moet weten hoe je erin zoekt. Voor een gemeenteraadslid of burger die willen weten hoeveel haltes in hun gemeente niet op orde zijn, is dat een doodlopende weg.

## 20.277 haltes die niet voldoen

Ik schreef een datapipeline die alle haltedata ophaalt en toetst aan de [CROW-normen](https://www.crow.nl) voor toegankelijkheid. Een halte voldoet niet als de stoeprand lager is dan 18 centimeter, het perron smaller dan 1,50 meter, er geen geleidelijnen liggen, of er geen obstakelvrije looproute is.

De cijfers:

| | Aantal |
|---|---|
| Actieve bushaltes in Nederland | 42.068 |
| Voldoet niet aan CROW-normen | 20.277 (48%) |
| Verantwoordelijke wegbeheerders | 384 |

Die 384 wegbeheerders — dat zijn 345 gemeenten, 12 provincies, 5 waterschappen, 7 kantoren van Rijkswaterstaat, en nog een handvol private partijen. Allemaal afzonderlijk verantwoordelijk voor hun eigen haltes.

De wegbeheerders met de meeste ontoegankelijke haltes:

- **Rotterdam**: 416
- **Provincie Overijssel**: 397
- **Amsterdam**: 393
- **Provincie Gelderland**: 367
- **Provincie Drenthe**: 268

## De tool: Toegankelijke Bushaltes

[**Toegankelijke Bushaltes**](https://albertsikkema.github.io/niet-toegankelijke-bushaltes/) is een interactieve kaart die alle 20.277 ontoegankelijke haltes toont, gegroepeerd per wegbeheerder. In de zijbalk klik je op je gemeente (of provincie, waterschap, etc.) en je ziet direct welke haltes niet voldoen. Je kunt inzoomen, haltes aanklikken, en zien welke haltes niet voldoen aan de eisen. En het belangrijkste: je kunt met één klik een e-mail genereren naar de verantwoordelijke wegbeheerder.

## De e-mail: goed onderbouwd, klaar om te versturen

De gegenereerde e-mail is geen vaag verzoekje. Hij bevat:

- Het exacte aantal ontoegankelijke haltes van die wegbeheerder
- Een verwijzing naar het **VN-verdrag inzake de rechten van personen met een handicap** (artikelen 9 en 20) — dat Nederland in 2016 heeft geratificeerd
- Een verwijzing naar de **Wet gelijke behandeling op grond van handicap of chronische ziekte** (Wgbh/cz, artikelen 2 en 3)
- Een verwijzing naar het **Bestuursakkoord Toegankelijkheid OV 2022-2032** — waarin overheden zelf hebben afgesproken om alle haltes toegankelijk te maken

Je hoeft geen jurist te zijn. Je hoeft geen expert te zijn in OV-wetgeving. Je klikt, je past de mail aan naar hoe jij het wilt, en je verstuurt hem. Dat is het.

## Waarom dit ertoe doet

Peter Waalboer, belangenbehartiger voor mensen met een beperking, zei het treffend in het NOS-artikel: *"Het openbaar vervoer is een publieke voorziening. Die moet voor iedereen toegankelijk zijn — daar is geen discussie over mogelijk."*

Helemaal waar, maar de realiteit is weerbarstig: gemeenten hebben beperkte budgetten en bushaltes aanpassen kost geld — een enkele halte kan al duizenden euro's kosten. Er bestaan subsidies van OV-autoriteiten, en het Bestuursakkoord zet ambities neer, maar naleving is vrijwillig. Zonder druk van inwoners verschuift "toegankelijkheid" makkelijk naar de onderkant van de prioriteitenlijst.

Wat er ontbreekt is niet wetgeving of goede bedoelingen — het is zichtbaarheid. Als een raadslid niet weet dat 60% van de haltes in haar gemeente niet voldoet, gaat ze er niet naar vragen. Als een dorpsgenoot niet weet dat zijn halte ongeschikt is voor zijn buurvrouw in een rolstoel, mist hij het signaal. Data die onzichtbaar is, leidt niet tot actie.

Deze tool maakt die data zichtbaar en actionable. In een paar klikken kun je zien wat er aan de hand is en de verantwoordelijke partij aanspreken — met een juridisch onderbouwd verzoek.

## Open source, voor iedereen

De tool is volledig open source. De broncode staat op [GitHub](https://github.com/albertsikkema/niet-toegankelijke-bushaltes). Technisch is het bewust simpel gehouden: een datapipeline in Node.js die de DOVA- en Allmanak-data ophaalt, en een statische frontend met vanilla HTML, CSS en JavaScript — met een Leaflet-kaart en marker clustering. Geen frameworks en geen build-stappen. De data is verversbaar door de pipeline opnieuw te draaien.

## De timing: gemeenteraadsverkiezingen op 18 maart

Op 18 maart 2026 zijn de gemeenteraadsverkiezingen. Dat maakt dit hét moment om actie te ondernemen. Kandidaat-raadsleden en zittende politici zijn nu extra ontvankelijk voor signalen van inwoners. Stuur die e-mail nu — vóór de verkiezingen. Vraag aan je lokale partijen wat zij gaan doen aan de ontoegankelijke haltes in jouw gemeente. Toegankelijkheid hoort in elk verkiezingsprogramma, niet als voetnoot maar als prioriteit.

## Wat kun jij doen?

1. **Ga naar [de tool](https://albertsikkema.github.io/niet-toegankelijke-bushaltes/)** en zoek je eigen gemeente op
2. **Bekijk welke haltes niet voldoen** — misschien is het die halte bij jou om de hoek
3. **Genereer een e-mail** en stuur die naar je wegbeheerder — liefst vóór 18 maart
4. **Deel de tool** met je gemeenteraad, je lokale belangenorganisatie, je buren
5. **Stel het aan de orde** bij verkiezingsdebatten en inspraakavonden in je gemeente
6. **Heb je suggesties of wil je bijdragen?** Open een issue op [GitHub](https://github.com/albertsikkema/niet-toegankelijke-bushaltes)

Toegankelijkheid is geen gunst. Het is een recht. En soms begint verandering met een simpele e-mail — zeker als die drie weken voor de verkiezingen op de mat valt.
