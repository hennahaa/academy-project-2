# AW ACADEMY RYHMÄTYÖ 2
## Konttiprojekti

Pohjana käytetty koodi: https://github.com/runeli/assesment-test

Pohja käyttää flaskia https://flask.palletsprojects.com/en/2.0.x/

## Asennus

(Alkuperäisen READMEn ohjeet)

1. Aloita asentamalla riippuvuudet `pip install flask`.
2. Aja `flask run --host=0.0.0.0 --port=80 --reload`. `--reload` parametri käynnistää projektin uusiksi aina kun lähdekoodi muuttuu. Samalla resetoituu tietokanta alkuperäiseen tilaansa.
3. Avaa selain omalla koneella ja kohdista se osoitteeseen http://localhost

Taustalla on SQLLite tietokanta, joka ei vaadi käyttäjältä erillistä serveriä. Kaikki tallennetaan lokaaliin tiedostoon ja luetaan sieltä.
Syntaksi on hyvin pitkälti samankaltainen kuin PostgreSQL:ssä.

Tutustu koodiin ja siinä oleviin kommentteihin. Niistä voi olla apua tehtävän kannalta.

