import ssl
import pandas as pd
from ast import literal_eval
from cdqa.utils.filters import filter_paragraphs
from cdqa.utils.download import download_model, download_bnpp_data
from cdqa.pipeline.cdqa_sklearn import QAPipeline

def answerQuery(query=None, database_path=None):
    """
    """
    # Download data and models
    ssl._create_default_https_context = ssl._create_unverified_context
    download_model(model='bert-squad_1.1', dir='./models')
    if not database_path:
        download_bnpp_data(dir='./data/bnpp_newsroom_v1.1/')
        database_path = "data/bnpp_newsroom_v1.1/bnpp_newsroom-v1.1.csv"

    # Loading data and filtering / preprocessing the documents
    df = pd.read_csv(f'{database_path}', converters={'paragraphs': literal_eval})
    df = filter_paragraphs(df)

    # Loading QAPipeline with CPU version of BERT Reader pretrained on SQuAD 1.1
    cdqa_pipeline = QAPipeline(reader='models/bert_qa_vCPU-sklearn.joblib')

    # Fitting the retriever to the list of documents in the dataframe
    cdqa_pipeline.fit_retriever(df)

    # Sending a question to the pipeline and getting prediction
    if not query:
        query = 'Since when does the Excellence Program of BNP Paribas exist?'
        
    prediction = cdqa_pipeline.predict(query)
    results = {
                "query": query,
                "answer": prediction[0],
                "title": prediction[1],
                "paragraph": prediction[2]
                }

    return results

answerQuery("what is life?")