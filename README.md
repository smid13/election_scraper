# election_scraper
Tento skript stahuje volební výsledky zvoleného okresu ze stránky www.volby.cz a ukládá je do csv souboru.
Výsledný soubor obsahuje na jednotlivých řádcích postupně všechny obce daného okresu s konkrétními čísly (počet voličů, vydané obálky, platné hlasy, počty hlasů pro jednotlivé strany).

Requirements

Pro správný běh programu je potřeba nainstalovat potřebné knihovny.
Instalaci provedeš přes příkazovou řádku příkazem: pip install -r requirements.txt 

Spuštění

Soubor se spouští přes příkazovou řádku pomocí dvou argumentů.
První argument musí obsahovat odkaz který okresek chcete stáhnout (př. https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4202).
Druhý argument obsahuje jméno výstupního souboru (př. volby_chomutov.csv).
path\py election_scraper "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4202" "volby_chomutov.csv"

