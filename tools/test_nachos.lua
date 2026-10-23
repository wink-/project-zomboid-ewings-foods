-- The production onCreate is inserted by the runner. No world is constructed.
local function assert(value, message) if not value then error(message) end end
local math={abs=function(value) if value<0 then return -value end return value end}
function instanceof(item, class) return item.class == class end
local function list(values)
    return {size=function() return #values end,get=function(self,i) return values[i+1] end}
end
local function ingredient(age, fresh)
    return {class='Food', age=age, fresh=fresh}
end
local function result(initial)
    return {age=initial or 0,cooked=false,
        getFullType=function() return 'EwingsFoods.LoadedNachos' end,
        getAge=function(self) return self.age end,
        setAge=function(self,age) self.age=age end,
        setCooked=function(self,value) self.cooked=value end,
        copyAgeFrom=function(self,source)
            -- This test double maps nonrotten ingredient age by freshness.
            -- The native implementation is separately executed by native_food_vm.
            if source.fresh then self.age=source.age/source.fresh*3 end
        end,
    }
end
local function data(output,inputs)
    return {getFirstCreatedItem=function() return output end,
            getAllConsumedItems=function() return list(inputs) end}
end
-- INSERT_NACHOS_SOURCE
local count=0
local function test(label,output,inputs,age)
    EwingsFoodsNachos.onCreate(data(output,inputs),{})
    assert(math.abs(output.age-age)<0.00001,label)
    assert(output.cooked,'ready-to-eat flag: '..label)
    count=count+1
end
test('fresh ingredients',result(),{ingredient(0,14),ingredient(0,4)},0)
test('relative age beats absolute age',result(),{ingredient(7,14),ingredient(3.6,4)},2.7)
test('reverse input order cannot freshen',result(),{ingredient(3.6,4),ingredient(7,14)},2.7)
test('stale ingredient stays stale',result(),{ingredient(4.4,4),ingredient(1,14)},3.3)
test('preexisting native inherited age never lowered',result(4),{ingredient(1,14)},4)
test('plate and knife are not food',result(),{{class='InventoryItem'},{class='InventoryItem'},ingredient(2,4)},1.5)
test('packaged chips with no aging do not reset age',result(),{ingredient(3,4),ingredient(0,nil)},2.25)
test('only nonfood inputs preserves age',result(1),{{class='InventoryItem'}},1)
local partial=result(2.5);partial.portion=0.5;partial.calories=240.2835
test('callback cannot alter portion/nutrition',partial,{ingredient(1,14)},2.5)
assert(partial.portion==0.5 and partial.calories==240.2835,'no nutrition/portion mutation')
EwingsFoodsNachos.onCreate(data(nil,{}),{})
count=count+1
local wrong={getFullType=function() return 'Base.Cheese' end}
EwingsFoodsNachos.onCreate(data(wrong,{}),{})
count=count+1
print('PASS '..count..' isolated nachos callback age/readiness/output-scope cases')

-- Actual installed native eating Lua methods are inserted, with a character spy.
ISEatFoodAction={}
local eaten={}
local character={Eat=function(self,item,fraction,utensil) eaten[#eaten+1]={item,fraction,utensil} end}
local meal={getFullType=function() return 'EwingsFoods.LoadedNachos' end,
            getHungerChange=function() return -0.325 end,getBaseHunger=function() return -0.25 end}
local action={character=character,item=meal,percentage=0.5,useUtensil=false}
-- INSERT_NATIVE_EATING
ISEatFoodAction.eat(action,meal,0.5)
assert(#eaten==1 and eaten[1][2]==0.25,'partial progress multiplies selected portion')
ISEatFoodAction.eat(action,meal,0.97)
assert(#eaten==2 and eaten[2][2]==0.5,'almost completed action finishes selected half, not entire plate')
assert(ISEatFoodAction.complete(action)==true,'native complete return')
assert(#eaten==3 and eaten[3][2]==0.5,'complete passes half portion to native Eat')
action.percentage=1
ISEatFoodAction.complete(action)
assert(#eaten==4 and eaten[4][2]==1,'full consumption passes full fraction to native Eat')
print('PASS 4 isolated installed eating Lua portion/complete spy cases; actual inventory replacement remains untested')
