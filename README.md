# LFCCZSK bot

Som adminom FB stránky, ktorá slúži na informovanie fanúšikov ohľadom noviniek
klubu Liverpool FC. Niektoré príspevky sú však z podstaty generické, preto som 
sa rozhodol naprogramovať bota, ktorý bude tieto príspevky pridávať bez nutnosti mojej interakcie.

## Typy príspevkov

Vrámci RP som zautomatizoval pridávanie nasledovných typov príspevkov:

- **Matchday** (`matchday.py`) &rarr; v deň zápasu pridá základné informácie o zápase, ktorý sa ide odohrať
- **Zostavy** (`lineups.py`) &rarr; hodinu pred zápasom pridá zverejnené zostavy na zápas
- **Komentovanie zápasu** (`commentary.py`) &rarr; počas zápasu pridáva príspevky o strelených góloch (a iných vážnych situáciach)

### Príklad: Matchday

![Matchday](images/matchday.png)

### Príklad: Zostavy

![Zostavy](images/zostavy.png)

### Príklad: Komentovanie zápasu

![Komentovanie zápasu](images/komentovanie.png)
