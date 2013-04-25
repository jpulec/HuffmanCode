import os
import Queue
import operator
import math
import matplotlib.pyplot as plt


class HuffmanNode:
    def __init__(self, frequency, word=None):
        self.frequency = frequency
        self.word = word
        self.right = None
        self.left = None

    def __str__(self):
        return "(" + str(self.frequency) + "," + str(self.word) + ")"

class HuffmanTree:
    def __init__(self):
        root = None


def run():
    word_set = dict()
    directory = os.path.join(os.getcwd(), "speechdata")
    for root, dirs, files in os.walk(directory):
        for fi in files:
            with open(os.path.join(directory, fi), 'r') as f:
                for word in f.read().split(" "):
                    word_set[word] = 1

    for root, dirs, files in os.walk(directory):
        files.sort()
        with open(os.path.join(directory, files[-1]), 'r') as f:
            for word in f.read().split(" "):
                word_set[word] += 1
    
    tree = build_huffman(word_set)
    dates = []
    ratios = []

    for root, dirs, files in os.walk(directory):
        files.sort()
        for fi in files:
            dates.append(fi)
            with open(os.path.join(directory, fi), 'r') as f:
                ratios.append(compute_compression(f.read(), tree))
    plt.plot(dates, ratios)


def compute_compression(file_data, tree):
    # encode text
    bit_stream = ""
    word_count = 0
    for word in file_data.split():
        bit_stream += find_word(word, tree, "")
        word_count += 1
    block_code = math.ceil(math.log(word_count, 2)) * word_count
    print str(len(bit_stream) / block_code)

def find_word(word, node, code):
    ret = ""
    if node.left == None and node.right == None:
        if node.word == word:
            ret = code
    else:
        ret = find_word(word, node.left, code + "0")
        if (ret == ""):
            ret = find_word(word, node.right, code + "1")
    return ret

def build_huffman(word_set):
    sort_list = sorted(word_set.iteritems(), key=operator.itemgetter(1))
    queue = Queue.PriorityQueue()
    for word in sort_list:
        node = HuffmanNode(word[1], word[0]) 
        queue.put(node)
    while queue.qsize() > 1:
        node1 = queue.get()
        node2 = queue.get()
        int_node = HuffmanNode(node1.frequency + node2.frequency)
        int_node.left = node1
        int_node.right = node2
        queue.put(int_node)
    return queue.get()
    #print_tree(queue.get())

def print_tree(root):
    if root.left == None:
        return root
    print print_tree(root.left)
    if root.right == None:
        return root
    print print_tree(root.right)

if __name__ == "__main__":
    run()
