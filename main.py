# main.py
from logmap.ontology import Ontology
from logmap.inverted_index import InvertedIndexBuilder
from logmap.anchor_mapper import AnchorMapper
from ontology_loader import OntologyLoader

# Assume source_ontology and target_ontology are provided by your existing code.
# They should have the methods: classes(), get_parents_of(), get_children_of(), etc.
# Wrap them with our Ontology class if needed.
source_address = 'data/mouse-human/source.xml'
target_address = 'data/mouse-human/target.xml'

source_ontology = OntologyLoader(source_address)
target_ontology = OntologyLoader(target_address)

source_ontology.load()
target_ontology.load()

source_ont = Ontology(source_ontology.ontology)
target_ont = Ontology(target_ontology.ontology)

# Build inverted indexes
index_builder = InvertedIndexBuilder(external_lexicon=None)  # Provide an external lexicon if available
source_index = index_builder.build_index(source_ont)
target_index = index_builder.build_index(target_ont)

# Compute anchor mappings
anchor_mapper = AnchorMapper(source_ont, target_ont, source_index, target_index, isub_threshold=0.8)
anchors = anchor_mapper.compute_anchors()

print("Anchor mappings with confidence scores:")
for mapping, confidence in anchors.items():
    print(f"{mapping}: {confidence}")
