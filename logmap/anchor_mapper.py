# logmap/anchor_mapper.py
from itertools import product
from logmap.similarity import SimilarityCalculator
from logmap.utils import get_local_name

class AnchorMapper:
    def __init__(self, ontology1, ontology2, index1, index2, isub_threshold=0.8):
        """
        ontology1, ontology2: Ontology objects (or wrapped ontology)
        index1, index2: The inverted indexes as returned by InvertedIndexBuilder.build_index()
        isub_threshold: Similarity threshold to consider a mapping as an anchor.
        """
        self.ontology1 = ontology1
        self.ontology2 = ontology2
        self.index1 = index1  # Tuple: (index, class_id_map)
        self.index2 = index2
        self.isub_threshold = isub_threshold

    def compute_anchors(self):
        anchors = {}
        # Unpack the indexes; here index[0] is the actual index dictionary.
        inverted_index1 = self.index1[0]
        inverted_index2 = self.index2[0]

        # Step 1: Find common term sets between the inverted indexes
        common_term_sets = set(inverted_index1.keys()) & set(inverted_index2.keys())

        # Convert ontology classes to lists for ID lookup
        ontology1_list = list(self.ontology1.classes())
        ontology2_list = list(self.ontology2.classes())

        for term_set in common_term_sets:
            classes1 = inverted_index1[term_set]
            classes2 = inverted_index2[term_set]

            # Step 2: Generate candidate pairs and compute ISUB similarity
            for c1_id, c2_id in product(classes1, classes2):
                c1_obj = ontology1_list[c1_id]
                c2_obj = ontology2_list[c2_id]

                c1_label = c1_obj.label[0] if getattr(c1_obj, 'label', None) else ""
                c2_label = c2_obj.label[0] if getattr(c2_obj, 'label', None) else ""

                similarity = SimilarityCalculator.isub_similarity(c1_label, c2_label)

                # Step 3: Check if similarity meets the threshold
                if similarity >= self.isub_threshold:
                    confidence = self.compute_structural_confidence(c1_obj, c2_obj)
                    anchors[(str(c1_id), str(c2_id))] = confidence

        return anchors

    def compute_structural_confidence(self, node1, node2):
        """
        Compute the structural confidence between two ontology nodes.
        """
        def canonical(n):
            # TODO: check if this is the right way to get the local name
            if getattr(n, 'label', None) and n.label:
                return n.label[0]
            elif hasattr(n, 'iri'):
                return get_local_name(n.iri)
            else:
                return str(n)

        # Get parents and children from each ontology
        c1_parents = {canonical(p) for p in self.ontology1.get_parents_of(node1)}
        c1_children = {canonical(c) for c in self.ontology1.get_children_of(node1)}
        c2_parents = {canonical(p) for p in self.ontology2.get_parents_of(node2)}
        c2_children = {canonical(c) for c in self.ontology2.get_children_of(node2)}

        set1 = c1_parents | c1_children
        set2 = c2_parents | c2_children

        return SimilarityCalculator.jaccard_similarity_tokens(set1, set2)
