-- Add stove heat to the native fire predicate without replacing any vanilla code.
EwingsFoodsHeat = EwingsFoodsHeat or {}

function EwingsFoodsHeat.canMakeCheese(item, character)
    if not item or not character or not character:getCurrentSquare() then
        return false
    end

    if RecipeCodeOnTest.openFire(item, character) then
        return true
    end

    -- Match the native openFire neighborhood; getRadius(2) is a same-floor 3x3.
    local squares = character:getCurrentSquare():getRadius(2)
    for i = 0, squares:size() - 1 do
        local objects = squares:get(i):getObjects()
        for j = 0, objects:size() - 1 do
            local object = objects:get(j)
            if instanceof(object, "IsoStove") and not object:isMicrowave()
                and not object:isBroken() and object:Activated() then
                local container = object:getContainer()
                -- isStove() also includes toasters/coffeemakers in this build.
                if container and container:getType() == "stove" and container:isPowered()
                    and object:getMaxTemperature() > 0 and object:getCurrentTemperature() > 1 then
                    return true
                end
            end
        end
    end
    return false
end
