# logmap/utils.py

def get_local_name(entity):
    """
    Extract a local name from an entity's IRI.
    For example, 'source.xml.MA_0000165' becomes 'MA_0000165'.
    """
    iri_str = str(entity)
    parts = iri_str.split('.')
    return parts[-1] if parts else iri_str
