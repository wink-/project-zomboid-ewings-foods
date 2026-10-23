"""Execute isolated Lua regression tests with the installed Kahlua VM, not a game world."""
from pathlib import Path
import argparse, os, struct, subprocess

ROOT=Path(__file__).resolve().parents[1]


def emit_runner(target):
    cp=[]
    def u2(n): return struct.pack('>H',n)
    def add(b): cp.append(b); return len(cp)
    def utf(s):
        b=s.encode('utf-8');return add(b'\x01'+u2(len(b))+b)
    def cls(s): return add(b'\x07'+u2(utf(s)))
    def ref(tag,c,n,d):
        owner=cls(c); name=utf(n);desc=utf(d);nt=add(b'\x0c'+u2(name)+u2(desc))
        return add(bytes([tag])+u2(owner)+u2(nt))
    this=cls('EFLuaCheck');obj=cls('java/lang/Object')
    main=utf('main');desc=utf('([Ljava/lang/String;)V');code_name=utf('Code')
    platform='se/krka/kahlua/j2se/J2SEPlatform'
    table='Lse/krka/kahlua/vm/KahluaTable;'
    thread='se/krka/kahlua/vm/KahluaThread'
    get=ref(10,platform,'getInstance','()L'+platform+';')
    newtable=ref(10,platform,'newTable','()'+table)
    base=ref(10,'se/krka/kahlua/stdlib/BaseLib','register','('+table+')V')
    threadclass=cls(thread)
    out=ref(9,'java/lang/System','out','Ljava/io/PrintStream;')
    init=ref(10,thread,'<init>','(Ljava/io/PrintStream;Lse/krka/kahlua/vm/Platform;'+table+')V')
    stringclass=cls('java/lang/String')
    paths=ref(10,'java/nio/file/Paths','get','(Ljava/lang/String;[Ljava/lang/String;)Ljava/nio/file/Path;')
    read=ref(10,'java/nio/file/Files','readString','(Ljava/nio/file/Path;)Ljava/lang/String;')
    title=add(b'\x08'+u2(utf('EwingsFoods isolated heat regression')))
    compilelua=ref(10,'se/krka/kahlua/luaj/compiler/LuaCompiler','loadstring','(Ljava/lang/String;Ljava/lang/String;'+table+')Lse/krka/kahlua/vm/LuaClosure;')
    call=ref(10,thread,'call','(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;')
    code=(b'\xb8'+u2(get)+b'\x4c\x2b\xb6'+u2(newtable)+b'\x4d\x2c\xb8'+u2(base)
          +b'\xbb'+u2(threadclass)+b'\x59\xb2'+u2(out)+b'\x2b\x2c\xb7'+u2(init)+b'\x4e'
          +b'\x2a\x03\x32\x03\xbd'+u2(stringclass)+b'\xb8'+u2(paths)+b'\xb8'+u2(read)
          +b'\x13'+u2(title)+b'\x2c\xb8'+u2(compilelua)+b'\x3a\x04'
          +b'\x2d\x19\x04\x01\x01\x01\xb6'+u2(call)+b'\x57\xb1')
    body=u2(6)+u2(5)+struct.pack('>I',len(code))+code+u2(0)+u2(0)
    method=u2(9)+u2(main)+u2(desc)+u2(1)+u2(code_name)+struct.pack('>I',len(body))+body
    target.write_bytes(b'\xca\xfe\xba\xbe'+u2(0)+u2(52)+u2(len(cp)+1)+b''.join(cp)
                       +u2(0x21)+u2(this)+u2(obj)+u2(0)+u2(0)+u2(1)+method+u2(0))


def run(game,mod):
    temp=ROOT/'.validation'
    temp.mkdir(exist_ok=True)
    source=(mod/'42/media/lua/shared/EwingsFoodsHeat.lua').read_text('utf-8-sig')
    harness=(ROOT/'tools/test_heat.lua').read_text('utf-8-sig')
    assert harness.count('-- INSERT_MOD_SOURCE')==1
    target=temp/'heat-regression.lua'
    target.write_text(harness.replace('-- INSERT_MOD_SOURCE',source),encoding='utf-8')
    emit_runner(temp/'EFLuaCheck.class')
    java=game/'jre64/bin/java.exe'
    result=subprocess.run([str(java),'-cp',str(temp)+os.pathsep+str(game/'projectzomboid.jar'),
                           'EFLuaCheck',str(target.resolve())],capture_output=True,text=True,cwd=temp)
    if result.returncode:
        raise AssertionError(result.stdout+'\n'+result.stderr)
    print(result.stdout.strip())
    print('PASS installed Kahlua compilation and isolated callback tests; engine APIs are test doubles, not live appliances')


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--game-root',type=Path,required=True)
    p.add_argument('--mod-root',type=Path,default=ROOT/'EwingsFoods')
    a=p.parse_args();run(a.game_root,a.mod_root)
