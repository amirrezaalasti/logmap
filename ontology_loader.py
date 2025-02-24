"""
ontology_loader.py

This module provides the OntologyLoader class for loading and preprocessing ontologies.
It uses owlready2 to load ontologies from a given file path or IRI.
"""

from owlready2 import get_ontology, Ontology
from typing import Optional

class OntologyLoader:
    def __init__(self, source: str) -> None:
        """
        Initialize the OntologyLoader with a source, which can be a file path or IRI.
        
        Args:
            source (str): The file path or IRI of the ontology to load.
        """
        self.source: str = source
        self.ontology: Optional[Ontology] = None

    def load(self) -> Ontology:
        """
        Load the ontology from the provided source.
        
        Returns:
            Ontology: The loaded ontology.
            
        Raises:
            Exception: If the ontology cannot be loaded.
        """
        try:
            self.ontology = get_ontology(self.source).load()
            print(f"Ontology loaded successfully from {self.source}")
        except Exception as e:
            print(f"Error loading ontology from {self.source}: {e}")
            raise e
        return self.ontology

    def normalize_labels(self) -> None:
        """
        Normalize labels of ontology entities by converting them to lowercase.
        This is a basic preprocessing step.
        
        Raises:
            ValueError: If the ontology has not been loaded.
        """
        if not self.ontology:
            raise ValueError("Ontology not loaded. Please call load() before normalization.")

        print("Normalizing labels for ontology entities...")
        for entity in self.ontology.classes():
            if hasattr(entity, 'label') and entity.label:
                # Convert each label to lowercase
                normalized_labels = [label.lower() for label in entity.label]
                entity.label = normalized_labels
        print("Normalization completed.")