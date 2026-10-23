# Changelog

## 1.1.0 - 2026-10-23

- Add one preparation recipe for custom Loaded Nachos from tortilla chips, cheese, tomato, fresh jalapeno and onion, incorporating one standard plate and retaining a sharp knife.
- Return one Base.Plate via native ReplaceOnUse after depletion; preserve native partial-eating behavior without an OnEat inventory callback or parallel plate output.
- Use native GoodHot for two less unhappiness while hot; no heating-related calories or macro changes. Ready-to-eat state avoids repeated cooking-age transitions, with native cooling/spoilage/burning.
- Preserve the oldest mapped ingredient freshness, including stale ingredients; leave cheese and tomato-paste runtime files byte-identical to 1.0.2.
- Add original 32x32 transparent icon and source/QA art, English translations, documented plain native 3D plate mesh reference, and 34 focused isolated nachos cases plus static recipe/lifecycle/art checks. Gameplay and multiplayer remain untested.


## 1.0.2 - 2026-10-23

- Add one Cooking recipe consuming nine whole, fresh, raw tomatoes for one existing vanilla TomatoPaste, with retained empty pot, sharp knife and stirring utensil; Cooking 1, time 1200, 5 Cooking XP.
- Reject stale, rotten, frozen, burnt, cooked and partly consumed tomatoes using native status/whole/raw flags plus a tomato-only freshness predicate.
- Reuse the 1.0.1 fire and powered/warmed stove predicate unchanged, including generator power; keep the cheese recipe and helper byte-identical.
- Deliberately preserve the vanilla packaged/nonperishable paste definition and nutrition; no new food type, sealing/opening recipe, empty-can reward or inventory mutation.
- Add English name/tooltip, installed-contract checks, 22 isolated tomato Lua cases, three native lifecycle spy cases, and separate deterministic install/source ZIPs. Gameplay/multiplayer acceptance remains pending.


## 1.0.1 - 2026-10-23

- Extend the existing cheese recipe with powered, active, unbroken and warmed ordinary stove support, using native power detection for both mains and generators.
- Preserve native lit campfire/fireplace/barbecue acceptance, ingredients, vanilla cheese output, IDs, skill, time and XP. No duplicate recipe or workstation tag is added.
- Reject off, unpowered, cold, broken, zero-setting stoves and non-stove appliances; add a heat-requirement tooltip.
- Add 25 isolated Lua regression cases using the installed Kahlua VM and static checks of the native power/temperature API chain. Live game, generator/stove and multiplayer acceptance remain pending.

## 1.0.0 — 2026-10-22

- Add a single Cooking recipe producing one vanilla cheese from one litre of pure cow/sheep milk, one vinegar charge and one salt food-use unit.
- Keep the empty pot, cheesecloth and reusable milk container; use native open-fire and input filters.
- Add manual installation, rollback, multiplayer limitations, offline validation, deterministic packaging and SHA-256 verification.
