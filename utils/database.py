import elasticsearch
from elasticsearch import helpers


def format_data_ES(dictionary):
    # variable for the Elasticsearch document _id
    id_num = 0
    # empty list for the Elasticsearch documents
    doc_list = []

    """
    Inject data into the doc_list
    """
    for entry, values in dictionary.items():
        doc_source = {"entry": str(entry)}

        for key, item in values.items():
            if key != "definitions":
                doc_source[str(key)] = str(item)
            else:
                doc_source["definitions"] = int(item)

        if "definitions" in doc_source:
            id_num += 1

            # Elasticsearch document structure as a Python dict
            doc = {
            # pass the integer value for _id to outer dict
            "_id": id_num,
            # nest the _source data inside the outer dict object
            "_source": doc_source,
            }
            # append the nested doc dict values to list
            doc_list += [ doc_source ]

    return doc_list


def load_ES(doc_list):
    """ Inject the docs into ElasticSearch
    Ref: https://kb.objectrocket.com/elasticsearch/how-to-parse-lines-in-a-text-file-and-index-as-elasticsearch-documents-using-python-641
    """

    # declare a client instance of the Python Elasticsearch client library
    client = Elasticsearch("http://localhost:9200")

    try:
        print ("nAttempting to index the dictionary entries using helpers.bulk()")
        # use the helpers library's Bulk API to index list of Elasticsearch docs
        response = helpers.bulk(client, doc_list, index='websters_dict', doc_type='_doc')
        # print the response returned by Elasticsearch
        print ("helpers.bulk() RESPONSE:", json.dumps(response, indent=4))
    except Exception as err:
        # print any errors returned by the Elasticsearch cluster
        print("helpers.bulk() ERROR:", err)


def load_database(dictionary):
    doc_list = format_data_ES(dictionary)
    if len(doc_list) > 0:
        load_ES(doc_list)
