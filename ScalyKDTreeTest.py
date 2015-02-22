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

    def test_iris(self):
        'A test with the IRIS dataset.'

        train = [(6.5000,    3.0000,    5.2000,    2.0000),
                 (5.2000,    4.1000,    1.5000,    0.1000),
                 (5.7000,    3.0000,    4.2000,    1.2000),
                 (5.0000,    2.0000,    3.5000,    1.0000),
                 (7.3000,    2.9000,    6.3000,    1.8000),
                 (4.7000,    3.2000,    1.3000,    0.2000),
                 (4.4000,    3.2000,    1.3000,    0.2000),
                 (5.1000,    3.5000,    1.4000,    0.2000),
                 (4.8000,    3.4000,    1.9000,    0.2000),
                 (6.9000,    3.1000,    5.4000,    2.1000),
                 (6.7000,    2.5000,    5.8000,    1.8000),
                 (4.6000,    3.1000,    1.5000,    0.2000),
                 (5.7000,    3.8000,    1.7000,    0.3000),
                 (7.7000,    2.8000,    6.7000,    2.0000),
                 (5.8000,    2.7000,    5.1000,    1.9000),
                 (5.4000,    3.9000,    1.7000,    0.4000),
                 (7.7000,    2.6000,    6.9000,    2.3000),
                 (5.0000,    3.2000,    1.2000,    0.2000),
                 (5.5000,    2.5000,    4.0000,    1.3000),
                 (6.6000,    3.0000,    4.4000,    1.4000),
                 (4.9000,    2.4000,    3.3000,    1.0000),
                 (5.1000,    3.8000,    1.5000,    0.3000),
                 (4.9000,    3.1000,    1.5000,    0.1000),
                 (6.7000,    3.3000,    5.7000,    2.1000),
                 (6.2000,    2.2000,    4.5000,    1.5000),
                 (5.1000,    2.5000,    3.0000,    1.1000),
                 (4.9000,    3.1000,    1.5000,    0.2000),
                 (5.2000,    2.7000,    3.9000,    1.4000),
                 (5.4000,    3.4000,    1.7000,    0.2000),
                 (6.3000,    3.3000,    4.7000,    1.6000),
                 (5.7000,    2.8000,    4.1000,    1.3000),
                 (5.6000,    2.9000,    3.6000,    1.3000),
                 (6.3000,    2.5000,    4.9000,    1.5000),
                 (4.9000,    3.6000,    1.4000,    0.1000),
                 (6.9000,    3.1000,    5.1000,    2.3000),
                 (6.7000,    3.0000,    5.0000,    1.7000),
                 (6.1000,    2.6000,    5.6000,    1.4000),
                 (5.5000,    2.4000,    3.8000,    1.1000),
                 (6.7000,    3.1000,    5.6000,    2.4000),
                 (5.0000,    2.3000,    3.3000,    1.0000),
                 (6.0000,    2.7000,    5.1000,    1.6000),
                 (6.3000,    2.7000,    4.9000,    1.8000),
                 (5.1000,    3.8000,    1.9000,    0.4000),
                 (7.2000,    3.2000,    6.0000,    1.8000),
                 (6.3000,    3.4000,    5.6000,    2.4000),
                 (5.5000,    2.4000,    3.7000,    1.0000),
                 (4.8000,    3.1000,    1.6000,    0.2000),
                 (7.0000,    3.2000,    4.7000,    1.4000),
                 (6.2000,    2.9000,    4.3000,    1.3000),
                 (7.2000,    3.6000,    6.1000,    2.5000),
                 (7.7000,    3.8000,    6.7000,    2.2000),
                 (5.1000,    3.4000,    1.5000,    0.2000),
                 (6.3000,    2.3000,    4.4000,    1.3000),
                 (6.7000,    3.3000,    5.7000,    2.5000),
                 (6.7000,    3.1000,    4.4000,    1.4000),
                 (5.5000,    3.5000,    1.3000,    0.2000),
                 (6.1000,    2.8000,    4.0000,    1.3000),
                 (6.0000,    2.9000,    4.5000,    1.5000),
                 (5.9000,    3.0000,    5.1000,    1.8000),
                 (5.1000,    3.7000,    1.5000,    0.4000),
                 (5.0000,    3.0000,    1.6000,    0.2000),
                 (6.8000,    3.0000,    5.5000,    2.1000),
                 (5.2000,    3.5000,    1.5000,    0.2000),
                 (5.3000,    3.7000,    1.5000,    0.2000),
                 (4.8000,    3.0000,    1.4000,    0.3000),
                 (6.3000,    3.3000,    6.0000,    2.5000),
                 (5.6000,    2.8000,    4.9000,    2.0000),
                 (5.7000,    2.9000,    4.2000,    1.3000),
                 (6.1000,    2.8000,    4.7000,    1.2000),
                 (5.4000,    3.4000,    1.5000,    0.4000),
                 (5.4000,    3.9000,    1.3000,    0.4000),
                 (6.2000,    2.8000,    4.8000,    1.8000),
                 (5.7000,    4.4000,    1.5000,    0.4000),
                 (6.4000,    2.8000,    5.6000,    2.1000),
                 (5.6000,    3.0000,    4.5000,    1.5000),
                 (6.3000,    2.9000,    5.6000,    1.8000),
                 (6.4000,    2.9000,    4.3000,    1.3000),
                 (4.4000,    3.0000,    1.3000,    0.2000),
                 (7.4000,    2.8000,    6.1000,    1.9000),
                 (4.8000,    3.4000,    1.6000,    0.2000),
                 (5.0000,    3.6000,    1.4000,    0.2000),
                 (5.0000,    3.4000,    1.6000,    0.4000),
                 (6.1000,    3.0000,    4.9000,    1.8000),
                 (6.5000,    3.2000,    5.1000,    2.0000),
                 (6.5000,    3.0000,    5.5000,    1.8000),
                 (5.5000,    2.3000,    4.0000,    1.3000),
                 (5.1000,    3.8000,    1.6000,    0.2000),
                 (5.9000,    3.0000,    4.2000,    1.5000),
                 (5.7000,    2.6000,    3.5000,    1.0000),
                 (5.6000,    3.0000,    4.1000,    1.3000),
                 (6.8000,    2.8000,    4.8000,    1.4000),
                 (5.6000,    2.7000,    4.2000,    1.3000),
                 (7.1000,    3.0000,    5.9000,    2.1000),
                 (6.2000,    3.4000,    5.4000,    2.3000),
                 (6.0000,    2.2000,    5.0000,    1.5000),
                 (5.8000,    2.7000,    3.9000,    1.2000),
                 (4.7000,    3.2000,    1.6000,    0.2000),
                 (6.4000,    2.8000,    5.6000,    2.2000),
                 (4.9000,    2.5000,    4.5000,    1.7000),
                 (5.9000,    3.2000,    4.8000,    1.8000)]

        test = [(4.3000,    3.0000,    1.1000,    0.1000),
                (6.4000,    2.7000,    5.3000,    1.9000),
                (5.2000,    3.4000,    1.4000,    0.2000),
                (5.4000,    3.7000,    1.5000,    0.2000),
                (6.9000,    3.1000,    4.9000,    1.5000),
                (5.7000,    2.8000,    4.5000,    1.3000),
                (5.8000,    2.7000,    5.1000,    1.9000),
                (6.1000,    2.9000,    4.7000,    1.4000),
                (6.4000,    3.1000,    5.5000,    1.8000),
                (6.3000,    2.5000,    5.0000,    1.9000),
                (7.7000,    3.0000,    6.1000,    2.3000),
                (4.9000,    3.0000,    1.4000,    0.2000),
                (6.0000,    3.0000,    4.8000,    1.8000),
                (6.5000,    3.0000,    5.8000,    2.2000),
                (6.5000,    2.8000,    4.6000,    1.5000),
                (7.6000,    3.0000,    6.6000,    2.1000),
                (6.4000,    3.2000,    4.5000,    1.5000),
                (5.8000,    2.8000,    5.1000,    2.4000),
                (4.4000,    2.9000,    1.4000,    0.2000),
                (6.7000,    3.1000,    4.7000,    1.5000),
                (5.0000,    3.5000,    1.6000,    0.6000),
                (6.9000,    3.2000,    5.7000,    2.3000),
                (6.7000,    3.0000,    5.2000,    2.3000),
                (5.8000,    4.0000,    1.2000,    0.2000),
                (5.1000,    3.3000,    1.7000,    0.5000),
                (5.0000,    3.4000,    1.5000,    0.2000),
                (5.8000,    2.6000,    4.0000,    1.2000),
                (4.6000,    3.4000,    1.4000,    0.3000),
                (5.7000,    2.5000,    5.0000,    2.0000),
                (5.4000,    3.0000,    4.5000,    1.5000),
                (5.1000,    3.5000,    1.4000,    0.3000),
                (4.6000,    3.6000,    1.0000,    0.2000),
                (6.8000,    3.2000,    5.9000,    2.3000),
                (5.6000,    2.5000,    3.9000,    1.1000),
                (7.2000,    3.0000,    5.8000,    1.6000),
                (6.1000,    3.0000,    4.6000,    1.4000),
                (6.0000,    2.2000,    4.0000,    1.0000),
                (5.5000,    2.6000,    4.4000,    1.2000),
                (4.5000,    2.3000,    1.3000,    0.3000),
                (4.6000,    3.2000,    1.4000,    0.2000),
                (7.9000,    3.8000,    6.4000,    2.0000),
                (5.0000,    3.5000,    1.3000,    0.3000),
                (6.3000,    2.8000,    5.1000,    1.5000),
                (6.4000,    3.2000,    5.3000,    2.3000),
                (4.8000,    3.0000,    1.4000,    0.1000),
                (5.8000,    2.7000,    4.1000,    1.0000),
                (6.0000,    3.4000,    4.5000,    1.6000),
                (5.0000,    3.3000,    1.4000,    0.2000),
                (5.5000,    4.2000,    1.4000,    0.2000),
                (6.6000,    2.9000,    4.6000,    1.3000)]

        found = [(4.4000,    3.0000,    1.3000,    0.2000),
                 (6.5000,    3.0000,    5.2000,    2.0000),
                 (5.2000,    3.5000,    1.5000,    0.2000),
                 (5.3000,    3.7000,    1.5000,    0.2000),
                 (7.0000,    3.2000,    4.7000,    1.4000),
                 (5.6000,    3.0000,    4.5000,    1.5000),
                 (5.8000,    2.7000,    5.1000,    1.9000),
                 (6.1000,    2.8000,    4.7000,    1.2000),
                 (6.5000,    3.0000,    5.5000,    1.8000),
                 (6.3000,    2.7000,    4.9000,    1.8000),
                 (7.4000,    2.8000,    6.1000,    1.9000),
                 (4.9000,    3.1000,    1.5000,    0.2000),
                 (6.1000,    3.0000,    4.9000,    1.8000),
                 (6.4000,    2.8000,    5.6000,    2.2000),
                 (6.6000,    3.0000,    4.4000,    1.4000),
                 (7.7000,    2.8000,    6.7000,    2.0000),
                 (6.3000,    3.3000,    4.7000,    1.6000),
                 (5.6000,    2.8000,    4.9000,    2.0000),
                 (4.4000,    3.0000,    1.3000,    0.2000),
                 (6.7000,    3.1000,    4.4000,    1.4000),
                 (5.0000,    3.4000,    1.6000,    0.4000),
                 (6.7000,    3.1000,    5.6000,    2.4000),
                 (6.9000,    3.1000,    5.1000,    2.3000),
                 (5.4000,    3.9000,    1.3000,    0.4000),
                 (5.0000,    3.4000,    1.6000,    0.4000),
                 (5.1000,    3.4000,    1.5000,    0.2000),
                 (5.8000,    2.7000,    3.9000,    1.2000),
                 (4.7000,    3.2000,    1.3000,    0.2000),
                 (5.8000,    2.7000,    5.1000,    1.9000),
                 (5.6000,    3.0000,    4.5000,    1.5000),
                 (5.1000,    3.5000,    1.4000,    0.2000),
                 (4.7000,    3.2000,    1.3000,    0.2000),
                 (6.7000,    3.3000,    5.7000,    2.1000),
                 (5.5000,    2.4000,    3.8000,    1.1000),
                 (7.2000,    3.2000,    6.0000,    1.8000),
                 (6.0000,    2.9000,    4.5000,    1.5000),
                 (5.5000,    2.4000,    3.8000,    1.1000),
                 (5.6000,    2.7000,    4.2000,    1.3000),
                 (4.4000,    3.0000,    1.3000,    0.2000),
                 (4.6000,    3.1000,    1.5000,    0.2000),
                 (7.7000,    3.8000,    6.7000,    2.2000),
                 (5.1000,    3.5000,    1.4000,    0.2000),
                 (6.0000,    2.7000,    5.1000,    1.6000),
                 (6.2000,    3.4000,    5.4000,    2.3000),
                 (4.9000,    3.1000,    1.5000,    0.1000),
                 (5.8000,    2.7000,    3.9000,    1.2000),
                 (6.3000,    3.3000,    4.7000,    1.6000),
                 (5.1000,    3.4000,    1.5000,    0.2000),
                 (5.2000,    4.1000,    1.5000,    0.1000),
                 (6.6000,    3.0000,    4.4000,    1.4000)]

        iris = KDTree(4)

        for t in train:
            iris.insert(t)

        counts = []

        for i in range(0,len(test)):
            (fnd,cnt) = iris.find_nearest(test[i],count_nodes=True)
            counts.append(cnt)

            if i != 36:
                self.assertEqual(fnd,found[i])

        # print sum(counts)
