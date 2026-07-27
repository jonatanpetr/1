# Přání

Automat na narozeniny, svátky a jednorázové zprávy. Texty píšu já,
systém je v den D pošle z mého čísla. Autor: Jonatan Petr.

## Jak to jede

```
Kokpit (claude.ai)  <->  prani-data.json (Google Drive, složka Přání)
                              |
                     cloud routine, 2x denně
                              |
                    outbox/fronta.json (tohle repo)
                              |
                Mac, launchd po 5 minutách: Messages
                              |
                    potvrzenky/potvrzenky.jsonl
```

- **Kokpit**: https://claude.ai/code/artifact/f13f2694-2171-4134-923b-b186514f86df
  Fronta na 30 dní, psaní textů, časy, jednorázovky, doplňování čísel.
  Ukládá na můj Google Drive, při prvním otevření se zeptá na povolení.
- **Cloud routine** běží ráno a večer: sesype data z Drivu, připraví outbox
  pro Mac, promítne potvrzenky a pošle mi push, když něco chybí nebo neodešlo.
  Přesný postup: `routine/pokyny.md`.
- **Mac** posílá. Jen on se dotýká Messages.

## Nastavení Macu (jednou)

```bash
git clone https://github.com/jonatanpetr/1.git prani
cd prani && git checkout claude/cloud-wishes-routine-n0ydqq
bash mac/install.sh
```

Potom:

1. Při prvním odeslání povolit skriptu ovládání Messages.
2. Na iPhonu zapnout Nastavení, Zprávy, Předávání textových zpráv,
   ať odejdou i klasické SMS na čísla bez iMessage.

Zkouška bez odeslání: `python3 mac/odesilac.py --dry-run`

## Struktura

| Cesta | Co v ní je |
|---|---|
| `web/sprava.html` | zdroj kokpitu (artefakt na claude.ai) |
| `data/seed.json` | startovní data: 279 lidí, svátky, dotazy |
| `mac/` | odesílač, launchd úloha, instalace |
| `routine/pokyny.md` | postup pro cloud routine |
| `outbox/fronta.json` | co se má poslat (píše cloud, čte Mac) |
| `potvrzenky/potvrzenky.jsonl` | co se poslalo (píše Mac, čte cloud) |

## Pravidla

- Bez textu se nic neposílá. Texty píšu jen já.
- Když Mac nejede, zpráva počká, po 20 hodinách propadne a přijde mi
  push s možností poslat ji ručně z kokpitu.
- Data na Drivu: každé uložení vytvoří novou verzi souboru
  `prani-data.json` ve složce Přání. Staré verze můžu klidně mazat,
  čte se vždy nejnovější.
