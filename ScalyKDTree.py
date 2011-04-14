import math

class KDNode(object):
    def __init__(self,point,disc):
        assert isinstance(point,tuple)
        assert isinstance(disc,int)
        assert disc >= 0 and disc < len(point)

        self.point = point
        self.disc = disc
        self.left = None
        self.right = None

    def __repr__(self):
        return 'KDNode(' + str(self.point) + ',' + str(self.disc) + ')'

    def __str__(self):
        return '(' + str(self.disc) + '|' + ','.join(map(str,self.point)) + ')'

    def __len__(self):
        return len(self.point)

    def __getitem__(self,key):
        assert key >= 0 and key < len(self.point)

        return self.point[key]

    def equal_with_mask(self,point,mask):
        assert isinstance(point,KDNode) or isinstance(point,tuple)
        assert isinstance(mask,tuple)
        assert len(self.point) == len(point)
        assert len(point) == len(mask)
        assert all(map(lambda x: isinstance(x,bool),mask))

        for i in range(0,len(point)):
            if mask[i] and self.point[i] != point[i]:
                return False

        return True

class KDTree(object):
    def __init__(self,size):
        assert isinstance(size,int)
        assert size > 1

        self.root = None
        self.size = size

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
    def _insert(size,node,point):
        if point[node.disc] <= node.point[node.disc]:
            if node.left == None:
                node.left = KDNode(point,(node.disc + 1) % size)
            else:
                KDTree._insert(size,node.left,point)
        else:
            if node.right == None:
                node.right = KDNode(point,(node.disc + 1) % size)
            else:
                KDTree._insert(size,node.right,point)

    @staticmethod
    def _find_exact(size,node,point):
        if node == None:
            return None
        elif node.point == point:
            return node
        else:
            if point[node.disc] <= node.point[node.disc]:
                return KDTree._find_exact(size,node.left,point)
            else:
                return KDTree._find_exact(size,node.right,point)

    @staticmethod
    def _find_with_mask(size,node,point,mask,result):
        if node == None:
            return result
        else:
            if node.equal_with_mask(point,mask):
                result.append(node)

            if mask[node.disc]:
                if point[node.disc] < node.point[node.disc]:
                    KDTree._find_with_mask(size,node.left,point,mask,result)
                elif point[node.disc] > node.point[node.disc]:
                    KDTree._find_with_mask(size,node.right,point,mask,result)
                else:
                    KDTree._find_with_mask(size,node.left,point,mask,result)
                    KDTree._find_with_mask(size,node.right,point,mask,result)
            else:
                KDTree._find_with_mask(size,node.left,point,mask,result)
                KDTree._find_with_mask(size,node.right,point,mask,result)

            return result

    @staticmethod
    def _node_point_distance(node,point):
        return math.sqrt(sum(map(lambda (x,y): (x - y)*(x - y),zip(node.point,point))))

    @staticmethod
    def _find_nearest(size,node,point,debug_path):
        if node == None:
            return (None,float("inf"))
        else:
            if debug_path:
                print node

            if node.equal_with_mask(point,(True,) * size):
                return (node,0)
            elif point[node.disc] < node.point[node.disc]:
                (best,distance) = KDTree._find_nearest(size,node.left,point,debug_path)
                direction = 0
            else:
                (best,distance) = KDTree._find_nearest(size,node.right,point,debug_path)
                direction = 1

            if KDTree._node_point_distance(node,point) < distance:
                (best,distance) = (node,KDTree._node_point_distance(node,point))

            if math.fabs(node.point[node.disc] - point[node.disc]) < distance:
                if direction == 0:
                    (alt_best,alt_distance) = KDTree._find_nearest(size,node.right,point,debug_path)
                else:
                    (alt_best,alt_distance) = KDTree._find_nearest(size,node.left,point,debug_path)

                if alt_distance < distance:
                    return (alt_best,alt_distance)
                else:
                    return (best,distance)
            else:
                return (best,distance)

    def __str__(self):
        return KDTree._node_to_str(self.root,0,'r')

    def insert(self,point):
        assert isinstance(point,tuple)
        assert len(point) == self.size

        if self.root == None:
            self.root = KDNode(point,0)
        else:
            KDTree._insert(self.size,self.root,point)

        return self

    def find_exact(self,point):
        assert isinstance(point,tuple)
        assert len(point) == self.size

        return KDTree._find_exact(self.size,self.root,point)

    def find_with_mask(self,point,mask):
        assert isinstance(point,tuple)
        assert isinstance(mask,tuple)
        assert len(point) == self.size
        assert len(mask) == self.size
        assert all(map(lambda x: isinstance(x,bool),mask))

        return KDTree._find_with_mask(self.size,self.root,point,mask,[])

    def find_nearest(self,point,debug_path=False):
        assert isinstance(point,tuple)
        assert isinstance(debug_path,bool)
        assert len(point) == self.size

        return KDTree._find_nearest(self.size,self.root,point,debug_path)[0]

def make_for_test1():
    q = KDTree()

    q.insert((1,2))
    q.insert((5,3))
    q.insert((0.5,5))
    q.insert((0.5,6))
    q.insert((0.4,3))
    q.insert((4,4))
    q.insert((7,7))
    q.insert((6,6))

    return q

def make_for_test2():
    q = KDTree()

    q.insert((5,5))
    q.insert((2,3))
    q.insert((2,4))
    q.insert((3,6))
    q.insert((8,2))
    q.insert((6,7))
    q.insert((8,4))
    q.insert((8,1))
    q.insert((6,2))
    q.insert((9,2))
    q.insert((4.95,0.25))

    return q
