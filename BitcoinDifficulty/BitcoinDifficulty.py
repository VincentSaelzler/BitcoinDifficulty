import csv

#https://en.bitcoin.it/wiki/Difficulty
BDIFF_1_HASH = 0x00000000ffff0000000000000000000000000000000000000000000000000000 # 32 leading 0 bits, 16 1 bits, 208 0 bits
PDIFF_1_HASH = 0x00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff # 32 leading 0 bits, 224 1 bits
STR_LENGTH_SHA_256 = 66 

def main():
    blocks = {
        'pdiff1' : Block(None, None, PDIFF_1_HASH)
        ,'bdiff1' : Block('0x1d00ffff')
        ,'sample from 2012' : Block('0x1b0404cb')
        ,'mine' : Block(None, 2927865188)
        ,'current' : Block('0x172f4f7b')
        }

    with open('BitcoinDiff.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['Hex Hash','Int Hash','Description','bdiff','pdiff'])
        for key in blocks:
            ds = blocks[key].hash_str
            ih = blocks[key].hash
            k = key
            bd = str(blocks[key].bdiff)
            pd = str(blocks[key].pdiff)
            spamwriter.writerow([ds,ih,k,bd,pd])

class Block:
    base_str = ''
    exp_str = ''
    hash_str = ''
    base = 0
    exp = 0
    hash = 0
    bdiff = 0.0
    pdiff = 0.0

    def __init__(self, packed_diff_str, bdiff = None, hash = None):
        if (bdiff is None) and (hash is None):
        #parse string
            self.base_str = '0x' + packed_diff_str[4:]
            self.exp_str = packed_diff_str[:4]
            #convert to ints
            self.base = int(self.base_str, 16)
            self.exp = int(self.exp_str, 16)
            #calculate hash (from packed string)
            self.hash = self.base * 2**(8*(self.exp - 3))
            self.bdiff = BDIFF_1_HASH / self.hash
        elif (hash is None):
            #calculate hash (from bdiff decimal number)
            self.bdiff = bdiff
            self.hash = int(BDIFF_1_HASH / self.bdiff)
        else:
            self.hash = hash
            self.bdiff = BDIFF_1_HASH / self.hash

        #create formatted diff string and calc pdiff
        self.hash_str = '{0:#0{1}x}'.format(self.hash,STR_LENGTH_SHA_256)
        self.pdiff = PDIFF_1_HASH / self.hash

if __name__ == '__main__':
    main()
