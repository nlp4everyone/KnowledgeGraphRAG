# Inherit
from ..base import BaseTextParser
# Main component
from llama_parse import LlamaParse
# Config
from src.core.config import LLAMAPARSE_API_KEY
# Object
from llama_index.core.schema import Document
from llama_cloud_services.parse.utils import ResultType
# Typing
from typing import List, Tuple

class LlamaParseParser(BaseTextParser):
    def __init__(self,
                 api_key :str = LLAMAPARSE_API_KEY,
                 num_worker :int = 1,
                 result_type :ResultType = ResultType.MD,
                 verbose :bool = True,
                 **kwargs):
        # Define params
        self._api_key = api_key
        self._num_worker = num_worker

        # Define parser
        self._parser = LlamaParse(api_key = self._api_key,
                                  result_type = result_type,
                                  num_workers = self._num_worker,
                                  verbose = verbose,
                                  **kwargs)

    async def parse(self,
                    file_input :str,
                    lazy_load :bool = False) -> Tuple[str, List[Document]]:
        # Check if enable lazy load
        if lazy_load:
            raise ValueError("Not support lazy load")
        # Parser document
        documents :List[Document] = await self._parser.aload_data(file_input)
        # Define content
        content = "\n".join([doc.text_resource.text for doc in documents])
        return content, documents