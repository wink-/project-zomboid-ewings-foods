# Ewing's Foods

Version **1.0.1** · mod ID **EwingsFoods** · standalone Project Zomboid **42.21** mod.

One crafting action turns milk into the existing vanilla `Base.Cheese`, ready for pizza and other vanilla recipes. No new food, intermediate item, dependency, vanilla replacement, global Lua override, or background system is added. One mod-owned shared Lua callback extends the native heat check.

## Make cheese

Find **Make Cheese (Ewing's Foods)** in the Cooking crafting category. Have Cooking level 1, an empty cooking pot, cheesecloth, and the ingredients below near a lit open fire or a powered, switched-on and warmed stove.

| Ingredient or tool | Per batch |
| --- | --- |
| Pure `CowMilk` or pure `SheepMilk` | 1.0 litre, in one fluid container |
| `Base.Vinegar2` or `Base.Vinegar_Jug` | 1 native drainable charge |
| `Base.Salt` | 1 native food-use unit (one tenth of a full salt item) |
| `Base.Pot` or `Base.PotForged` | 1 empty pot, kept |
| `Base.CheeseCloth` | 1, kept |
| Result | 1 vanilla `Base.Cheese` |

The milk container is kept, including after its last litre is drained. The pot and cloth are tools and are never consumed by this recipe. Vinegar is a vanilla drainable item, not a refillable fluid container: its final charge removes its packaging under vanilla rules. Partial vinegar and salt remain. No extra empty containers are generated.

Heat accepts the existing native `RecipeCodeOnTest.openFire` options (lit fireplaces, lit barbecues and native nearby fire/campfire checks), or a nearby ordinary stove. The stove must be unbroken, switched on, supplied with power through the game's `container:isPowered()` API, have a positive temperature setting, and have begun warming. Mains electricity and generator-supplied electricity both qualify; a generator is not specifically required. An off or unpowered stove does not qualify even if residual heat remains. Microwaves, toasters and coffeemakers are excluded.

Stand in the same square as the stove or an adjacent square on the same floor (the native `getRadius(2)` 3-by-3 neighborhood). Turn the stove on with a positive temperature setting and let it begin warming, then select this same cheese recipe. The installed `getCurrentTemperature()` returns a normalized heat value, with unwarmed raw zero represented as 1; the callback requires a value above 1. This is an abstract heating gate, not a real food-safety temperature or a separate heating recipe. Ingredient placement and the one-action recipe remain unchanged.

The recipe requires exact, unmixed milk. Water, tainted water, hazardous liquids, chocolate milk, and milk mixtures are excluded. Native rotten/frozen item restrictions remain enabled; there is no `AllowRottenItem` or `AllowFrozenItem` exception. In the inspected build, milk is a normal item with a fluid component, with no food-age fields in its definition. This mod does not invent fluid spoilage or claim to detect an age state the engine does not supply.

Balance choices: one litre yields one 0.2-weight vanilla cheese; time is 600 native recipe units (the handcraft UI displays base recipe time divided by ten, before engine modifiers); Cooking 1 and 5 Cooking XP. This is an abstract, deliberately modest batch. One litre fits the vanilla pot's 1.5-litre capacity. The real-life gallon recipe inspired the milk/acid/strain/salt combination, all represented by one crafting action. Vinegar charges are game units, not a measured quarter cup. This is gameplay, not food-preparation guidance.

Vanilla cheese is unchanged: pizza ingredient support, 113 calories, -15 hunger, 14 fresh days and 20 days to fully rotten in the inspected definitions. Normal game storage, time, and cooking rules still apply.

## Install

1. Use the locally built `EwingsFoods-1.0.1.zip` and verify its SHA-256 sidecar. This update is prepared locally and has not been pushed or released; published versions are listed under [Releases](https://github.com/wink-/project-zomboid-ewings-foods/releases). Close the game before installing.
2. Extract the single `EwingsFoods` directory into the effective Project Zomboid user-data `mods` directory. It must contain `EwingsFoods/42/mod.info` and `EwingsFoods/common/`. Do not install a GitHub source archive as the install ZIP.
3. Enable **Ewing's Foods** in the appropriate mod selection. For an existing world, use its own mod selection and back up the world first. No additional mod is required. When upgrading, replace only the old EwingsFoods folder instead of merging versions.

This release is a manual download, not a Steam Workshop subscription. Nothing is installed or enabled by the build tools.

## Compatibility, multiplayer, removal

Inspected target: Windows, game 42.21, Steam build 25485521. The version bounds intentionally cover only 42.21. Recheck future builds before widening them.

Native crafting data, English translations and one shared, read-only mod-owned heat predicate are shipped. For multiplayer, distribute the identical version to server and every client and add `EwingsFoods` to the server's mod list according to its normal administration process. No Workshop ID exists. The absence of custom networking does not establish multiplayer compatibility: client/server crafting, sync, interruption, and reconnect still require runtime testing.

To roll back, close the game/server normally, disable this mod for that world/server, then remove only its `EwingsFoods` directory or restore a previous version. It creates no custom saved item types; existing crafted cheese stays vanilla cheese. Consumed ingredients are not refunded. Keep backups and check other mods for recipe conflicts. Do not merge a replacement release into an old folder.

## Validation and development

See [validation evidence](docs/VALIDATION.md) and [runtime acceptance checks](docs/ACCEPTANCE.md). Offline checks are not an in-game or multiplayer certification. No game/server was launched, no mod was installed, and no saves or enabled-mod lists were accessed during development.

Requires Python 3.12+ and a local copy of the inspected game for definition checks. The native structural syntax check invokes `ScriptParser` from the local game JAR through a tiny generated Java bridge; it does not boot the game. The heat regression harness compiles and executes the actual callback using the installed Kahlua VM with test-double world objects; it does not use a live generator or stove. Supply paths as arguments; no machine-specific paths are stored in the repository.

```powershell
python tools/validate.py --game-root '<your ProjectZomboid installation>'
python tools/package.py
python tools/package.py --verify dist/EwingsFoods-1.0.1.zip
```

The packager uses an explicit file allowlist, fixed timestamps, stable ordering and ZIP_STORED. It builds twice, requires identical bytes, and checks the checksum and install layout. Source contains original mod data, original tooling and documentation only; no game assets/source, credentials, personal paths or logs. No license has been selected by the owner; no third-party license is asserted.
