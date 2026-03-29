""""
Workflow minimal

Vecteurs numpy
→
Créer index
→
index.add()
→
index.search()
→
IDs + distances
"""

import faiss
import numpy as np

d = 128           # dimension des vecteurs
n = 10000         # nombre de vecteurs

# FAISS exige float32 C-contiguous
xb = np.random.randn(n, d).astype('float32')

# Créer + peupler l'index
index = faiss.IndexFlatL2(d)
index.add(xb)

# Recherche des 5 plus proches voisins
xq = np.random.randn(3, d).astype('float32')
D, I = index.search(xq, k=5)
# D: distances (n_queries, k)  I: indices (n_queries, k)
#⚡ Toujours float32 et C-contiguous. Si erreur → np.ascontiguousarray(x.astype('float32'))


# Creation des diffrents types d'index (Voir md)

#IVFFlat besoin train
# nlist = nb de clusters (√n)
quantizer = faiss.IndexFlatL2(d)
index = faiss.IndexIVFFlat(
    quantizer, d, nlist=100
)

index.train(xb)
index.add(xb)

index.nprobe = 10  # clusters sondés


#IVFPQ besoin train
# m=nb sous-vecteurs, bits/subvec
index = faiss.IndexIVFPQ(
    quantizer, d,
    nlist=100, m=8, nbits=8
)
index.train(xb)
index.add(xb)
index.nprobe = 10


#HNSW no training
# M = nb de liens par nœud
index = faiss.IndexHNSWFlat(
    d, M=32
)
index.add(xb)  # pas de train()


# Cosine similarity
# Normaliser → L2 = cosine
faiss.normalize_L2(xb)
faiss.normalize_L2(xq)
index = faiss.IndexFlatIP(d)
index.add(xb)


#String factory (notation compacte)
# Équivalent IVFPQ avec OPQ preprocessing
index = faiss.index_factory(
    d, "OPQ16,IVF256,PQ16", faiss.METRIC_L2
)
# Autres exemples : "Flat", "IVF100,Flat", "HNSW32"