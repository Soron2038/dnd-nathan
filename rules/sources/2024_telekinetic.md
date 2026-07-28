# Telekinetic — provided 2024 rules text

Status: am 2026-07-28 vom DM über die freigegebene Aidedd-D&D-5.5-Datenbank bezogen
(`https://www.aidedd.org/feat/telekinetic`, Source der Seite: **Player's Handbook 2024**).
Gewählt bei Nathans Bard-Level-4-Feature (Ability Score Improvement).

## Regeltext

**General Feat** (Prerequisite: Level 4+)

- **Ability Score Increase.** Increase your Intelligence, Wisdom, or Charisma score by 1, to a
  maximum of 20.
- **Minor Telekinesis.** You learn the `Mage Hand` spell. You can cast it without Verbal or Somatic
  components, you can make the spectral hand Invisible, and its range and the distance it can be
  away from you both increase by 30 feet when you cast it. The spell's spellcasting ability is the
  ability increased by this feat.
- **Telekinetic Shove.** As a Bonus Action, you can telekinetically shove one creature you can see
  within 30 feet of yourself. When you do so, the target must succeed on a Strength saving throw
  (DC 8 plus the ability modifier of the score increased by this feat and your Proficiency Bonus)
  or be moved 5 feet toward or away from you.

## Nathan implementation

- Erhöhtes Ability Score: **Charisma** 16 → **17**. Der Modifier bleibt bei +3; der Punkt zahlt sich
  erst bei einem künftigen zweiten Increase auf 18 aus. Charisma ist dennoch die richtige Wahl, weil
  es sowohl die Spellcasting Ability von `Mage Hand` als auch den DC von `Telekinetic Shove` bestimmt.
- **`Mage Hand`**: ohne Verbal- und Somatic-Komponente, Hand nach Wahl unsichtbar, Reichweite
  **60 feet**, maximale Entfernung von Nathan ebenfalls **60 feet**. Spellcasting Ability Charisma.
  Zählt nicht gegen Nathans bekannte Cantrips.
- **`Telekinetic Shove`**: Bonus Action, 30 feet, Strength save gegen
  **DC 8 + 3 (Charisma) + 3 (Proficiency Bonus) = 14**; bei Misserfolg 5 feet Bewegung.
- Hinweis für den Tisch: Der Shove konkurriert mit `Bardic Inspiration` um Nathans Bonus Action.

## Kampagnenrelevanz

`Mage Hand` ohne sichtbare Komponenten und mit unsichtbarer Hand ist Nathans stärkstes Werkzeug für
die Rolle, die er in der Hohlen Falte etabliert hat: Dinge geschehen zu lassen, ohne dass jemand ihn
zaubern sieht. In Kombination mit `Minor Illusion` und `Phantasmal Force` ergibt das ein
vollständiges Repertoire für vorgetäuschte übernatürliche Wirkung.
