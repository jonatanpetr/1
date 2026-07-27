# Pokyny pro routine systému Přání

Tohle je přesný postup pro každé probuzení cronem. Běhy jsou dva denně:
ranní (05:30 UTC) a večerní (19:30 UTC). Postup je stejný, liší se jen okno
a notifikace. Časy v datech jsou pražské.

Klíčové konstanty:

- Google Drive složka Přání: id `1K5T38peUqGtDsFhsC8bR5ycdD3TQvlCE`
- Datový soubor: nejnovější `prani-data.json` v té složce (podle modifiedTime)
- Repo: `jonatanpetr/1`, větev `claude/cloud-wishes-routine-n0ydqq`
- Kokpit: https://claude.ai/code/artifact/f13f2694-2171-4134-923b-b186514f86df

## Postup

1. **Git pull** větve. V repu jsou `outbox/fronta.json` (co má Mac poslat)
   a `potvrzenky/potvrzenky.jsonl` (co Mac skutečně poslal).

2. **Načti data z Drivu**: `search_files` v složce, vyber nejnovější
   `prani-data.json`, stáhni přes `download_file_content` (base64), rozparsuj.
   - Když soubor neexistuje: data se zakládají prvním otevřením kokpitu.
     Pošli Jonatanovi jednou (ne opakovaně) push: ať otevře kokpit Přání
     a klepne na Založit data. Pro tenhle běh použij `data/seed.json` z repa
     jen pro čtení a nic na Drive nezapisuj.

3. **Zpracuj potvrzenky**: každou potvrzenku, jejíž `id` ještě není promítnuté
   v datech, promítni do `fronta` (stav `odeslano` nebo `selhalo`,
   `odeslanoKdy`, `kanal`/`chyba`) a odeslané přidej i do pole `odeslane`
   ve tvaru `{id, osobaId, typ, datum, text, stav, odeslanoKdy}`.

4. **Doplň frontu**: pro každou osobu s `pratNarozeniny`/`pratSvatek`
   vygeneruj chybějící položky fronty na příštích 30 dní
   (id `typ-osobaId-YYYY-MM-DD`, stav `chybi`), stejně jako to dělá kokpit.

5. **Zapiš data zpět na Drive**, jen pokud se něco změnilo:
   `create_file` s `title: prani-data.json`, `parentId` složky,
   `contentMimeType: application/json`, `disableConversionToGoogleType: true`,
   zvyš `verze` a nastav `aktualizovano`.

6. **Vygeneruj outbox**: do `outbox/fronta.json` zapiš položky fronty
   se stavem `ceka`, neprázdným textem a telefonem, s datem dnes nebo zítra:
   `[{id, jmeno, tel, text, typ, kdy: "YYYY-MM-DDTHH:MM"}]`
   (`kdy` = datum + čas položky, jinak čas osoby, jinak výchozí čas
   z nastavení). Celý soubor pokaždé přepiš. Commit a push
   (při konfliktu pull --rebase a znovu, potvrzenky nemaž).

7. **Notifikace** (PushNotification, česky, stručně):
   - ranní běh: dnešní událost bez textu nebo bez čísla
     („Dnes má narozeniny X, chybí text. Otevři Přání.");
     zprávy se stavem `selhalo` od minulého běhu
     („Přání pro X neodešlo. Pošli ho ručně z kokpitu.").
   - večerní běh: co zítra odejde („Zítra odejde přání pro X v 9:00.").
     Když zítra nic není a nic nechybí, neposílej nic.

## Zásady

- Nikdy neodesílej zprávy příjemcům z cloudu. Odesílá jen Mac.
- Nikdy nevymýšlej ani neupravuj texty přání. Texty píše jen Jonatan.
  Položka bez textu se neposílá, jen se na ni upozorní.
- Žádné upomínky na doplňování textů dopředu, Jonatan je nechtěl.
  Upozornění se týká jen dneška, selhání a zítřejšího přehledu.
- Odpověď v chatu drž na pár řádcích (co se stalo, co odešlo, co chybí).
