-- Appended to the existing isolated heat harness. Engine objects are doubles.
local function tomato(options)
    options = options or {}
    return {
        class = options.class or "Food",
        getFullType = function() return "Base.Tomato" end,
        isFresh = function() return options.fresh ~= false end,
        isRotten = function() return options.rotten or false end,
        isFrozen = function() return options.frozen or false end,
        isBurnt = function() return options.burnt or false end,
    }
end
local tool = {getFullType=function() return "Base.Pot" end}
local pasteCount = 0
local function paste(label, candidate, expected, who)
    assert(EwingsFoodsTomatoPaste.canMake(candidate, who or character) == expected, label)
    pasteCount = pasteCount + 1
end
fire = false
world({stove()})
paste("fresh tomato / mains stove", tomato(), true)
paste("fresh tomato / generator powered=true path", tomato(), true)
paste("retained pot has no food API", tool, true)
paste("stale tomato rejected", tomato({fresh=false}), false)
paste("rotten tomato rejected", tomato({fresh=false,rotten=true}), false)
paste("inconsistent rotten state rejected", tomato({rotten=true}), false)
paste("frozen tomato rejected", tomato({frozen=true}), false)
paste("burnt tomato rejected", tomato({burnt=true}), false)
paste("wrong runtime item class rejected", tomato({class="InventoryItem"}), false)
paste("missing item", nil, false)
assert(EwingsFoodsTomatoPaste.canMake(tomato(), nil) == false, "missing character")
pasteCount = pasteCount + 1
paste("missing square", tomato(), false, {getCurrentSquare=function() return nil end})
world({stove({power=false})})
paste("power lost before predicate evaluation", tomato(), false)
world({stove({on=false})})
paste("stove switched off", tomato(), false)
world({stove({temperature=1})})
paste("stove cold", tomato(), false)
world({stove({microwave=true})})
paste("microwave", tomato(), false)
world({stove({kind="toaster"})})
paste("toaster", tomato(), false)
world({stove({broken=true})})
paste("broken stove", tomato(), false)
world({})
paste("no heat", tomato(), false)
fire = true
paste("native open fire", tomato(), true)
paste("native fire does not rescue stale food", tomato({fresh=false}), false)
paste("knife tool at native fire", {getFullType=function() return "Base.KitchenKnife" end}, true)
assert(radius == 2, "same-floor 3x3 neighborhood unchanged")
print("PASS " .. pasteCount .. " isolated tomato freshness/tool/heat cases")

-- Exercise actual installed stop/performRecipe functions with lifecycle spies.
ISHandcraftAction = {}
local stopped, cancelled, completed = 0, 0, 0
ISBaseTimedAction = {stop=function() stopped=stopped+1 end}
ArrayList = {new=function()
    local values = {}
    return {size=function() return #values end,
            get=function(self, i) return values[i+1] end,
            add=function(self, value) values[#values+1]=value end}
end}
local delivered, consumed, created, performed = 0, 0, 0, 0
Actions = {addOrDropItem=function() delivered=delivered+1 end}
local success = true
local outputData = {}
local output = {getModData=function() return outputData end}
local used = {}
for i=1,9 do used[i]=tomato() end
local data = {
    luaCallOnCreate=function() created=created+1 end,
    processDestroyAndUsedItems=function() consumed=consumed+1 end,
    getAllConsumedItems=function() return list(used) end,
}
local action = {
    character=character,
    clearItemsProgressBar=function() end,
    onCancelFunc=function() cancelled=cancelled+1 end,
    onCompleteFunc=function() completed=completed+1 end,
    logic={performCurrentRecipe=function() performed=performed+1 return success end,
           getCreatedOutputItems=function(self, items) items:add(output) end,
           getRecipeData=function() return data end},
}
-- INSERT_NATIVE_LIFECYCLE
ISHandcraftAction.stop(action)
assert(stopped==1 and cancelled==1 and completed==1, "native stop callbacks")
assert(performed==0 and delivered==0 and consumed==0 and created==0,
       "cancel path never performs recipe, adds output or processes ingredients")
success=false
ISHandcraftAction.performRecipe(action)
assert(performed==1 and delivered==0 and consumed==0 and created==0, "failed native perform has no output/consume calls")
success=true
ISHandcraftAction.performRecipe(action)
assert(performed==2 and delivered==1 and consumed==1 and created==1, "one successful native perform delivers and consumes once")
assert(outputData["Base.Tomato"]==9, "native output provenance records nine consumed tomatoes")
print("PASS 3 isolated native lifecycle spy scenarios: cancel, failed perform, successful perform")
