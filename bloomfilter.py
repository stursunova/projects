from bitarray import bitarray
import hashlib
import random
import string
import math
import time

class BloomFilter:
    def __init__(self, h_functions=[], error=0.1, expected = 1000):
        self.hash_functions = h_functions #hash functions
        self.error = error ## error probability


        ## actually, it should be calculated
        ## size = -(#expected_elem * ln self.error)/(ln2)**2
        self.array_size = 2**32 #int(-(expected * math.log(self.error))/(math.log(2))**2)
        print("\tBF array size = ", self.array_size)


        ## initialize bit array and set its all bits to 0
        self.bit_array = bitarray(self.array_size)
        self.bit_array.setall(0)


    ## add new item
    def add(self, item):
        for f in self.hash_functions:
            hashed = f(item) % self.array_size
            self.bit_array[hashed] = 1


    ## check whether bloom filter contains an item
    def contains(self, item):
        for f in self.hash_functions:
            hashed = f(item) % self.array_size
            if (self.bit_array[hashed]):
                return True

        return False



def hash_sha256(content):
    return int.from_bytes(hashlib.sha256(content.encode()).digest()[:32], 'little')

def hash_sha512(content):
    return int.from_bytes(hashlib.sha512(content.encode()).digest()[:32], 'little')

def hash_md5(content):
    return int.from_bytes(hashlib.md5(content.encode()).digest()[:32], 'little')

def hash_blake2b(content):
    return int.from_bytes(hashlib.blake2b(content.encode()).digest()[:32], 'little')


def id_generator(size=6):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits + "_") for _ in range(size))


if __name__ == "__main__":

    error = float(input("What is error probability[0.1~0.99]?:"))
    total = int(input("What is the total number of usernames: "))
    check = int(input("How many of them need to be checked: "))

    bf = BloomFilter([hash_sha256, hash_sha512, hash_md5, hash_blake2b], error, total)


    start = time.time()
    for i in range(total):
        #generate randome id between [5, 15] chars and add it to BF
        bf.add(id_generator(random.randrange(5, 15)))
    end = time.time()
    print(f"Time to add {total} number of users: [", round(end - start, 2), "] sec")
    cnt = 0

    for i in range(check):
        name = id_generator(random.randrange(6, 15))
        if (bf.contains(name)):
            cnt += 1
            #print(f"!!! {name} is in BF")


    print("Total number of found names: ", cnt)

    #for names in check_names:
    #    if (bf.contains(names)):
    #        print(f"!!! {names} is in BF")
    #    else:
    #        print(f"{names} does not exist in BF")
