import unittest

from ScalyKDTree import KDNode
from ScalyKDTree import KDTree

class KDNodeTest(unittest.TestCase):
    'Test harness for "KDNode".'

    def test_ctor(self):
        'Constructor.'

        a = KDNode((1,2),0)

        self.assertEqual(a.point[0],1)
        self.assertEqual(a.point[1],2)
        self.assertEqual(a.disc,0)

        b = KDNode((1,2,3,4),2)

        self.assertEqual(b.point[0],1)
        self.assertEqual(b.point[1],2)
        self.assertEqual(b.point[2],3)
        self.assertEqual(b.point[3],4)
        self.assertEqual(b.disc,2)

        c = KDNode((1,),0)

        self.assertEqual(c.point[0],1)

        self.assertRaises(AssertionError,KDNode,'hello',3)
        self.assertRaises(AssertionError,KDNode,(1,2),'j')
        self.assertRaises(AssertionError,KDNode,'hello','j')
        self.assertRaises(AssertionError,KDNode,(1,2,3),4)

    def test_repr(self):
        'Python representation.'

        a = KDNode((1,2,3),2)

        self.assertEqual(repr(a),'KDNode((1, 2, 3),2)')

    def test_str(self):
        'String representation.'

        a = KDNode((1,2,3),1)

        self.assertEqual(str(a),'(1|1,2,3)')

    def test_len(self):
        'Obtaining the length.'

        a = KDNode((1,2,3),1)

        self.assertEqual(len(a),3)
        
        b = KDNode((1,),0)

        self.assertEqual(len(b),1)

        c = KDNode((1,2,4,10,20),4)

        self.assertEqual(len(c),5)

    def test_getitem(self):
        'Array addressing.'

        a = KDNode((1,2,3),1)
        
        self.assertEqual(a[0],1)
        self.assertEqual(a[1],2)
        self.assertEqual(a[2],3)

        self.assertRaises(AssertionError,KDNode.__getitem__,a,4)
        self.assertRaises(AssertionError,KDNode.__getitem__,a,-2)

    def test_equal_with_mask(self):
        'Masked equality.'

        a = KDNode((1,3,2),1)
        b = KDNode((1,3,2),1)
        c = KDNode((1,4,2),2)

        self.assertTrue(a.equal_with_mask(b,(True,True,True)))
        self.assertFalse(a.equal_with_mask(c,(True,True,True)))
        self.assertTrue(a.equal_with_mask(c,(True,False,True)))
        self.assertTrue(a.equal_with_mask(b,(True,False,True)))
        self.assertTrue(a.equal_with_mask(b,(False,False,False)))
        self.assertTrue(a.equal_with_mask(c,(False,False,False)))

        self.assertTrue(a.equal_with_mask((1,3,2),(True,True,True)))
        self.assertFalse(a.equal_with_mask((1,4,2),(True,True,True)))
        self.assertTrue(a.equal_with_mask((1,4,2),(True,False,True)))
        self.assertTrue(a.equal_with_mask((1,3,2),(True,False,True)))
        self.assertTrue(a.equal_with_mask((1,3,2),(False,False,False)))
        self.assertTrue(a.equal_with_mask((1,4,2),(False,False,False)))

        self.assertRaises(AssertionError,KDNode.equal_with_mask,a,'ola',(True,True,True))
        self.assertRaises(AssertionError,KDNode.equal_with_mask,a,(1,2,3),'time')
        self.assertRaises(AssertionError,KDNode.equal_with_mask,a,(1,2,3,4),(True,False,True))
        self.assertRaises(AssertionError,KDNode.equal_with_mask,a,(1,2,3),(True,False,True,False))
        self.assertRaises(AssertionError,KDNode.equal_with_mask,a,(3,2,1),(1,0,0))
        

class KDTreeTest(unittest.TestCase):
    'Test harness for "KDTree".'

    def test_ctor(self):
        'Constructor.'

        a = KDTree(2)

        self.assertEqual(a.root,None)
        self.assertEqual(a.size,2)

        self.assertRaises(AssertionError,KDTree,'t')
        self.assertRaises(AssertionError,KDTree,0)

    def test_insert(self):
        'Insertion.'

        a = KDTree(3)

        a.insert((1,1,1))

        self.assertTrue(a.root.equal_with_mask((1,1,1),(True,True,True)))

        b = KDTree(2)

        b.insert((5,5))
        b.insert((2,3))
        b.insert((2,4))
        b.insert((3,6))
        b.insert((8,2))
        b.insert((6,7))
        b.insert((8,4))
        b.insert((8,1))
        b.insert((6,2))
        b.insert((9,2))
        b.insert((4.95,0.25))

        self.assertTrue(b.root.equal_with_mask((5,5),(True,True)))
        self.assertTrue(b.root.left.equal_with_mask((2,3),(True,True)))
        self.assertTrue(b.root.left.left.equal_with_mask((4.95,0.25),(True,True)))
        self.assertTrue(b.root.left.right.equal_with_mask((2,4),(True,True)))
        self.assertTrue(b.root.left.right.right.equal_with_mask((3,6),(True,True)))
        self.assertTrue(b.root.right.equal_with_mask((8,2),(True,True)))
        self.assertTrue(b.root.right.left.equal_with_mask((8,1),(True,True)))
        self.assertTrue(b.root.right.left.left.equal_with_mask((6,2),(True,True)))
        self.assertTrue(b.root.right.left.right.equal_with_mask((9,2),(True,True)))
        self.assertTrue(b.root.right.right.equal_with_mask((6,7),(True,True)))
        self.assertTrue(b.root.right.right.right.equal_with_mask((8,4),(True,True)))

        c = KDTree(3)

        self.assertRaises(AssertionError,KDTree.insert,c,'hello')
        self.assertRaises(AssertionError,KDTree.insert,c,(1,2))

    def test_find_exact(self):
        'Find exact match.'

        a = KDTree(2)

        a.insert((5,5))
        a.insert((2,3))
        a.insert((2,4))
        a.insert((3,6))
        a.insert((8,2))
        a.insert((6,7))
        a.insert((8,4))
        a.insert((8,1))
        a.insert((6,2))
        a.insert((9,2))
        a.insert((4.95,0.25))

        self.assertEqual(a.find_exact((5,5)).point,(5,5))
        self.assertEqual(a.find_exact((2,3)).point,(2,3))
        self.assertEqual(a.find_exact((5,8)),None)

        self.assertRaises(AssertionError,KDTree.find_exact,a,'hello')
        self.assertRaises(AssertionError,KDTree.find_exact,a,(1,2,3))

    def test_find_with_mask(self):
        'Find masked match.'

        a = KDTree(2)

        a.insert((5,5))
        a.insert((2,3))
        a.insert((2,4))
        a.insert((3,6))
        a.insert((8,2))
        a.insert((6,7))
        a.insert((8,4))
        a.insert((8,1))
        a.insert((6,2))
        a.insert((9,2))
        a.insert((4.95,0.25))

        self.assertEqual(map(lambda x: x.point,a.find_with_mask((8,-1),(True,False))),[(8,2),(8,1),(8,4)])
        self.assertEqual(map(lambda x: x.point,a.find_with_mask((6,-1),(True,False))),[(6,2),(6,7)])
        self.assertEqual(map(lambda x: x.point,a.find_with_mask((8,1),(True,True))),[(8,1)])
        self.assertEqual(map(lambda x: x.point,a.find_with_mask((1,2),(True,True))),[])

        self.assertRaises(AssertionError,KDTree.find_with_mask,a,'helo',(True,False))
        self.assertRaises(AssertionError,KDTree.find_with_mask,a,(1,2),'j')
        self.assertRaises(AssertionError,KDTree.find_with_mask,a,'helo','j')
        self.assertRaises(AssertionError,KDTree.find_with_mask,a,(1,2,3),(True,False))
        self.assertRaises(AssertionError,KDTree.find_with_mask,a,(1,2),(True,True,False))
        self.assertRaises(AssertionError,KDTree.find_with_mask,a,(1,2),(True,True,'true'))

    def test_find_nearest(self):
        'Find nearest match.'

        a = KDTree(2)

        a.insert((5,5))
        a.insert((2,3))
        a.insert((2,4))
        a.insert((3,6))
        a.insert((8,2))
        a.insert((6,7))
        a.insert((8,4))
        a.insert((8,1))
        a.insert((6,2))
        a.insert((9,2))
        a.insert((4.95,0.25))

        self.assertEqual(a.find_nearest((7.5,2.5)).point,(8,2))
        self.assertEqual(a.find_nearest((7.5,1.5)).point,(8,1))
        self.assertEqual(a.find_nearest((5.01,0.22)).point,(4.95,0.25))
        self.assertEqual(a.find_nearest((3,6)).point,(3,6))
        self.assertEqual(a.find_nearest((5,5)).point,(5,5))
        self.assertEqual(a.find_nearest((8,3)).point,(8,4))

        self.assertRaises(AssertionError,KDTree.find_nearest,a,'hello')
        self.assertRaises(AssertionError,KDTree.find_nearest,a,(1,2,3))
        self.assertRaises(AssertionError,KDTree.find_nearest,a,(1,2),'yello')
