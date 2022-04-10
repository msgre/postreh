Postřehová hra pro 2-4 hráče, realizovaná pro [Vrtuli, svět her a
poznání](https://zlatesipy.tomici.cz/vrtule/).

![Hra Postřeh](/docs/imgs/postreh.jpg "Hra postřeh")

Jde o stolek se 4 tlačítky a světlem uprostřed.

Cílem hry je co nejdříve získat devět bodů. Ty se získávají stiskem tlačítka
ihned po rozsvícení světla uprostřed. Pokud se některý hráč unáhlí a stiskne
tlačítko ještě před rozsvícením, o bod přichází.

[Demonstrační video](https://youtu.be/h4fl8f8gwDo).

### Obsah

* [Hardware](#hardware)
* [Software](#software)
* [3D modely](#3d-modely)
* [Polepy](#polepy)
* [Opravy](#opravy)

## Hardware

Hru ovládá malý jednodeskový počítač Raspberry Pico (`U1`) a Micropython kód z
tohoto repozitáře. Hlavní světlo a signalizace získaných bodů jsou zrealizovány s
pomocí programovatelných diod Neopixel. Protože RPico používá 3.3V logiku, je
nutné mezi LED pásek a počítač vložit převodník logických úrovní (`U2`).
Tlačítka ze stolu (`SW1..4`) připínají 5V přímo na piny RPico. Na napájecích
pinech počítače a u konektorů vedoucích do Neopixelů jsou [dle
doporučení](https://learn.adafruit.com/adafruit-neopixel-uberguide/best-practices)
připojeny odrušovací kondenzátory (`C1..3`).

![Ovládací deska](/docs/imgs/deska.jpeg "Ovládací deska")

[![Schéma zapojení](/docs/imgs/postreh_schema.png "Schéma zapojení")](/schema/)

Do hlavního světla vedou 2 kablíky (`B` a `C`). Kabel `C` ale přivádí pouze
napájení doprostřed pásku, to aby diody v druhé polovině v důsledku úbytku
napětí nesvítily méně než ty v první polovině.

Upozornění: na datovém vstupu Neopixelů je připájen odpor 390R, který chrání
první diodu v pásku (ve schématu výše není zakreslen).

[Schéma zapojení v KiCadu](/schema/)

**Napájení**

Celou hru napájí malý spínaný 50W zdroj, připojený do svorek +/- na okraji desky.

Během vývoje jsem ale desku připojoval (a napájel) z externího docku co mám
u počítače, zkrz standardní RPico USB vstup. Pro klid duše je asi vhodné v této
konfiguraci stáhnout jas diod (konstanty `LED_MAIN_BRIGHTNESS` a `LED_NUMBERS_BRIGHTNESS`
v souboru `postreh/config.py`), ať proudy tekoucí z docku nejsou moc velké.

Hru utáhne i Powerbanka, opět připojená standardně přes RPico USB vstup
(odzkoušeno).

## Software

Hra je naprogramovaná pro Micropython v1.17 (Python 3.4).

Nahrávání SW dovnitř RPico je možné provést s pomocí aplikace
[Thonny](https://thonny.org/). Stačí nakopírovat soubor [`main.py`](/main.py) a kompletní
podadresář [`postreh/`](/postreh/).

Logika aplikace není nijak složitá. Snažil jsem se rozdělit funkční celky do
samostaných modulů. Hra se řídí stavovou mašinou dle následujícího nákresu:

![Stavy](/docs/imgs/stavy.jpeg "Stavy")

Jednotlivé stavy jsou popsány soubory v [`postreh/states/`](/postreh/states/).

V adresáři [`postreh/effects/`](postreh/effects/) jsou naimplementovaný vizuální efekty pro
Neopixel LEDky. Protože jejich tunění zabralo hodně času, jsou v
[`postreh/effects/tests/`](postreh/effects/tests/) jednoduché skripty, které po spuštěním v aplikaci
Thonny efekt oddemonstrují.

## 3D modely

V adresáři [`3d/`](/3d/) jsou uložené zdrojové 3D modely (Fusion 360) pro díly použité
v Postřehu a z nich vygenerované `.gcode` pro patřičné materiály a tiskárnu Prusa MK3.

[**Signalizace skóre**](/3d/postreh_cisla_u_tlacitek_v10.f3d)

Kulatý díl s prosvětlenými čísly. Skládá se z několika částí.

![Signalizace skóre](/docs/imgs/skore.jpeg "Signalizace skóre, starší verze")

Hlavní díl (černý Prusament PETG) do kterého jsou vloženy Neopixely:

![Hlavní černý díl](/docs/imgs/postreh_cisla_u_tlacitek_v10_kolco.png "Hlavní černý díl")

Průsvitný díl s čísly (průsvitné noname PLA), který se vkládá do černého.
Jeho součástí jsou i šikmé plošky s nalepenou zrcadlovou fólií, která odráží
světlo z Neopixelů do čísel. Zároveň se stará o zafixování pozice Neopixel
pásku:

![Průsvitný díl s čísly](/docs/imgs/postreh_cisla_u_tlacitek_v10_cisla.png "Průsvitný díl s čísly")

Titěrné středy čísel (černý Prusament PETG), které se vlepí dovnitř děr
v průhledném dílu:

![Středy čísel](/docs/imgs/postreh_cisla_u_tlacitek_v10_stredy.png "Středy čísel")

[**Žárovka**](/3d/postreh_zarovka_v3.f3d)

![Zkompletovaná žárovka](/docs/imgs/zarovka.jpeg "Zkompletovaná žárovka")

Hlavní světlo je opět Neopixel pásek, ale zapojený tak, aby byl použitelný
jako žárovka (jde o sadu osmi pásků po 7-mi diodách zapojených za sebou):

![Žárovka](/docs/imgs/postreh_zarovka_v3.png "Žárovka")

Volitelnou součástí je i díl, který zaoblí horní část žárovky. Neopixel pásky
pak nejsou na horní hraně tak namáhány (v aktuální verzi Postřehu jsme jej ale
nepoužili, diody byly už příliš blízko stínítka a nevypadalo to dobře):

![Špunt](/docs/imgs/postreh_zarovka_v3_spunt.png "Špunt")

[**Krytka stínítka**](/3d/krouzek_svetlo_v1.f3d)

Překrytí keramického dílu a nevzhledného středu na hrací desce:

![Krytka](/docs/imgs/krytka.jpeg "Krytka")

![Krytka](/docs/imgs/krouzek_svetlo_v1.png "Krytka")

[**Držák řídící desky**](/3d/drzak_ridici_desky_v1.f3d)

![Držák řídící desky](/docs/imgs/drzak_ridici_desky_v1.png "Držák řídící desky")

## Polepy

Pro lepší přehlednost jsou konektory označené [barevnýma samolepkama](/docs/polepy.pdf) ([zdrojové SVG](/docs/polepy.svg))
a pod krytem je i [schématický návod](/docs/konektory.pdf) jak je zapojit ([zdrojové SVG](/docs/konektory.svg)).

![Konektory](/docs/imgs/konektory.png "Konektory")

## Opravy

Před jakoukoliv servisní manipulací odpoj Postřeh od elektřiny: sundej kryt na
stojanu a přepni vypínač do polohy 0.

### Jak sundat skleněné stínítko

1. **Odpoj elektřinu**
2. Polož ruku na stínítko, lehce zatlač a začni otáčet proti směru hodinových
   ručiček. Až se stínítko uvolní, pokračuj v otáčení a zároveň jej opatrně
   zvedej.

### Jak vyměnit/vytáhnout žárovku

1. **Odpoj elektřinu**
2. Odmontuj kryt na stojanu a odpoj modré konektory **B** a **C**
3. [Sundej skleněné stínítko](#jak-sundat-skleněné-stínítko)
4. Opatrně uchop žárovku a vyšroubuj ji proti směru hodinových ručiček. Po
   vyšroubování ji **pomalu** začni zvedat a dávej pozor ať se někde nezaseknou
   konektory.

### Jak vyměnit vadné tlačítko

1. **Odpoj elektřinu**
2. [Sundej skleněné stínítko](#jak-sundat-skleněné-stínítko)
3. [Odpoj a vytáhni žárovku](#jak-vyměnitvytáhnout-žárovku)
4. Odpoj tlačítka (červené konektory **1**, **2**, **3** a **4**)
5. Odpoj ovládání skóre (žlutý konektor **A**)
6. Odmontuj keramický držák skleněného stínítka (dva šrouby)
7. Poznamenej si orientaci hrací desky (až budeš hru zase skládat, musí být
   deska položená naprosto stejně, tlačítka a diody s číslama jsou spárované)
8. Odstraň XXX označené šrouby ze spodní strany a ve **dvou lidech** opatrně
   hrací desku nadzvedni. Z díry uprostřed stolu se začnou vytahovat uvolněné
   dráty od tlačítek. Třetí člověk musí všechny kabely vytáhnout a teprve pak
   můžeš desku odložit stranou.
9. Nyní máš přístup ke všem tlačítkům. Uvolni čtyři šrouby u vadného tlačítka
   a vyšroubuj všechny do výšky mezery mezi plastovou krabicí a dřevěným
   mačkadlem. Chytni tlačítko za dřevo a opatrně jej nadzdvihni.

Uvnitř krabice najdeš 2 tlačítka, zelené a červené.

![Tlačítka v krabici](/docs/imgs/tlacitka.jpeg "Tlačítka v krabici")

Zelené je NO (Normaly Open, zmáčknutím se sepne), červené je NC (Normaly
Closed, zmáčknutím se rozpojí). Obvykle využíváme zelené NC, ale pokud nějaké
tlačítko selže, nejprve se jej snažíme nahradit červeným a teprve pokud ani to
nefunguje, tak jej vyměníme fyzicky.

Podle toho které z tlačítek je využito je třeba adekvátně upravit konstantu
`BUTTON_CONFIG` v souboru [`postreh/config.py`](/postreh/config.py#L37-L43).

Upozornění: v krabici musí být vždy oba spínače, mechanismus tlačítka s tím
počítá. Nevyužitý spínač ale klidně může být vadný (proto je dobré je
nevyhazovat).

Upozornění: červené spínače (NC) jsou citlivější než zelené (NO)
