import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from enum import Enum

def sampling_knear(embeddings,k,n_clusters,random_state=None):
  """
  Apply KMeans and obtain the indices from the 'k' points closest 
  to each cluster
  
  Args:
    embeddings:np.ndarray - Embeddings to extract the sampless
    k:int - number of points extracted from each cluster
    n_clusters:int - number of clusters generated by KMeans
    random_state:int [default=None] - random state of kmeans
  
  Returns:
    all_borders_ids:list[int] - a list of all sampled points
  """
  
  
  kmeans = KMeans(n_clusters=n_clusters,n_init='auto',random_state=random_state).fit(embeddings)
  
  nearest_neighbors = NearestNeighbors(n_neighbors=k+1,algorithm='ball_tree').fit(embeddings)
  _, representative_docs_ids = nearest_neighbors.kneighbors(kmeans.cluster_centers_)
  
  representative_docs_ids_k = []
  for ids in representative_docs_ids: representative_docs_ids_k.extend(ids[0:])
  
  return representative_docs_ids_k


def sampling_kborder(embeddings,k,n_clusters,random_state=None):
  """
  Apply KMeans and obtain the indices from the 'k' points further 
  to each cluster (they don't belong to cluster)
  
  Args:
    embeddings:np.ndarray - Embeddings to extract the sampless
    k:int - number of points extracted from each cluster
    n_clusters:int - number of clusters generated by KMeans
    random_state:int [default=None] - random state of kmeans
  
  Returns:
    all_borders_ids:list[int] - a list of all sampled points
  """
  kmeans = KMeans(n_clusters=n_clusters,n_init='auto',random_state=random_state).fit(embeddings)

  max_data_by_cluster = np.unique(kmeans.labels_,return_counts=True)[1]
  
  all_borders_ids = []
  for cluster_id in range(n_clusters):
    nearest_neighbors = NearestNeighbors(n_neighbors=max_data_by_cluster[cluster_id]+k,algorithm='ball_tree').fit(embeddings)
    _, docs_ids = nearest_neighbors.kneighbors([kmeans.cluster_centers_[cluster_id]])
    docs_ids = docs_ids[0]
    borders_ids = docs_ids[::-1]
    # print(f"representative_borders_ids: {borders_ids[:k]}       --->>> {[kmeans.labels_[i] for i in borders_ids[:k]]}")
    all_borders_ids.extend(borders_ids[:k])
  return all_borders_ids


def sampling_krandom(len_data,k):
  """
  Choose 'k' random indices between 0 and len(data)-1
  
  Args:
    len_data:int - len of embeddings to extract the sampless
    k:int - number of points extracted from each cluster
  
  Returns:
    :list[int] - a list of all sampled points
  """
  return np.random.randint(len_data,size=k)
  

def sampling_krandomclustered(embeddings,k,n_clusters,random_state=None):
  """
  Apply KMeans and obtain the indices from 'k' random points 
  to each cluster
  
  Args:
    embeddings:np.ndarray - Embeddings to extract the sampless
    k:int - number of points extracted from each cluster
    n_clusters:int - number of clusters generated by KMeans
    random_state:int [default=None] - random state of kmeans
  
  Returns:
    representative_ids:list[int] - a list of all sampled points
  """
  kmeans = KMeans(n_clusters=n_clusters,n_init='auto',random_state=random_state).fit(embeddings)
  representative_ids = []
  for label in range(n_clusters):
    whereis = np.where(kmeans.labels_ == label)[0]
    choosed = np.random.choice(whereis,size=(k,))
    representative_ids.extend(choosed)
  return representative_ids
  

class methods(Enum):
  KNEAR = 1
  KBORDER = 2
  KRANDOM = 3
  KRCLUSTER = 4

def sampling(embeddings,k,n_clusters=1,method=methods.KNEAR,random_state=None):
    """
    Main funcion for samplings, that group all the methods and choose one using the 
    enum sampling.methods.
    
    Args:
      embeddings:np.ndarray - Embeddings to extract the sampless
      k:int - number of points extracted
      n_clusters:int [default=1] - number of clusters generated by KMeans (don't used if it's random points)
      method:methods [default = methods.KNEAR] - choosed method
      random_state:int [default=None] - random state of kmeans
    
    Returns:
      representative_ids:list[int] - a list of all sampled points
    """
    if methods.KNEAR==method:
        return sampling_knear(embeddings,k,n_clusters,random_state=random_state)
    elif methods.KBORDER==method:
        return sampling_kborder(embeddings,k,n_clusters,random_state=random_state)
    elif methods.KRANDOM==method:
        return sampling_krandom(len(embeddings),k)
    elif methods.KRCLUSTER==method:
        return sampling_krandomclustered(embeddings,k,n_clusters,random_state=random_state)
    else:
        raise ValueError("sampling's method is invalid")