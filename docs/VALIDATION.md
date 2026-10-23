# Validation evidence - 1.0.1

Date: 2026-10-23. Target: Windows, Project Zomboid 42.21, Steam build 25485521. Mod ID: EwingsFoods. Dependencies: none.

## Observed offline results

`python tools/validate.py --game-root <installation>` passed the ingredient/recipe checks, native structural syntax check, installed API checks and isolated Lua heat regressions:

1. Version/layout, exactly one additive recipe, its translated name, ingredients, tools, quantities, skill/XP and output contract.
2. All seven explicit item references and both milk fluid IDs resolve in installed definitions. Both pots hold the batch. Cheesecloth exists. Vinegar charge and salt food-use definitions match the documented units. Vanilla cheese keeps pizza support and its original stats.
3. Installed JAR inspection reconfirms 42.21 (Core's GameVersion initialization), default Exact fluid matching, the native rotten-food test, the openFire callback signature and source classes, the IsEmpty flag and every selected recipe property.
4. Fluid input binding/retention syntax matches installed DisinfectBandage; exact cow/sheep milk syntax matches MakeBowlOfCereal; heat callback matches FireHardenSpear. This is evidence about supported contracts, not copied game content in this release.
5. An original generated Java bridge called the installed ScriptParser.stripComments and ScriptParser.parse successfully on the mod script. It never invokes a game/client/server entry point. This checks structural syntax; it does not perform full world/runtime recipe registration.
6. One mod-owned shared heat callback delegates fire acceptance to the original native predicate, then checks ordinary stove type, on/off, broken state, power, positive setpoint and normalized warmth. There are no global overrides, permissive rotten/frozen flags, mixture matching, item definitions or inherited food mutations.
7. The actual Lua callback compiles and executes under the installed Kahlua VM against test-double world objects. All 25 cases passed: native-fire delegation; powered-stove success; off/unpowered/residually-hot/cold/broken/zero-setting rejection; microwave/toaster/coffeemaker rejection; missing objects, multiple objects/squares and absent arguments. The mains and generator cases both supply the native powered=true result; actual generator coverage is established only by inspecting the power API chain, not by a live generator test.
8. Native bytecode confirms `ItemContainer.isPowered()` delegates to `IsoObject.checkObjectPowered()` and `ItemContainer.isObjectPowered()`. Both object and square power logic include `hasGridPower()` and `haveElectricity()`. `IsoGridSquare.haveElectricity()` delegates to `IsoChunk.isGeneratorPoweringSquare(x,y,z)`, confirming that this is the generator-aware path. The installed oven UI uses this same container power check. The stove's own update checks power; `getCurrentTemperature()` returns `(raw + 100) / 100`, so raw-zero cold is normalized 1. The mod requires normalized warmth above 1 and positive setpoint, as well as on/powered/unbroken state.
9. Native `IsoGridSquare.getRadius(2)` scans a same-floor 3-by-3 neighborhood. It is also used by native `openFire`; the callback preserves that neighborhood. No workstation tags or generator-item requirements are guessed.

The skill's supplemental reference files/bundled validator were unavailable through its resource provider. The project-local validator above provides the reported checks; no claim is made that the unavailable validator ran.

## Source evidence fingerprints

These are SHA-256 fingerprints of inspected installed files. Paths are relative to the game root. The files themselves are not included.

| File | SHA-256 |
| --- | --- |
| projectzomboid.jar | e1a69eb743ede60b213a0fe7f8b83d4fcab773036d256cc4543a336f3b058a33 |
| media/scripts/generated/items/normal.txt | b76cf5f91dce33567ca2bda305c4e450be297aae6b1fc11b5b34dcb280d74567 |
| media/scripts/generated/items/food.txt | 408f2091bca9b1059ff8a8fb067076dcda7412903c84007656334ba6ac662e03 |
| media/scripts/generated/items/drainable.txt | 2fc00391613c83d581b53d1142f4f233f8392b29d8f8702fb1b3516b0c047732 |
| media/scripts/generated/fluids.txt | 444a9f693d51e557ee782ae761558ba6d6d970d49ed3e7bca586d231195e38c7 |
| media/lua/client/ISUI/Fireplace/ISOvenUI.lua | f4810738df267b681362a7b05bdec4aaa421186be8b0ceb897d5b79c848dad00 |
| media/lua/client/ISUI/ISInventoryPaneContextMenu.lua | 4cbbc52cbab591cee0c7d1c5927125bf59c70c588936b04d3ce0fe75648a96cc |

Steam's installed app manifest supplied build 25485521; that manifest and machine paths are not distributed.

## Packaging contract

`python tools/package.py` must create the install archive twice and require identical bytes. Verification checks the explicit member list, single EwingsFoods root, sibling 42/mod.info and common/, stable ordering/timestamps, CRCs, runtime bytes against source and SHA-256 sidecar. ZIP_STORED avoids compressor-version variability. The sidecar is supplied separately to avoid a self-referential checksum.

Version 1.0.1 is prepared and committed locally only. No push, tag or release publication is performed for this update. The package is extracted locally and validated again. If publication is later authorized, compare the remote commit to local HEAD, anonymously download release assets and verify bytes/hash/members against this reviewed local package.

## Runtime limitations

No game/server launch, install, enabled-list edit or save access was performed. Recipe UI discovery, full CraftRecipe registration, selected-container consumption, actual action duration, live mains/generator stove behavior, heat/power loss during a craft, cancellation, food behavior in a world, multiplayer authority and synchronization are unobserved. Native data declarations and structural tests are evidence, not end-to-end certification. See ACCEPTANCE.md for disposable-world checks.

Fluid milk definitions in this build do not expose food-age fields. Exact fluid matching excludes mixtures including tainted/hazardous liquids; native rotten/frozen restrictions are retained where the engine represents those states. This release adds no fluid-aging system.
