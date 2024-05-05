
# Ominaisuudet 05.05.2024:
- Voit rekisteröityä, kirjautua sisään ja ulos
- Voit tehdä kammioita
- Voit tehdä kammioihin lankoja
- Voit laittaa lankoihin viestejä
- Voit selata käyttäjien profiileja, joissa näkyy heidän kommentointi/lankahistoria
- Viesteillä ja langoilla on "kaiut", joita käyttäjät voivat koventaa tai hiljentää. Jos langan tai kommentin kaiku laskee alle -4, lanka/kommentti poistetaan. Kaiun äänestämiseen ei ole rajaa, koska se tekee testaamisesta helpompaa
- Käyttäjien profiileissa näkyy käyttäjien yhteenlaskettu kaikumäärä ja "harhaoppi"-laskuri, joka pitää kirjaa poistetuista viesteistä/langoista

# Ohjeet (kopioitu suoraan materiaalista), jotka toivottavasti toimii
Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:
- DATABASE_URL= sun tietokannan-paikallinen-osoite
- SECRET_KEY= sun salainen-avain

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla
- python3 -m venv venv
- source venv/bin/activate
- pip install -r ./requirements.txt

Käynnistä tietokanta komennolla
- start-pg.sh

Määritä vielä tietokannan skeema komennolla 
- psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla 
- flask run

# Keskustelusovellus

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Keskustelualueet ovat käyttäjien luomia "kaikukammioita", joihin muihin käyttäjät voivat luoda ketjuja. Jokaisella ketjun viestillä on "kaiku", jota muut käyttäjät voivat lujentaa tai hiljentää. Jos viestiä hiljennetään tarpeeksi, se poistetaan. Sivulla ei ole ylläpitoa lainkaan, sen sijaan kaiken moderoinnin hoitavat kammioissa olevat käyttäjät. 
