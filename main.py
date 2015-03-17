import sys

class TrieNode:
    def __init__(self):
        # Initialize empty hash(dict)
        self.next = {}
        self.word_end = False
        self.ids = []

    def add_item(self, string, id):
        if len(string)==0:
            self.word_end = True
            self.ids.append(id)
            return

        key = string[0]
        string = string[1:]

        if self.next.has_key(key):
            self.next[key].add_item(string,id)
        else:
            node = TrieNode()
            self.next[key] = node
            node.add_item(string,id)

    def dfs(self, so_far=None):
        if self.next.keys()==[]: # this means it's a leaf node and this a complete word has to be included
            return self.ids

        if self.word_end == True:
            return self.ids

        for key in self.next.keys():
            return self.next[key].dfs(so_far+key)

    def search(self, string, so_far=""):
        if len(string)>0:
            key = string[0]
            string = string[1:]
            if self.next.has_key(key.upper()):
                so_far = so_far + key.upper()
                return self.next[key.upper()].search(string, so_far)
            elif self.next.has_key(key.lower()):
                so_far = so_far + key.lower()
                return self.next[key.lower()].search(string, so_far)
            else:
                return []
        else:
            if self.word_end==True:
                return self.ids
            for key in self.next.keys():
                return self.next[key].dfs(so_far+key)

root = TrieNode()
file = open("input.txt", "r")
data = file.readlines()
N = int(data[0])
data = data[1:]

time=0
dic={}

def custom_sort_util(a,b):
    if dic[a][1]!=dic[b][1]:
        if dic[a][1]<dic[b][1]:
            return 1
        else:
            return -1
    return -(dic[a][2] - dic[b][2])

def custom_sort(results):
    results = sorted(results, cmp = custom_sort_util)
    return results

for i in range(N):
    line = data[i].strip('\r\n')
    if line.startswith("ADD"):
        time+=1 # increment the time counter to keep track of recent entries in case of tie based on score
        line    = line.split()
        topic   = line[1]
        id      = line[2]
        score   = float(line[3])
        dic[id] = [topic,score,time]
        for word in line[4:]:
            if word==' ':
                continue
            root.add_item(word, id)
    elif line.startswith("QUERY"):
        results = []
        count=0
        line = line.split()
        num = int(line[1])
        for word in line[2:]:
            if word==' ':
                continue;
            if count==0:
                count+=1
                results = root.search(word)
                continue
            results = list(set(results)&set(root.search(word)))
        results = list(set(results)&set(dic.keys()))
        results = (custom_sort(results))[:num]
        print ' '.join(results)
    elif line.startswith("DEL"):
        line = line.split()
        id   = line[1]
        if id in dic:
            del dic[id]
    elif line.startswith("WQUERY"):
        results = []
        line = line.split()
        num = int(line[1])
        print 
