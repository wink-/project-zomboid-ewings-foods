-- Minimal assert: the game normally supplies it from its standard Lua library.
local function assert(condition, message)
    if not condition then error(message) end
    return condition
end
-- Test doubles for world objects; the production callback is inserted below.
local fire = false
local calls = 0
RecipeCodeOnTest = {openFire = function(item, character)
    calls = calls + 1
    return fire
end}
function instanceof(object, class) return object.class == class end
local function list(values)
    return {size = function() return #values end, get = function(self, index) return values[index + 1] end}
end
local function stove(options)
    options = options or {}
    local container = {
        getType = function() return options.kind or "stove" end,
        isPowered = function() return options.power ~= false end,
    }
    return {
        class = options.class or "IsoStove",
        isMicrowave = function() return options.microwave or false end,
        isBroken = function() return options.broken or false end,
        Activated = function() return options.on ~= false end,
        getContainer = function() if options.noContainer then return nil end return container end,
        getMaxTemperature = function() return options.setpoint or 100 end,
        getCurrentTemperature = function() return options.temperature or 1.5 end,
    }
end
local squares = {}
local radius
local origin = {getRadius = function(self, value) radius = value return list(squares) end}
local character = {getCurrentSquare = function() return origin end}
local item = {}
local function world(objects)
    squares = {{getObjects = function() return list(objects) end}}
end
-- INSERT_MOD_SOURCE
local count = 0
local function expect(label, expected)
    local actual = EwingsFoodsHeat.canMakeCheese(item, character)
    assert(actual == expected, label)
    count = count + 1
end
world({stove()})
expect("mains-powered stove", true)
expect("generator-powered stove (same native powered=true API)", true)
assert(radius == 2, "match native openFire neighborhood")
world({stove({on=false})}); expect("powered but off", false)
world({stove({power=false})}); expect("unpowered but activated", false)
world({stove({power=false,temperature=3})}); expect("unpowered residual heat", false)
world({stove({temperature=1})}); expect("cold powered stove", false)
world({stove({temperature=0.8})}); expect("below cold baseline", false)
world({stove({setpoint=0})}); expect("zero heating setting despite residual heat", false)
world({stove({broken=true})}); expect("broken stove", false)
world({stove({microwave=true})}); expect("microwave excluded", false)
world({stove({kind="toaster"})}); expect("toaster excluded", false)
world({stove({kind="coffeemaker"})}); expect("coffeemaker excluded", false)
world({stove({noContainer=true})}); expect("missing container", false)
world({stove({class="IsoObject"})}); expect("non-stove object", false)
world({}); expect("no nearby source", false)
squares = {}; expect("no loaded nearby squares", false)
world({stove({on=false}),stove()}); expect("second object can supply heat", true)
squares = {{getObjects=function() return list({stove({power=false})}) end},
           {getObjects=function() return list({stove()}) end}}
expect("later square can supply heat", true)
-- No matching stove: success must come only from the existing native predicate.
world({stove({power=false})});fire=true
expect("native lit campfire accepted", true)
expect("native lit fireplace accepted", true)
expect("native lit barbecue accepted", true)
fire=false; expect("native fire unavailable with no valid stove", false)
assert(EwingsFoodsHeat.canMakeCheese(nil, character) == false,"missing item")
assert(EwingsFoodsHeat.canMakeCheese(item, nil) == false,"missing character")
assert(EwingsFoodsHeat.canMakeCheese(item, {getCurrentSquare=function() return nil end}) == false,"missing square")
count = count + 3
assert(calls >= 22,"native fire predicate remains in every ordinary heat check")
print("PASS " .. count .. " isolated Lua heat regression cases")
