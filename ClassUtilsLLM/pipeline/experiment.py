## incomplete yet ##
from ..sampling import sampling as sampling_f
from ..llm.taxonomy import taxonomy as taxonomy_f
from ..llm.resume import resume as resume_f
from ..llm.context import context as context_f
from ..llm.query import create_llm_query
# from ..llm.find_group import itBelongs
from ..predictors.predictors import predictor
# from utme.UTME import UTME
# from ..utme.utme_pipeline import utme_pipeline

import datetime

class Experiment():
    def __init__(self,config):
        """
        Init function
        
        Args:
            config:dict - a dict in which the keys are strings and 
                the values are a tuple. The first item of the tuple is 
                the method used and the second item is the kwargs. The 
                dict must be the following keys: 'sampling','taxonomy', 
                'resume', 'context', 'predictor'.
            
        """
        self.config=config   
    def run(self,embeddings,docs,llm_query):
        """
        Method to run all the steps in sequence
        
        Args:
            embeddings:np.ndarray - all embeddings of the documents of your dataset
            docs:list[str] - all documents of your dataset
            llm_query:func(str)->str - function to query to llm's API
        """
        self.datetime_begin = datetime.datetime.now()
        
        mS,Skwargs = self.config['sampling']
        mT,Tkwargs = self.config['taxonomy']
        mR,Rkwargs = self.config['resume']
        mC,Ckwargs = self.config['context']
        # mP,Pkwargs = self.config['predictor']
        
        ## Sampling
        self.samples = sampling_f(embeddings,method=mS,
                           k=Skwargs['k'],
                           n_clusters=Skwargs['n_clusters'])
        
        
        ## Taxonomy
        sampled_docs = [docs[sample] for sample in self.samples]
        self.taxonomy = taxonomy_f(sampled_docs,llm_query,
                       n_taxonomy=Tkwargs['n_taxonomy'],method=mT)
        
        ## Resume
        self.resume = resume_f(self.taxonomy,llm_query,
                     n_taxonomy=Rkwargs['n_taxonomy'],method=mR)
        
        ## Context
        self.context = context_f(self.resume, llm_query, method=mC)
        
        
        
        
        # hasUTME = ('UTME' in self.config.keys())
        # UTMEkwargs={}
        # if(hasUTME):
        #     UTMEkwargs=self.config['UTME']
        ## UTME - group finetunin (FAZER UM REAJUSTE DOS KMEANS !!! CONSIDERANDO O NOME DO TOPICO)
        # llm_options = {'model': "openchat_3.5", 'max_tokens': 1024}
        # utme_base = UTME(self.llm_base, self.llm_key, llm_options)
        # utme_pipeline(df,indexes,tax,con,utme_base)
        
        
        
        ## Predictor
            ## most representatives to each kmeans group
        # most_representatives = sampling(embeddings,method=methods.KNEAR,
        #                    k=1,
        #                    n_clusters=Skwargs['n_clusters'])
        
        # most_representatives_docs = [docs[idx] for idx in most_representatives]
        # samples_Y = [itBelongs(docs[s],most_representatives_docs,llm_query) for s in samples]
        
        # self.prediction = predictor(samples,samples_Y,embeddings)
        
        
        self.datetime_final = datetime.datetime.now()
        self.duration_time  = self.datetime_begin-self.datetime_final