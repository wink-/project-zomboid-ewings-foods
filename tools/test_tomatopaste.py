"""Focused installed-contract and actual Lua tests; no world or inventory simulation."""
from pathlib import Path
import hashlib, os, re, subprocess, zipfile
from classfile import Class
from test_heat import emit_runner
from validate import block, native_parser_bridge

ROOT = Path(__file__).resolve().parents[1]


def check(game, mod):
    recipe = mod / '42/media/scripts/ewingsfoods_tomatopaste.txt'
    text = recipe.read_text('utf-8-sig')
    assert len(list((mod/'42/media/scripts').glob('*.txt'))) == 3
    assert text.count('craftRecipe ') == 1 and 'module EwingsFoods' in text
    assert 'craftRecipe EwingsFoods_MakeTomatoPaste' in text
    assert not re.search(r'\bitem\s+[A-Za-z_]', text), 'no replacement/new item definition'
    assert [s.strip() for s in re.findall(r'^\s*item\s+[^\n]+', text, re.M)] == [
        'item 1 [Base.Pot;Base.PotForged] mode:keep flags[IsEmpty],',
        'item 1 tags[base:sharpknife;base:meatcleaver] mode:keep flags[IsNotDull],',
        'item 1 tags[base:mixingutensil;base:spoon] mode:keep,',
        'item 9 [Base.Tomato] mode:destroy flags[ItemCount;IsWholeFoodItem;IsUncookedFoodItem],',
        'item 1 Base.TomatoPaste,',
    ]
    props = dict(re.findall(r'^\s*(\w+)\s*=\s*([^,\n]+),', text, re.M))
    assert props == dict(timedAction='Making', time='1200', Tags='InHandCraft;Cooking;CanBeDoneInDark',
                         category='Cooking', SkillRequired='Cooking:1', xpAward='Cooking:5',
                         OnTest='EwingsFoodsTomatoPaste.canMake', Tooltip='Tooltip_EwingsFoods_TomatoPaste')
    for forbidden in ['OnCreate', 'OnStart', 'OnTick', 'AllowRottenItem', 'AllowFrozenItem', 'InheritFood', 'Base.TinCanEmpty']:
        assert forbidden not in text
    # Frozen baseline hashes prevent unnoticed cheese regression even in a detached stage.
    for rel, expected in {
        '42/media/scripts/ewingsfoods_cheese.txt': 'a30c8a1bcab17ac23a2b8d00eea4faae267e1db64028ecadaf2afd01abd69999',
        '42/media/lua/shared/EwingsFoodsHeat.lua': 'b0687ca6f5a3a7f946210a2e72f1ac6538ef9851c3c9575f3cf6e0c4b32578d0',
    }.items():
        assert hashlib.sha256((mod/rel).read_bytes()).hexdigest() == expected, rel
    print('PASS tomato recipe: nine whole raw items destroyed, three retained tools, one vanilla output; cheese files byte-identical')

    scripts = game/'media/scripts/generated'
    food = (scripts/'items/food.txt').read_text('utf-8-sig')
    normal = (scripts/'items/normal.txt').read_text('utf-8-sig')
    tomato = block(food, r'\bitem\s+Tomato\b')
    paste = block(food, r'\bitem\s+TomatoPaste\b')
    assert 'DaysFresh = 4' in tomato and 'DaysTotallyRotten = 12' in tomato
    assert 'Calories = 14.0' in tomato and 'Weight = 0.2' in tomato
    for s in ['Packaged = true', 'CantBeFrozen = true', 'Calories = 120.0', 'HungerChange = -15.0',
              'Carbohydrates = 32.0', 'Lipids = 8.0', 'Proteins = 0.0', 'UnhappyChange = 20',
              'Weight = 0.2', 'Spice = true', 'Pizza:3', 'base:pizzasauce']:
        assert s in paste, s
    for s in ['DaysFresh', 'DaysTotallyRotten', 'ReplaceOnUse', 'OnEat', 'ReplaceOnDeplete']:
        assert s not in paste
    assert len(re.findall(r'\bitem\s+TomatoPaste\w*\b', food)) == 1
    assert 9 * 14 >= 120 and 9 * .2 > .2
    for pot in ['Pot','PotForged']:
        assert 'Capacity' in block(normal, r'\bitem\s+'+pot+r'\b')
    all_items = '\n'.join(p.read_text('utf-8-sig') for p in (scripts/'items').glob('*.txt'))
    for tag in ['sharpknife', 'meatcleaver', 'mixingutensil', 'spoon']:
        assert 'base:'+tag in all_items, tag
    cooking = (scripts/'recipes/recipes_cooking.txt').read_text('utf-8-sig')
    assert 'tags[base:mixingutensil] mode:keep' in cooking
    assert 'tags[base:sharpknife;base:meatcleaver] mode:keep' in cooking
    assert 'flags[InheritFoodAge;ItemCount]' in block(cooking, r'craftRecipe\s+MakeGuacamole')
    print('PASS installed IDs/tags/native cooking patterns, calorie balance and packaged/nonperishable/no-can-return output contract')

    with zipfile.ZipFile(game/'projectzomboid.jar') as jar:
        def cls(name): return Class(jar.read(name+'.class'))
        def code(owner, method):
            a = next(a['Code'] for n,d,a in owner.methods if n == method)
            return a[8:8+int.from_bytes(a[4:8], 'big')]
        def calls(owner, method, fragment):
            b = code(owner,method)
            return any(bytes([op])+i.to_bytes(2,'big') in b for i,v in enumerate(owner.cp)
                       if v and v[0] in (10,11) and fragment in owner.val(i) for op in (0xb6,0xb8,0xb9))
        inputs = cls('zombie/scripting/entity/components/crafting/InputScript')
        flags = cls('zombie/entity/components/crafting/InputFlag')
        assert {'IsWholeFoodItem','IsUncookedFoodItem','ItemCount','IsEmpty','IsNotDull'} <= {n for n,d,a in flags.fields}
        assert calls(inputs,'doesItemPassFoodAndCookingTests','Food:isWholeFoodItem:()Z')
        assert calls(inputs,'doesItemPassFoodAndCookingTests','Food:isUncooked:()Z')
        assert calls(inputs,'passesRottenTest','Food:isRotten:()Z')
        assert calls(inputs,'passesFrozenTest','Food:isFrozen:()Z')
        foods = cls('zombie/inventory/types/Food')
        assert ('isFresh','()Z') in {(n,d) for n,d,a in foods.methods}
        fresh = code(foods,'isFresh')
        assert b'\x96\x9c' in fresh, 'freshness boundary uses age < offAge'
        assert calls(foods,'isWholeFoodItem','Food:getCalories:()F')
        inventory = cls('zombie/inventory/InventoryItem')
        assert ('isBurnt','()Z') in {(n,d) for n,d,a in inventory.methods}
        recipe_data = cls('zombie/entity/components/crafting/recipe/CraftRecipeData')
        assert calls(recipe_data,'processDestroyAndUsedItems','InputScript:isDestroy:()Z')
        assert calls(recipe_data,'processDestroyAndUsedItems','InputScript:isKeep:()Z')
        assert calls(recipe_data,'processDestroyAndUsedItems','ItemUser:UseItem:')
        manager = cls('zombie/entity/components/crafting/recipe/CraftRecipeManager')
        assert calls(manager,'consumeInputItemInternal','CraftRecipe:OnTestItem:')
        assert calls(manager,'isItemValidForInputScript','CraftRecipeManager:consumeInputItem:')
    print('PASS installed per-item OnTest, fresh/rotten/frozen/whole/raw guards, native destroy/keep consumption contracts')

    temp=ROOT/'.validation'; temp.mkdir(exist_ok=True)
    native_parser_bridge(temp/'EFScriptCheck.class')
    java=game/'jre64/bin/java.exe'
    cp=str(temp)+os.pathsep+str(game/'projectzomboid.jar')
    result=subprocess.run([str(java),'-cp',cp,'EFScriptCheck',str(recipe.resolve())],capture_output=True,text=True)
    assert result.returncode==0, result.stderr
    print(result.stdout.strip())
    harness=(ROOT/'tools/test_heat.lua').read_text('utf-8-sig')
    harness=harness.replace('-- INSERT_MOD_SOURCE',(mod/'42/media/lua/shared/EwingsFoodsHeat.lua').read_text('utf-8-sig'))
    # require is deliberately inert: the exact production heat code is already loaded above.
    harness+='\nfunction require(name) assert(name == "EwingsFoodsHeat", "unexpected dependency") end\n'
    harness+=(mod/'42/media/lua/shared/EwingsFoodsTomatoPaste.lua').read_text('utf-8-sig')+'\n'
    action=(game/'media/lua/shared/Entity/TimedActions/ISHandcraftAction.lua').read_text('utf-8-sig')
    lifecycle='\n'.join(re.search(r'function ISHandcraftAction:'+method+r'\([^\n]*\)\n.*?\nend',action,re.S)[0]
                        for method in ['stop','performRecipe'])
    harness+=(ROOT/'tools/test_tomatopaste.lua').read_text('utf-8-sig').replace('-- INSERT_NATIVE_LIFECYCLE',lifecycle)
    target=temp/'tomato-regression.lua'; target.write_text(harness,encoding='utf-8')
    emit_runner(temp/'EFLuaCheck.class')
    result=subprocess.run([str(java),'-cp',cp,'EFLuaCheck',str(target.resolve())],capture_output=True,text=True,cwd=temp)
    assert result.returncode==0, result.stdout+'\n'+result.stderr
    print(result.stdout.strip())
    print('PASS installed Kahlua callback/lifecycle execution with doubles; actual inventory, world, timing and multiplayer untested')
