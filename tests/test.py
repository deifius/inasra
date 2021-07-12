import os
import unittest
import sys
import inspect
from functools import reduce

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import Start_New_inasra
import lambda_experiment as ws

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_createdirs(self):
        Start_New_inasra.directory_initializer()
        self.assertTrue(os.path.isdir('acronym/summary'))
        self.assertFalse(os.path.isdir('i/am/not/a/dir'))

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_col(self):
        wordspace = (('h', 'i'), (' ', 'f'))
        self.assertEqual(ws.getColumn(wordspace, 1), ('i', 'f'))
        self.assertEqual(ws.flipWordspace(wordspace), (('h', ' '), ('i', 'f')))
        self.assertEqual(ws.offAxis('y'), 'x')
        self.assertEqual(ws.offAxisVal('y', 5, 10), 5)

    def test_wordspace(self):
        wordspace = (
            ('h', 'o', 'w'),
            ('e', '' , '' ),
            ('f', '' , '' ),
            ('t', '' , '' ),
        )
        self.assertEqual(ws.getWordspaceLen(wordspace, 'x'), 3)
        self.assertEqual(ws.getWordspaceLen(wordspace, 'y'), 4)

        self.assertEqual(ws.getLine(wordspace, 0, 2, 'y'), ('h', 'e', 'f', 't')) #f
        self.assertEqual(ws.getLine(wordspace, 1, 0, 'x'), ('h', 'o', 'w'))      #o

        self.assertEqual(ws.getNeighborIndexes(wordspace, 0, 0, 'y'), (0, 1))    #h
        self.assertEqual(ws.getNeighborIndexes(wordspace, 0, 2, 'y'), (1, 2, 3)) #f
        self.assertEqual(ws.getNeighborIndexes(wordspace, 0, 3, 'y'), (2, 3))    #t
        self.assertEqual(ws.getNeighborIndexes(wordspace, 0, 0, 'x'), (0, 1))    #h
        self.assertEqual(ws.getNeighborIndexes(wordspace, 2, 0, 'x'), (1, 2))    #w

        self.assertEqual(ws.condenseComparisonTriplet(('a', '', '')), '|')
        self.assertEqual(ws.condenseComparisonTriplet(('', '', 'a')), '|')
        self.assertEqual(ws.condenseComparisonTriplet(('', 'a', '')), 'a')
        self.assertEqual(ws.condenseComparisonTriplet(('', '', '')), '')

        self.assertEqual(ws.buildComparisonLine(wordspace, 1, 0, 'x'), ('o', '|', '|', '|'))
        self.assertEqual(ws.buildComparisonLine(wordspace, 2, 0, 'x'), ('w', '',  '',  '' ))
        self.assertEqual(ws.buildComparisonLine(wordspace, 0, 1, 'y'), ('e', '|', '|'))
        self.assertEqual(ws.buildComparisonLine(wordspace, 0, 3, 'y'), ('t', '',  '' ))

        wordspace2 = wordspace + (('y', 'e', 's'),)
        self.assertEqual(ws.buildComparisonLine(wordspace2, 1, 0, 'x'), ('o', '|', '|', '|', 'e'))
        self.assertEqual(ws.buildComparisonLine(wordspace2, 2, 0, 'x'), ('w', '',  '',  '',  's'))

        expectedRegexes = ('p.{1,2}')
        # self.assertEqual(ws.getRegexesForLetter(wordspace, 2, 0, 'x'), expectedRegexes)
        # self.assertEqual(ws.getRegexesForLetter(wordspace, 0, 2, 'y'), expectedRegexes)

if __name__ == '__main__':
    unittest.main()
