import os,gzip
import numpy as np
from collections import defaultdict


class Embeddings(object):

    def __init__(self):
        self.vectors = {}
        self.prefixes = defaultdict(int)

    def load_precomputed(self):
        with gzip.open(os.path.dirname(os.path.abspath(__file__)) + '/data/claims_codes_hs_300.txt.gz') as fh:
            for i, line in enumerate(fh):
                if i > 2:
                    entries = line.strip().split()
                    code = entries[0].replace('IPR_', 'P_').replace('IDX_', 'D_').replace('.','').replace('D_E','E_E')
                    self.prefixes[code.split('_')[0]] += 1
                    code = code.replace('_', '')
                    if code in self.vectors:
                        print "Warning {} repeated {}".format(code,entries[0])
                    else:
                        self.vectors[code] = np.array([float(k) for k in entries[1:]],dtype=np.float)


    def get_vectors_from_visit(self,v):
        procedures = {}
        diagnoses = {}
        missing = set()
        for pr in v.prs:
            pcode = pr.pcode.split('_')[0]
            if pcode in self.vectors:
                procedures[pcode] = self.vectors[pcode]
            else:
                missing.add(pcode)
        for dx in v.dxs:
            if dx in self.vectors:
                diagnoses[dx] = self.vectors[dx]
            else:
                missing.add(dx)
        return procedures,diagnoses,missing