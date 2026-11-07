
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px


# A fajlok helye
# A program a sajat mappajaban keresi az autok.csv fajlt.
projekt_mappa = Path(__file__).resolve().parent
csv_fajl = projekt_mappa / "autok.csv"
diagram_mappa = projekt_mappa / "diagrammok"
diagram_mappa.mkdir(exist_ok=True)


# Adatok beolvasasa: a Pandas egy tablazatot (DataFrame) hoz letre.
autok = pd.read_csv(csv_fajl)
print("\n=== AZ ADATOK ELLENORZESE ===")
print("Az elso 5 sor:")
print(autok.head())
print("\nOszlopnevek:", list(autok.columns))
print("Sorok szama a legelejen:", len(autok))
print("Hianyzo ertekek oszloponkent:")
print(autok.isna().sum())

# Adattisztitas
szukseges = [
    "name", "year", "selling_price", "km_driven", "fuel",
    "seller_type", "transmission", "owner"
]
# Ha ket sor minden adata teljesen megegyezik, egyet tartunk meg.
autok = autok.drop_duplicates()

# Szamma alakitjuk az arat, a futast es az evjaratot.
# Ha valamelyik ertek nem szam, NaN (hianyzo ertek) lesz belole.
for oszlop in ["year", "selling_price", "km_driven"]:
    autok[oszlop] = pd.to_numeric(autok[oszlop], errors="coerce")

# A vizsgalt adatokban nem lehetnek hianyzo alapadatok.
autok = autok.dropna(subset=szukseges).copy()

# Kizarjuk a nyilvanvaloan ervenytelen ertekeket.
autok = autok[
    (autok["selling_price"] > 0)
    & (autok["km_driven"] >= 0)
    & (autok["year"].between(1990, 2025))
].copy()

print("\nA tisztitas utan megmaradt sorok szama:", len(autok))
print("Az eladasi ar mertekegysege: indiai rupia (INR).")
print("Az osszes auto medianara:", round(autok["selling_price"].median()), "INR")

# Kategorizalas: az evjaratot es a megtett kilometert csoportokra bontjuk.
evjarat_cimkek = ["1990–2009", "2010–2014", "2015–2017", "2018–2025"]
km_cimkek = ["0–50 ezer", "50–100 ezer", "100–150 ezer", "150 ezer felett"]

autok["evjarat_csoport"] = pd.cut(
    autok["year"],
    bins=[1989, 2009, 2014, 2017, 2025],
    labels=evjarat_cimkek,
)
autok["km_csoport"] = pd.cut(
    autok["km_driven"],
    bins=[-1, 50000, 100000, 150000, np.inf],
    labels=km_cimkek,
)


# 1. KERDES: Evjarat, eladasi ar es valtótipus
# groupby: csoportokat kepezunk evjarat es valtotipus alapjan.
# median: a sorba rendezett ertekek kozepe; kevesbe erzekeny a nagyon draga autokra.
print("\n=== 1. KERDES: EVJARAT ES VALTOTIPUS ===")
evjarat_arak = (
    autok.groupby(["year", "transmission"])["selling_price"]
    .median()
    .reset_index()
)
print(evjarat_arak.tail(12).to_string(index=False))

abra1 = px.line(
    evjarat_arak,
    x="year",
    y="selling_price",
    color="transmission",
    markers=True,
    title="1. Evjarat es medianar – valtotipus szerint",
    labels={"year": "Evjarat", "selling_price": "Medianar (INR)",
            "transmission": "Valto"},
)
abra1.write_html(diagram_mappa / "01_evjarat_valto.html")


# 2. KERDES: Futasteljesitmeny, ar es uzemanyag
print("\n=== 2. KERDES: FUTASTELJESITMENY ES UZEMANYAG ===")
ket_uzemanyag = autok[autok["fuel"].isin(["Petrol", "Diesel"])].copy()
for uzemanyag in ["Petrol", "Diesel"]:
    resz = ket_uzemanyag[ket_uzemanyag["fuel"] == uzemanyag]
    if len(resz) >= 2:
        # Numpy: a Pearson-korrelacio -1 es +1 koze esik.
        # Negativ ertek: a nagyobb futashoz jellemzoen kisebb ar tarsul.
        korrelacio = np.corrcoef(resz["km_driven"], resz["selling_price"])[0, 1]
        print(f"{uzemanyag}: {len(resz)} auto, korrelacio = {korrelacio:.3f}")

abra2 = px.scatter(
    ket_uzemanyag,
    x="km_driven",
    y="selling_price",
    color="fuel",
    hover_data=["name", "year", "transmission"],
    opacity=0.45,
    title="2. Futasteljesitmeny es ar – benzin / dizel",
    labels={"km_driven": "Futasteljesitmeny (km)",
            "selling_price": "Eladasi ar (INR)", "fuel": "Uzemanyag"},
)
abra2.write_html(diagram_mappa / "02_kilometer_uzemanyag.html")


# 3. KERDES: Elado tipusa, valto es ar
print("\n=== 3. KERDES: ELADO ES VALTO ===")
eladok = (
    autok.groupby(["seller_type", "transmission"])["selling_price"]
    .agg(["median", "count"])
    .reset_index()
)
print(eladok.to_string(index=False))

abra3 = px.bar(
    eladok,
    x="seller_type",
    y="median",
    color="transmission",
    barmode="group",
    text="count",  # az oszlopokon a csoport darabszama latszik
    title="3. Medianarak – elado es valtotipus szerint",
    labels={"seller_type": "Elado tipusa", "median": "Medianar (INR)",
            "transmission": "Valto", "count": "Adatok szama"},
)
abra3.write_html(diagram_mappa / "03_elado_valto.html")


# 4. KERDES: Benzin / dizel arak evjaratcsoportonkent
print("\n=== 4. KERDES: UZEMANYAG ES EVJARATCSOPORT ===")
uzemanyag_arak = (
    ket_uzemanyag.groupby(["evjarat_csoport", "fuel"], observed=True)
    ["selling_price"].agg(["median", "count"]).reset_index()
)
print(uzemanyag_arak.to_string(index=False))

abra4 = px.box(
    ket_uzemanyag,
    x="evjarat_csoport",
    y="selling_price",
    color="fuel",
    points=False,
    title="4. Benzines es dizel autok arainak eloszlasa",
    labels={"evjarat_csoport": "Evjaratcsoport",
            "selling_price": "Eladasi ar (INR)", "fuel": "Uzemanyag"},
)
abra4.write_html(diagram_mappa / "04_uzemanyag_evjarat.html")


# 5. KERDES: Evjaratcsoport es kilometer-kategoria egyutt
print("\n=== 5. KERDES: EVJARATCSOPORT ES KM-CSOPORT ===")
ket_csoport = (
    autok.groupby(["evjarat_csoport", "km_csoport"], observed=True)
    ["selling_price"].agg(["median", "count"]).reset_index()
)
print(ket_csoport.to_string(index=False))

# Keves adatbol nem szeretnenk eros kovetkeztetest levonni:
# ahol 10-nel kevesebb auto van, ott nem rajzolunk erteket.
ket_csoport.loc[ket_csoport["count"] < 10, "median"] = np.nan

hotabla = ket_csoport.pivot(
    index="evjarat_csoport", columns="km_csoport", values="median"
)
hotabla = hotabla.reindex(index=evjarat_cimkek, columns=km_cimkek)

abra5 = px.imshow(
    hotabla,
    text_auto=".0f",
    aspect="auto",
    title="5. Medianarak evjarat es futasteljesitmeny szerint",
    labels={"x": "Futasteljesitmeny", "y": "Evjaratcsoport",
            "color": "Medianar (INR)"},
)
abra5.write_html(diagram_mappa / "05_hoterkep.html")

print("\nKESZ! Az 5 interaktiv diagram itt talalhato:")
print(diagram_mappa)