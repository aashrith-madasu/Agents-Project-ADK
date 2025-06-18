from dotenv import load_dotenv
load_dotenv()

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
import os
import requests
import json


def retrieve_external_knowledge(query: str) -> dict:
    """Tool used to retrieve external knowledge about anything that is not relevant to weather
        Args:
            query (str) : query string to use for searching retrieve knowledge
    """
    
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_REST_ENDPOINT"),
        auth_credentials=Auth.api_key(os.getenv("WEAVIATE_API_KEY")),
    )
    questions = client.collections.get("Question")
    response = questions.query.near_text(
        query=query,
        limit=1
    )
    obj = response.objects[0].properties
    result_str = (f"Question: {obj['question']}"
                  f"Answer: {obj['answer']}")
    return {
        "status": "success",
        "result": result_str
    }
