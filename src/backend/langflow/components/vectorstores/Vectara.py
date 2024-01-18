from typing import Optional, Union, List
from langflow import CustomComponent
import tempfile
import urllib.request
import urllib

from langchain.vectorstores import Vectara
from langchain.schema import Document
from langchain.vectorstores.base import VectorStore
from langchain.schema import BaseRetriever
from langchain.embeddings import FakeEmbeddings


class VectaraComponent(CustomComponent):
    display_name: str = "Vectara"
    description: str = "Implementation of Vector Store using Vectara"
    documentation = "https://python.langchain.com/docs/integrations/vectorstores/vectara"
    beta = True
    field_config = {
        "vectara_customer_id": {
            "display_name": "Vectara Customer ID",
            "required": True,
        },
        "vectara_corpus_id": {
            "display_name": "Vectara Corpus ID",
            "required": True,
        },
        "vectara_api_key": {
            "display_name": "Vectara API Key",
            "password": True,
            "required": True,
        },
        "code": {"show": False},
        "documents": {
            "display_name": "Documents",
            "info": "Pass in either for Self Query Retriever or for making a Vectara Object",
        },
        "files_url": {
            "display_name": "Files Url",
            "info": "Make vectara object using url of files(documents not needed)",
        },
    }

    def build(
        self,
        vectara_customer_id: str,
        vectara_corpus_id: str,
        vectara_api_key: str,
        files_url: Optional[List[str]] = None,
        documents: Optional[Document] = None,
    ) -> Union[VectorStore, BaseRetriever]:
        if documents is not None:
            return Vectara.from_documents(
                documents=documents,
                embedding=FakeEmbeddings(size=768),
                vectara_customer_id=vectara_customer_id,
                vectara_corpus_id=vectara_corpus_id,
                vectara_api_key=vectara_api_key,
            )

        if files_url is not None:
            files_list = []
            for url in files_url:
                name = tempfile.NamedTemporaryFile().name
                urllib.request.urlretrieve(url, name)
                files_list.append(name)

            return Vectara.from_files(
                files=files_list,
                embedding=FakeEmbeddings(size=768),
                vectara_customer_id=vectara_customer_id,
                vectara_corpus_id=vectara_corpus_id,
                vectara_api_key=vectara_api_key,
            )

        return Vectara(
            vectara_customer_id=vectara_customer_id,
            vectara_corpus_id=vectara_corpus_id,
            vectara_api_key=vectara_api_key,
        )
