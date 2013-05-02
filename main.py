import sys
import os
import heapq
import operator
import math
import matplotlib.pyplot as plt
import datetime

class HuffmanNode:
    def __init__(self, frequency, word=None):
        self.frequency = frequency
        self.word = word
        self.right = None
        self.left = None
 
    def __cmp__(self, other):
        return cmp(self.frequency, other.frequency)
    
    def __eq__(self, other):
        if not isinstance(other, HuffmanNode):
            return False
        return (self.frequency == other.frequency) and (self.word == other.word) and (self.right == other.right) and (self.left == other.left)

    def __repr__(self):
        return "(" + str(self.frequency) + "," + str(self.word) + ")"

    def __str__(self):
        return "(" + str(self.frequency) + "," + str(self.word) + ")"

mappings = dict()
worst_ten = []
best_ten = []

def run(num_speeches):
    word_set = dict()
    directory = os.path.join(os.getcwd(), "speechdata")
    for root, dirs, files in os.walk(directory):
        for fi in files:
            with open(os.path.join(directory, fi), 'r') as f:
                for word in f.read().split(" "):
                    word_set[word] = 1

    for root, dirs, files in os.walk(directory):
        files.sort()
        if int(num_speeches) > 0:
            count = 1
            while count <= int(num_speeches):
                with open(os.path.join(directory, files[count]), 'r') as f:
                    for word in f.read().split(" "):
                        word_set[word] += 1
                count +=1
        else:
            count = -1
            while count >= int(num_speeches):
                with open(os.path.join(directory, files[count]), 'r') as f:
                    for word in f.read().split(" "):
                        word_set[word] += 1
                count -=1

    tree = build_huffman(word_set)
    build_mappings(tree, "")
    dates = []
    ratios = []

    for root, dirs, files in os.walk(directory):
        files.sort()
        for fi in files:
            dt = fi[:-9].split("_")
            dates.append(datetime.date(int(dt[0]), int(dt[1]), int(dt[2])))
            with open(os.path.join(directory, fi), 'r') as f:
                ratio = compute_compression(f.read())
                #if len(worst_ten) < 10: 
                #    worst_ten.append((fi, ratio))
                #    worst_ten.sort(cmp=lambda x,y: cmp(x[1], y[1]))
                #elif worst_ten[0] < ratio:
                #    worst_ten[0] = (fi, ratio)
                #    worst_ten.sort(cmp=lambda x,y: cmp(x[1], y[1]))
                #if len(best_ten) < 10: 
                #    best_ten.append((fi, ratio))
                #    best_ten.sort(cmp=lambda x,y: cmp(x[1], y[1]))
                #elif best_ten[9] > ratio:
                #    best_ten[9] = (fi, ratio)
                #    best_ten.sort(cmp=lambda x,y: cmp(x[1], y[1]))
                ratios.append(ratio)
    plt.plot(dates, ratios)
    plt.ylim((0.5, 2.0))
    #print worst_ten
    #print best_ten
    plt.show()

def compute_compression(file_data):
    # encode text
    bit_stream = ""
    word_count = 0
    for word in file_data.split():
        bit_stream += mappings[word]
        word_count += 1
    block_code = math.ceil(math.log(word_count, 2)) * word_count
    ratio = len(bit_stream) / block_code
    return str(len(bit_stream) / block_code)

def build_mappings(node, code):
    ret = ""
    if node.left == None and node.right == None:
        mappings[node.word] = code
        return
    ret = build_mappings(node.left, code + "0")
    ret = build_mappings(node.right, code + "1")

def build_huffman(word_set):
    sort_list = [HuffmanNode(v, k) for k,v in sorted(word_set.iteritems(), key=operator.itemgetter(1), reverse=True)]
    heap = []
    for item in sort_list:
        heapq.heappush(heap, item)
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        int_node = HuffmanNode(node1.frequency + node2.frequency)
        int_node.left = node1
        int_node.right = node2
        heapq.heappush(heap, int_node)
    return heap[0]
    #print_tree(queue.get())

if __name__ == "__main__":
    run(sys.argv[1])
