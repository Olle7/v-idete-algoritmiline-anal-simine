class Vertex:
    def __init__(self,params,type1_branches,type2_branches):
        self.params=params
        self.type1_branches=type1_branches
        self.type2_branches=type2_branches

v1_1_1=Vertex(["9","7","M","M","L"],[],[])
v1_1=Vertex(["1","5","8","2"],[v1_1_1],[])
v1_2=Vertex(["9","A","9","7"],[],[])
v1_3=Vertex(["0","0","H","7"],[],[])
v1_4_1=Vertex(["R","7","8","9","9"],[],[])
v1_4=Vertex(["1","2","F","5"],[],[v1_4_1])
v1=Vertex(["0","3","5"],[v1_1,v1_2,v1_3],[v1_4])


vertex=Vertex({"PARAM1":"2","MY_PARAM":"3"},[],[])