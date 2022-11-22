import Sub_list
class fulllist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.admin_head=None
        self.admin_tail=None

    def addmusic_admin(self,id,url):
        newnode=Sub_list.Node(id,url)
        if self.admin_head == None:
            self.admin_head = newnode
            self.admin_tail = newnode
            return
        self.admin_tail.nextnode = newnode
        newnode.prevnode = self.admin_tail
        self.admin_tail = newnode
    
    def getmusic_admin(self):
        if self.admin_head == None:
            return list()
        node=self.admin_head
        if self.admin_head.nextnode != None:
            temp=self.admin_head.nextnode
            temp.prevnode=None
        self.admin_head=node.nextnode
        return node.data
    
    def get_adminlist(self):
        
        list1=[]
        current=self.admin_head
        while current is not None:
            list1+=current.data
            current=current.nextnode
        return list1
    
    def removemusic_admin(self,url):
        current=self.admin_head
        while current is not None:
            if current.data[0]['url']==url:
                prevnode=current.prevnode
                nextnode=current.nextnode
                
                if prevnode != None and nextnode != None:
                    prevnode.nextnode=nextnode
                    nextnode.prevnode=prevnode
                elif prevnode == None and nextnode == None:
                    print("a")
                    self.admin_head = None
                    self.admin_tail = None
                elif prevnode == None:
                    self.admin_head=nextnode
                    nextnode.prevnode=None
                elif nextnode == None:
                    self.admin_tail=prevnode
                    prevnode.nextnode=None
                return
            current=current.nextnode
    
    def removemusicall_admin(self,url):
        current=self.admin_head
        while current is not None:
            if current.data[0]['url']==url:
                prevnode=current.prevnode
                nextnode=current.nextnode
                
                if prevnode != None and nextnode != None:
                    prevnode.nextnode=nextnode
                    nextnode.prevnode=prevnode
                elif prevnode == None and nextnode == None:
                    print("a")
                    self.admin_head = None
                    self.admin_tail = None
                elif prevnode == None:
                    self.admin_head=nextnode
                    nextnode.prevnode=None
                elif nextnode == None:
                    self.admin_tail=prevnode
                    prevnode.nextnode=None
                
            current=current.nextnode

    #adds a sublist into the full linked list
    def addlist(self,sub):
        if self.head == None:
            self.head = sub
            self.tail = sub
            return
        self.tail.nextlist = sub
        sub.prevlist = self.tail
        self.tail = sub

    #main function for adding music. parameters be usertype, user id (integer), and music name.
    #usertype and music are strings for now, can change later
    def addmusic(self,id,url):
        newnode= Sub_list.Node(id,url)
        if self.head is None:
            newsublist = Sub_list.sublist_class()
            newsublist.addnode(newnode)
            self.addlist(newsublist)
            return
        current = self.head
        while current is not None:
            # print(newnode.id)
            # print("+++++++++++++++++")
            if current.counter() < 5:
                if current.sublength() == 1:
                    current.addnode(newnode)
                    return
                # print(current.subhead.id)
                # print(current.subtail.id)
                # print("===============")
                if current.subhead.id == current.subtail.id:
                    if newnode.id == current.subtail.id:
                        newsublist = Sub_list.sublist_class()
                        newsublist.addnode(newnode)
                        self.addlist(newsublist)
                        return         
                    else:
                        currentnode = current.subhead
                        while currentnode.nextnode is not None:
                            if newnode.id == currentnode.id and newnode.id != "0" and currentnode.count < 3:
                                print(currentnode.id)
                                currentnode.data += newnode.data
                                currentnode.count += 1
                                return
                            pnode = currentnode
                            currentnode = currentnode.nextnode
                        newnode.nextnode = currentnode
                        pnode.nextnode = newnode
                        newnode.prevnode = pnode
                        currentnode.prevnode = newnode
                        return
                else:
                    current.addnode(newnode)
                    return
            else:
                current = current.nextlist
        newsublist = Sub_list.sublist_class()
        newsublist.addnode(newnode)
        self.addlist(newsublist)
        return

    #removes a certain music from all nodes if it contains
    #music is a string for now
    def remove_music(self,url):
      if self.head == None:
        return 

      current = self.head
      while current != None:
        
        current.remove_node(url)
        if current.counter()==0:
            self.delete_node(current)
        current = current.nextlist
        

    #remove a music from a specific id
    def remove_id(self,user,url):
      if self.head == None:
        return 

      current = self.head
      while current != None:

        temp=current.remove_node_id(user,url)
        if current.counter()==0:
            self.delete_node(current)
        current = current.nextlist
      
      if not temp:
          print("no user and/or id")
    
    def delete_node(self,current):
        prevlist=current.prevlist
        nextlist=current.nextlist
        if prevlist != None and nextlist != None:
            prevlist.next=nextlist
            nextlist.prevlist=prevlist
        elif prevlist == None and nextlist == None:
            self.head = None
            self.tail = None
        elif prevlist == None:
            nextlist.prevlist=None
        elif nextlist == None:
            prevlist.next=None

    #pops the first sublist, also prints it
    def get_sublist(self):
        if self.head==None:
            return list()
        sub = self.head
        if sub.nextlist is None:
            self.head = None
            self.tail = None
        else:
            self.head = sub.nextlist
            self.head.prevlist = None
        return sub.return_sublist()

    #prints the linked list in normal list form 
    def get_list(self):
        list1 = []
        current = self.head
        while current is not None:
            list1+=current.return_sublist()
            current=current.nextlist
        return list1

    def countlist(self):
        c = 0
        current = self.head
        while current is not None:
            c += 1
            current = current.nextlist
        return c
    

# test=fulllist()
# test1={"id":"0","url":"2"}
# test2={"id":"2","url":"1"}
# test3={"id":"0","url":"2"}
# test4={"id":"4","url":"4"}
# test5={"id":"5","url":"5"}
# test6={"id":"6","url":"6"}
# test7={"id":"7","url":"7"}
# test8={"id":"8","url":"8"}
# test9={"id":"9","url":"9"}
# test.addmusic(**test1)
# test.addmusic(**test2)
# test.addmusic(**test3)
# test.addmusic(**test4)
# test.addmusic(**test5)
# test.addmusic(**test6)
# test.addmusic(**test7)
# test.addmusic(**test8)
# test.addmusic(**test9)


# print(test.get_sublist())




