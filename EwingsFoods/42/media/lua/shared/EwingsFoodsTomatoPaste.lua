require "EwingsFoodsHeat"

EwingsFoodsTomatoPaste = EwingsFoodsTomatoPaste or {}

-- OnTest is evaluated for each candidate input, including retained tools.
-- Whole/raw portions are enforced by native input flags; freshness is stricter
-- than the native rotten-food exclusion and must only apply to tomatoes.
function EwingsFoodsTomatoPaste.canMake(item, character)
    if not item then return false end
    if item:getFullType() == "Base.Tomato" then
        if not instanceof(item, "Food") or not item:isFresh()
            or item:isRotten() or item:isFrozen() or item:isBurnt() then
            return false
        end
    end
    -- Preserve the existing cheese recipe and its tested native-fire/stove gate.
    return EwingsFoodsHeat.canMakeCheese(item, character)
end
