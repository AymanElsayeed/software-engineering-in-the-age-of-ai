import weaviate
from weaviate.client import WeaviateClient
from weaviate.classes.config import Configure, DataType, Property
from weaviate.classes.data import DataObject
from weaviate.classes.init import Auth
from weaviate.util import generate_uuid5
import weaviate.classes as wvc
import os
import json
from dotenv import load_dotenv
from pathlib import Path
from utils.embeddings import embed_text
from utils.logging_config import get_task2_logger
logger = get_task2_logger(__name__)


def connect_to_my_db() -> WeaviateClient:
    """
    Helper function to connect to the demo Weaviate database.
    For queries only.
    This database instance has the necessary data loaded.
    :return: WeaviateClient
    :rtype: WeaviateClient
    """
    utils_env = Path(__file__).resolve().parent / ".env"
    task_env = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=utils_env if utils_env.exists() else task_env)
    cluster_url = (
        os.getenv("WEAVIATE_CLUSTER_URL")
        or os.getenv("WEAVIATE_URL")
        or ""
    ).strip().strip('"')
    if cluster_url and not cluster_url.startswith(("http://", "https://")):
        cluster_url = f"https://{cluster_url}"
    api_key = (os.getenv("WEAVIATE_API_KEY") or "").strip().strip('"')
    if not cluster_url:
        raise RuntimeError("Missing WEAVIATE_CLUSTER_URL/WEAVIATE_URL in .env")
    if not api_key:
        raise RuntimeError("Missing WEAVIATE_API_KEY in .env")
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=cluster_url,
        auth_credentials=Auth.api_key(api_key),
    )
    logger.info(f"Connected to Weaviate database: {client.is_ready()}")
    return client

def create_collection(client: WeaviateClient, collection_name: str):
    """
    Create a collection in the Weaviate database.
    :param client: WeaviateClient
    :param collection_name: str
    :return: WeaviateClient
    :rtype: WeaviateClient
    """
    if client.collections.exists(collection_name):
        return client.collections.get(collection_name)
    else:
        properties = [
            Property(name="kind", data_type=DataType.TEXT),
            Property(name="text", data_type=DataType.TEXT),
            Property(name="answer", data_type=DataType.TEXT, skip_vectorization=True,),
            Property(name="meta_json", data_type=DataType.TEXT),
        ]
        # Match "self-provided" vector mode: when inserting/searching we must pass `vector=...`.
        client.collections.create(
            collection_name,
            properties=properties,
            vector_config=Configure.Vectors.self_provided(),
        )
    return client.collections.get(collection_name)

def add_document_to_collection(client: WeaviateClient, collection_name: str, text: str, answer: str, metaq: dict):
    properties = {
        "kind": "kb",
        "text": text,
        "answer": answer,
        "meta_json": json.dumps(metaq),
    }
    uuid = generate_uuid5(text)
    try:
        vec = embed_text(text)
        client.collections.get(collection_name).data.insert(
            properties=properties,
            vector=vec,
            uuid=uuid,
        )
    except weaviate.exceptions.UnexpectedStatusCodeError as e:
        print(f"Error adding document to collection: {e}")
        return False
    return True

def hybrid_search(client: WeaviateClient, collection_name: str, query: str, top_k: int = 10):
    collection = client.collections.get(collection_name)
    qv = embed_text(query)
    return_metadata=wvc.query.MetadataQuery(score=True, explain_score=True)
    alpha = 0.5 # alpha is the weight of the vector search
    results = collection.query.hybrid(query=query, vector=qv,limit=top_k, return_metadata=return_metadata,alpha=alpha)
    return results

def import_data_from_csv(client: WeaviateClient, limit = 12):
    import pandas as pd

    csv_file_path = "/Users/aymanelsayeed/Library/Mobile Documents/com~apple~CloudDocs/Documents/Education/תואר שיני/תשפו/סמסטר ב/הנדסת תוכנה בעידן ה- AI/software-engineering-in-the-age-of-ai/vdb/train_df.csv"
    collection_name = "Tickets"
    if not client.collections.exists(collection_name):
    #     client.collections.delete(collection_name)
        client.collections.create(
        name=collection_name,
        vector_config=Configure.Vectors.self_provided(),
        properties=[
            Property(name="body", data_type=DataType.TEXT),
            Property(name="department", data_type=DataType.TEXT),
            Property(name="priority", data_type=DataType.TEXT),
            Property(name="tags", data_type=DataType.TEXT),
            Property(name="answer", data_type=DataType.TEXT),
        ],
    )

    collection = client.collections.get(collection_name)

    df = pd.read_csv(csv_file_path)
    tickets_objects = []
    
    count = 0
    for index, row in df.iterrows():
        if count >= limit:
            break
        count += 1
        # add_document_to_collection(client, collection_name, row["text"], row["answer"], row["meta_json"])
        props ={
            "body": row["Body"],
            "department": row["Department"],
            "priority": row["Priority"],
            "tags": row["Tags"],
            "answer": "No answer found",
        }
        uuid = generate_uuid5(row["Body"])
        data_obj = DataObject(
            properties=props,
            uuid=uuid,
            vector=embed_text(row["Body"]),
        )
        #tickets_objects.append(data_obj)
        # insert the data object into the collection
        try:
            response = collection.data.insert(properties=props, vector=embed_text(row["Body"]), uuid=uuid)
            logger.info(f"Insertion complete with {response} objects.")
        except weaviate.exceptions.UnexpectedStatusCodeError as e:
            # print(f"Error inserting data object: {e}")
            logger.error(f"Error inserting data object: {e}")
            continue
    # response =client.collections.get(collection_name).data.insert_many(tickets_objects)
    # print(f"Insertion complete with {len(response.all_responses)} objects.")
    #print(f"Insertion errors: {len(response.errors)}.")
    return True

def rag(client: WeaviateClient, question: str):
    tickets = client.collections.get("Tickets")
    # question = "How to reset my password on my account"
    response = tickets.generate.near_text(query=question, limit=3,
                                        single_prompt="""
                                        You are a helpful assistant that can answer questions about the tickets.
                                        You are given a question and a list of tickets.
                                        You need to answer the question based on the tickets.
                                        The question is: {question}
                                        The tickets are: {tickets}
                                        The answer is:
    """)
    for result in response.objects:
        print("body: ", result.properties["body"])
        print(f"explain_score: {result.metadata.explain_score}\n")  # What was the distance?
        print(f"score: {result.metadata.score}\n")

def add_cache_entry(question: str, answer: str, meta: dict):
    client = connect_to_my_db()
    try:
        create_collection(client, "Ticket")
        result = add_document_to_collection(client, "Ticket", question, answer, meta)
        return result
    finally:
        client.close()

def semantic_cache_lookup(question: str, threshold: float = 0.88) -> str | None:
    client = connect_to_my_db()
    try:
        create_collection(client, "Ticket")
        result = hybrid_search(client, "Ticket", question)
        if not result.objects:
            return None
        best = result.objects[0]
        score = float(getattr(best.metadata, "score", 0.0) or 0.0)
        if score < threshold:
            return None
        return best.properties.get("answer")
    finally:
        client.close()

if __name__ == "__main__":
    # client = connect_to_my_db()
    # collection = create_collection(client, "test_collection")
    # add_document_to_collection(client, "test_collection", "test_text2", "test_answer", {"source": "test"})
    # results = hybrid_search(client, "test_collection", "test_text2")
    # # print(results)
    # import_data_from_csv(client)
    # results = hybrid_search(client, "Ticket", "How to reset my password on my account")
    # for result in results.objects:
    #     # print(result.properties)
    #     print("body: ", result.properties["body"])
    # #     print(result.properties["answer"])
    #     # print(result.properties["meta_json"])
    #     # print(result.vector)
    #     # print(result.score)
    #     print(f"explain_score: {result.metadata.explain_score}\n")  # What was the distance?
    #     print(f"score: {result.metadata.score}\n")
    
    # rag(client, "How to reset my password on my account")
    # client.close()
    # result = semantic_cache_lookup(question="How to reset my password on my account")
    # print(result)
    pass