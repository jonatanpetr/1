#!/bin/bash
# Instalace odesilace prani na Mac. Spustit jednou:
#   bash mac/install.sh
# Autor: Jonatan Petr
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
PLIST_ZDROJ="$REPO/mac/com.jonatanpetr.prani.plist"
PLIST_CIL="$HOME/Library/LaunchAgents/com.jonatanpetr.prani.plist"

echo "Repo: $REPO"

if ! git -C "$REPO" fetch --quiet origin; then
  echo "Pozor: git fetch selhal. Zkontroluj, ze mas k repu pristup (git pull rucne)."
fi

mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"
sed -e "s|__REPO__|$REPO|g" -e "s|__HOME__|$HOME|g" "$PLIST_ZDROJ" > "$PLIST_CIL"

launchctl unload "$PLIST_CIL" 2>/dev/null || true
launchctl load "$PLIST_CIL"

echo
echo "Hotovo. Odesilac pobezi kazdych 5 minut."
echo
echo "Jeste dve veci:"
echo "1. Pri prvnim odeslani se macOS zepta, jestli smi skript ovladat Messages. Povol to."
echo "   (Kdyz se nezepta: Nastaveni systemu, Soukromi a zabezpeceni, Automatizace.)"
echo "2. Aby odesly i SMS na cisla bez iMessage, zapni na iPhonu"
echo "   Nastaveni, Zpravy, Predavani textovych zprav, a povol tenhle Mac."
echo
echo "Zkouska bez odeslani:  python3 mac/odesilac.py --dry-run"
echo "Log:                   tail -f ~/Library/Logs/prani.log"
