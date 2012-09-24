from dht_tornado import dhttornado
import pdb

dhttornado.DHTTree.MAX_LIST_LENGTH = 2

def sb(arr):
    return ''.join(chr(x) for x in arr)

def new_node(arr):
	return dhttornado.DHTPeer(sb(arr), ("127.0.0.1", 30))

bit_iter = dhttornado.string_bit_iterator('\xff\xff\xff\xff\xff\xff\xff\xff')
for b in bit_iter:
    assert(b == 1)

#pdb.set_trace()
count = 0
last = 0
bit_iter = dhttornado.string_bit_iterator('\xaa')
for b in bit_iter:
    assert(b != last)
    last = b
    count = count + 1
assert(count == 8)

peer = new_node([0xAA,0xAA])
for b in peer:
    assert(b != last)
    last = b


assert(dhttornado.byte_array_to_uint([0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA]) == 0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA)

p_id =  sb([0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA])

t = dhttornado.DHTTree(p_id)
#t.insert(sb([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
#Test duplicate ids on the left side
t.insert(new_node([0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
t.insert(new_node([0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
assert(len(t._root.left.value) == 1)

#Try adding another to the left branch
t.insert(new_node([0x55,0x51,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
assert(len(t._root.left.value) == 2)

#Add 2 to the right left right
t.insert(new_node([0xAA,0xAA,0xA1,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
t.insert(new_node([0xAA,0xAA,0xA2,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
assert(len(t._root.right.value) == 2)

bucket = t.get_target_bucket('\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa')
assert(bucket[0].id == '\xaa\xaa\xa1UUUUUUUUUUUUUUUUU')
assert(bucket[1].id == '\xaa\xaa\xa2UUUUUUUUUUUUUUUUU')

bucket = t.get_target_bucket('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert(bucket[0].id == 'UUUUUUUUUUUUUUUUUUUU')
assert(bucket[1].id == 'UQUUUUUUUUUUUUUUUUUU')

#Send one left to right left left
t.insert(new_node([0x8A,0xAA,0xA3,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))

assert(len(t._root.right.left.left.value) == 1)
assert(len(t._root.right.left.right.value) == 2)

#Cause an overflow on a branch not going my way
t.insert(new_node([0x8A,0xAA,0xA4,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
assert(len(t._root.right.left.left.value) == 2)
t.insert(new_node([0x8A,0xAA,0xA5,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
assert(len(t._root.right.left.left.value) == 2)

#Cause a split on right left right
t.insert(new_node([0xBA,0xAA,0xA2,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
assert(len(t._root.right.left.right.left.value) == 2)
assert(len(t._root.right.left.right.right.value) == 1)

bucket = t.get_target_bucket('\xba\xaa\xa2\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert(bucket[0].id == '\xba\xaa\xa2UUUUUUUUUUUUUUUUU')


node_list = dhttornado.NodeListHeap(p_id)
node_list.push(new_node([0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
node_list.push(new_node([0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
assert(len(node_list.node_heap) == 1)

node_list.push(new_node([0xAA,0xAA,0xA1,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
node_list.push(new_node([0xAA,0xAA,0xA2,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]))
assert(len(node_list.node_heap) == 3)

contacts = node_list.get_contact_list()
assert(len(contacts) == 3)

assert(contacts[0][1].id == '\xaa\xaa\xa2UUUUUUUUUUUUUUUUU')


#pdb.set_trace()

#pdb.set_trace()
#assert(len(t._root.right.value) == 2)

#pdb.set_trace()

#assert(len(t._root.left.value) == 2)
#assert(len(t._root.right.value) == 3)

#t.insert(0xAA4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA)
#t.insert(0xAA5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA)
#t.insert(0xAA6AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA)


