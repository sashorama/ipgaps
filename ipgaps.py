import re
import ipaddress
from ip_tree import ip_tree
#import time

def load_networks(input_file):
 """Parses an input_file to return a list of ipaddress.ip_network objects"""
 routed_networks = [];
 with open(input_file, "r") as f_in:
     for line in f_in:
         line = line.lower()
         if line.find('null') != -1 or line.find('sh') != -1 or line.find('dscd') != -1 or line.find('blackh') != -1:
             print('Skipping aggregates:',line)
             continue
         m = re.search(r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}/\d{1,2})", line)
         if m is not None:
             try:
                 new_routed = ipaddress.ip_network(m.group(1))
             except ValueError:
                 print("Warning: {} will be ignored! It is not a valid IPv4 network/prefix.".format(m.group(1)))
                 continue

             routed_networks.append(new_routed)
 return routed_networks

def get_free_networks(aggregate_networks, routed_networks):
 """Returns networks from aggregate space that are not in routed_networks.
 Very slow O(n*n) search. Used for testing of other faster searches."""
 free_networks = []
 for str_network in aggregate_networks:
     print(str_network)                      lkwe
     free_networks.append(ipaddress.ip_network(str_network))
 for routed_net in routed_networks:
     for free_net in free_networks:
         if (routed_net.network_address >= free_net.network_address and
                     routed_net.broadcast_address <= free_net.broadcast_address):


             new_networks = list(free_net.address_exclude(routed_net))
             free_networks.remove(free_net)
             for y in new_networks:
              free_networks.append(y)
             break
 return free_networks

def networks_to_file(free_networks, output_file):
 """Writes list to textfile with new lines for each element"""
 with open(output_file, "w") as f_out:
     for free_net in free_networks:
         if free_net not in mtel_networks:
             f_out.write(free_net.__str__())
             f_out.write("\n")

blizoo_networks = (
                  "5.53.128.0/17",
                  "37.130.240.0/21",
                  "46.232.152.0/21",
                  "62.221.128.0/19",
                  "77.236.160.0/19",
                  "77.244.192.0/20",
                  "80.253.48.0/20",
                  "84.252.0.0/18",
                  "85.130.0.0/17",
                  "87.97.128.0/17",
                  "89.186.200.0/21",
                  "89.215.0.0/16",
                  "89.253.128.0/18",
                  "95.140.208.0/20",
                  "130.204.0.0/16",
                  "151.251.0.0/16",
                  "194.187.132.0/22",
                  "212.104.96.0/19",
                  "213.191.160.0/19",
                  "217.9.224.0/20",
                  "217.10.240.0/20",
                  "217.18.240.0/20"
                   )

mtel_networks = (
                 "85.118.64.0/19",
                 "213.226.0.0/18",
                 "176.222.0.0/20"
                 )

spnet_mega_networks = (
                  "37.63.0.0/17",
                  "46.238.0.0/18",
                  "62.204.128.0/19",
                  "77.70.0.0/17",
                  "78.83.0.0/16",
                  "78.90.0.0/16",
                  "82.103.64.0/18",
                  "82.147.128.0/19",
                  "83.97.24.0/21",
                  "84.242.128.0/18",
                  "85.91.128.0/19",
                  "85.196.128.0/18",
                  "87.227.128.0/17",
                  "88.203.128.0/17",
                  "89.190.192.0/19",
                  "92.247.0.0/16",
                  "95.111.0.0/17",
                  "176.12.0.0/18",
                  "213.222.32.0/19",
                  "185.151.156.0/22",
                  "185.224.160.0/22",
                  "195.24.32.0/19",
                  "195.34.96.0/19",
                  "195.149.248.0/21",
                  "212.36.0.0/19",
                  "212.50.0.0/19",
                  "212.91.160.0/19",
                  "212.95.160.0/19",
                  "217.79.32.0/20",
                  "213.169.32.0/19"
                  )



input_file = "main_vrf.txt"
output_file = "free_networks.txt"
routed_networks = []
free_networks = []
aggregate_networks = spnet_mega_networks+blizoo_networks+mtel_networks
print("Loading routed networks from {}".format(input_file))
routed_networks = load_networks(input_file)
print("Networks successfully loaded from {}".format(input_file))
#when we need to measure the speed of our script
#start_time = time.time()

#Initialize aggregate A1 prefixes. The root has to be 0.0.0.0/0
#We need aggregates to check later of free network branches belong to A1 space.
aggregates = ip_tree(ipaddress.ip_network('0.0.0.0/0'),root=True)
#Insert the aggregates.
for agg_net in aggregate_networks:
    aggregates.insert(ipaddress.ip_network(agg_net))
#Initialize the ip_tree of routed networks.
routed = ip_tree(ipaddress.ip_network('0.0.0.0/0'),root=True)
#Insert aggregates in routed with insertunrouted. The will be labeled as unrouted.
#We only need this if we have a comletely unused prefix like 37.63.0.0/17.
for agg_net in aggregate_networks:
   routed.insertunrouted(ipaddress.ip_network(agg_net))
#Finally let's insert the actually routed networks form input files.
for routed_net in routed_networks:
    routed.insert(ipaddress.ip_network(routed_net))
#Walk over the tree to get unrouted networks
for rnet in routed.IterFree():
#Check of the unrouted network belongs to A1 prefixes.
   if aggregates.FindRoutedNetwork(rnet):
       free_networks.append(rnet)

#get_free_networks() is very slow. This is the old way.
#free_networks = get_free_networks(aggregate_networks, routed_networks)

#sort them so the bigger networks are first
free_networks.sort(key=lambda prefix: prefix.prefixlen)
print("Writing non routed networks to  {}".format(output_file))
networks_to_file(free_networks,output_file)
#when we need to measure the speed of our script
#print(time.time() - start_time)