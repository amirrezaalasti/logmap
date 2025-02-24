# logmap/inverted_index.py
from collections import defaultdict

class InvertedIndexBuilder:
    def __init__(self, external_lexicon=None):
        """
        external_lexicon: An object with a method get_variations(term)
        """
        self.external_lexicon = external_lexicon

    def build_index(self, ontology):
        if ontology is None:
            raise ValueError("Ontology is not loaded!")

        index = defaultdict(set)  # Key: frozenset of normalized terms, Value: set of class IDs
        class_id_map = {}         # Map class URIs to numerical IDs
        current_id = 0

        # Assign numerical IDs to classes
        for cls in ontology.classes():
            class_id_map[cls.iri] = current_id
            current_id += 1

        for cls in ontology.classes():
            cls_id = class_id_map[cls.iri]
            labels = cls.label if hasattr(cls, 'label') else []  # Get all labels

            for label in labels:
                # Split into components (e.g., "cellular_secretion" → ["cellular", "secretion"])
                components = label.lower().replace('_', ' ').split()

                # Add base term set
                term_set = frozenset(components)
                index[term_set].add(cls_id)

                # Add variations from external lexicon (if provided)
                if self.external_lexicon:
                    variations = set()
                    for term in components:
                        variations.update(self.external_lexicon.get_variations(term))
                    if variations:
                        expanded_terms = components + list(variations)
                        term_set_variations = frozenset(expanded_terms)
                        index[term_set_variations].add(cls_id)

        return index, class_id_map
