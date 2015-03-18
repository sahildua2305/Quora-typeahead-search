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

    def dfs(self):
        if self.next.keys()==[]: # this means it's a leaf node and this a complete word has to be included
            return self.ids

        results = []
        if self.word_end == True:
            results += self.ids

        for key in self.next.keys():
            results += self.next[key].dfs()
        return results

    def search(self, string):
        if len(string)>0:
            key = string[0]
            string = string[1:]
            results = []
            if self.next.has_key(key.upper()):
                 results += self.next[key.upper()].search(string)
            if self.next.has_key(key.lower()):
                results += self.next[key.lower()].search(string)
            return results
        else:
            results = []
            if self.word_end==True:
                results += self.ids
            for key in self.next.keys():
                results += self.next[key].dfs()
            return results

root = TrieNode()
file = open("input.txt", "r")
data = file.readlines()
N = int(data[0])
data = data[1:]

time        = 0
dic         = {}
deleted_ids = []
boosts = {'user':1.0,'topic':1.0,'question':1.0,'board':1.0}

def custom_sort_util(a,b):
    a_score = dic[a][1]*dic[a][3]*boosts[dic[a][0]]
    b_score = dic[b][1]*dic[b][3]*boosts[dic[b][0]]
    if a_score!=b_score:
        if a_score<b_score:
            return 1
        else:
            return -1
    return -(dic[a][2] - dic[b][2])

def custom_sort(results):
    results = sorted(results, cmp = custom_sort_util)
    return results

for p in range(N):
    line = data[p].strip('\r\n')
    if line.startswith("ADD"):
        time+=1 # increment the time counter to keep track of recent entries in case of tie based on score
        line    = line.split()
        topic   = line[1]
        id      = line[2]
        score   = float(line[3])
        boost   = 1.0
        dic[id] = [topic,score,time,boost]
        for word in line[4:]:
            if word==' ' or word=='':
                continue
            root.add_item(word, id)
    elif line.startswith("QUERY"):
        results = []
        count=0
        line = line.split()
        num_results = int(line[1])
        for word in line[2:]:
            if word==' ':
                continue;
            if count==0:
                count+=1
                results = root.search(word)
                continue
            results = list(set(results)&set(root.search(word)))
        results = [x for x in results if x not in deleted_ids]
        results = (custom_sort(results))[:num_results]
        print ' '.join(results)
    elif line.startswith("DEL"):
        line = line.split()
        id   = line[1]
        deleted_ids.append(id)
        if id in dic:
            del dic[id]
    elif line.startswith("WQUERY"):
        results = []
        line = line.split()
        num_results = int(line[1])
        num_boosts = int(line[2])
        line = line[3:]
        for i in range(num_boosts):
            boost = line[0].split(":")
            line = line[1:]
            type_id = boost[0]
            if type_id in boosts.keys():
                type = type_id
                boosts[type] *= float(boost[1])
            else:
                id   = type_id
                if id in dic:
                    dic[id][3] *= float(boost[1])
        # Search operation
        count=0
        results = []
        for word in line:
            if word==' ':
                continue
            if count==0:
                count+=1
                results = root.search(word)
                continue
            results = list(set(results)&set(root.search(word)))
        results = [x for x in results if x not in deleted_ids]
        results = (custom_sort(results))[:num_results]
        print ' '.join(results)
        # do stuff
        for item in dic:
            dic[item][3]=1.0
        for item in boosts:
            boosts[item]=1.0
