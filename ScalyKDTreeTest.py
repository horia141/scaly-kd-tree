import unittest

from ScalyKDTree import KDTree

class KDNodeTest(unittest.TestCase):
    'Test harness for "KDNode".'

    def test_ctor(self):
        'Constructor.'

        a = KDTree.KDNode((1,2),0)

        self.assertEqual(a.point[0],1)
        self.assertEqual(a.point[1],2)
        self.assertEqual(a.disc,0)

        b = KDTree.KDNode((1,2,3,4),2)

        self.assertEqual(b.point[0],1)
        self.assertEqual(b.point[1],2)
        self.assertEqual(b.point[2],3)
        self.assertEqual(b.point[3],4)
        self.assertEqual(b.disc,2)

        c = KDTree.KDNode((1,),0)

        self.assertEqual(c.point[0],1)

        self.assertRaises(AssertionError,KDTree.KDNode,'hello',3)
        self.assertRaises(AssertionError,KDTree.KDNode,(1,2),'j')
        self.assertRaises(AssertionError,KDTree.KDNode,'hello','j')
        self.assertRaises(AssertionError,KDTree.KDNode,(1,2,3),4)

    def test_repr(self):
        'Python representation.'

        a = KDTree.KDNode((1,2,3),2)

        self.assertEqual(repr(a),'KDTree.KDNode((1, 2, 3),2)')

    def test_str(self):
        'String representation.'

        a = KDTree.KDNode((1,2,3),1)

        self.assertEqual(str(a),'(1|1,2,3)')

    def test_eq(self):
        'Node equality.'

        a = KDTree.KDNode((1,2),0)
        b = KDTree.KDNode((1,2),0)
        c = KDTree.KDNode((1,2),1)
        d = KDTree.KDNode((3,1),1)

        self.assertEqual(a,b)
        self.assertEqual(a,c)
        self.assertNotEqual(a,d)
        self.assertEqual(a,(1,2))
        self.assertNotEqual(a,(3,1))

        self.assertNotEqual(a,KDTree.KDNode((1,2,3),0))
        self.assertNotEqual(a,(1,2,3))
        self.assertNotEqual(a,'hello')

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

        self.assertTrue(a.root,(1,1,1))

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

        self.assertTrue(b.root,(5,5))
        self.assertTrue(b.root.left,(2,3))
        self.assertTrue(b.root.left.left,(4.95,0.25))
        self.assertTrue(b.root.left.right,(2,4))
        self.assertTrue(b.root.left.right.right,(3,5))
        self.assertTrue(b.root.right,(8,2))
        self.assertTrue(b.root.right.left,(8,1))
        self.assertTrue(b.root.right.left.left,(6,2))
        self.assertTrue(b.root.right.left.right,(9,2))
        self.assertTrue(b.root.right.right,(6,7))
        self.assertTrue(b.root.right.right.right,(8,4))

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

        self.assertEqual(a.find_exact((5,5)),(5,5))
        self.assertEqual(a.find_exact((2,3)),(2,3))
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

        self.assertEqual(a.find_with_mask((8,-1),(True,False)),[(8,2),(8,1),(8,4)])
        self.assertEqual(a.find_with_mask((6,-1),(True,False)),[(6,2),(6,7)])
        self.assertEqual(a.find_with_mask((8,1),(True,True)),[(8,1)])
        self.assertEqual(a.find_with_mask((1,2),(True,True)),[])

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

        self.assertEqual(a.find_nearest((7.5,2.5)),(8,2))
        self.assertEqual(a.find_nearest((7.5,1.5)),(8,1))
        self.assertEqual(a.find_nearest((5.01,0.22)),(4.95,0.25))
        self.assertEqual(a.find_nearest((3,6)),(3,6))
        self.assertEqual(a.find_nearest((5,5)),(5,5))
        self.assertEqual(a.find_nearest((8,3)),(8,4))

        self.assertRaises(AssertionError,KDTree.find_nearest,a,'hello')
        self.assertRaises(AssertionError,KDTree.find_nearest,a,(1,2,3))
        self.assertRaises(AssertionError,KDTree.find_nearest,a,(1,2),'yello')
