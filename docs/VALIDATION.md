# Validation evidence - 1.1.0

Target: installed PZ 42.21 / Steam build 25485521 on Windows. These are development/offline results; publication and installation are recorded separately. No game launch/stop, screen control or save/settings edit was performed. Development did not modify the installed mod.

## New nachos results

- Three scripts pass installed native structural ScriptParser checks. The new recipe/item IDs, actual ingredient IDs, food-use quantities, one consumed plate, retained knife, one output, English name/tooltip, native flags, model reference and all selected properties are checked. Nutrition totals equal the exact selected portions to rounding. Four existing cheese/paste runtime files match their baseline SHA-256 hashes.
- Native food references, plate variants, generated recipe definitions and container-return examples were inspected. The generated recipes include a ClayPlate kiln output; EatType Plate occurs on foods actually returning pans/vessels and is not proof that Base.Plate is a native preparation ingredient. Standard Plate was selected deliberately; ClayPlate is excluded to preserve exact return type.
- Installed bytecode confirms OnCreate receives recipe data and character; used recipe-data, age-copy and cooked-state APIs exist; native raw/rotten/frozen guards, partial-food scaling and depleted-food replacement paths exist. Ready-to-eat/alreadycooked and hidecooked tags match native bread/toast patterns. No new OnEat or OnCooked callback, inventory insertion, age-reset or global override exists.
- **14 native food instruction cases** execute the actual installed mood/hunger/calorie getter bytecode against field/method doubles. They establish strict normalized heat >1.3, two-point hot unhappiness bonus, cooling removal, cooked/cookable requirements, stale-food modifiers and identical hunger/calories at cold/hot temperatures. **5 native age-copy instruction cases** verify installed relative-age mapping. The tiny interpreter reads installed code at validation time; no extracted bytecode/source is distributed, and no world is booted.
- **11 isolated Kahlua OnCreate cases** exercise actual mod code: fresh/stale inputs, worst relative age despite absolute-age ordering, reverse ordering, preserving older inherited age, nonfood plate/tools, nonaging packaged chips, output scope/readiness and no portion/nutrition mutation.
- **4 installed eating Lua spy cases** execute actual native eat/complete functions against a character spy, checking selected half-portion progress, almost-complete action scaling, half completion and full completion. This does not execute actual inventory mutation. Native full/depleted UseAndSync and partial multiplyFoodValues/replacement references are separately inspected.
- Original icon was built and visually inspected at 32x32 on light/dark backgrounds. Its canvas matches installed Item_Plate and Item_CornChips metadata. Dimensions, RGBA alpha, transparent corners, visible area and margins pass. The 3D hand/world reference remains the native plain plate mesh; toppings are visible in the icon.
- Existing **25 heat + 22 tomato + 3 native handcraft spy cases** pass unchanged in behavior. They are 50 unique cases; repeated heat-harness execution is not counted again. New nachos cases total 34, giving 84 unique isolated/instruction cases overall.

## Limits and acceptance

No full game recipe registration, UI rendering, actual inventory return/consumption/plate condition, partial eating, preparation cancellation, live appliance warming/cooling/burning, storage/save/reload or multiplayer has been observed. Those remain explicitly pending in ACCEPTANCE.md. A cancelled eating action can retain the native already-eaten fraction; no free-undo guarantee is made. Native ReplaceOnUse returns a plate on depletion, not a custom identity-preserving plate object.

Both install/source archives are built twice with fixed timestamps, stable ordering, explicit allowlists and SHA-256 sidecars, then verified against reviewed source. The extracted install archive is validated separately. No game source, texturepack pixels, binaries, logs, .validation files or credentials are distributed. Source includes only original mod art and tooling. The prior skill supplemental references/standard validator remained unavailable; these are project-local checks.

## Inherited 1.0.2 investigation

The following retained evidence describes the earlier two-recipe baseline; the new custom food/lifecycle differences are documented above and in NACHOS.md.

### 1.0.2 baseline

Date: 2026-10-23. Target: Windows, Project Zomboid 42.21, Steam build 25485521. Mod ID: EwingsFoods. Dependencies: none.

## Observed offline results

`python tools/validate.py --game-root <installation>` passed the ingredient/recipe checks, native structural syntax check, installed API checks and isolated Lua heat regressions:

1. Version/layout, exactly two additive recipes, their translated names, ingredients, tools, quantities, skill/XP and output contract.
2. All seven explicit item references and both milk fluid IDs resolve in installed definitions. Both pots hold the batch. Cheesecloth exists. Vinegar charge and salt food-use definitions match the documented units. Vanilla cheese keeps pizza support and its original stats.
3. Installed JAR inspection reconfirms 42.21 (Core's GameVersion initialization), default Exact fluid matching, the native rotten-food test, the openFire callback signature and source classes, the IsEmpty flag and every selected recipe property.
4. Fluid input binding/retention syntax matches installed DisinfectBandage; exact cow/sheep milk syntax matches MakeBowlOfCereal; heat callback matches FireHardenSpear. This is evidence about supported contracts, not copied game content in this release.
5. An original generated Java bridge called the installed ScriptParser.stripComments and ScriptParser.parse successfully on both mod scripts. It never invokes a game/client/server entry point. This checks structural syntax; it does not perform full world/runtime recipe registration.
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

Both 1.0.2 install and source ZIPs use separate explicit allowlists, fixed timestamps and stable ordering; each is built twice and compared byte-for-byte. The install root is EwingsFoods with 42/mod.info and common/. The source ZIP contains development tools and no .validation output, game code/assets, logs, profile paths or credentials. The install ZIP is extracted and validated again; source bytes are compared to the reviewed stage. Publication verification must compare commit/tag to remote main and anonymously downloaded asset hashes. Distribution checks do not establish gameplay or multiplayer compatibility.

## Runtime limitations

No game/server launch, install, enabled-list edit or save access was performed. Recipe UI discovery, full CraftRecipe registration, selected-container consumption, actual action duration, live mains/generator stove behavior, heat/power loss during a craft, cancellation, food behavior in a world, multiplayer authority and synchronization are unobserved. Native data declarations and structural tests are evidence, not end-to-end certification. See ACCEPTANCE.md for disposable-world checks.

Fluid milk definitions in this build do not expose food-age fields. Exact fluid matching excludes mixtures including tainted/hazardous liquids; native rotten/frozen restrictions are retained where the engine represents those states. This release adds no fluid-aging system.

## Tomato paste checks observed offline

- `Base.Tomato` and `Base.TomatoPaste` resolve in installed food definitions. The sole paste item is packaged, nonperishable, cannot freeze, has no opening variant or empty-container replacement, and already has pizza-sauce and evolved-recipe support. Its nutrition is untouched. Nine 14-calorie tomatoes provide 126 calories for one 120-calorie paste. Its 8 g fat macro is a retained vanilla inconsistency, not an added oil ingredient.
- Recipe contract checks require exactly nine native item-count tomatoes with mode:destroy and IsWholeFoodItem/IsUncookedFoodItem, three retained tools, one existing paste output, Cooking 1/time 1200/5 XP, matching English translations and no custom lifecycle/item definitions. Cheese script and heat helper hashes match the 1.0.1 baseline exactly (BASELINE.md).
- Native InputFlag values and InputScript food checks resolve. Installed bytecode confirms that whole-food checks compare original food/nutritional values, uncooked checks use Food:isUncooked(), and native rotten/frozen guards remain enabled. InputScript IsFull is for other item/container state and is not used to assume that a food portion is whole. Native per-item OnTest is reached by CraftRecipeManager.consumeInputItemInternal and receives candidate item plus character. Food:isFresh compares age strictly below offAge, rejecting stale at the boundary (Tomato: 4 fresh days, 12 to fully rotten).
- Both actual shared Lua callbacks compile/execute in the installed Kahlua VM against doubles. All **25 heat cases**, **22 tomato freshness/tool/heat cases** and **3 native lifecycle spy scenarios** pass. The heat harness is also rerun while composing the tomato harness; this repeat is not an additional 25 unique cases. Tomato cases include stale/rotten/frozen/burnt/wrong class, retained non-food tools without food methods, missing arguments, native fire, powered and failed stove conditions. Mains/generator are the same powered=true API double; no live generator was used.
- The installed ISHandcraftAction stop and performRecipe functions are read at validation time into a private generated harness (never included in either ZIP). Spies confirm cancellation does not call perform/consume/output, failed native perform does not deliver or consume, and one successful native perform delivers one output and processes consumption once, recording nine tomatoes. This tests Lua orchestration, not actual CraftRecipeManager inventory transactions. Native destroy/keep/UseItem paths were inspected separately. Mode:keep and absence of degradation flags preserve tools by declaration; in-world identity/condition and partial-food selection remain gameplay acceptance checks.
- There are no custom OnStart, OnTick, OnCreate, output mutation, inventory insertion, per-frame polling, container rewards or global overrides. The native engine owns item selection, completion, consumption and cancellation. Continuous heat tracking is not introduced; changes in power, range or freshness during an action still require an actual gameplay check.

## Execution boundaries

No game/server was launched or stopped, screen controlled, mod installed, or saves/settings accessed. Local source and installed mod fingerprints were checked independently. Static bytecode/definition inspection, structural ScriptParser checks and isolated Kahlua execution are the only behavior evidence. Full CraftRecipe registration, UI discovery, actual duration, live appliance behavior, inventory consumption/retention, repeated batches, mid-action changes, save/reload and multiplayer remain unobserved. See ACCEPTANCE.md.

The skill's supplemental references/standard validator could not be read through its provider, as in the baseline; the original project-local validator is the one actually run. A helper to discover bundled workspace dependencies was unsupported for this delegated environment; the already-installed Python runtime and game JVM were located directly. Neither limitation blocked implementation or tests.
