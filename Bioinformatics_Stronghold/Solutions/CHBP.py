##  Character-Based Phylogeny 

# Straight forward implement, may further optimized to save time/space expense.

"""
Problem
Because a tree having n
 nodes has n−1
 edges (see “Completing a Tree”), removing a single edge from a tree will produce two smaller, disjoint trees. Recall from “Creating a Character Table” that for this reason, each edge of an unrooted binary tree corresponds to a split S∣Sc
, where S
 is a subset of the taxa.

A consistent character table is one whose characters' splits do not conflict with the edge splits of some unrooted binary tree T
 on the n
 taxa. More precisely, S1∣Sc1
 conflicts with S2∣Sc2
 if all four intersections S1∩S2
, S1∩Sc2
, Sc1∩S2
, and Sc1∩Sc2
 are nonempty. As a simple example, consider the conflicting splits {a,b}∣{c,d}
 and {a,c}∣{b,d}
.

More generally, given a consistent character table C
, an unrooted binary tree T
 "models" C
 if the edge splits of T
 agree with the splits induced from the characters of C
.

Given: A list of n
 species (n≤80
) and an n
-column character table C
 in which the j
th column denotes the j
th species.

Return: An unrooted binary tree in Newick format that models C
.

Sample Dataset
cat dog elephant mouse rabbit rat
011101
001101
001100

Sample Output
(dog,(cat,rabbit),(rat,(elephant,mouse)));
"""

# Straight forward implement, may further optimized to save time/space expense.
##  define function
def chbp(taxaList, charTableList):
    class edge():
        def __init__(self) -> None:
            self.taxas = set()
            self.splits = []
            self.reverse = None
            self.nd = None
    class node():
        def __init__(self) -> None:
            self.child = []

    edges = []
    
    # Fill up nontrivial edges, different directions noted as different edges

    for ct in charTableList:
        edges.append(edge())
        edges.append(edge())
        edges[-1].reverse = edges[-2]
        edges[-2].reverse = edges[-1]
        for i in range(len(ct)):
            if ct[i] =="0":
                edges[-2].taxas.add(i)
            else:
                edges[-1].taxas.add(i)
    
    # Fill up trivial edges, one side is a the leaf, another side use completeSet
    completeSet = set([i for i in range(len(taxaList))])
    
    for i in range(len(taxaList)):
        edges.append(edge())
        edges.append(edge())
        edges[-1].reverse = edges[-2]
        edges[-2].reverse = edges[-1]
        edges[-1].taxas.add(i)
        edges[-2].taxas = completeSet

    # Find all edges in down stream of current edge

    for i in range(len(edges)):
        for j in range((i//2+1)*2, len(edges)): 
            if len(edges[i].taxas & edges[j].taxas) == 0:
                edges[i].reverse.splits.append(edges[j])
                edges[j].reverse.splits.append(edges[i])
    
    # Build the tree, only the first node (root) will recursive three sub nodes.

    def buildTree(eg,root):
        if len(eg.taxas)==1:
            return list(eg.taxas)[0]
        nd = node()
        for i in range(len(eg.splits)):
            for j in range(i+1, len(eg.splits)):
                if eg.splits[i].taxas|eg.splits[j].taxas == eg.taxas:
                    nd.child.append(buildTree(eg.splits[i],False))
                    nd.child.append(buildTree(eg.splits[j],False))
                    if root:
                        nd.child.append(buildTree(eg.reverse,False))
                    return nd

    def printTree(nd,parent):
        if nd != None:
            if isinstance(nd,int):
                return taxaList[nd]
            else:
                return f"({','.join(printTree(c,nd) for c in nd.child if c != parent)})"
    
    # excute all functions above

    root = buildTree(edges[0],True)
    return printTree(root,None)
    
##  import dataset
with open("../datasets/CHBP_dataset.txt",'r') as f:
    taxaList = f.readline().strip().split()
    charTableList = [i.strip() for i in f.readlines()] 

##  print result
print(f"{chbp(taxaList, charTableList)};")



# verify the result by excute CTBL.py to generate a charTabale, compare to original charTable by code below

# with open("charTable_original.txt",'r') as f:
#     f.readline()
#     oriCT = [i.strip() for i in f.readlines()]

# with open("charTable_new.txt",'r') as f:
#     newCT = [i.strip() for i in f.readlines()]

# mapping = str.maketrans('01', '10')

# same = 0
# diff = 0

# for i in oriCT:
#     if i in newCT or i.translate(mapping) in newCT:
#         same +=1
#     else:
#         diff +=1

# print(same, diff)

