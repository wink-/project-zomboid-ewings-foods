"""Tiny pure-method interpreter for installed Food bytecode; never boots a game.

Only the inspected getters and age-copy routine are supported. This executes
their actual installed instructions against field/method doubles, not a world.
No extracted bytecode or game source is stored in this tool.
"""
import math, struct


def f32(value): return struct.unpack('>f',struct.pack('>f',value))[0]


def execute(cls, name, obj, *args):
    a=next(a['Code'] for n,d,a in cls.methods if n==name)
    code=a[8:8+int.from_bytes(a[4:8],'big')]
    local={0:obj, **{i+1:v for i,v in enumerate(args)}}
    stack=[];pc=0;steps=0
    def constant(index):
        v=cls.cp[index]
        if v[0]==4: return struct.unpack('>f',bytes.fromhex(v[1]))[0]
        if v[0]==3: return int(v[1],16)
        return cls.val(index)
    while pc<len(code):
        start=pc;op=code[pc];pc+=1;steps+=1
        assert steps<2000, 'unexpected loop'
        if op==0x2a: stack.append(local[0])
        elif 0x1a<=op<=0x1d: stack.append(local[op-0x1a])
        elif 0x22<=op<=0x25: stack.append(local[op-0x22])
        elif 0x2b<=op<=0x2d: stack.append(local[op-0x2a])
        elif 0x3b<=op<=0x3e: local[op-0x3b]=stack.pop()
        elif 0x43<=op<=0x46: local[op-0x43]=stack.pop()
        elif 0x4b<=op<=0x4e: local[op-0x4b]=stack.pop()
        elif 0x02<=op<=0x08: stack.append(op-3)
        elif 0x0b<=op<=0x0d: stack.append(float(op-0x0b))
        elif op in (0x12,0x13):
            width=1 if op==0x12 else 2;i=int.from_bytes(code[pc:pc+width],'big');pc+=width;stack.append(constant(i))
        elif op==0x10: stack.append(int.from_bytes(code[pc:pc+1],'big',signed=True));pc+=1
        elif op in (0xb2,0xb4):
            i=int.from_bytes(code[pc:pc+2],'big');pc+=2
            field=cls.val(i).split(':')[1]
            stack.append(field if op==0xb2 else stack.pop()[field])
        elif op==0xb6:
            i=int.from_bytes(code[pc:pc+2],'big');pc+=2
            owner,method,desc=cls.val(i).split(':',2)
            arguments=[]
            if not desc.startswith('()'): arguments=[stack.pop()]
            receiver=stack.pop()
            if method=='equals': value=receiver==arguments[0]
            elif method=='hasTag': value=arguments[0] in receiver.get('tags',set())
            elif method=='setAge': receiver['age']=f32(arguments[0]);value=None
            else:
                fields={'isFertilized':'fertilized','isFrozen':'frozen','isCooked':'cooked',
                        'isGoodHot':'goodHot','isBadCold':'badCold','getType':'type',
                        'canAge':'canAge','getAge':'age','getOffAge':'offAge','getOffAgeMax':'offAgeMax'}
                assert method in fields, method
                value=receiver[fields[method]]
            if not desc.endswith('V'): stack.append(value)
        elif op==0xb8:
            i=int.from_bytes(code[pc:pc+2],'big');pc+=2
            owner,method,desc=cls.val(i).split(':',2)
            assert owner=='java/lang/Math' and method in ['abs','max'],(owner,method)
            right=stack.pop()
            stack.append(f32(abs(right) if method=='abs' else max(stack.pop(),right)))
        elif op==0x86: stack.append(f32(stack.pop()))
        elif op in (0x62,0x66,0x6a,0x6e):
            right=stack.pop();left=stack.pop()
            stack.append(f32({0x62:lambda:left+right,0x66:lambda:left-right,
                              0x6a:lambda:left*right,0x6e:lambda:left/right}[op]()))
        elif op in (0x95,0x96):
            right=stack.pop();left=stack.pop()
            stack.append((-1 if op==0x95 else 1) if math.isnan(left) or math.isnan(right) else (left>right)-(left<right))
        elif 0x99<=op<=0x9e:
            offset=int.from_bytes(code[pc:pc+2],'big',signed=True);pc+=2;value=stack.pop()
            if {0x99:value==0,0x9a:value!=0,0x9b:value<0,0x9c:value>=0,0x9d:value>0,0x9e:value<=0}[op]: pc=start+offset
        elif op in (0xc6,0xc7):
            offset=int.from_bytes(code[pc:pc+2],'big',signed=True);pc+=2;value=stack.pop()
            if (value is None)==(op==0xc6): pc=start+offset
        elif op==0xa7: pc=start+int.from_bytes(code[pc:pc+2],'big',signed=True)
        elif op in (0xac,0xae): return stack.pop()
        elif op==0xb1: return None
        else: raise AssertionError(f'unsupported opcode {op:02x} at {start} in {name}')
    raise AssertionError('missing return')


def food(**values):
    result=dict(unhappyChange=-5.0,heat=1.0,hungChange=-0.25,calories=480.567,isCookable=True,burnt=False,age=0.0,
                offAge=3,offAgeMax=5,fertilized=False,frozen=False,cooked=True,
                goodHot=True,badCold=False,type='LoadedNachos',canAge=True)
    result.update(values)
    return {k:f32(v) if type(v)==float else v for k,v in result.items()}
