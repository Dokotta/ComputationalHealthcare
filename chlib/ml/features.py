import os,gzip
import numpy as np
from collections import defaultdict
from ..entity import enums
from sklearn.feature_extraction.text import CountVectorizer

class VisitToFeature(object):

    def __init__(self,dataset):
        self.feature_to_index = {}
        self.index_to_feature = {}
        self.current_index = 0
        self.max_los = 50
        self.dataset = dataset
        self.features_path = "{}/featurelist.txt".format(self.dataset.ml_dir)
        if os.path.isfile(self.features_path):
            for line in file(self.features_path):
                feat,index = line.strip('\n').split('\t')
                index = int(index)
                self.feature_to_index[feat] = index
                self.index_to_feature[index] = feat
                self.current_index = len(self.feature_to_index)
            self.mode_fit = False
        else:
            self.mode_fit = True
            self.generate_features()

    def generate_features(self):
        for code in self.dataset.iter_codes():
            if code.code_type in ['dx','pr','ex'] and code.visits_count() >= 25:
                self.add_feature(code.code)
        for age in range(0,100):
            self.add_feature('Age_{}'.format(age/10))
        for los in range(0,self.max_los):
            self.add_feature('LOS_{}'.format(los))
        for i in enums.PAYER.values():
            self.add_feature('Payer_{}'.format(i))
        for i in enums.SOURCE.values():
            self.add_feature('Source_{}'.format(i))
        for i in enums.DISPOSITION.values():
            self.add_feature('Disp_{}'.format(i))
        with open(self.features_path,'w') as out:
            for k,v in self.feature_to_index.iteritems():
                out.write("{}\t{}\n".format(k,v))
        self.mode_fit = False

    def add_feature(self,value):
        if self.mode_fit and value not in self.feature_to_index:
            self.feature_to_index[value] = self.current_index
            self.index_to_feature[self.current_index] = value
            self.current_index += 1

    def get_feature(self,value):
        if value in self.feature_to_index:
            return (value,self.feature_to_index[value])
        else:
            return None

    def all_past_codes(self,p,last_visit):
        not_found = True
        indexes = []
        for v in p.visits:
            if v.key == last_visit.key:
                not_found = False
            elif v.day < last_visit.day: # visit earlier than the day of index visit
                indexes += self.get_code_features(v)
        if not_found:
            raise ValueError
        else:
            return indexes

    def get_code_features(self,v):
        indexes = []
        for pr in v.prs:
            indexes.append(self.get_feature(pr.pcode))
        for dx in v.dxs:
            indexes.append(self.get_feature(dx))
        for ex in v.exs:
            indexes.append(self.get_feature(ex))
        return filter(None,indexes)

    def get_features(self,v):
        indexes = []
        for pr in v.prs:
            indexes.append(self.get_feature(pr.pcode))
        for dx in v.dxs:
            indexes.append(self.get_feature(dx))
        for ex in v.exs:
            indexes.append(self.get_feature(ex))
        if v.age >= 0:
            indexes.append(self.get_feature('Age_{}'.format(int(v.age)/10)))
        if v.los >= 0 and v.los < self.max_los:
            indexes.append(self.get_feature('LOS_{}'.format(v.los)))
        elif v.los >= self.max_los:
            indexes.append(self.get_feature('LOS_{}'.format(self.max_los-1)))
        indexes.append(self.get_feature('Source_{}'.format(v.source)))
        indexes.append(self.get_feature('Payer_{}'.format(v.payer)))
        indexes.append(self.get_feature('Disp_{}'.format(v.disposition)))
        return filter(None,indexes)


    # def get_form_features(self, form_data):
    #     indexes = []
    #     for k in form_data:
    #         if k.startswith('D') or k.startswith('')
    #     for pr in v.prs:
    #         indexes.append(self.get_feature(pr.pcode))
    #     for dx in v.dxs:
    #         indexes.append(self.get_feature(dx))
    #     for ex in v.exs:
    #         indexes.append(self.get_feature(ex))
    #     if v.age >= 0:
    #         indexes.append(self.get_feature('Age_{}'.format(int(v.age) / 10)))
    #     if v.los >= 0 and v.los < self.max_los:
    #         indexes.append(self.get_feature('LOS_{}'.format(v.los)))
    #     elif v.los >= self.max_los:
    #         indexes.append(self.get_feature('LOS_{}'.format(self.max_los - 1)))
    #     indexes.append(self.get_feature('Source_{}'.format(v.source)))
    #     indexes.append(self.get_feature('Payer_{}'.format(v.payer)))
    #     indexes.append(self.get_feature('Disp_{}'.format(v.disposition)))
    #     return filter(None, indexes)


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