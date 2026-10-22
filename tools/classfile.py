"""Original read-only JVM metadata reader used by the offline validator."""


class Class:
    def __init__(self, data):
        self.d=data; self.p=8
        n=self.u2(); self.cp=[None]*n; i=1
        while i<n:
            t=self.u1()
            if t==1: self.cp[i]=(t,self.take(self.u2()).decode('utf-8','replace'))
            elif t in (3,4): self.cp[i]=(t,self.take(4).hex())
            elif t in (5,6): self.cp[i]=(t,self.take(8).hex()); i+=1
            elif t in (7,8,16,19,20): self.cp[i]=(t,self.u2())
            elif t in (9,10,11,12,17,18): self.cp[i]=(t,self.u2(),self.u2())
            elif t==15: self.cp[i]=(t,self.u1(),self.u2())
            else: raise ValueError(t)
            i+=1
        self.take(6); self.take(2*self.u2())
        self.fields=self.members(); self.methods=self.members()
    def take(self,n):
        b=self.d[self.p:self.p+n]; self.p+=n; return b
    def u1(self): return self.take(1)[0]
    def u2(self): return int.from_bytes(self.take(2),'big')
    def u4(self): return int.from_bytes(self.take(4),'big')
    def val(self,i):
        v=self.cp[i]
        if v[0]==1: return v[1]
        if v[0] in (3,4,5,6): return v[1]
        return ':'.join(self.val(x) for x in v[1:])
    def attrs(self):
        a={}
        for _ in range(self.u2()):
            name=self.val(self.u2()); a[name]=self.take(self.u4())
        return a
    def members(self):
        a=[]
        for _ in range(self.u2()):
            flags=self.u2(); name=self.val(self.u2()); desc=self.val(self.u2()); attrs=self.attrs()
            a.append((name,desc,attrs))
        return a
