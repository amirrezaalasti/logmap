# logmap/ontology.py

class Ontology:
    """
    A simple wrapper for an ontology object.
    Assumes that the underlying ontology object provides:
      - classes(): iterable of class objects (each having an 'iri' and optional 'label')
      - get_parents_of(node)
      - get_children_of(node)
    """
    def __init__(self, ontology):
        self.ontology = ontology

    def classes(self):
        return self.ontology.classes()

    def get_parents_of(self, node):
        return self.ontology.get_parents_of(node)

    def get_children_of(self, node):
        return self.ontology.get_children_of(node)
