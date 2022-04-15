import numpy as np
from scipy.integrate import solve_ivp, odeint
import matplotlib.pyplot as plt

T = "TERMINAL"
N = "NO-TERIMAL"
C = "CONSTANT"
CT = "TABLE_CONSTANT"
TYPE = (T, N, C, CT)

class ErrorNodeAlreadyExists(Exception): pass

class Node():
    def __init__(self, t, name, val=None, hg=None):
        self.t = t        # string TYPE
        self.name = name  # string
        self.val = val    # float
        self.cons = None  # fonction
        self.pred = []    # predecesseurs
        self.succ = []    # successeurs
        self.rank = None  # rang
        if hg is not None: # ajout du noeud à l'hypergraphe hg
            hg.add_node(self)

    def __repr__(self):
        value = "None"
        if self.val is not None:
            if self.t == CT:
                l1 = ",".join([str(x) for x in self.val[0]])
                l2 = ",".join([str(x) for x in self.val[1]])
                value = "[{}]:[{}]".format(l1, l2)
            else:
                value = "{0.val:.03f} ".format(self)
        return "{0.name:<8} {3} ({0.t:<10}) IN: {1:<20} OUT: {2}".format(self, ",".join(self.get_pred_name()), ",".join(self.get_succ_name()), value)

    def set_cons(self, f, pred):
        self.cons = f
        self.pred = pred
        for p in pred:
            p.succ.append(self)

    def eval(self):
        text = "{}:{}->".format(self.name, self.val)
        self.val = self.cons(*[p.val for p in self.pred])
        text += "{}".format(self.val)
        print(text)
        
    def get_pred_name(self):
        return [p.name for p in self.pred]

    def get_succ_name(self):
        return [p.name for p in self.succ]

class Hypergraph():
    def __init__(self, nodes=[]):
        self.nodes = {n.name: n for n in nodes}
        self.nbrank = None
        self.nodesrank = None
        self.terminaux = [n for n in nodes if n.t == T]

    def __repr__(self):
        return "\n".join([str(v) for c,v in self.nodes.items()])

    def add_node(self, node):
        if node.name in self.nodes:
            print("Le Node {} existe déjà. Modifier la modélisation :".format(node.name))
            print(self.nodes[node.name])
            raise ErrorNodeAlreadyExists()
        self.nodes[node.name] = node
        if node.t == T: self.terminaux.append(node)

    def add_nodes(self, nodes):
        for n in nodes:
            self.add_node(n)

    def add_edge(self, f, x_target, x_s):
        x_target.set_cons(f, x_s)

    def eval(self):
        for ns in self.nodesrank:
            for n in ns:
                n.eval()

    def eval2(self, t, y):
        for i, n in enumerate(self.terminaux):
            n.val = y[i]
        self.eval()
        return np.array([n.val for n in self.terminaux])

    def cond(n): return n.t == N
     
    def sub_graph_vertex(self, cond):
        d2 = [name for name, n in self.nodes.items() if cond(n)]
        d1 = {name : i for i, name in enumerate(d2)}
        size = len(d2)
        gM = [[] for _ in range(size)]
        gP = [[] for _ in range(size)]
        for name in d2:
            n = self.nodes[name]
            for u in n.pred:
                if cond(u):
                    gM[d1[name]].append(d1[u.name])
                    gP[d1[u.name]].append(d1[name])
        return d2, gM, gP
        
    def set_rank(self):
        d2, gM, gP = self.sub_graph_vertex(lambda x : x.t == N)
        size = len(d2)
        dM = [len(gi) for gi in gM]
        S0 = [i for i,di in enumerate(dM) if di == 0]
        r = [None]*size
        def rang_rec(Sk, k):
            Sk1 = []
            for i in Sk:
                r[i] = k
                for j in gP[i]:
                    dM[j] -= 1
                    if dM[j] == 0:
                        Sk1.append(j)
            if len(Sk1) > 0 :
                return rang_rec(Sk1, k+1)
        rang_rec(S0, 0)
        print(d2)
        print(r)
        self.nbrank = max(r) + 1
        self.nodesrank = [[] for _ in range(self.nbrank)]
        for i, ri in enumerate(r):
            self.nodesrank[ri].append(self.nodes[d2[i]])
        self.nodesrank.append(self.terminaux)

    def set_rank2(self):
        d2 = [name for name, n in self.nodes.items() if n.t != C]
        d1 = {name : i for i, name in enumerate(d2)}
        size = len(d2)
        gM = [[] for _ in range(size)]
        gP = [[] for _ in range(size)]
        for name in d2:
            n = self.nodes[name]
            gM[d1[name]] = [d1[u.name] for u in n.pred if u.t == N]
            if n.t != T:
                gP[d1[name]] = [d1[u.name] for u in n.succ if u.t != C]
        dM = [len(gi) for gi in gM]
        S0 = [i for i,di in enumerate(dM) if di == 0]
        r = [None]*size
        def rang_rec(Sk, k):
            Sk1 = []
            for i in Sk:
                r[i] = k
                for j in gP[i]:
                    dM[j] -= 1
                    if dM[j] == 0:
                        Sk1.append(j)
            if len(Sk1) > 0 :
                return rang_rec(Sk1, k+1)
        rang_rec(S0, 0)
        print(r)
        self.nbrank = max(r) + 1
        self.nodesrank = [[] for _ in range(self.nbrank)]
        for i,ri in enumerate(r):
            self.nodesrank[ri].append(self.nodes[d2[i]])

