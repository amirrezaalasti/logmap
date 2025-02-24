# logmap/similarity.py
import re
from difflib import SequenceMatcher

class SimilarityCalculator:
    @staticmethod
    def isub_similarity(str1, str2):
        """
        Compute similarity score between two strings using SequenceMatcher as a proxy for ISUB.
        """
        return SequenceMatcher(None, str1, str2).ratio()

    @staticmethod
    def normalize_label(label):
        """
        Normalize a label by lowercasing, removing punctuation, and tokenizing.
        Returns a set of tokens.
        """
        label = label.lower().strip()
        label = re.sub(r'[^\w\s]', '', label)
        tokens = label.split()
        return set(tokens)

    @staticmethod
    def jaccard_similarity_tokens(set1, set2):
        """
        Compute the Jaccard similarity between two sets of tokenized labels.
        Each set (set1, set2) is assumed to be a set of strings.
        """
        tokens1 = set.union(*(SimilarityCalculator.normalize_label(s) for s in set1))
        tokens2 = set.union(*(SimilarityCalculator.normalize_label(s) for s in set2))
        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        return len(intersection) / len(union) if union else 0.0
