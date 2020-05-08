import ipaddress

class ip_tree:
    def __init__(self, network, root=False,routed=False):
        self.left = None
        self.right = None
        self.network = network
        self.level = network.prefixlen
        self.root = root
        self.routed = routed

    @property
    def IterTree(self):
        '''Iterates over the tree and yeilds the childless nodes(ip_tree objects)'''
        if self.left:
            yield from self.left.IterTree()

        if self.right:
            yield from self.right.IterTree()

        yield self

    def IterFree(self):
        '''Iterates over the tree and yields free ipaddress.ip_network objects'''
        if self.routed == False:
           if (self.right == None and self.left == None):
               yield self.network
           else:
                      if self.left:
                          yield from self.left.IterFree()
                      else:
                          if self.root != True:
                             yield subnet(self.network, False)

                      if self.right:
                          yield from self.right.IterFree()
                      else:
                          if self.routed != True:
                             yield subnet(self.network, True)


    def FindRoutedNetwork(self,network):
        '''Checks if a network is routed in a ip_tree object'''
        if (self.network.network_address <= network.network_address and
                    self.network.broadcast_address >= network.broadcast_address):
            #print ('True is',network,self.network)
            if self.routed == True:
                return True
            if isKthBitSet(int(network.network_address), (32 - self.level)):
                if self.right is None:
                    return False
                else:
                    return self.right.FindRoutedNetwork(network)
            else:
                if self.left is None:
                    return False
                else:
                    return self.left.FindRoutedNetwork(network)
        else:
            #Tried to look for a network that is not within the root of the tree
            return False

    def insert(self, network):
        '''Inserts new networks in a ip_tree as routed.'''
        #if self.root == True:
        if (self.network.network_address > network.network_address or
                self.network.broadcast_address <  network.broadcast_address):
            raise Exception("Subnet is not in network", network, self.network)
        #print(32 - self.level)
        if self.level < 32:
            if isKthBitSet(int(network.network_address), (32 - self.level)):
                if self.level != network.prefixlen:
                    if self.right is None:
                        #print('Create right ',network.supernet(new_prefix=self.level+1), 'level=',self.level
                        self.right = ip_tree(network.supernet(new_prefix=self.level+1), routed=self.routed)
                    self.right.insert(network)
                else:
                    self.routed = True

            else:
                if self.level != network.prefixlen:
                     if self.left is None:
                         #print('Create left', network.supernet(new_prefix=self.level+1), 'level=', self.level)
                         self.left = ip_tree(network.supernet(new_prefix=self.level+1), routed=self.routed)
                     self.left.insert(network)
                else:
                    self.routed = True

    def insertunrouted(self, network):
        '''Inserts new networks in a ip_tree as unrouted.'''
        if (self.network.network_address > network.network_address or
                self.network.broadcast_address <  network.broadcast_address):
            raise Exception("Error subnet not in network", network, self.network)
        #print(32 - self.level)
        if self.level < 32:
            if isKthBitSet(int(network.network_address), (32 - self.level)):
                if self.level != network.prefixlen:
                    if self.right is None:
                        #print('Create right ',network.supernet(new_prefix=self.level+1), 'level=',self.level
                        self.right = ip_tree(network.supernet(new_prefix=self.level+1), routed=self.routed)
                    self.right.insertunrouted(network)
                else:
                       self.routed = False

            else:
                if self.level != network.prefixlen:
                     if self.left is None:
                         #print('Create left', network.supernet(new_prefix=self.level+1), 'level=', self.level)
                         self.left = ip_tree(network.supernet(new_prefix=self.level+1), routed=self.routed)
                     self.left.insertunrouted(network)
                else:
                       self.routed = False

def isKthBitSet(n, k):
    if n & (1 << (k - 1)):
        return True
    else:
        return False

def subnet(network, right):
    if right is True:
        number = int(network.network_address)
        number = number|(1<<(31-network.prefixlen))
        #print('Right on ', network)
        return ipaddress.ip_network((number, network.prefixlen+1))

    else:
        number = int(network.network_address)
        #print('Left on ', network)
        return ipaddress.ip_network((number, network.prefixlen + 1))
