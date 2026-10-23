EwingsFoodsNachos = EwingsFoodsNachos or {}

function EwingsFoodsNachos.onCreate(recipeData, character)
    local result = recipeData:getFirstCreatedItem()
    if not result or result:getFullType() ~= "EwingsFoods.LoadedNachos" then return end

    -- Native InheritFoodAge picks an input by absolute age. Different foods have
    -- different shelf lives; retain the oldest relative freshness as well.
    -- copyAgeFrom maps each ingredient to this dish's own freshness thresholds.
    local oldestAge = result:getAge()
    local ingredients = recipeData:getAllConsumedItems()
    for i = 0, ingredients:size() - 1 do
        local ingredient = ingredients:get(i)
        if instanceof(ingredient, "Food") then
            result:copyAgeFrom(ingredient)
            if result:getAge() > oldestAge then oldestAge = result:getAge() end
        end
    end
    result:setAge(oldestAge)
    -- These ingredients are ready to eat. Mark the assembled dish ready for
    -- reheating, avoiding a fresh cooking transition or age reset on reheats.
    result:setCooked(true)
end
