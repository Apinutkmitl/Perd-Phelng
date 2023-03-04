#base node cladss containing relavent data for each song
class Node:
    def __init__(self, id,url):
        self.id = id
        self.count = 1
        self.nextnode = None
        self.prevnode = None
        self.picture = None
        self.data=[{'id':id,'url':url}]
                

class sublist_class:
    def __init__(self):
        self.subhead = None
        self.subtail = None
        self.nextlist = None
        self.prevlist = None

    #these are methods used to help the other methods under the fulllist class

    #adds a node into a sublist
    def addnode(self,newnode):
        if self.subhead is None:
            self.subhead = newnode
            self.subtail = newnode
            return
        current = self.subhead
        while current is not None:
            id = current.id
            if id == newnode.id and newnode.id != "0" and current.count < 3:
                current.data += newnode.data
                current.count += 1
                return
            current = current.nextnode
        self.subtail.nextnode = newnode
        newnode.prevnode = self.subtail
        self.subtail = newnode

    #count number of music in the sublist
    def counter(self):
        currentnode = self.subhead
        c = 0
        while currentnode is not None:
            c += currentnode.count
            currentnode = currentnode.nextnode
        return c
    
    #count number of nodes
    def sublength(self):
        currentnode = self.subhead
        c = 0
        while currentnode is not None:
            c+= 1
            currentnode = currentnode.nextnode
        return c

    #removes a node containing musicc
    def remove_node(self, url):
        currentnode = self.subhead
        
        while currentnode is not None:
            i=0
            while i!=len(currentnode.data):
                if currentnode.data[i]['url'] == url:
                    
                    currentnode.data.pop(i)
                    currentnode.count -=1
                    if currentnode.count==0:
                        self.delete_None(currentnode)
                    return
                else:
                    i+=1
            if currentnode==self.subtail:
                return 
            currentnode = currentnode.nextnode

    def remove_node_id(self, id,url):
        currentnode = self.subhead
        temp=False
        while currentnode is not None:
            i=0
            while i!=len(currentnode.data):
                if currentnode.id== id and currentnode.data[i]['url'] == url:
                    temp=True
                    currentnode.data.pop(i)
                    currentnode.count -=1
                    if currentnode.count==0:
                        self.delete_None(currentnode)
                else:
                    i+=1
                    
            if currentnode==self.subtail:
                return temp
            currentnode = currentnode.nextnode
        return temp
    def delete_None(self,current):
        prevnode=current.prevnode
        nextnode=current.nextnode
        if prevnode != None and nextnode != None:
            prevnode.nextnode=nextnode
            nextnode.prevnode=prevnode
        elif prevnode == None and nextnode == None:
            self.subhead = None
            self.subtail = None
        elif prevnode == None:
            self.subhead=nextnode
            nextnode.prevnode=None
        elif nextnode == None:
            self.subtail=prevnode
            prevnode.nextnode=None

    def return_sublist(self):
        currentnode=self.subhead
        list1=[]
        while currentnode is not None:
            data=currentnode.data
            list1+=data
            currentnode = currentnode.nextnode
        return list1


# test=sublist_class()
# test.addnode(Node("3","test"))
# test.addnode(Node("3","test"))
# test.addnode(Node("3","test"))
# test.addnode(Node("3","test"))
# test.addnode(Node("3","test"))
# test.addnode(Node("3","test"))
# test.addnode(Node("3","test"))
# test.addnode(Node("3","test"))
# test.addnode(Node("3","test"))
# test.addnode(Node("2","test"))
# test.remove_node_id("3","test")
# print(len(test.return_sublist()))
