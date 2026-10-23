"""Offline structural and installed-definition checks. Does not launch the game."""
from pathlib import Path
import argparse, hashlib, json, re, struct, subprocess, zipfile
from classfile import Class

ROOT = Path(__file__).resolve().parents[1]


def block(text, heading):
    m = re.search(heading + r"\s*\{", text)
    assert m, f"missing block {heading}"
    start = m.end()
    level = 1
    for pos in range(start, len(text)):
        if text[pos] == "{": level += 1
        if text[pos] == "}": level -= 1
        if level == 0: return text[start:pos]
    raise AssertionError("unbalanced block")


def native_parser_bridge(target):
    # An original minimal Java class emitter, not extracted game bytecode.
    # The bridge only calls Files.readString and ScriptParser; no game entry point.
    pool = []
    def add(data):
        pool.append(data)
        return len(pool)
    def u2(n): return struct.pack(">H", n)
    def utf(s):
        b = s.encode("utf-8")
        return add(b"\x01" + u2(len(b)) + b)
    def cls(s): return add(b"\x07" + u2(utf(s)))
    def nt(n, d): return add(b"\x0c" + u2(utf(n)) + u2(utf(d)))
    def ref(tag, c, n, d): return add(bytes([tag]) + u2(cls(c)) + u2(nt(n,d)))
    this, obj = cls("EFScriptCheck"), cls("java/lang/Object")
    main, descriptor, code_name = utf("main"), utf("([Ljava/lang/String;)V"), utf("Code")
    string_class = cls("java/lang/String")
    paths = ref(10,"java/nio/file/Paths","get","(Ljava/lang/String;[Ljava/lang/String;)Ljava/nio/file/Path;")
    read = ref(10,"java/nio/file/Files","readString","(Ljava/nio/file/Path;)Ljava/lang/String;")
    strip = ref(10,"zombie/scripting/ScriptParser","stripComments","(Ljava/lang/String;)Ljava/lang/String;")
    parse = ref(10,"zombie/scripting/ScriptParser","parse","(Ljava/lang/String;)Lzombie/scripting/ScriptParser$Block;")
    out = ref(9,"java/lang/System","out","Ljava/io/PrintStream;")
    println = ref(10,"java/io/PrintStream","println","(Ljava/lang/String;)V")
    message = add(b"\x08" + u2(utf("PASS native ScriptParser structural syntax (no game boot)")))
    code = (b"\x2a\x03\x32\x03\xbd" + u2(string_class) + b"\xb8" + u2(paths)
            + b"\xb8" + u2(read) + b"\xb8" + u2(strip) + b"\xb8" + u2(parse) + b"\x57"
            + b"\xb2" + u2(out) + b"\x13" + u2(message) + b"\xb6" + u2(println) + b"\xb1")
    body = u2(4)+u2(1)+struct.pack(">I",len(code))+code+u2(0)+u2(0)
    method = u2(9)+u2(main)+u2(descriptor)+u2(1)+u2(code_name)+struct.pack(">I",len(body))+body
    target.write_bytes(b"\xca\xfe\xba\xbe"+u2(0)+u2(52)+u2(len(pool)+1)+b"".join(pool)
                       +u2(0x21)+u2(this)+u2(obj)+u2(0)+u2(0)+u2(1)+method+u2(0))


def check(game, mod):
    recipe_path = mod / "42/media/scripts/ewingsfoods_cheese.txt"
    text = recipe_path.read_text("utf-8-sig")
    assert text.count("craftRecipe ") == 1
    assert re.search(r"module\s+EwingsFoods\s*\{", text)
    assert "recipe " not in text and not re.search(r"\bitem\s+[A-Za-z_]", text)
    stack = []
    for c in text:
        if c in "{[": stack.append(c)
        elif c in "}]":
            assert stack and stack.pop() == {"}":"{", "]":"["}[c]
    assert not stack
    actual = re.findall(r"^\s*(?:-fluid|item)\s+[^\n]+", text, re.M)
    expected = [
        "item 1 [Base.Pot;Base.PotForged] mode:keep flags[IsEmpty],",
        "item 1 [Base.CheeseCloth] mode:keep,",
        "item 1 [*] mode:keep,",
        "-fluid 1.0 [CowMilk;SheepMilk],",
        "item 1 [Base.Vinegar2;Base.Vinegar_Jug],",
        "item 1 [Base.Salt],",
        "item 1 Base.Cheese,",
    ]
    assert [s.strip() for s in actual] == expected
    props = dict(re.findall(r"^\s*(\w+)\s*=\s*([^,\n]+),", text, re.M))
    assert props == dict(timedAction="Making", time="600", Tags="InHandCraft;Cooking;CanBeDoneInDark",
                         category="Cooking", SkillRequired="Cooking:1", xpAward="Cooking:5",
                         OnTest="EwingsFoodsHeat.canMakeCheese", Tooltip="Tooltip_EwingsFoods_CheeseHeat")
    assert "AllowRottenItem" not in text and "AllowFrozenItem" not in text
    assert "InheritFood" not in text and "mode:mixture" not in text and "mode:primary" not in text
    assert [p.relative_to(mod).as_posix() for p in mod.rglob("*.lua")] == ["42/media/lua/shared/EwingsFoodsHeat.lua"], "only the mod-owned heat callback is expected"
    info = dict(line.split("=",1) for line in (mod / "42/mod.info").read_text().splitlines() if "=" in line)
    assert info["id"] == "EwingsFoods" and info["version"] == "1.0.1"
    assert info["versionMin"] == info["versionMax"] == "42.21"
    assert (mod / "common").is_dir()
    translation = json.loads((mod / "42/media/lua/shared/Translate/EN/Recipes.json").read_text("utf-8-sig"))
    assert translation == {"EwingsFoods_MakeCheese": "Make Cheese (Ewing's Foods)"}
    tooltip = json.loads((mod / "42/media/lua/shared/Translate/EN/Tooltip.json").read_text("utf-8-sig"))
    assert "Tooltip_EwingsFoods_CheeseHeat" in tooltip and "generator" in tooltip["Tooltip_EwingsFoods_CheeseHeat"]
    print("PASS layout, version bounds, single additive recipe, translations, tools, unchanged quantities/balance/output")

    scripts = game / "media/scripts/generated"
    normal = (scripts / "items/normal.txt").read_text("utf-8-sig")
    food = (scripts / "items/food.txt").read_text("utf-8-sig")
    drain = (scripts / "items/drainable.txt").read_text("utf-8-sig")
    fluids = (scripts / "fluids.txt").read_text("utf-8-sig")
    item_texts = {"Pot":normal,"PotForged":normal,"CheeseCloth":normal,
                  "Vinegar2":drain,"Vinegar_Jug":drain,"Salt":food,"Cheese":food}
    definitions = {name:block(source,r"\bitem\s+"+name+r"\b") for name,source in item_texts.items()}
    assert all(re.search(r"\bfluid\s+"+name+r"\b",fluids) for name in ["CowMilk","SheepMilk"])
    assert "ItemType = base:normal" in definitions["CheeseCloth"]
    for name in ["Pot","PotForged"]:
        assert float(re.search(r"Capacity\s*=\s*([\d.]+)", definitions[name])[1]) >= 1.0
    assert "UseDelta = 0.1" in definitions["Vinegar2"]
    assert "UseDelta = 0.05" in definitions["Vinegar_Jug"]
    assert "HungerChange = -10.0" in definitions["Salt"]
    cheese = definitions["Cheese"]
    for value in ["Pizza:15", "Weight = 0.2", "DaysFresh = 14", "DaysTotallyRotten = 20", "Calories = 113.0"]:
        assert value in cheese
    milk = block(normal,r"\bitem\s+Milk\b")
    assert "CowMilk:1.0" in milk and "DaysFresh" not in milk
    print("PASS installed ingredient IDs, fluid IDs, vessel capacity, vinegar/salt units, cheese/pizza/spoilage definitions")

    with zipfile.ZipFile(game / "projectzomboid.jar") as jar:
        def get(name): return Class(jar.read(name+".class"))
        core = get("zombie/core/Core")
        init = next(a["Code"][8:] for n,d,a in core.methods if n=="<clinit>")
        assert init[:8].endswith(b"\x10\x2a\x10\x15"), "installed game must be 42.21"
        inputs = get("zombie/scripting/entity/components/crafting/InputScript")
        methods = {n for n,d,a in inputs.methods}
        assert {"passesRottenTest","allowRottenItem","isFluidMatch","isFluidExact"} <= methods
        exact = [i for i,v in enumerate(inputs.cp) if v and v[0]==9 and inputs.val(i).endswith("FluidMatchMode:Exact:Lzombie/entity/components/crafting/FluidMatchMode;")]
        constructor = next(a["Code"][8:] for n,d,a in inputs.methods if n=="<init>")
        assert exact and b"\xb2"+struct.pack(">H",exact[0]) in constructor
        rotten = next(a["Code"][8:] for n,d,a in inputs.methods if n=="passesRottenTest")
        rotten_calls = [i for i,v in enumerate(inputs.cp) if v and v[0]==10 and ":isRotten:" in inputs.val(i)]
        assert any(b"\xb6"+struct.pack(">H",i) in rotten for i in rotten_calls)
        heat = get("zombie/scripting/logic/RecipeCodeOnTest")
        assert any(n=="openFire" and d=="(Lzombie/inventory/InventoryItem;Lzombie/characters/IsoGameCharacter;)Z" for n,d,a in heat.methods)
        values = [v[1] for v in heat.cp if v and v[0]==1]
        assert {"zombie/iso/objects/IsoFireplace","zombie/iso/objects/IsoBarbecue","isLit","hasAdjacentFireObject"} <= set(values)
        flags = get("zombie/entity/components/crafting/InputFlag")
        assert {"IsEmpty","AllowRottenItem","AllowFrozenItem"} <= {n for n,d,a in flags.fields}
        recipe = get("zombie/scripting/entity/components/crafting/CraftRecipe")
        keys = {v[1] for v in recipe.cp if v and v[0]==1}
        assert set(props) <= keys
        def calls(owner, method, target):
            cls = get(owner)
            attribute = next(a["Code"] for n,d,a in cls.methods if n == method)
            code = attribute[8:8+int.from_bytes(attribute[4:8],"big")]
            matches = [i for i,v in enumerate(cls.cp) if v and v[0] in (10,11) and target in cls.val(i)]
            return any(bytes([op])+struct.pack(">H",i) in code for i in matches for op in (0xb6,0xb8,0xb9))
        assert calls("zombie/inventory/ItemContainer","isPowered","IsoObject:checkObjectPowered:()Z")
        assert calls("zombie/iso/IsoObject","checkObjectPowered","ItemContainer:isObjectPowered:")
        for method in ("isObjectPowered","isSquarePowered"):
            for predicate in ("haveElectricity:()Z","hasGridPower:()Z"):
                assert calls("zombie/inventory/ItemContainer",method,predicate)
        assert calls("zombie/iso/IsoGridSquare","haveElectricity","IsoChunk:isGeneratorPoweringSquare:(III)Z")
        assert calls("zombie/iso/IsoGridSquare","getRadius","IsoGridSquare:getZ:()I")
        stove = get("zombie/iso/objects/IsoStove")
        signatures = {(n,d) for n,d,a in stove.methods}
        for method,descriptor in [("Activated","()Z"),("isBroken","()Z"),("isMicrowave","()Z"),
                                  ("getCurrentTemperature","()F"),("getMaxTemperature","()F")]:
            assert (method,descriptor) in signatures
        attribute = next(a["Code"] for n,d,a in stove.methods if n=="getCurrentTemperature")
        temperature = attribute[8:8+int.from_bytes(attribute[4:8],"big")]
        hundred = next(i for i,v in enumerate(stove.cp) if v == (4,"42c80000"))
        current = next(i for i,v in enumerate(stove.cp) if v and v[0]==9 and stove.val(i).endswith("IsoStove:currentTemperature:F"))
        # Verify native normalization (raw + 100) / 100: an unwarmed raw zero is 1.
        assert temperature == (b"\x2a\xb4"+struct.pack(">H",current)+b"\x13"+struct.pack(">H",hundred)
                               +b"\x62\x13"+struct.pack(">H",hundred)+b"\x6e\xae")
        assert calls("zombie/iso/objects/IsoStove","update","ItemContainer:isPowered:()Z")
        print("PASS installed stove/power API chain: active stove, normalized warmth, grid plus generator electricity, same-floor neighborhood")
    print("PASS installed 42.21 bytecode contracts: exact milk filter default, rotten guard, native open-fire callback, flags and recipe keys")

    cooking = (scripts / "recipes/recipes_cooking.txt").read_text("utf-8-sig")
    cereal = block(cooking,r"craftRecipe\s+MakeBowlOfCereal")
    assert "-fluid 0.3 [CowMilk;SheepMilk]" in cereal
    medical = (scripts / "recipes/recipes_medical.txt").read_text("utf-8-sig")
    assert "item 1 [*] mode:keep," in medical and "-fluid 0.5 [Water]" in medical
    assert "OnTest = RecipeCodeOnTest.openFire" in (scripts / "recipes/recipes_spears.txt").read_text("utf-8-sig")
    print("PASS syntax patterns cross-checked against installed native fluid-container, milk and open-fire recipes")

    temp = ROOT / ".validation"
    temp.mkdir(exist_ok=True)
    native_parser_bridge(temp / "EFScriptCheck.class")
    java = game / "jre64/bin/java.exe"
    if not java.exists():
        java = Path("java")
    result = subprocess.run([str(java),"-cp",str(temp)+__import__("os").pathsep+str(game/"projectzomboid.jar"),
                             "EFScriptCheck",str(recipe_path.resolve())],capture_output=True,text=True)
    assert result.returncode == 0, result.stderr
    print(result.stdout.strip())
    print("Inspected game-file SHA-256 (relative paths; game content is not distributed):")
    for rel in ["projectzomboid.jar", "media/scripts/generated/items/normal.txt", "media/scripts/generated/items/food.txt",
                "media/scripts/generated/items/drainable.txt", "media/scripts/generated/fluids.txt"]:
        print(hashlib.sha256((game/rel).read_bytes()).hexdigest(), rel)
    from test_heat import run
    run(game, mod)
    print("Offline checks passed. Gameplay, interruption/revalidation and multiplayer remain untested.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--game-root",type=Path,required=True)
    parser.add_argument("--mod-root",type=Path,default=ROOT/"EwingsFoods")
    args=parser.parse_args()
    check(args.game_root,args.mod_root)
