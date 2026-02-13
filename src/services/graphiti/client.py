from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF

class GraphitiClient:
    def __init__(self,
                 neo4j_uri: str,
                 neo4j_user: str,
                 neo4j_password: str):
        # Params
        self._neo4j_uri = neo4j_uri
        self._neo4j_user = neo4j_user
        self._neo4j_password = neo4j_password

        self._graphiti_client = None

    async def build(self,
                    **kwargs):
        # Initialize Graphiti with Neo4j connection
        self._graphiti_client = Graphiti(uri = self._neo4j_uri,
                                         user = self._neo4j_user,
                                         password = self._neo4j_password,
                                         **kwargs)
        try:
            # Initialize the graph database with graphiti's indices. This only needs to be done once.
            await self._graphiti_client.build_indices_and_constraints()

        finally:
            # Close the connection
            await self._graphiti_client.close()