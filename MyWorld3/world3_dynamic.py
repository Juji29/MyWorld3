C = "CONSTANT"
CT = "CONSTANT_TABLE"

class ErrorNodeAlreadyExists(Exception): pass


class Node:
    def __init__(self, name, val=None, hg=None):
        self.name = name  # string
        self.val = val    # float
        self.cons = None  # function
        self.pred = []    # predecessors
        self.succ = []    # successors
        self.rank = None  # rank
        if hg is not None:  # add node to a hypergraph hg
            hg.add_node(self)

    def __repr__(self):
        value = "None"
        if self.val:
            value = "{:.03f}".format(self.val)
        return "{0.name:<8} {3} IN: {1:<20} OUT: {2}".format(self, ",".join(self.get_pred_name()), ",".join(self.get_succ_name()), value)

    def set_cons(self, f, pred):
        self.cons = f
        self.pred = pred
        for p in pred:
            p.succ.append(self)

    def get_pred_name(self):
        return [p.name for p in self.pred]

    def get_succ_name(self):
        return [p.name for p in self.succ]


class NodeStock(Node):
    def __init__(self, name, val=None, hg=None):
        super().__init__(name, val, hg)
        self.hist = [val]

    def eval(self, ts, save=True):
        # text = "{}:{}->".format(self.name, self.val)
        if self.val:
            self.val = self.val + self.cons(*[p.val for p in self.pred]) * ts
        else:
            self.val = self.cons(*[p.val for p in self.pred]) * ts
        if save:
            self.hist.append(self.val)
        # text += "{}".format(self.val)
        # print(text)


class NodeFlow(Node):
    def __init__(self, name, val=None, hg=None):
        super().__init__(name, val, hg)
        self.hist = []

    def eval(self, dt, save=True):
        # text = "{}:{}->".format(self.name, self.val)
        self.val = self.cons(*[p.val for p in self.pred])
        if save:
            self.hist.append(self.val)
        # text += "{}".format(self.val)
        # print(text)

class NodeDelay3(Node):
    def __init__(self, name, val=None, hg=None):
        super().__init__(name, val, hg)
        self.hist = []
        self.cst = None
        self.node = None
        self.I1 = None
        self.I2 = None
        self.I3 = None

    def eval(self, ts, save=True):
        # text = "{}:{}->".format(self.name, self.val)
        self.cons(*[p.val for p in self.pred])
        dl = self.cst / 3
        RT1 = self.I1 / dl
        self.I1 = self.I1 + (self.node - RT1) * ts
        RT2 = self.I2 / dl
        self.I2 = self.I2 + (RT1 - RT2) * ts
        self.I3 = self.I3 + (RT2 - self.I3 / dl) * ts
        self.val = self.I3 / dl
        if save:
            self.hist.append(self.val)
        # text += "{}".format(self.val)
        # print(text)

    def f_delayinit(self, flow, constant):
        self.node = flow
        self.cst = constant
        if not self.hist:
            self.val = flow
            self.I1 = self.I2 = self.I3 = flow * constant / 3


class NodeConstant(Node):
    def __init__(self, name, t, val=None, hg=None):
        super().__init__(name, val, hg)
        self.type = t

    def __repr__(self):
        value = "None"
        if self.val is not None:
            if self.type == CT:
                l1 = ",".join([str(x) for x in self.val[0]])
                l2 = ",".join([str(x) for x in self.val[1]])
                value = "[{}]:[{}]".format(l1, l2)
            else:
                value = "{0.val:.03f} ".format(self)
        return "{0.name:<8} {3} IN: {1:<20} OUT: {2}".format(self, ",".join(self.get_pred_name()), ",".join(self.get_succ_name()), value)


class Hypergraph():
    def __init__(self, version, nodes=[]):
        self.nodes = {n.name: n for n in nodes}
        self.version = version
        self.nbrank = None
        self.nodesrank = None
        self.stocks = [n for n in nodes if type(n) == NodeStock]

    def __repr__(self):
        return "\n".join([str(v) for c,v in self.nodes.items()])

    def add_node(self, node):
        if node.name in self.nodes:
            print("Node {} already exists. Modify the modelling :".format(node.name))
            print(self.nodes[node.name])
            raise ErrorNodeAlreadyExists()
        self.nodes[node.name] = node
        if type(node) == NodeStock:
            self.stocks.append(node)

    def add_nodes(self, nodes):
        for n in nodes:
            self.add_node(n)

    def add_edge(self, f, x_target, x_s):
        x_target.set_cons(f, x_s)

    def eval(self, ts):
        for ns in self.nodesrank:
            ns.eval(ts)

    def run(self, it, ft, ts):
        nb_step = int((ft - it) / ts)
        for i in range(nb_step):
            self.eval(ts)
        for stock in self.stocks:
            stock.hist.pop()

    def sub_graph_vertex(self, cond):
        d2 = [name for name, n in self.nodes.items() if cond(n)]
        d1 = {name: i for i, name in enumerate(d2)}
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
        d2, gM, gP = self.sub_graph_vertex(lambda x: type(x) == NodeDelay3 or type(x) == NodeFlow)
        size = len(d2)
        dM = [len(gi) for gi in gM]
        S0 = [i for i, di in enumerate(dM) if di == 0]
        r = [None] * size

        def rang_rec(Sk, k):
            Sk1 = []
            for i in Sk:
                r[i] = k
                for j in gP[i]:
                    dM[j] -= 1
                    if dM[j] == 0:
                        Sk1.append(j)
            if len(Sk1) > 0:
                return rang_rec(Sk1, k+1)

        rang_rec(S0, 0)
        self.nbrank = max(r) + 1
        self.nodesrank = [self.nodes[d2[j]] for _, j in sorted([(ri, i) for i, ri in enumerate(r)])]
        self.nodesrank += self.stocks
