# Runtime acceptance checks — pending

These checks have not been run. Use a disposable world with only EwingsFoods enabled, and test the same mod version on a separate test server/client before multiplayer use. Do not use a valuable save to discover compatibility.

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
| Heat | Accept native-supported lit campfire/fireplace/barbecue nearby; reject cold/out-of-range source and kitchen stove alone |
| Interrupted action | No free output or duplicate consumption after cancel, moving away or losing heat; inspect native timing behavior |
| Repeated crafting | Each completion consumes exactly one batch; tools persist |
| Vanilla food | Cheese retains vanilla nutrition, freshness, spoilage and pizza use |
| Save/reload/removal | Crafted cheese remains vanilla; recipe disappears after disabling mod |
| Multiplayer | Server authoritative result; matching client/server inventories after craft, cancel, reconnect and simultaneous attempts |

If a check fails, preserve the reproduction and inspect the exact current build before changing native behavior. Avoid publishing a runtime-verified claim until these checks are observed.
