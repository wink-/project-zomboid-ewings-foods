"""Focused nachos checks using installed scripts, bytecode and isolated Lua.

These are not inventory/world or multiplayer tests.
"""
from pathlib import Path
import hashlib, json, os, re, struct, subprocess, zipfile
from PIL import Image
from classfile import Class
from native_food_vm import execute, food, f32
from test_heat import emit_runner
from validate import block, native_parser_bridge

ROOT=Path(__file__).resolve().parents[1]


def check(game,mod):
    path=mod/'42/media/scripts/ewingsfoods_nachos.txt'
    text=path.read_text('utf-8-sig')
    item=block(text,r'\bitem\s+LoadedNachos\b')
    recipe=block(text,r'craftRecipe\s+EwingsFoods_MakeLoadedNachos')
    assert text.count('craftRecipe ')==1
    assert 'module EwingsFoods' in text
    lines=[x.strip() for x in re.findall(r'^\s*item\s+[^\n]+',recipe,re.M)]
    assert lines==[
        'item 1 [Base.Plate] mode:destroy flags[ItemCount],',
        'item 1 tags[base:sharpknife;base:meatcleaver] mode:keep flags[IsNotDull],',
        'item 1 [Base.TortillaChips] mode:destroy flags[ItemCount;IsWholeFoodItem],',
        'item 5 [Base.Cheese] flags[InheritFoodAge],',
        'item 6 [Base.Tomato] flags[InheritFoodAge;IsUncookedFoodItem],',
        'item 1 [Base.PepperJalapeno] flags[InheritFoodAge;IsUncookedFoodItem],',
        'item 3 [Base.Onion] flags[InheritFoodAge;IsUncookedFoodItem],',
        'item 1 EwingsFoods.LoadedNachos,',
    ]
    assert 'OnTest' not in recipe and 'OnCreate = EwingsFoodsNachos.onCreate' in recipe
    assert 'time = 80' in recipe and 'Cooking:1' in recipe and 'Cooking:3' in recipe
    for forbidden in ['AllowRottenItem','AllowFrozenItem','ReplaceOnCooked','OnEat','OnCooked','DangerousUncooked','EvolvedRecipe']:
        assert forbidden not in text
    props=dict(re.findall(r'^\s*(\w+)\s*=\s*([^,\n]+),',item,re.M))
    expected={'ItemType':'base:food','Icon':'EwingsFoods_LoadedNachos','Weight':'1.5','EatType':'Plate',
              'ReplaceOnUse':'Base.Plate','IsCookable':'true','MinutesToCook':'0','MinutesToBurn':'20',
              'DaysFresh':'3','DaysTotallyRotten':'5','HungerChange':'-25.0','GoodHot':'true',
              'UnhappyChange':'-5','BoredomChange':'-5','Tags':'base:alreadycooked;base:hidecooked',
              'StaticModel':'Base.Plate_Ground','WorldStaticModel':'Base.Plate_Ground'}
    assert all(props[k]==v for k,v in expected.items())
    names=json.loads((mod/'42/media/lua/shared/Translate/EN/ItemName.json').read_text('utf-8-sig'))
    assert names=={'EwingsFoods.LoadedNachos':'Loaded Nachos'}
    tips=json.loads((mod/'42/media/lua/shared/Translate/EN/Tooltip.json').read_text('utf-8-sig'))
    assert '2 less unhappiness' in tips['Tooltip_EwingsFoods_LoadedNachos']
    for rel,digest in {
        '42/media/scripts/ewingsfoods_tomatopaste.txt':'33abcb1614bca4e5981240121ae3ecd1a1ce22804ba2d6c4e30999bba3af4319',
        '42/media/lua/shared/EwingsFoodsTomatoPaste.lua':'20a4374c291e19e7c9a239cd79a10609e095f4f8667bdcc155f53b6d50cd21d9',
    }.items(): assert hashlib.sha256((mod/rel).read_bytes()).hexdigest()==digest

    generated=game/'media/scripts/generated'
    source=(generated/'items/food.txt').read_text('utf-8-sig')
    normal=(generated/'items/normal.txt').read_text('utf-8-sig')
    definitions={name:block(source,r'\bitem\s+'+name+r'\b') for name in ['TortillaChips','Cheese','Tomato','PepperJalapeno','Onion']}
    ratios={'TortillaChips':1,'Cheese':5/15,'Tomato':6/12,'PepperJalapeno':1/2,'Onion':3/10}
    for nutrient in ['Calories','Carbohydrates','Lipids','Proteins']:
        total=sum(float(re.search(nutrient+r'\s*=\s*([\d.]+)',definitions[n])[1])*fraction for n,fraction in ratios.items())
        assert abs(float(props[nutrient])-total)<0.0011,(nutrient,total)
    assert 'Packaged = true' in definitions['TortillaChips']
    assert 'Weight = 1.0' in block(normal,r'\bitem\s+Plate\b')
    assert 'Weight = 0.2' in block(normal,r'\bitem\s+ClayPlate\b')
    assert 'model Plate_Ground' in (generated/'models_items.txt').read_text('utf-8-sig')
    assert 'ReplaceOnUse = Base.Bowl' in source and 'EatType = Plate' in source
    assert 'Tags = base:alreadycooked;base:hidecooked' in source
    # Count real plate references, avoiding the word Template and EatType=Plate.
    plate_recipes=[]
    for candidate in generated.rglob('*.txt'):
        if 'recipe' in candidate.name.lower() or 'craftrecipe' in str(candidate.parent).lower():
            if re.search(r'\bBase\.(?:Plate|ClayPlate)\b',candidate.read_text('utf-8-sig')):
                plate_recipes.append(candidate.relative_to(generated).as_posix())
    print('PASS inspected native plate recipe references:',plate_recipes)
    print('PASS nachos input uses/output, single consumed plate, nutrition equals selected portions, inherited age and unchanged 1.0.2 recipes')

    with zipfile.ZipFile(game/'projectzomboid.jar') as jar:
        def cls(name): return Class(jar.read(name+'.class'))
        def method_code(owner,name):
            return [(d,a['Code'][8:8+int.from_bytes(a['Code'][4:8],'big')]) for n,d,a in owner.methods if n==name and 'Code' in a]
        def calls(owner,name,fragment):
            return any(bytes([op])+i.to_bytes(2,'big') in code for d,code in method_code(owner,name)
                       for i,v in enumerate(owner.cp) if v and v[0] in (10,11) and fragment in owner.val(i) for op in [0xb6,0xb8,0xb9])
        foods=cls('zombie/inventory/types/Food')
        field_api={(n,d) for n,d,a in foods.methods}
        assert {('copyAgeFrom','(Lzombie/inventory/types/Food;)V'),('getCalories','()F')}<=field_api
        data=cls('zombie/entity/components/crafting/recipe/CraftRecipeData')
        assert {'getFirstCreatedItem','getAllConsumedItems'}<={n for n,d,a in data.methods}
        assert calls(data,'createOutputItems','Food:copyAgeFrom:')
        assert calls(data,'luaCallOnCreate','LuaCaller:protectedCallVoid:')
        assert calls(foods,'update','Food:setCooked:(Z)V')
        assert calls(foods,'update','Food:isCooked:()Z')
        assert any(v and v[0]==9 and 'ALREADY_COOKED' in foods.val(i) for i,v in enumerate(foods.cp))
        inputs=cls('zombie/scripting/entity/components/crafting/InputScript')
        assert calls(inputs,'passesRottenTest','Food:isRotten:()Z')
        assert calls(inputs,'passesFrozenTest','Food:isFrozen:()Z')
        assert calls(inputs,'doesItemPassFoodAndCookingTests','Food:isUncooked:()Z')
        characters=cls('zombie/characters/IsoGameCharacter')
        assert calls(characters,'Eat','Food:UseAndSync:()V')
        assert calls(characters,'Eat','Food:multiplyFoodValues:(F)V')
        assert calls(characters,'Eat','Food:getReplaceOnUseFullType:')
        user=cls('zombie/inventory/ItemUser')
        assert calls(user,'UseItem','ItemUser:CreateItem:') and calls(user,'UseItem','ItemUser:RemoveItem:')
        print('PASS installed native age/onCreate, cooked/reheat, raw/rotten/frozen and partial/depleted consumption/replacement API contracts')

        heat_cases=[('cold',{},-5),('exact hot threshold',{'heat':1.3},-5),('hot',{'heat':1.31},-7),
                    ('very hot',{'heat':2.0},-7),('cooling',{'heat':1.29},-5),
                    ('uncooked',{'heat':2.0,'cooked':False},-5),
                    ('bonus disabled',{'heat':2.0,'goodHot':False},-5),
                    ('not cookable',{'heat':2.0,'isCookable':False},-5),
                    ('stale cold',{'age':3.2},5),('stale hot',{'age':3.2,'heat':1.5},3)]
        for label,values,expected_value in heat_cases:
            assert execute(foods,'getUnhappyChange',food(**values))==expected_value,label
        for heat in [1.0,1.5]:
            assert abs(execute(foods,'getHungerChange',food(heat=heat))-(-0.325))<0.00001
            assert execute(foods,'getCalories',food(heat=heat))==f32(480.567)
        for age,fresh in [(0,4),(2,4),(3.6,4),(4.4,4),(7,14)]:
            output=food();ingredient=food(age=float(age),offAge=fresh,offAgeMax=12 if fresh==4 else 20)
            execute(foods,'copyAgeFrom',output,ingredient)
            assert abs(output['age']-age/fresh*3)<0.00001,(age,output)
        print('PASS 14 actual installed Food hot-mood/hunger/calorie instruction cases and 5 native age-copy instruction cases (field/method doubles; no game boot)')

    pack=(game/'media/texturepacks/UI2.pack').read_bytes()
    for icon in [b'Item_Plate',b'Item_CornChips']:
        p=pack.index(icon)+len(icon)
        metadata=struct.unpack_from('<8i',pack,p)
        assert metadata[-2:]==(32,32),(icon,metadata)
    icon=Image.open(mod/'common/media/textures/Item_EwingsFoods_LoadedNachos.png')
    assert icon.size==(32,32) and icon.mode=='RGBA'
    alpha=icon.getchannel('A')
    assert alpha.getextrema()==(0,255)
    assert 300<sum(v>0 for v in alpha.getdata())<950
    assert all(alpha.getpixel(p)==0 for p in [(0,0),(31,0),(0,31),(31,31)])
    assert icon.getbbox()[0]>0 and icon.getbbox()[2]<32
    print('PASS native-sized 32x32 original icon RGBA alpha, visible pixel area, safe margins and transparent corners')

    temp=ROOT/'.validation';temp.mkdir(exist_ok=True)
    native_parser_bridge(temp/'EFScriptCheck.class')
    cp=str(temp)+os.pathsep+str(game/'projectzomboid.jar');java=game/'jre64/bin/java.exe'
    run=subprocess.run([str(java),'-cp',cp,'EFScriptCheck',str(path.resolve())],capture_output=True,text=True)
    assert run.returncode==0,run.stderr
    print(run.stdout.strip())
    harness=(ROOT/'tools/test_nachos.lua').read_text('utf-8-sig').replace('-- INSERT_NACHOS_SOURCE',(mod/'42/media/lua/shared/EwingsFoodsNachos.lua').read_text('utf-8-sig'))
    native=(game/'media/lua/shared/TimedActions/ISEatFoodAction.lua').read_text('utf-8-sig')
    excerpt='\n'.join(re.search(r'function ISEatFoodAction:'+name+r'\([^\n]*\)\n.*?\nend',native,re.S)[0] for name in ['eat','complete'])
    harness=harness.replace('-- INSERT_NATIVE_EATING',excerpt)
    target=temp/'nachos-regression.lua';target.write_text(harness,encoding='utf-8')
    emit_runner(temp/'EFLuaCheck.class')
    run=subprocess.run([str(java),'-cp',cp,'EFLuaCheck',str(target.resolve())],capture_output=True,text=True,cwd=temp)
    assert run.returncode==0,run.stdout+'\n'+run.stderr
    print(run.stdout.strip())
    print('Nachos offline checks passed. Real plate return, inventory identity, warming/burning, interruption and multiplayer remain untested.')
