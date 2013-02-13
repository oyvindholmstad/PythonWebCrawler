README.TXT

* Hva?
PyWebCrawler - en enkel distribuert WebCrawler

* Av?
Øyvind Holmstad, 2012


* Krav?
Pyro4 (se http://irmen.home.xs4all.nl/pyro/)


* Hvordan kjøre?
1. Start Pyro Namer Server med "python -m Pyro4.naming"
2. Start Aggregator med "python AggregatorMain.py" (krever mappen 'tmp/' i aktive katalog)
3. Start crawlere med "python CrawlingClientMain.py"

NB! Koden er kun testet på localhost, så trøbbel med hostname/port samt discovery av name server kan forekomme ved kjøring på flere noder.

Tips:
Kjør "python LinkStorage.py" for å se hvilke lenker som er funnet 

-----------

* Beskrivelse:
PyWebCrawler er en enkel WebCrawler som crawler Internett for lenker å besøke. I nåværende tilstand gjør den ingenting annet enn å samle linker, men den kunne fort blitt brukt som første komponent i en søkemotor for å finne nettsider å indeksere. Crawleren er skrevet i Python og kjører distribuert ved hjelp av Pyro. Python ble brukt grunnet sin største styrke, nemlig at det er raskt til prototyping av applikasjoner. Det passet perfekt i dette tilfellet hvor tiden var knapp. Av samme grunn benytter jeg Pyro, et enkelt, men kraftig bibliotek, som gjemmer nettverkstrafikken bak en proxy/remote object, og sqlite, som tilbyr et SQL-grensesnitt mot en enkel fil uten konfigurering.

Hvis ytelse var hovedmålet med crawleren hadde jeg nok valgt en annen tilnærming, med et litt raskere programmeringsspråk/platform og en litt mer effektiv mellomvare. Men for denne oppgaven valgte jeg å vektlegge solid kode og litt ekstra funksjonalitet (selv om crawleren ikke er på langt nær så innholdsrik som jeg skulle ønske)

Klientene stopper å crawle så snart en av dem har funnet den siste siden på internett, definert i LinkStorageProxy. 

* Begrensninger, mangler, mulige optimaliseringer, og andre kommentarer:
- Ingen konfigurasjonsfil.
- Lenker til seksjoner i dokumenter ved bruk av # er ignorert. Selv om dette ikke ville vært et stort problem tidligere, kan det være kritisk i dag, siden flere nettsteder bruker Javascript/Ajax til å laste inn data asynkront identifisert med #-anker. 
- Relative lenker (som f.eks. "../../main/index.html") er ignorert. 
- Noen nettsider bruker ikke quotes ("") etter href-tagen. Disse blir ignorert.
- Robots.txt blir ikke lagret permanent, og må lastes ned for hver kjøring av hver klient. Blir alikevel lastet kun en gang per domene per kjøring.
- Klientene burde vært trådet, hvor de forskjellige trådene ville hatt forskjellige arbeidsoppgaver. Slik klientene er nå vil prosessering vente på IO, og IO vente på prosessering, slik at vi ikke får maksimert utnyttelsen av noen av delene. Med en enkel ordning hvor én tråd hele tiden henter ned og laster opp linker, og en annen tråd prosesserer dem på jakt etter nye, ville vi kunne økt hastigheten betraktelig (på tross av Pythons føle Global Interpreter Lock).
- Fault tolerance er ikke implementert. Om aggregatoren går ned vil også klientene kræsje. I en ideell applikasjon ville kanskje klientene visst om hverandre, slik at de kunne holdt en votering om hvem som skulle bytte rolle til Aggregator hvis så skulle skje. Om en klient går ned er det ingen krise. Vi mister kanskje de siste linkene klienten har funnet, men Aggregatoren vil kjøre videre som om ingenting har hendt.
- Parametrene for memorycachene er ikke tilpasset, og kunne nok vært økt betraktelig.
- Memory-cachene bruker et simpelt FIFO-system for å bestemme hvilken link som skal evictes, når LRU eller andre tilnærminger kanskje hadde vært mer effektive.
- Filtrering av tvilsomme nettsider er ikke implementer. Dette vil føre til unødvendig ressursbruk på uinteressante spam-sider og annet snusk.

