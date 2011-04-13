POINT_SIZE = 2

class KDNode(object):
    def __init__(self,point,disc):
        assert isinstance(point,tuple)
        assert isinstance(disc,int)
        assert len(point) == POINT_SIZE
        assert disc >= 0 and disc < POINT_SIZE

        self.point = point
        self.disc = disc
        self.left = None
        self.right = None

    def __repr__(self):
        return 'KDNode(' + str(self.point) + ',' + str(self.disc) + ')'

    def __str__(self):
        return '(' + str(self.disc) + '|' + ','.join(map(str,self.point)) + ')'

class KDTree(object):
    def __init__(self):
        self.root = None

    @staticmethod
    def _node_to_str(node,level,mode):
        if node != None:
            c_str = ' ' * level + mode + ':' + str(node)
            l_str = KDTree._node_to_str(node.left,level + 2,'l')
            r_str = KDTree._node_to_str(node.right,level + 2,'r')

            return c_str + ('\n' + l_str if l_str != '' else '') + \
                           ('\n' + r_str if r_str != '' else '')
        else:
            return ''
        
    @staticmethod
    def _insert(node,point):
        if point[node.disc] < node.point[node.disc]:
            if node.left == None:
                node.left = KDNode(point,(node.disc + 1) % POINT_SIZE)
            else:
                KDTree._insert(node.left,point)
        else:
            if node.right == None:
                node.right = KDNode(point,(node.disc + 1) % POINT_SIZE)
            else:
                KDTree._insert(node.right,point)

    def __str__(self):
        return KDTree._node_to_str(self.root,0,'r')

    def insert(self,point):
        assert isinstance(point,tuple)
        assert len(point) == POINT_SIZE

        if self.root == None:
            self.root = KDNode(point,0)
        else:
            KDTree._insert(self.root,point)

        return self
