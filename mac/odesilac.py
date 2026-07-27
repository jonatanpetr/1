#!/usr/bin/env python3
# Odesilac prani. Bezi na Macu pres launchd kazdych 5 minut.
# Precte outbox/fronta.json, posle splatne zpravy pres Messages
# a zapise potvrzenky do potvrzenky/potvrzenky.jsonl.
# Autor: Jonatan Petr

import json
import os
import subprocess
import sys
import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTBOX = os.path.join(REPO, "outbox", "fronta.json")
POTVRZENKY = os.path.join(REPO, "potvrzenky", "potvrzenky.jsonl")
LOG = os.path.expanduser("~/Library/Logs/prani.log")
VETEV = "claude/cloud-wishes-routine-n0ydqq"
MAX_ZPOZDENI_HODIN = 20

DRY_RUN = "--dry-run" in sys.argv


def log(zprava):
    radek = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  " + zprava
    print(radek)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(radek + "\n")
    except OSError:
        pass


def git(*args, ok_kody=(0,)):
    vysledek = subprocess.run(
        ["git", "-C", REPO] + list(args),
        capture_output=True, text=True, timeout=120,
    )
    if vysledek.returncode not in ok_kody:
        log("git " + " ".join(args) + " selhal: " + vysledek.stderr.strip()[:200])
    return vysledek.returncode == 0


def posli_applescript(sluzba, telefon, text):
    skript = (
        'on run argv\n'
        'set cisloPrijemce to item 1 of argv\n'
        'set telo to item 2 of argv\n'
        'tell application "Messages"\n'
    )
    if sluzba == "imessage":
        skript += 'set sluzba to 1st account whose service type = iMessage\n'
    else:
        skript += 'set sluzba to service "SMS"\n'
    skript += (
        'send telo to participant cisloPrijemce of sluzba\n'
        'end tell\n'
        'end run'
    )
    vysledek = subprocess.run(
        ["osascript", "-", telefon, text],
        input=skript, capture_output=True, text=True, timeout=60,
    )
    return vysledek.returncode == 0, vysledek.stderr.strip()[:200]


def posli(telefon, text):
    ok, chyba = posli_applescript("imessage", telefon, text)
    if ok:
        return True, "imessage"
    ok, chyba2 = posli_applescript("sms", telefon, text)
    if ok:
        return True, "sms"
    return False, (chyba or chyba2 or "neznama chyba")


def main():
    if not DRY_RUN:
        git("pull", "--rebase", "--quiet", "origin", VETEV)

    if not os.path.exists(OUTBOX):
        return
    with open(OUTBOX, encoding="utf-8") as f:
        fronta = json.load(f)

    hotove = set()
    if os.path.exists(POTVRZENKY):
        with open(POTVRZENKY, encoding="utf-8") as f:
            for radek in f:
                radek = radek.strip()
                if radek:
                    try:
                        hotove.add(json.loads(radek)["id"])
                    except (ValueError, KeyError):
                        pass

    ted = datetime.datetime.now()
    nove_potvrzenky = []
    for polozka in fronta:
        if polozka["id"] in hotove:
            continue
        telefon = (polozka.get("tel") or "").replace(" ", "")
        text = polozka.get("text") or ""
        if not telefon or not text:
            continue
        kdy = datetime.datetime.strptime(polozka["kdy"], "%Y-%m-%dT%H:%M")
        if kdy > ted:
            continue
        if (ted - kdy).total_seconds() > MAX_ZPOZDENI_HODIN * 3600:
            log("propadlo: " + polozka["id"])
            nove_potvrzenky.append({
                "id": polozka["id"], "stav": "selhalo",
                "kdy": ted.isoformat(timespec="seconds"),
                "chyba": "neodeslano vcas, Mac nebezel",
            })
            continue
        if DRY_RUN:
            log("DRY RUN, poslal bych: " + polozka.get("jmeno", "?") + " (" + telefon + "): " + text[:60])
            continue
        ok, info = posli(telefon, text)
        if ok:
            log("odeslano: " + polozka.get("jmeno", "?") + " pres " + info)
            nove_potvrzenky.append({
                "id": polozka["id"], "stav": "odeslano",
                "kdy": ted.isoformat(timespec="seconds"), "kanal": info,
            })
        else:
            log("selhalo: " + polozka.get("jmeno", "?") + ": " + info)
            nove_potvrzenky.append({
                "id": polozka["id"], "stav": "selhalo",
                "kdy": ted.isoformat(timespec="seconds"), "chyba": info,
            })

    if DRY_RUN or not nove_potvrzenky:
        return

    os.makedirs(os.path.dirname(POTVRZENKY), exist_ok=True)
    with open(POTVRZENKY, "a", encoding="utf-8") as f:
        for p in nove_potvrzenky:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    git("add", "potvrzenky")
    git("commit", "-m", "Potvrzenky: " + str(len(nove_potvrzenky)) + " zprav", "--quiet")
    for pokus in range(3):
        if git("push", "--quiet", "origin", VETEV):
            break
        git("pull", "--rebase", "--quiet", "origin", VETEV)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log("chyba behu: " + repr(e)[:300])
        raise
