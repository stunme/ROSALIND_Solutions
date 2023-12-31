##  Quartet Distance

#Gerth et al. 2004 Algorithmica. DOI: 10.1007/s00453-003-1065-y
#Unfinished code. Stopped at F fuction definition. 

import re
import time
def unrootTree(treeSeq):
    class node():
        def __init__(self,childs) -> None:
            self.child = childs
            self.isInnerNode = (len(childs)>1)
            self.taxa = ""
            self.color = (0,0,0)

    tokens = re.split("([(,)])",treeSeq)
    stack = [[]]
    for t in tokens:
        if t == '(':
            stack.append([])
        elif t == ')':
            cur = stack.pop()
            stack[-1].append(node(cur))
        elif t not in ' ,':
            taxaPointer[t].append(node([t]))
            taxaPointer[t][-1].taxa = t
            stack[-1].append(taxaPointer[t][-1])
    root = node(cur)
    nodes = {root}
    def addOrient(nd):
        for c in nd.child:
            if c.isInnerNode:
                addOrient(c)
            c.child.append(nd)
            nodes.add(c)
    addOrient(root)
    return nodes

def hdTree(urTreeSet):
    class component():
        def __init__(self) -> None:
            self.child = []
            self.edge = []
            self.edgeColor = []
            self.content = None
            self.type = 0
            self.colorCode = (0,0,0)

        def F3(self,x,y,z):
            sum = 0
            a1,b1,c1 = x
            a2,b2,c2 = y
            a3,b3,c3 = z
            sum += int(a1*(a1-1)/2)*(b2*c3+b3*c2)
            sum += int(a2*(a2-1)/2)*(b1*c3+b3*c1)
            sum += int(a3*(a3-1)/2)*(b2*c1+b1*c2)
            sum += int(b1*(b1-1)/2)*(a2*c3+a3*c2)
            sum += int(b2*(b2-1)/2)*(a1*c3+a3*c1)
            sum += int(b3*(b3-1)/2)*(a2*c1+a1*c2)
            sum += int(c1*(c1-1)/2)*(b2*a3+b3*a2)
            sum += int(c2*(c2-1)/2)*(b1*a3+b3*a1)
            sum += int(c3*(c3-1)/2)*(b2*a1+b1*a2)
            return sum
        
        def F2(self,x,y):
            sum = 0
            a1,b1,c1 = x
            a2,b2,c2 = y
            sum += int(a1*(a1-1)/2)*(b2*c1+b1*c2)
            sum += int(a2*(a2-1)/2)*(b2*c1+b1*c2)
            sum += int(b1*(b1-1)/2)*(a2*c1+a1*c2)
            sum += int(b2*(b2-1)/2)*(a2*c1+a1*c2)
            sum += int(c1*(c1-1)/2)*(b2*a1+b1*a2)
            sum += int(c2*(c2-1)/2)*(b2*a1+b1*a2)
            return sum
        
        def F1(self,x):
            sum = 0
            a1,b1,c1 = x
            sum += int(a1*(a1-1)/2)*b1*c1
            sum += int(b1*(b1-1)/2)*a1*c1
            sum += int(c1*(c1-1)/2)*b1*a1
            return sum

        def F(self):
            sum = 0
            if self.type == 0:
                if len(self.edge()) == 3:
                    sum += self.F3(self.edgeColor[0],self.edgeColor[1],self.edgeColor[2])
            elif self.type == 1:
                sum += self.F3(self.child[0].colorCode,self.edgeColor[0],self.edgeColor[1])
                sum += self.F1( self.child[1].colorCode[0]+self.edgeColor[0][0]+self.edgeColor[1][0],
                                self.child[1].colorCode[1]+self.edgeColor[0][1]+self.edgeColor[1][1],
                                self.child[1].colorCode[2]+self.edgeColor[0][2]+self.edgeColor[1][2],
                                )
            elif self.type == 2:
                sum += self.F2(,)
            elif self.type == 3:
                pass
            elif self.type == 4:
                for c in self.child:
                    sum += self.F1(c.colorCode)
            return sum
    nodeDict = {}
    edgeDict = {}
    edgeColor = {}

    def countColor(edge):
        if edge in edgeColor:
            return edgeColor[edge]
        a,b = edge
        sum = (0,0,0)
        if b.isInnerNode:
            for c in b.child:
                if c!=a:
                    sum = tuple(x+y for x,y in zip(sum,countColor((b,c))))
        else:
            sum = b.color
        edgeColor[edge] = sum
        return sum
            
    for n in urTreeSet:
        nd = component()
        nd.type = 0
        nd.content = n
        nd.colorCode = n.color
        for c in n.child:
            if not isinstance(c,str):
                try:
                    nodeDict[nd].append((n,c))
                except KeyError:
                    nodeDict[nd] = [(n,c)]
                nd.edge.append((n,c))
                edgeDict[(n,c)] = nd
                edgeColor[(n,c)] = countColor((n,c))
                nd.edgeColor.append(edgeColor[(n,c)])

    print(sum(len(nodeDict[n])==1 for n in nodeDict))
    print(sum(len(nodeDict[n])==3 for n in nodeDict))
    print(len(edgeDict),len(nodeDict))

    while len(nodeDict)>1:
        nextNodes = {}
        usedNodes = set()
        for nd in nodeDict:
            if nd in usedNodes:
                continue
            for ea,eb in nodeDict[nd]:
                ndPair = edgeDict[(eb,ea)]
                if ndPair in usedNodes or ndPair in nextNodes:
                    continue
                if len(nodeDict[ndPair]) + len(nodeDict[nd]) < 5:
                    tmp = component()
                    tmp.child = sorted([nd,ndPair],key=lambda a: len(a.edge))
                    tmp.colorCode = tuple(x+y for x,y in zip(nd.colorCode,ndPair.colorCode))

                    newEdges = [x for x in nodeDict[nd] if x!=(ea,eb)]
                    newEdges += [x for x in nodeDict[ndPair] if x!=(eb,ea)]
                    if len(nd.edge) == 3 or len(ndPair.edge) == 3:
                        tmp.type = 1
                    else:
                        tmp.type = 4-len(newEdges)

                    del edgeDict[(ea,eb)]
                    del edgeDict[(eb,ea)] 
                    for ne in newEdges:
                        edgeDict[ne] = tmp
                        tmp.edge.append(ne)

                    usedNodes.add(nd)
                    usedNodes.add(ndPair)

                    nextNodes[tmp] = newEdges[:]
                    break
        for n in nodeDict:
            if n not in usedNodes:
                nextNodes[n] = nodeDict[n]
        nodeDict = nextNodes
    
    for n in nodeDict:
        root = n
    return root

def colorLeaf(taxa,color):
    for n in taxaPointer[taxa]:
        n.color = color

def rootTree(urTreeSet):
    for n in urTreeSet:
        if not n.isInnerNode:
            root = n
            colorLeaf(n.child[0],(0,0,1))
            n.child = [n.child[1]]
            break
    def removeOrient(nd):
        sum = 0
        for c in nd.child:
            if len(c.child) ==2:
                c.child = [c.child[0]]
                colorLeaf(c.child[0],(1,0,0))
                c.size = 1
            else:
                c.child = [i for i in c.child if i!=nd]
                c.size = removeOrient(c)
            sum += c.size
        nd.child = sorted(nd.child,key=lambda a:a.size)
        return sum
    
    root.size = removeOrient(root)
    print(f"root.size = {root.size}")
    return root

with open("../datasets/QRTD_dataset.txt",'r') as f:
    taxaList = f.readline().strip().split()
    treeSeq1 = f.readline().strip().replace(';','')
    treeSeq2 = f.readline().strip().replace(';','')

taxaPointer = {}
for t in taxaList:
    taxaPointer[t] = []

urTreeSet1 = unrootTree(treeSeq1)
urTreeSet2 = unrootTree(treeSeq2)

rootT1 = rootTree(urTreeSet1)
rootHDT2 = hdTree(urTreeSet2)



def colorLeaves(node,color):
    if len(node.child)>0:
        for c in node.child:
            if isinstance(c,str):
                colorLeaf(c,color)
            else:
                colorLeaves(c,color)

def count(nd):
    if nd.isInnerNode:
        colorLeaves(nd.child[0],(0,1,0))
        x = nodeCount(nd)
        colorLeaves(nd.child[0],(0,0,1))
        y = count(nd.child[1])
        colorLeaves(nd.child[0],(1,0,0))
        z = count(nd.child[0])
        return x+y+z

    else:
        colorLeaf(nd.taxa,(0,0,1))
        return 0











import random
ABC = [(1,0,0),(0,1,0),(0,0,1)]
def randomColor(node):
    if len(node.child)>0:
        for c in node.child:
            if isinstance(c,str):
                colorLeaf(c,random.choice(ABC))
            else:
                randomColor(c)

randomColor(rootT1)

print(f"rootHDT2.colorCode = {rootHDT2.colorCode}")
print(f"rootHDT2.child[0].colorCode = {rootHDT2.child[0].colorCode}")
print(f"rootHDT2.child[1].colorCode = {rootHDT2.child[1].colorCode}")
print(f"rootHDT2.F = {rootHDT2.F()}")


sumQuantet = []
def checker2(node):
    sumQuantet.append(node.F())
    if len(node.child)>0:
        for c in node.child:
            checker2(c)

checker2(rootHDT2)
print(f"sumAllQuantet --> {sum(i for i in sumQuantet)}")
print(f"totalQuantet  --> {int(1963*1962*1961*1960/4/3/2)}")
print(f"F=0 --> {sum(i==0 for i in sumQuantet)}")

# for i in urTreeSet1:
#     print(len(i.child),i.isInnerNode)