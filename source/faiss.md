
| Index | Cas d'usage | Vitesse | RAM | Précision |
|---|---|---|---|---|
| IndexFlatL2 | Recherche exacte, baseline, < 1M vecteurs | Lent | Élevée | 100% |
| IndexFlatIP | Similarité cosinus (avec normalisation) | Lent | Élevée | 100% |
| IndexIVFFlat | ANN rapide, > 100k vecteurs | Rapide | Élevée | ~98% |
| IndexIVFPQ | Millions de vecteurs, RAM limitée | Très rapide | Faible | ~95% |
| IndexHNSW | ANN haute précision, sans entraînement | Rapide | Élevée | ~99% |
| IndexPQ | Compression maximale, sans IVF | Moyen | Très faible | ~90% |
