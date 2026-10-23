# Loaded nachos - 1.1.0

Target: Windows, PZ 42.21, Steam build 25485521. Existing cheese and tomato-paste runtime files are preserved byte-for-byte from published 1.0.2.

## Prepare one plate

Find **Make Loaded Nachos (Ewing's Foods)** under Cooking. Requires Cooking 1 and a sharp knife/meat cleaver (native tags, not dull), which is kept without recipe-added wear. No fire or stove is required to assemble safe, ready-to-eat ingredients. Preparation time is 80 native recipe units, before engine modifiers; 3 Cooking XP.

| Input | Consumed per plate |
| --- | --- |
| `Base.TortillaChips` | 1 full packaged bag (15 native hunger-use units) |
| `Base.Cheese` | 5 native food-use units, one third of a full cheese |
| `Base.Tomato` | 6 units, half a normal raw tomato |
| `Base.PepperJalapeno` | 1 unit, half a normal raw fresh jalapeno |
| `Base.Onion` | 3 units, three tenths of a normal raw onion |
| `Base.Plate` | 1 standard plate, incorporated into the food |
| Output | 1 `EwingsFoods.LoadedNachos` |

Native food-use units are hunger units, not item counts. Sufficient partial cheese/vegetables can be used and remaining portions stay under native rules. Chips must be a whole bag. Vegetables must be uncooked; native rotten/frozen restrictions remain enabled. Stale ingredients are allowed but their relative age carries over conservatively. No new empty bags, plates or other containers are emitted during preparation. Cancelling preparation uses the native handcraft cancellation path.

The installed build also has `Base.TortillaChipsBaked` from cutting a tortilla, dried jalapenos, habaneros, potato crisps and `Base.ClayPlate`. This deliberately uses the packaged tortilla chips and fresh jalapeno requested, and only the standard plate so the eventual return type is exact. Clay plates are not upgraded or exchanged. A full scan of generated recipe scripts found a kiln recipe producing ClayPlate, but no Base.Plate food-preparation reference. Existing foods use `EatType = Plate` as an eating animation while actually returning pans or other vessels; that field alone does not mean a recipe consumes a dinner plate.

## Warm, eat and store

The dish is ready to eat cold and marked cooked using the same supported already-cooked tag pattern as native bread/toast. Place it in a normal working heated appliance or supported fire container to warm it, using the game's ordinary food-heating behavior. A powered stove can use mains or generator electricity. The new preparation recipe itself does not check heat or borrow the cheese recipe's nearby-heat gate. Do not leave the food cooking indefinitely: it is cookable and burns at the selected native 20-minute cooking-time threshold. Actual elapsed heating/burning time has not been measured.

For a fresh full dish, base unhappiness change is **-5 cold and -7 hot**: native `GoodHot` subtracts 2 when the item is cookable, cooked and normalized food heat is strictly above 1.3. The bonus disappears as it cools. No BadCold penalty is added. Boredom is -5 at either temperature. The engine scales eating effects to the portion consumed and applies native spoilage/burning effects. Native heat values are not Celsius or food-safety guidance.

Nutrition is the sum of the selected vanilla portions, rounded to three decimals: **480.567 calories, 46.002 carbohydrate, 43.336 fat, 5.514 protein**. These inherit vanilla's numerical inconsistencies; no real-world nutrition claim is made. Heating changes none of these. Script hunger is -25; native cooked-food handling makes a fresh dish approximately -32.5 hunger at either temperature. Item weight 1.5 includes the native 1.0-weight plate and approximately 0.5 food.

Native `ReplaceOnUse = Base.Plate` returns exactly one standard plate when the food is fully depleted. Partial eating retains the plated food and returns no plate. No OnEat callback, extra inventory insertion, parallel empty-plate output or custom plate counter is added. A cancelled eating action can consume the fraction already eaten under native behavior; it is not promised to be a free undo. Actual inventory replacement and partial eating still need gameplay validation.

Shelf life is 3 fresh days / 5 days to fully rotten at normal game rates, affected by native storage/sandbox settings. Native InheritFoodAge is retained, and a narrow OnCreate callback takes the oldest mapped freshness across all consumed food inputs so a younger absolute-age vegetable cannot be hidden behind an older but slower-spoiling cheese. It never lowers the inherited age or changes nutrition/portions. The food is already cooked before reheating, preventing repeat cooking-age transitions. There is no custom OnCooked callback, replacement recipe, reheating recipe or age reset.

## Visuals and removal

The 32x32 transparent icon is original generated art, visually checked at actual size on light/dark backgrounds; see ART.md. The standard native plate mesh is referenced for hand/world models, so the 3D model is a plain plate; toppings are represented by the original inventory/equipped-slot icon. No extracted native mesh, texture or code is distributed.

Unlike the prior vanilla-only outputs, this is a custom saved item. Removing 1.1.0 while loaded nachos still exist can remove/strand that item and its incorporated plate. Eat or otherwise resolve them and back up the world before removing the mod. No save migration was attempted. Build and publication do not install this update. Gameplay validation remains pending; use the acceptance checklist before relying on runtime behavior.
