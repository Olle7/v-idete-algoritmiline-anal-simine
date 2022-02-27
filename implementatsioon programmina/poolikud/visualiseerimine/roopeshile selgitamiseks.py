print("""d={}
d[True]="o0"
d[1]="o1"
d[1.0]="o2"

class Something2:
    def __init__(self,p):
        self.p=p
    def __hash__(self):
        return hash(self.p)
    def __eq__(self, other):
        return self.p==other.p
    def __repr__(self):
        return "[ p="+str(self.p)+"]"
key_v1=Something2(28)
key_v2=Something2(28)
key2=Something2(29)
d[key_v1]="key1 value1"
d[key_v2]="key1 value2"
d[key2]="key2 value"

print(d.items())
print(d[key_v1])
print(d[key_v2])
print(d[key2])""".replace("    ","____"))