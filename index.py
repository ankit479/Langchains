ASTRA_DB_SECURE_BUNDLE_PATH="\Users\Ankit\desktop\webproj\search-python\secure-connect-db-ankit.zip"
ASTRA_DB_APPLICATION_TOKEN="AstraCS:UumFCRchKbaXTbSXtCAtComb:5c24bdd6d3e2ff9cbec391112931a833655ffc053a0692f49bd42e123cb5a87a"
ASTRA_DB_CLIENT_ID="UumFCRchKbaXTbSXtCAtComb"
ASTRA_DB_CLIENT_SECRET="hoFHcFhOMHUvFEzDPT0v4_ZTRmUioMjlMsh9mfqBjOjCBarHG-Z+tEBLlwa_3im_a1Sj1BLsbfAuXut-UdB-h1J.wg3Z0zSOv9Z2Z94D3N.bDrY9h5PT8yd_+iFd6c2F"
ASTRA_DB_KEYSPACE="ankit_db"
OPENAI_API_KEY="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"

from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorshare import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datasets import load_dataset
cloud_config={
    'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH
}
auth_provider= PlainTextAuthProvider(ASTRA_DB_CLIENT_ID,ASTRA_DB_CLIENT_SECRET)
cluster=Cluster(cloud=cloud_config, auth_provider=auth_provider)
astraSession=cluster.connect()

llm=OpenAi(openai_api_key=OPENAI_API_KEY)
myEmbedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

myCassandraVstore =Cassandra(
    embedding=myEmbedding,
    sessio=astraSession,
    keyspace=ASTRA_DB_KEYSPACE,
    table_name="qa_mini_demo"
)
print("Loading Data from Huggingface")
myDataset=load_dataset("Biddls/Onion News", split="train")
headlines= myDataset["text"][:50]
print("\n Generating embeddings and storing in AstraDB")
myCassandraVstore.add_texts(headlines)
print("Inserted %i headlines .\n" %len(headlines))
vectorIndex= VectorStoreIndexWrapper(vectorstore=myCassandraVStore)