# Přímí předci podle Kekulého čísel: 1 = výchozí osoba (ten, pro koho rodokmen děláme),
# otec osoby n má číslo 2n, matka 2n+1. Tedy 2 = otec, 3 = matka, 4–7 prarodiče, 8–15 pradědečci a prababičky…
#
# Každá osoba:  číslo: dict(n="Jméno Příjmení", y="1850–1910", st="doc", f=[...], r=[...], note="...")
#   n    jméno; ženy rodným příjmením („Anna Dvořáková“), u nejistého čtení otazník („Marie Špalková (?)“)
#   y    roky života pro přehledy: "* 1931" (žije / úmrtí neznámé), "1850–1910", "asi 1720–1785", "1680 – před 1740"
#   st   stav doložení:  doc  = doloženo matrikou (čteno přímo ze snímku)
#                        prob = pravděpodobné (shoda údajů, ale ne přímý doklad)
#                        fam  = údaj od rodiny / z rodinného dokumentu
#                        mh   = jen z cizího rodokmenu na internetu (MyHeritage, Geni…) – neověřeno
#                        unk  = neznámé (jen místo v rodokmenu)
#   f    fakta jako krátké věty: "* 12. 3. 1873 Hořice čp. 477", "kovář", "× 28. 1. 1897 Anna Stejskalová", "† 14. 5. 1902"
#        (* narození, × sňatek, † úmrtí – podle těchto značek web pozná sňatky a místa pro mapu)
#   r    klíče zápisů z data/zaznamy.json, které osobu dokládají
#   note poznámka: proč je údaj nejistý, rozpory, odkud se vzal
#   sex  jen u osoby 1: "M" nebo "F" (u ostatních plyne z čísla)
# Žijící lidé: jen jméno a rok narození (soukromí), note="Žijící – údaje jen základní."
# Neznámý otec nemanželského dítěte: dict(n="otec neuveden", st="unk", f=[], note="…")

P = {
    1: dict(n="Jonatan Petr", y="* 2004", st="fam", sex="M", f=[],
            note="Žijící – údaje jen základní. Výchozí osoba rodokmenu."),
    2: dict(n="Jan Petr", y="", st="fam", f=[],
            note="Žijící – údaje jen základní. Otec. Rok narození doplnit."),
    3: dict(n="Helena Petrová (rodné příjmení?)", y="* 1973", st="fam", f=[],
            note="Žijící – údaje jen základní. Matka. Rodné příjmení zatím neznáme (Dvořáková?)."),
    4: dict(n="Jan Petr", y="", st="prob", f=[],
            note="Děda „Jenda Petr“. Podle příjmení otec otce – potvrdit. Žije? Rok narození?"),
    5: dict(n="(babička z otcovy strany)", st="unk", f=[], note="Jméno zatím neznáme."),
    6: dict(n="Milan Dvořák", y="* 1951", st="prob", f=[],
            note="Žijící – údaje jen základní. Manžel babičky Blanky, „děda“. Jestli je to máminin vlastní otec, potvrdit."),
    7: dict(n="Blanka Dvořáková (rodné příjmení?)", y="* 1950", st="fam", f=[],
            note="Žijící – údaje jen základní. Matka Heleny (doloženo rodinnou smlouvou 2025). Rodné příjmení zjistit."),
}

# Rody = osm větví podle pradědečků a prababiček (čísla 8–15). Doplňte, jakmile je znáte:
# 8: ("Novákové", "Jedna věta, kdo to byli a odkud – ukáže se na webu u rodu."),
LINES = {
}

# Příbuzní mimo přímou linii (sourozenci, strýcové…): k = číslo předka, ke kterému patří.
# dict(k=16, n="Josef Novák (1865–1920)", t="Bratr Jana. Kovář v …", r=["klic_zapisu"])
SIDE = [
    dict(k=1, n="Nela Winkler, roz. Petrová (* 1998)", t="Sestra Jonatana. Manžel Petr Winkler, syn William (* 2026)."),
    dict(k=1, n="Benjamin Petr (* 2007)", t="Bratr Jonatana."),
    dict(k=7, n="Tereza Chromovská (* 1979)", t="Teta, podle rodinné smlouvy nejspíš sestra Heleny. Dcery Josefina a Evelína."),
]

# Rozpory a otevřené otázky (na web do „Co hledáme“) jako dvojice (otázka, odpověď). Odpověď začněte
# „Vyřešeno: …“ (na webu se skryje), „Hypotéza: …“ nebo „Otevřené: …“. Jde na web – nic citlivého.
# ("Kdy se narodil Jan Novák?", "Otevřené: rodina říká 1850, v Holicích 1848–1852 nenalezen.")
ISSUES = [
    ("Jaké je rodné příjmení mámy Heleny?", "Otevřené: zeptat se mámy nebo babičky Blanky."),
    ("Jaké je rodné příjmení babičky Blanky Dvořákové a odkud pochází?", "Otevřené: zeptat se babičky."),
    ("Je Milan Dvořák vlastní otec Heleny?", "Otevřené: v rodině ho všichni berou jako dědu, potvrdit."),
    ("Kdo je babička z tátovy strany a odkud pocházejí Petrovi?", "Otevřené: zeptat se táty a dědy Jendy."),
    ("Jak patří do rodiny Kludajovi ze Slovenska (nevlastní prarodiče)?", "Otevřené: zjistit, přes koho se rodiny propojily."),
]

# Hypotézy o původu rodu nad rámec doložené linie (zobrazí se na stránce rodu):
# dict(rod=8, nadpis="Hypotéza: Novákové z Lhoty", text="…", polozky=[("Jan Novák", "kmotr 1681…")], zaznamy=["klic"])
HYPOTEZY = [
]

# Předek v rodokmenu vícekrát (příbuzní rodiče): {alias: hlavní číslo}, např. {350: 140}
SAME = {}
