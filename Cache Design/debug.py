import os
import sys
import math 

class GlobalVariables:
    address_size = 32
    block_size = 0
    replacement_policy = 0
    inclusion_property = 0
    trace_file = ''
    address = ''
    memtraffic = 0

var = GlobalVariables()

class CacheVariables:
    size = 0
    assoc = 0
    tag_width = 0
    index_width = 0
    offset_width = 0
    decimal_tag = 0
    decimal_index = 0
    decimal_offset = 0
    counter = 0
    reads = 0
    read_hits = 0
    read_misses = 0
    writes = 0
    write_hits = 0
    write_misses = 0
    write_backs = 0
    replacement_policy = 0
    miss_rate = 0

l1 = CacheVariables()
l2 = CacheVariables()

# Class definition of Cache
class Cache:
    def __init__(self):
        self.address = 0
        self.valid = 0
        self.tag = 0
        self.dirty = 0
        self.counter = 0	

# Function to calculate widths 
def calculate_widths(size, block_size, assoc):
    offset_width = int(math.log(block_size, 2))
    index_width = int(math.log(size / (assoc * block_size), 2))
    tag_width = var.address_size - offset_width - index_width;

    return offset_width, index_width, tag_width

# Function to read from L1 Cache 
def read_l1_cache(L1_cache, L2_cache):
    l1.reads += 1
    l1.counter += 1
    flag = False
    filled_blocks = 0

    print(f"L1 read : {var.address} (tag {hex(l1.decimal_tag)[2:]}, index {l1.decimal_index})")

    if var.replacement_policy == 0: 		# Replacement Policy - LRU
        for i in range(l1.assoc):
            if L1_cache[l1.decimal_index][i].valid == 1 and L1_cache[l1.decimal_index][i].tag == l1.decimal_tag:
                l1.read_hits += 1 
                flag = True
                L1_cache[l1.decimal_index][i].counter = l1.counter
                print("L1 hit")
                print("L1 update LRU")
                break

        if not flag: 
            l1.read_misses += 1
            print("L1 miss")
            for i in range(l1.assoc):
                if L1_cache[l1.decimal_index][i].valid == 0:
                    victim_block = i
                    print("L1 victim: none")
                    break
                if L1_cache[l1.decimal_index][i].valid == 1:
                    filled_blocks += 1 

            if filled_blocks == l1.assoc:
                victim, victim_block = find_victim(L1_cache, l1.decimal_index, l1.assoc)
                print(f"L1 victim: {victim.address} (tag {hex(victim.tag)[2:]}, index {l1.decimal_index}, {'dirty' if victim.dirty else 'clean'})")

            if L1_cache[l1.decimal_index][victim_block].dirty == 1 and L1_cache[l1.decimal_index][victim_block].valid == 1:
                l1.write_backs += 1
                if l2.size != 0:
                    write_l2_cache(L1_cache, L2_cache, victim)

            # if l2.size != 0:
            #     read_l2_cache(L1_cache, L2_cache)

            L1_cache[l1.decimal_index][victim_block].address = var.address
            L1_cache[l1.decimal_index][victim_block].tag = l1.decimal_tag
            L1_cache[l1.decimal_index][victim_block].counter = l1.counter
            # print("L1 update LRU")
            L1_cache[l1.decimal_index][victim_block].dirty = 0
            L1_cache[l1.decimal_index][victim_block].valid = 1

            if l2.size != 0:
                read_l2_cache(L1_cache, L2_cache)
            print('L1 update LRU')
    else:								# Replacement Policy - FIFO
        for i in range(l1.assoc):
            if L1_cache[l1.decimal_index][i].valid == 1 and L1_cache[l1.decimal_index][i].tag == l1.decimal_tag:
                l1.read_hits += 1 
                flag = True
                print("L1 hit")
                break

        if not flag:
            l1.read_misses += 1
            print("L1 miss")
            for i in range(l1.assoc):
                if L1_cache[l1.decimal_index][i].valid == 0:
                    victim_block = i
                    print("L1 victim: none")
                    break
                if L1_cache[l1.decimal_index][i].valid == 1:
                    filled_blocks += 1 

            if filled_blocks == l1.assoc:
                victim, victim_block = find_victim(L1_cache, l1.decimal_index, l1.assoc)
                print(f"L1 victim: {victim.address} (tag {hex(victim.tag)[2:]}, index {l1.decimal_index}, {'dirty' if victim.dirty else 'clean'})")

            if L1_cache[l1.decimal_index][victim_block].dirty == 1 and L1_cache[l1.decimal_index][victim_block].valid == 1:
                l1.write_backs += 1
                if l2.size != 0:
                    write_l2_cache(L1_cache, L2_cache, victim)

            if l2.size != 0:
                read_l2_cache(L1_cache, L2_cache)
            
            L1_cache[l1.decimal_index][victim_block].address = var.address
            L1_cache[l1.decimal_index][victim_block].tag = l1.decimal_tag
            L1_cache[l1.decimal_index][victim_block].counter = l1.counter
            print("L1 update FIFO")
            L1_cache[l1.decimal_index][victim_block].dirty = 0
            L1_cache[l1.decimal_index][victim_block].valid = 1

# Function to find the victim block
def find_victim(cache, decimal_index, assoc):
    min_counter = cache[decimal_index][0].counter
    victim = cache[decimal_index][0]
    victim_block = 0

    for i in range(1, assoc):
        if cache[decimal_index][i].counter < min_counter:
            min_counter = cache[decimal_index][i].counter
            victim = cache[decimal_index][i]
            victim_block = i

    return victim, victim_block

# Function to read from L2 Cache
def read_l2_cache(L1_cache, L2_cache):
    l2.reads += 1
    l2.counter += 1

    flag = False
    filled_blocks = 0

    print(f"L2 read : {var.address} (tag {hex(l2.decimal_tag)[2:]}, index {l2.decimal_index})")

    if var.replacement_policy == 0: 		# Replacement Policy - LRU
        for i in range(l2.assoc):
            if L2_cache[l2.decimal_index][i].valid == 1 and L2_cache[l2.decimal_index][i].tag == l2.decimal_tag:
                l2.read_hits += 1 
                flag = True
                L2_cache[l2.decimal_index][i].counter = l2.counter
                print("L2 hit")
                print("L2 update LRU")
                break

        if not flag:
            l2.read_misses += 1
            victim = ''
            print("L2 miss")
            for i in range(l2.assoc):
                if L2_cache[l2.decimal_index][i].valid == 0:
                    victim_block = i
                    print("L2 victim: none")
                    break
                if L2_cache[l2.decimal_index][i].valid == 1:
                    filled_blocks += 1 

            if filled_blocks == l2.assoc:
                victim, victim_block = find_victim(L2_cache, l2.decimal_index, l2.assoc)
                print(f"L2 victim: {victim.address} (tag {hex(victim.tag)[2:]}, index {l2.decimal_index}, {'dirty' if victim.dirty else 'clean'})")

            if L2_cache[l2.decimal_index][victim_block].dirty == 1 and L2_cache[l2.decimal_index][victim_block].valid == 1:
                l2.write_backs += 1
            
            if var.inclusion_property == 1 and victim:
                invalidate_l1_cache_item(L1_cache, victim)

            L2_cache[l2.decimal_index][victim_block].address = var.address
            L2_cache[l2.decimal_index][victim_block].tag = l2.decimal_tag
            L2_cache[l2.decimal_index][victim_block].counter = l2.counter
            print("L2 update LRU")
            L2_cache[l2.decimal_index][victim_block].dirty = 0
            L2_cache[l2.decimal_index][victim_block].valid = 1

    else:								# Replacement Policy - FIFO
        for i in range(l2.assoc):
            if L2_cache[l2.decimal_index][i].valid == 1 and L2_cache[l2.decimal_index][i].tag == l2.decimal_tag:
                l2.read_hits += 1 
                flag = True
                print("L2 hit")
                break

        if not flag:
            l2.read_misses += 1
            victim = ''
            print("L2 miss")
            for i in range(l2.assoc):
                if L2_cache[l2.decimal_index][i].valid == 0:
                    victim_block = i
                    print("L2 victim: none")
                    break
                if L2_cache[l2.decimal_index][i].valid == 1:
                    filled_blocks += 1 

            if filled_blocks == l2.assoc:
                victim, victim_block = find_victim(L2_cache, l2.decimal_index, l2.assoc)
                print(f"L2 victim: {victim.address} (tag {hex(victim.tag)[2:]}, index {l2.decimal_index}, {'dirty' if victim.dirty else 'clean'})")

            if L2_cache[l2.decimal_index][victim_block].dirty == 1 and L2_cache[l2.decimal_index][victim_block].valid == 1:
                l2.write_backs += 1
            
            if var.inclusion_property == 1 and victim:
                invalidate_l1_cache_item(L1_cache, victim)

            L2_cache[l2.decimal_index][victim_block].address = var.address
            L2_cache[l2.decimal_index][victim_block].tag = l2.decimal_tag
            L2_cache[l2.decimal_index][victim_block].counter = l2.counter
            print("L2 update FIFO")
            L2_cache[l2.decimal_index][victim_block].dirty = 0
            L2_cache[l2.decimal_index][victim_block].valid = 1

# Function to write into L1 Cache
def write_l1_cache(L1_cache, L2_cache):
    l1.writes += 1
    l1.counter += 1

    flag = False
    filled_blocks = 0

    print(f"L1 write : {var.address} (tag {hex(l1.decimal_tag)[2:]}, index {l1.decimal_index})")

    if var.replacement_policy == 0: 		# Replacement Policy - LRU
        for i in range(l1.assoc):
            if L1_cache[l1.decimal_index][i].valid == 1 and L1_cache[l1.decimal_index][i].tag == l1.decimal_tag:
                l1.write_hits += 1 
                flag = True
                print("L1 hit")
                L1_cache[l1.decimal_index][i].counter = l1.counter
                print("L1 update LRU")
                L1_cache[l1.decimal_index][i].dirty = 1
                print("L1 set dirty")
                break

        if not flag:
            l1.write_misses += 1
            print("L1 miss")
            for i in range(l1.assoc):
                if L1_cache[l1.decimal_index][i].valid == 0:
                    victim_block = i
                    print("L1 victim: none")
                    break
                if L1_cache[l1.decimal_index][i].valid == 1:
                    filled_blocks += 1 

            if filled_blocks == l1.assoc:
                victim, victim_block = find_victim(L1_cache, l1.decimal_index, l1.assoc)
                print(f"L1 victim: {victim.address} (tag {hex(victim.tag)[2:]}, index {l1.decimal_index}, {'dirty' if victim.dirty else 'clean'})")

            if L1_cache[l1.decimal_index][victim_block].dirty == 1 and L1_cache[l1.decimal_index][victim_block].valid == 1:
                l1.write_backs += 1
                if l2.size != 0:
                    write_l2_cache(L1_cache, L2_cache, victim)

            L1_cache[l1.decimal_index][victim_block].address = var.address
            L1_cache[l1.decimal_index][victim_block].tag = l1.decimal_tag
            L1_cache[l1.decimal_index][victim_block].counter = l1.counter
            L1_cache[l1.decimal_index][victim_block].dirty = 1
            L1_cache[l1.decimal_index][victim_block].valid = 1

            if l2.size != 0:
                read_l2_cache(L1_cache, L2_cache)
            print("L1 update LRU")
            print("L1 set dirty")
    else:								# Replacement Policy - FIFO
        for i in range(l1.assoc):
            if L1_cache[l1.decimal_index][i].valid == 1 and L1_cache[l1.decimal_index][i].tag == l1.decimal_tag:
                l1.write_hits += 1 
                flag = True
                print("L1 hit")
                L1_cache[l1.decimal_index][i].dirty = 1
                print("L1 set dirty")
                break

        if not flag:
            l1.write_misses += 1
            print("L1 miss")
            for i in range(l1.assoc):
                if L1_cache[l1.decimal_index][i].valid == 0:
                    victim_block = i
                    print("L1 victim: none")
                    break
                if L1_cache[l1.decimal_index][i].valid == 1:
                    filled_blocks += 1 

            if filled_blocks == l1.assoc:
                victim, victim_block = find_victim(L1_cache, l1.decimal_index, l1.assoc)
                print(f"L1 victim: {victim.address} (tag {hex(victim.tag)[2:]}, index {l1.decimal_index}, {'dirty' if victim.dirty else 'clean'})")

            if L1_cache[l1.decimal_index][victim_block].dirty == 1 and L1_cache[l1.decimal_index][victim_block].valid == 1:
                l1.write_backs += 1
                if l2.size != 0:
                    write_l2_cache(L1_cache, L2_cache, victim)

            if l2.size != 0:
                read_l2_cache(L1_cache, L2_cache)

            L1_cache[l1.decimal_index][victim_block].address = var.address
            L1_cache[l1.decimal_index][victim_block].tag = l1.decimal_tag
            L1_cache[l1.decimal_index][victim_block].counter = l1.counter
            print("L1 update FIFO")
            L1_cache[l1.decimal_index][victim_block].dirty = 1
            print("L1 set dirty")
            L1_cache[l1.decimal_index][victim_block].valid = 1

# Function to write into L2 Cache
def write_l2_cache(L1_cache, L2_cache, victim):
    l2.writes += 1
    l2.counter += 1

    flag = False
    filled_blocks = 0

    bin_address = bin(int(victim.address,16))[2:].zfill(32)
    decimal_tag = int(bin_address[0:l2.tag_width], 2)
    decimal_index = int(bin_address[l2.tag_width: l2.tag_width+l2.index_width], 2)

    print(f"L2 write : {hex(int(bin_address, 2))[2:]} (tag {hex(decimal_tag)[2:]}, index {decimal_index})")

    if var.replacement_policy == 0: 		# Replacement Policy - LRU
        for i in range(l2.assoc):
            if L2_cache[decimal_index][i].valid == 1 and L2_cache[decimal_index][i].tag == decimal_tag:
                l2.write_hits += 1 
                flag = True
                print("L2 hit")
                L2_cache[decimal_index][i].counter = l2.counter
                print("L2 update LRU")
                L2_cache[decimal_index][i].dirty = 1
                print("L2 set dirty")
                break

        if not flag:
            l2.write_misses += 1
            victim = ''
            print('L2 miss')
            for i in range(l2.assoc):
                if L2_cache[decimal_index][i].valid == 0:
                    victim_block = i
                    print("L2 victim: none")
                    break
                if L2_cache[decimal_index][i].valid == 1:
                    filled_blocks += 1 

            if filled_blocks == l2.assoc:
                victim, victim_block = find_victim(L2_cache, decimal_index, l2.assoc)
                print(f"L2 victim: {victim.address} (tag {hex(victim.tag)[2:]}, index {decimal_index}, {'dirty' if victim.dirty else 'clean'})")

            if L2_cache[decimal_index][victim_block].dirty == 1 and L2_cache[decimal_index][victim_block].valid == 1:
                l2.write_backs += 1
            
            if var.inclusion_property == 1 and victim:
                invalidate_l1_cache_item(L1_cache, victim)

            L2_cache[decimal_index][victim_block].address = victim.address
            L2_cache[decimal_index][victim_block].tag = decimal_tag
            L2_cache[decimal_index][victim_block].counter = l2.counter
            print("L2 update LRU")
            L2_cache[decimal_index][victim_block].dirty = 1
            print("L2 set dirty")
            L2_cache[decimal_index][victim_block].valid = 1
    else:								# Replacement Policy - FIFO
        for i in range(l2.assoc):
            if L2_cache[decimal_index][i].valid == 1 and L2_cache[decimal_index][i].tag == decimal_tag:
                l2.write_hits += 1 
                flag = True
                print("L2 hit")
                L2_cache[decimal_index][i].dirty = 1
                print("L2 set dirty")
                break

        if not flag:
            l2.write_misses += 1
            victim = ''
            print("L2 miss")
            for i in range(l2.assoc):
                if L2_cache[decimal_index][i].valid == 0:
                    victim_block = i
                    print("L2 victim: none")
                    break
                if L2_cache[decimal_index][i].valid == 1:
                    filled_blocks += 1 

            if filled_blocks == l2.assoc:
                victim, victim_block = find_victim(L2_cache, decimal_index, l2.assoc)
                print(f"L2 victim: {victim.address} (tag {hex(victim.tag)[2:]}, index {decimal_index}, {'dirty' if victim.dirty else 'clean'})")

            if L2_cache[decimal_index][victim_block].dirty == 1 and L2_cache[decimal_index][victim_block].valid == 1:
                l2.write_backs += 1
            
            if var.inclusion_property == 1 and victim:
                invalidate_l1_cache_item(L1_cache, victim)
                
            L2_cache[decimal_index][victim_block].address = victim.address
            L2_cache[decimal_index][victim_block].tag = decimal_tag
            L2_cache[decimal_index][victim_block].counter = l2.counter
            print("L2 update FIFO")
            L2_cache[decimal_index][victim_block].dirty = 1
            print("L2 set dirty")
            L2_cache[decimal_index][victim_block].valid = 1
    

def invalidate_l1_cache_item(L1_cache, victim):
    bin_address = bin(int(victim.address,16))[2:].zfill(32)
    decimal_tag = int(bin_address[0:l1.tag_width], 2)
    decimal_index = int(bin_address[l1.tag_width: l1.tag_width+l1.index_width], 2)

    for i in range(l1.assoc):
        if L1_cache[decimal_index][i].valid == 1 and L1_cache[decimal_index][i].tag == decimal_tag:
            print(f"L1 invalidated: {victim.address} (tag {hex(decimal_tag)[2:]}, index {decimal_index}, {'dirty' if L1_cache[decimal_index][i].dirty else 'clean'})")
            if L1_cache[decimal_index][i].dirty == 1:
                var.memtraffic += 1
                print("L1 writeback to main memory directly")
            L1_cache[decimal_index][i].address = ''
            L1_cache[decimal_index][i].valid = 0
            L1_cache[decimal_index][i].tag = 0
            L1_cache[decimal_index][i].counter = 0
            L1_cache[decimal_index][i].dirty = 0
            break

# Main function 
def main(args):
    var.block_size = int(args[1])			# Same size for all blocks
    l1.size = int(args[2])					# L1 Cache Size
    l1.assoc = int(args[3])					# L1 Set Associativity (1-Direct Mapped)
    l2.size = int(args[4])					# L2 Cache Size
    l2.assoc = int(args[5])					# L2 Set Associativity (1-Direct Mapped)
    var.replacement_policy = int(args[6])	# 0-LRU	| 1-FIFO
    var.inclusion_property = int(args[7])	# 0-Non-inclusive | 1-Inclusive
    var.trace_file = args[8]				# Full name of trace file

    # Find relevant parameters for L1 and L2 Caches 
    l1.offset_width, l1.index_width, l1.tag_width = calculate_widths(l1.size, var.block_size, l1.assoc)
    if l2.assoc!=0 and l2.size!=0:
        l2.offset_width, l2.index_width, l2.tag_width = calculate_widths(l2.size, var.block_size, l2.assoc)
        
    # Define L1 and L2 Caches as 2D arrays of size assoc*2^idx
    L1_cache = [[Cache() for _ in range(l1.assoc)] for _ in range(2**l1.index_width)]
    L2_cache = [[Cache() for _ in range(l2.assoc)] for _ in range(2**l2.index_width)]

    print("===== Simulator configuration =====")
    print("BLOCKSIZE:\t\t", var.block_size)
    print("L1_SIZE:\t\t", l1.size)
    print("L1_ASSOC:\t\t", l1.assoc)
    print("L2_SIZE:\t\t", l2.size)
    print("L2_ASSOC:\t\t", l2.assoc)

    if var.replacement_policy == 0:
        print("REPLACEMENT POLICY:\t LRU")
    else:
        print("REPLACEMENT POLICY:\t FIFO")

    if var.inclusion_property == 0:
        print("INCLUSION PROPERTY:\t non-inclusive")
    else:
        print("INCLUSION PROPERTY:\t inclusive")

    print("trace_file:\t\t", var.trace_file)

    f = open(var.trace_file, 'r')
    f.seek(0)
    cnt = 0
    while True:
        cnt += 1
        if f.tell() == os.fstat(f.fileno()).st_size:
            break

        r_w, var.address = f.readline().split()
        bin_address = bin(int(var.address, 16))[2:].zfill(32)

        l1.decimal_tag = int(bin_address[0:l1.tag_width], 2)
        l1.decimal_index = int(bin_address[l1.tag_width: l1.tag_width+l1.index_width], 2)
        l1.decimal_offset = int(bin_address[l1.tag_width+l1.index_width:], 2)

        if l2.size != 0:
            l2.decimal_tag = int(bin_address[0:l2.tag_width], 2)
            l2.decimal_index = int(bin_address[l2.tag_width: l2.tag_width+l2.index_width], 2)
            l2.decimal_offset = int(bin_address[l2.tag_width+ l2.index_width:], 2)
        
        if r_w.lower() == 'r':
            print('-'*40)
            print(f"# {cnt} : read {var.address}")
            var.address = var.address[:-1]+'0'
            read_l1_cache(L1_cache, L2_cache)
        elif r_w.lower() == 'w':
            print('-'*40)
            print(f"# {cnt} : write {var.address}")
            var.address = var.address[:-1]+'0'
            write_l1_cache(L1_cache, L2_cache)
        else:
            print("Error in the input trace file")
    
    print("===== L1 contents =====")
    for i in range(len(L1_cache)):
        print(f"Set \t{i}:", end='\t\t')
        for j in range(l1.assoc):
            print(f"{hex(L1_cache[i][j].tag)[2:]} {'D' if L1_cache[i][j].dirty else ' '}", end='  ')
        print()

    if l2.size != 0:
        print("===== L2 contents =====")
        for i in range(len(L2_cache)):
            print(f"Set \t{i}:", end='\t\t')
            for j in range(l2.assoc):
                print(f"{hex(L2_cache[i][j].tag)[2:]} {'D' if L2_cache[i][j].dirty else ' '}", end='  ')
            print()

    l1.miss_rate = (l1.read_misses + l1.write_misses) / (l1.reads + l1.writes)
    l2.miss_rate = 0 if l2.size == 0 else (l2.read_misses) / (l2.reads)
    memtraffic = l1.read_misses + l1.write_misses + l1.write_backs if l2.size == 0 else l2.read_misses + l2.write_misses + l2.write_backs + var.memtraffic

    print("===== Simulation results (raw) =====")
    print("a. number of L1 reads:         ", l1.reads)
    print("b. number of L1 read misses:   " , l1.read_misses)
    print("c. number of L1 writes:        ", l1.writes)
    print("d. number of L1 write misses:  ", l1.write_misses)
    print("e. L1 miss rate:               ", "{:.6f}".format(l1.miss_rate))
    print("f. number of L1 writebacks:    ", l1.write_backs)
    print("g. number of L2 reads:         ", l2.reads)
    print("h. number of L2 read misses:   ", l2.read_misses)
    print("i. number of L2 writes:        ", l2.writes)
    print("j. number of L2 write misses:  ", l2.write_misses)
    print("k. L2 miss rate:               ", "{:.6f}".format(l2.miss_rate) if l2.miss_rate else l2.miss_rate)
    print("l. number of L2 writebacks:    ", l2.write_backs)
    print("m. total memory traffic:       ", memtraffic)
    f.close()

# Start of the program 
if __name__ == "__main__":
    main(sys.argv)