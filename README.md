# Használt autók adatelemzése – NumPy, Pandas, Plotly

**Cél:** megvizsgálni, hogyan függ össze a használt autók ára az évjárattal, a futásteljesítménnyel, a váltóval, az üzemanyaggal és az eladó típusával.


## Adatforrás

 [Vehicle dataset (Kaggle)](https://www.kaggle.com/datasets/akshaydattatraykhare/car-details-dataset?resource=download).


**Figyelem:** az ár indiai rúpiában (INR) szerepel; az adatok nem az aktuális magyar autópiacot írják le.

## Telepítés és futtatás 

   ```powershell
   py -m pip install -r requirements.txt
   py elemzes.py
   ```

## Kimenetek

Az `elemzes.py` a terminálra kiírja a tisztítás és az öt elemzés főbb eredményeit, továbbá létrehozza a `diagramok` mappában ezt az öt HTML-diagramot:

1. `01_evjarat_valto.html` – évjárat, mediánár és váltó
2. `02_kilometer_uzemanyag.html` – futásteljesítmény, ár és üzemanyag
3. `03_elado_valto.html` – eladó, váltó és ár
4. `04_uzemanyag_evjarat.html` – árak eloszlása évjárat és üzemanyag szerint
5. `05_hoterkep.html` – mediánár évjárat- és kilométercsoport szerint

A HTML-fájlok böngészőben nyithatók és interaktívak. 

## Öt kérdés

1. Hogyan függ össze az évjárat és az ár, és eltér-e a kapcsolat a manuális és automata váltóknál?
2. Van-e kapcsolat a kilométer és az ár között, és ugyanilyen-e a benzines és dízelautóknál?
3. Hogyan különböznek az árak az eladó típusa és a váltótípus szerint?
4. Hogyan alakul az árak eloszlása a benzines és dízelautók között az évjáratcsoportokban?
5. Mely évjárat- és kilométercsoportokban magas vagy alacsony a mediánár?

## Adatkezelés és korlátok

A program a teljesen azonos sorokból egyet tart meg, eltávolítja a hiányzó és alapvetően hibás adatokat, és kategóriákat hoz létre. Az egyező sorok eldobása valódi, de azonos jellemzőkkel rendelkező autók eltűnéséhez is vezethet. A csoportok megfigyelt árkülönbsége **nem bizonyít ok-okozati kapcsolatot**, mert például az autómárka, a felszereltség és az állapot is számíthat.


## Felhasznált eszközök

Python, NumPy, Pandas, Plotly. 