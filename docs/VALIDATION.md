# Validation evidence — 1.0.0

Date: 2026-10-22. Target: Windows, Project Zomboid 42.21, Steam build 25485521. Mod ID: EwingsFoods. Dependencies: none.

## Observed offline results

`python tools/validate.py --game-root <installation>` passed all six check groups:

1. Version/layout, exactly one additive recipe, its translated name, ingredients, tools, quantities, skill/XP and output contract.
2. All seven explicit item references and both milk fluid IDs resolve in installed definitions. Both pots hold the batch. Cheesecloth exists. Vinegar charge and salt food-use definitions match the documented units. Vanilla cheese keeps pizza support and its original stats.
3. Installed JAR inspection confirms 42.21 (Core's GameVersion initialization), default Exact fluid matching, the native rotten-food test, the openFire callback signature and source classes, the IsEmpty flag and every selected recipe property.
4. Fluid input binding/retention syntax matches installed DisinfectBandage; exact cow/sheep milk syntax matches MakeBowlOfCereal; heat callback matches FireHardenSpear. This is evidence about supported contracts, not copied game content in this release.
5. An original generated Java bridge called the installed ScriptParser.stripComments and ScriptParser.parse successfully on the mod script. It never invokes a game/client/server entry point. This checks structural syntax; it does not perform full world/runtime recipe registration.
6. No Lua overrides, permissive rotten/frozen flags, mixture matching, item definitions or inherited food mutations are included.

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

Steam's installed app manifest supplied build 25485521; that manifest and machine paths are not distributed.

## Packaging contract

`python tools/package.py` must create the install archive twice and require identical bytes. Verification checks the explicit member list, single EwingsFoods root, sibling 42/mod.info and common/, stable ordering/timestamps, CRCs, runtime bytes against source and SHA-256 sidecar. ZIP_STORED avoids compressor-version variability. The sidecar is supplied separately to avoid a self-referential checksum.

Remote publication verification is recorded with the release: compare remote commit to local HEAD, download release assets anonymously, verify bytes/hash/members against the reviewed local package, then run the same definition/native structural checks against an extracted copy. No credentials are sent to release-asset hosts.

## Runtime limitations

No game/server launch, install, enabled-list edit or save access was performed. Recipe UI discovery, full CraftRecipe registration, selected-container consumption, actual action duration, heat loss during a craft, cancellation, food behavior in a world, multiplayer authority and synchronization are unobserved. Native data declarations and structural tests are evidence, not end-to-end certification. See ACCEPTANCE.md for disposable-world checks.

Fluid milk definitions in this build do not expose food-age fields. Exact fluid matching excludes mixtures including tainted/hazardous liquids; native rotten/frozen restrictions are retained where the engine represents those states. This release adds no fluid-aging system.
