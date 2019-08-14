"""
Implementation of the dynamic programming algorithm to
adjust text evenly at both margins, left and right.

Copyright 2018

Luka Steinbach <luka.steinbach@gmx.de>
"""

import sys


class Block:
    '''
    Block wraps the functions for printing text as fully justified block
    '''

    def __init__(self):
        '''
        Standard constructor
        '''
        # list of words to be printed fully justified
        self.word_list = []

        # dictionary for the dynamic programming approach
        self.memo = {}

        # dictionary containing (i,j) if a line starting with
        # word i is followed by a line starting with word j
        self.nextline = {}

        self.width = 80

    @classmethod
    def print_as_block(cls, filepath):
        '''
        Prints an input file fully justified into file output.txt.

        Uses 'file_to_block' to create a block and then run the function
        blocksatz(0) on that object.

        Uses the dictionary 'nextline' and the function 'pretty_print'
        to create the lines, which can be concatenated and written into
        the result file 'output.txt'.

        Arg:
            filepath - Print a text-file from filepath
        '''
        block = cls.file_to_block(filepath)
        badness_sum = block.blocksatz(0)
        print("Total badness of output.txt:", badness_sum)
        i = 0
        current = i
        orig_stdout = sys.stdout
        f = open('output.txt', 'w')
        sys.stdout = f

        while True:
            block.pretty_print(current, block.nextline[current])
            current = block.nextline[current]
            if current == len(block.nextline):
                break

        sys.stdout = orig_stdout
        f.close()

    @classmethod
    def file_to_block(cls, filepath):
        '''
        Factory that reads a text-file and creates a Block from it

        Arg:
            filepath - Reads a text-file from filepath

        Returns:
            instance of Block containing list of words from input file
        '''
        file = open(filepath, "r")
        block = cls()
        block.word_list = file.read().split()
        return block

    def badness(self, i, j):
        '''
        Implementation of the badness function from the lecture

        Args:
            i,j - calculate badness for putting word_list[i:j] into a line

        Returns:
            badness as defined in the lecture
        '''
        w = self.width
        words = j - i
        chars = 0
        for word in self.word_list[i:j]:
            chars += len(word)
        if chars + (words - 1) > w and words > 1:
            return 1000000000
        else:
            return (w - chars - (words - 1)) ** 3

    def blocksatz(self, i):
        '''
        Compute blocksatz(i), which is defined as minimum total badness
        by writing the i-th word to the n-th into a block of width 80.

        Also stores in nextline[i] the index j of the word where the next
        line begins, if the block would start with word i.

        Args:
            i - compute minimal badness for putting words i to n into a block

        Returns:
            minimum badness (essentially the sum of the badness of each
            line of the block)
        '''
        if i in self.memo:
            return self.memo[i]
        if i >= len(self.word_list):
            cost = 0
        else:
            b = self.badness(i, i + 1)
            cost = 1000000000
            j = i + 1
            min_idx = i + 1
            while j <= len(self.word_list) and b < 1000000000:
                c = b + self.blocksatz(j)
                if c < cost:
                    cost = c
                    min_idx = j
                j += 1
                b = self.badness(i, j)
            self.memo[i] = cost
            self.nextline[i] = min_idx
        return cost

    def pretty_print(self, i, j):
        '''
            Creates a string of length 80 containing word_list[i:j],
            such that the difference in the number of spaces between
            consecutive words does not exceed 1.

            Args:
                i,j - produce aforementioned string for word_list[i:j]
        '''
        s = ""
        length = self.width
        words_length = 0
        for word in self.word_list[i:j]:
            words_length += len(word)
        spaces = length - words_length - 1
        # min spaces per word (excluding last word)
        min_spaces = spaces // (len(self.word_list[i:j]) - 1)
        # extra spaces in total
        extra_spaces = spaces % (len(self.word_list[i:j]) - 1)
        for word in self.word_list[i:j]:
            if word is not self.word_list[i]:
                if extra_spaces == 0:
                    s += " " * min_spaces + word
                else:
                    s += " " * (min_spaces + 1) + word
                    extra_spaces -= 1
            else:
                s += word
        print(s)


Block.print_as_block("input.txt")
