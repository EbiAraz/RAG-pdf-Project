from configs.settings import TOP_K


def retrieve(index,query_vector):

    distances , indices = index.search(query_vector, TOP_K)

    return indices[0]