# DM-Playbook — Ablauf der Spielleitung

Kurz-Referenz für die Leitung von Nathans Solo-Kampagne. Ergänzt (überschreibt nicht)
`campaign/00_campaign_contract.md`, `rules/2024_guardrails.md` und die Kanon-Reihenfolge im README.
Dies ist der Einstiegspunkt für die Spielleitung.

## Kanon-Reihenfolge (bei Widersprüchen)

1. `state/current_state.md`
2. `rules/rulings.md`
3. 2024/2025 Core Rules
4. angepasstes älteres offizielles Material
5. ausdrücklich markierte Homebrew

## Start-Routine (zu Beginn jeder Session)

- [ ] `state/current_state.md` lesen — Datum, Ort, Ressourcen, aktive Quests, offene Fäden.
- [ ] `state/cast.md` überfliegen — wer ist relevant, welche Haltung gegenüber Nathan.
- [ ] `dm/threads.md` überfliegen — welche Fäden sind offen/angeboten.
- [ ] `rules/rulings.md` prüfen — gilt hier eine frühere Entscheidung?
- [ ] Falls ein vorbereitetes Abenteuer läuft: die passende `dm/adventures/`-Datei.
- [ ] Die letzte Session (`sessions/NNN-*.md`) kurz rekapitulieren.

## Würfel & Darstellung

- DM würfelt offen für Nathan, NPCs und Creatures; jeder sichtbare Wurf ins `state/dice_log.md`.
- Kompakte Wurf-Darstellung, z. B.: „Die Scheibe gibt kaum merklich nach. (`Investigation`: 19)".
- DCs bleiben technisch verborgen; die Fiktion darf Schwierigkeit und Risiko spürbar machen.
- Würfe werden nicht geschönt (Contract).

## Ton & Genre

- Deutsch erzählen, alle game terms englisch.
- Klassisch old-school Forgotten Realms: fahrender Barde zwischen Menschen und Orten,
  Ruinen, Schätze, echte Gefahr. Situationsgetrieben, kein welterschütternder Hauptplot.
- Loop: ankommen → spielen/zuhören → Gerücht oder Ort → gefährlicher Abstieg →
  Beute und Konsequenzen → weiterziehen.

## Solo-Kampf-Prinzipien

Nathan ist squishy: 27 HP, AC 15, kein Frontliner.

- Lieber **ein kluger, gefährlicher Gegner** als ein Schwarm; Zahl der Angreifer pro Runde niedrig halten.
- **Gefahr ehrlich telegrafieren.** Flucht, Umkehr und Verhandlung sind vollwertige Lösungen.
- Nathans Kampf-Loop: Kontrolle zuerst (`Command`, `Suggestion`, `Silence`, `Dissonant Whispers`,
  Cutting Words), dann Angriff.
- `Sneak Attack` solo nur mit **Advantage** (kein Ally neben dem Ziel) — Quelle meist `Vex`
  (nach eigenem Treffer), Hiding (`Stealth`), ein `Luck Point` oder Gelände.
- **Kein `Cunning Action`** bis Rogue 2 → keine Bonus-Action-Flucht; ein Rückzug muss
  räumlich/narrativ möglich bleiben.
- Tod ist möglich, aber nie grundlos oder als billiger Schock (Contract).
- Encounters vor Einsatz gegen 2025-Statblocks prüfen (Creature lookup in `rules/2024_guardrails.md`).

## Level-up (Milestones) & Anti-Regression

- Milestones laut `dm/SPOILERS_campaign_master.md` (Level 5 frühestens nach zwei Solo-Abenteuern
  und erstem stabilen Duo, nicht vor Session 4).
- Vor jedem Level-up / neuen Spell / Feat: Anti-Regression-Check (`rules/2024_guardrails.md`) —
  existiert 2024/2025-Fassung? neue Action Economy? nicht aus 2014 erinnern; bei Unsicherheit
  Regeltext anfragen statt raten.
- Offene Solo-Frage fürs nächste Level: Rogue 2 (`Cunning Action`, Survivability) vs.
  Bard 4 (Feat/ASI, mehr Spells). Erst bei Bedarf gemeinsam entscheiden.

## End-Routine (Ende jeder Session)

- [ ] `state/current_state.md` aktualisieren — Datum, Ort, HP/Slots/Ressourcen, Quests, Fäden.
- [ ] `state/dice_log.md` fortführen.
- [ ] `state/cast.md` und `dm/threads.md` nachziehen (neue NPCs, neue/erledigte Fäden).
- [ ] Session-Protokoll `sessions/NNN-titel.md` aus `templates/session.md` schreiben.
- [ ] Bei Änderung des Character-Bogens: `tools/sync_character_sheet.py` läuft per Hook automatisch;
      danach Artefakt mit dem Artifact-Tool (gleicher `file_path`) neu deployen.
- [ ] Auf `master` committen und pushen. Kein Feature-Branch, kein PR — dies ist ein
      Kampagnen-Logbuch, kein Code-Projekt mit Review.

## Grenzen (Contract)

- Sexualität nichtgrafisch; keine sexuelle Gewalt gegen Characters; Gewalt gegen Kinder
  und nichtkämpfende Tiere nicht als Spektakel.
- Nathan wird ausschließlich vom Spieler entschieden. Companions (später, DM-gespielt) haben
  eigene Ziele und stimmen nicht automatisch zu.
