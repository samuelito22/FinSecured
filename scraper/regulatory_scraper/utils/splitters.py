from typing import Sequence, Any, List
from llama_index.core.node_parser import SentenceSplitter, SemanticSplitterNodeParser
import logging
from llama_index.core.schema import BaseNode, Document, ObjectType, TextNode
from llama_index.core import Settings

class SafeSemanticSplitter(SemanticSplitterNodeParser):
    safety_chunker: SentenceSplitter = SentenceSplitter(
        chunk_size=Settings.chunk_size, chunk_overlap=Settings.chunk_overlap
    )

    def _parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        all_nodes: List[BaseNode] = super()._parse_nodes(
            nodes=nodes, show_progress=show_progress, **kwargs
        )
        all_good = True
        for node in all_nodes:
            if node.get_type() == ObjectType.TEXT:
                node: TextNode = node
                if self.safety_chunker._token_size(node.text) > self.safety_chunker.chunk_size:
                    logging.info("Chunk size too big after semantic chunking: switching to static chunking")
                    all_good = False
                    break
        if not all_good:
            all_nodes = self.safety_chunker._parse_nodes(nodes, show_progress=show_progress, **kwargs)
        return all_nodes
