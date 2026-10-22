# Ewing's Foods

Version **1.0.0** · mod ID **EwingsFoods** · standalone Project Zomboid **42.21** mod.

One crafting action turns milk into the existing vanilla `Base.Cheese`, ready for pizza and other vanilla recipes. No new food, intermediate item, dependency, vanilla replacement, Lua override, or background system is added.

## Make cheese

Find **Make Cheese (Ewing's Foods)** in the Cooking crafting category. Have Cooking level 1, an empty cooking pot, cheesecloth, and the ingredients below near a lit open fire.

| Ingredient or tool | Per batch |
| --- | --- |
| Pure `CowMilk` or pure `SheepMilk` | 1.0 litre, in one fluid container |
| `Base.Vinegar2` or `Base.Vinegar_Jug` | 1 native drainable charge |
| `Base.Salt` | 1 native food-use unit (one tenth of a full salt item) |
| `Base.Pot` or `Base.PotForged` | 1 empty pot, kept |
| `Base.CheeseCloth` | 1, kept |
| Result | 1 vanilla `Base.Cheese` |

The milk container is kept, including after its last litre is drained. The pot and cloth are tools and are never consumed by this recipe. Vinegar is a vanilla drainable item, not a refillable fluid container: its final charge removes its packaging under vanilla rules. Partial vinegar and salt remain. No extra empty containers are generated.

Heat uses the installed game's `RecipeCodeOnTest.openFire`: lit fireplaces, lit barbecues, and the game's supported nearby fire/campfire checks. A powered kitchen stove alone does not meet this particular open-fire check. This provides an off-grid route without introducing a separate heating recipe. Follow the crafting UI's heat requirement; temperature in degrees is not simulated by this mod.

The recipe requires exact, unmixed milk. Water, tainted water, hazardous liquids, chocolate milk, and milk mixtures are excluded. Native rotten/frozen item restrictions remain enabled; there is no `AllowRottenItem` or `AllowFrozenItem` exception. In the inspected build, milk is a normal item with a fluid component, with no food-age fields in its definition. This mod does not invent fluid spoilage or claim to detect an age state the engine does not supply.

Balance choices: one litre yields one 0.2-weight vanilla cheese; time is 600 native recipe units (the handcraft UI displays base recipe time divided by ten, before engine modifiers); Cooking 1 and 5 Cooking XP. This is an abstract, deliberately modest batch. One litre fits the vanilla pot's 1.5-litre capacity. The real-life gallon recipe inspired the milk/acid/strain/salt combination, all represented by one crafting action. Vinegar charges are game units, not a measured quarter cup. This is gameplay, not food-preparation guidance.

Vanilla cheese is unchanged: pizza ingredient support, 113 calories, -15 hunger, 14 fresh days and 20 days to fully rotten in the inspected definitions. Normal game storage, time, and cooking rules still apply.

## Install

1. Download `EwingsFoods-1.0.0.zip` from [Releases](https://github.com/wink-/project-zomboid-ewings-foods/releases/tag/v1.0.0), optionally verify its SHA-256 sidecar, and close the game before installing.
2. Extract the single `EwingsFoods` directory into the effective Project Zomboid user-data `mods` directory. It must contain `EwingsFoods/42/mod.info` and `EwingsFoods/common/`. Do not install a GitHub source archive as the install ZIP.
3. Enable **Ewing's Foods** in the appropriate mod selection. For an existing world, use its own mod selection and back up the world first. No additional mod is required.

This release is a manual download, not a Steam Workshop subscription. Nothing is installed or enabled by the build tools.

## Compatibility, multiplayer, removal

Inspected target: Windows, game 42.21, Steam build 25485521. The version bounds intentionally cover only 42.21. Recheck future builds before widening them.

Only native crafting data and one English translation are shipped. For multiplayer, distribute the identical version to server and every client and add `EwingsFoods` to the server's mod list according to its normal administration process. No Workshop ID exists. The absence of custom networking does not establish multiplayer compatibility: client/server crafting, sync, interruption, and reconnect still require runtime testing.

To roll back, close the game/server normally, disable this mod for that world/server, then remove only its `EwingsFoods` directory or restore a previous version. It creates no custom saved item types; existing crafted cheese stays vanilla cheese. Consumed ingredients are not refunded. Keep backups and check other mods for recipe conflicts. Do not merge a replacement release into an old folder.

## Validation and development

See [validation evidence](docs/VALIDATION.md) and [runtime acceptance checks](docs/ACCEPTANCE.md). Offline checks are not an in-game or multiplayer certification. No game/server was launched, no mod was installed, and no saves or enabled-mod lists were accessed during development.

Requires Python 3.12+ and a local copy of the inspected game for definition checks. The native structural syntax check invokes only `ScriptParser` from the local game JAR through a tiny generated Java bridge; it does not boot the game. Supply paths as arguments; no machine-specific paths are stored in the repository.

```powershell
python tools/validate.py --game-root '<your ProjectZomboid installation>'
python tools/package.py
python tools/package.py --verify dist/EwingsFoods-1.0.0.zip
```

The packager uses an explicit file allowlist, fixed timestamps, stable ordering and ZIP_STORED. It builds twice, requires identical bytes, and checks the checksum and install layout. Source contains original mod data, original tooling and documentation only; no game assets/source, credentials, personal paths or logs. No license has been selected by the owner; no third-party license is asserted.
