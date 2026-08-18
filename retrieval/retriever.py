from configs.settings import CANDIDATE_K, TOP_K


def retrieve(index, query_vector, k=None):
    if index is None or index.ntotal == 0:
        return [], []

    k = min(k or CANDIDATE_K or TOP_K, index.ntotal)
    scores, indices = index.search(query_vector, k)

    ids = []
    similarities = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue
        ids.append(int(idx))
        similarities.append(float(score))

    return ids, similarities
