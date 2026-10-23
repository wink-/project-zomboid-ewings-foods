# Runtime acceptance checks — pending

These gameplay checks have not been run for 1.0.2. Static and isolated Lua checks are recorded separately in VALIDATION.md. Use a disposable world with only EwingsFoods enabled, and test the same mod version on a separate test server/client before multiplayer use. Do not use a valuable save to discover compatibility.

| Check | Expected result |
| --- | --- |
| Crafting registration | Cooking shows Make Cheese (Ewing's Foods), correct quantities and Cooking 1 |
| Valid batch | One native cheese appears; exactly 1 L milk, one vinegar charge and one salt use are consumed |
| Reusables | Empty pot, cloth and milk vessel remain; no duplicate containers |
| Last vinegar charge | Native vinegar packaging is removed; no refillable container is promised |
| Sheep milk | Same output and quantities as cow milk |
| Short inputs | No cheese with <1 L milk, missing acid/salt/pot/cloth, or Cooking 0 |
| Invalid milk | Reject water, tainted water, hazardous/diluted/chocolate milk and mixed cow/sheep milk |
| Bad food | Reject rotten/frozen food items if the engine can supply such input states; no fluid-age state is invented |
| Heat | Accept native-supported lit campfire/fireplace/barbecue nearby; reject cold/out-of-range fire sources; powered, switched-on and warmed ordinary stoves now qualify |
| Mains stove | On, unbroken ordinary stove with positive setting and warmth works with normal grid electricity, with no generator nearby |
| Generator stove | After mains shutoff, a fueled/running generator supplying the stove permits the same one-action recipe |
| Stove failures | Off, unpowered (including hot residual), cold, zero-setting, broken, out-of-range and other-floor stoves fail |
| Other appliances | Microwaves, toasters and coffeemakers fail |
| Power loss mid-craft | Test generator shutdown, fuel exhaustion, stove switch-off and movement during craft; check native revalidation/cancellation and inventory consistency |
| Interrupted action | No free output or duplicate consumption after cancel, moving away or losing heat; inspect native timing behavior |
| Repeated crafting | Each completion consumes exactly one batch; tools persist |
| Vanilla food | Cheese retains vanilla nutrition, freshness, spoilage and pizza use |
| Save/reload/removal | Crafted cheese remains vanilla; recipe disappears after disabling mod |
| Multiplayer | Server authoritative result; matching client/server inventories after craft, cancel, reconnect and simultaneous attempts |

If a check fails, preserve the reproduction and inspect the exact current build before changing native behavior. Avoid publishing a runtime-verified claim until these checks are observed.

## Tomato paste acceptance - pending actual gameplay

| Check | Expected result |
| --- | --- |
| Registration | Exactly one Make Tomato Paste (Ewing's Foods), alongside unchanged Make Cheese; Cooking 1, nine tomatoes, time 1200 |
| Valid batch | Nine full fresh raw thawed tomatoes consumed; one Base.TomatoPaste appears; no other output |
| Tools | Test Pot and PotForged; empty pot, knife and spoon/mixing utensil keep item identity, condition and quantities |
| Missing requirements | Eight tomatoes, Cooking 0, missing/dull knife, missing stirrer, missing/full pot block crafting |
| Freshness boundary | Native Fresh tomatoes pass; stale at fresh-age boundary, rotten, frozen, burnt, cooked and partly eaten/used tomatoes fail |
| Mixed stock | With eight fresh and one stale tomato there is no batch; with nine fresh plus bad leftovers only the nine valid tomatoes are selected; repeat manual and automatic selection |
| Container exploit | No empty can, jar, lid, duplicate pot or other free container after crafting or eating/using all paste |
| Native food | Same 120 calories, 0.2 weight, -15 hunger and packaged/nonperishable behavior as looted paste; pizza and evolved recipes accept it without opening |
| Heat success | Repeat with lit campfire/fireplace/barbecue, active warm mains stove, then generator-powered stove after mains shutoff |
| Heat failure | Off, cold, broken, zero-setting, unpowered/residually-hot stove; microwave/toaster/coffeemaker; heat outside same-floor 3x3 all fail |
| Cancel | Cancel early and late; no paste and no consumed tomatoes; tool counts and identities unchanged |
| Mid-action changes | Move away, remove a tool/tomato, turn off stove, stop generator/exhaust fuel, and age across fresh boundary; record native revalidation and inventory behavior |
| Repeated batches | 18 fresh tomatoes make exactly two pastes, reusing the same three tools |
| Cheese regression | Repeat the cheese cases above on both fire and mains/generator stove |
| Save/reload/MP | Vanilla output survives reload/removal; separately test identical server/client versions, simultaneous crafts, cancel/reconnect and authoritative consumption |

The Lua spy tests check the installed stop/performRecipe call flow only; they do not establish any of these actual inventory/world outcomes. Continuous heat tracking or custom transaction handling is not introduced.
