"""Variation Differentiator - Ensures LLMON variations are sufficiently distinct."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class VariationDifferentiator:
    """Validates and ensures variation differentiation."""
    
    def __init__(self, min_difference=0.3):
        """
        Initialize differentiator.
        
        Args:
            min_difference: Minimum required difference (0-1, where 1 = completely different)
        """
        self.min_difference = min_difference
    
    def calculate_similarity(self, text1, text2):
        """
        Calculate similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0 = completely different, 1 = identical)
        """
        try:
            # Use TF-IDF vectorization
            vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Fit and transform both texts
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            # Fallback: simple word overlap
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 or not words2:
                return 0.0
            
            overlap = len(words1 & words2)
            total = len(words1 | words2)
            
            return overlap / total if total > 0 else 0.0
    
    def calculate_difference(self, text1, text2):
        """
        Calculate difference between two texts.
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Difference score (0 = identical, 1 = completely different)
        """
        similarity = self.calculate_similarity(text1, text2)
        return 1.0 - similarity
    
    def validate_variations(self, variations):
        """
        Validate that variations are sufficiently different.
        
        Args:
            variations: List of variation texts
        
        Returns:
            Dictionary with validation results and similarity matrix
        """
        n = len(variations)
        
        if n < 2:
            return {
                'valid': True,
                'min_difference': 1.0,
                'avg_difference': 1.0,
                'similarity_matrix': [],
                'pairs_below_threshold': []
            }
        
        # Calculate pairwise similarities
        similarities = []
        pairs_below_threshold = []
        
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(1.0)  # Same text = 100% similar
                elif i < j:
                    sim = self.calculate_similarity(variations[i], variations[j])
                    row.append(sim)
                    similarities.append(sim)
                    
                    # Check if difference is below threshold
                    difference = 1.0 - sim
                    if difference < self.min_difference:
                        pairs_below_threshold.append({
                            'pair': (i + 1, j + 1),  # 1-indexed for display
                            'similarity': round(sim, 3),
                            'difference': round(difference, 3)
                        })
                else:
                    # Use already calculated value (matrix is symmetric)
                    row.append(similarities[self._get_similarity_index(j, i, n)])
            
        # Calculate statistics
        min_similarity = min(similarities) if similarities else 0.0
        avg_similarity = np.mean(similarities) if similarities else 0.0
        
        max_difference = 1.0 - min_similarity
        avg_difference = 1.0 - avg_similarity
        
        valid = len(pairs_below_threshold) == 0
        
        return {
            'valid': valid,
            'min_difference': round(max_difference, 3),
            'avg_difference': round(avg_difference, 3),
            'min_similarity': round(min_similarity, 3),
            'avg_similarity': round(avg_similarity, 3),
            'pairs_below_threshold': pairs_below_threshold,
            'threshold': self.min_difference
        }
    
    def _get_similarity_index(self, i, j, n):
        """Get index in flattened similarity list for pair (i, j) where i < j."""
        # Convert 2D coordinates to 1D index
        return int(i * n - (i * (i + 1)) / 2 + j - i - 1)
    
    def get_differentiation_report(self, variations):
        """
        Generate a human-readable differentiation report.
        
        Args:
            variations: List of variation texts
        
        Returns:
            Formatted report string
        """
        validation = self.validate_variations(variations)
        
        report = f"\n{'='*60}\n"
        report += "VARIATION DIFFERENTIATION REPORT\n"
        report += f"{'='*60}\n\n"
        
        report += f"Minimum Difference: {validation['min_difference']*100:.1f}%\n"
        report += f"Average Difference: {validation['avg_difference']*100:.1f}%\n"
        report += f"Required Threshold: {validation['threshold']*100:.1f}%\n\n"
        
        if validation['valid']:
            report += "[OK] All variations are sufficiently different!\n"
        else:
            report += f"[WARNING] {len(validation['pairs_below_threshold'])} pair(s) below threshold:\n\n"
            for pair_info in validation['pairs_below_threshold']:
                report += f"  Variation {pair_info['pair'][0]} <-> Variation {pair_info['pair'][1]}: "
                report += f"{pair_info['difference']*100:.1f}% different "
                report += f"(similarity: {pair_info['similarity']*100:.1f}%)\n"
        
        report += f"\n{'='*60}\n"
        
        return report
    
    def identify_least_different_pair(self, variations):
        """
        Find the pair of variations that are most similar.
        
        Args:
            variations: List of variation texts
        
        Returns:
            Tuple of (index1, index2, similarity_score)
        """
        if len(variations) < 2:
            return None
        
        max_similarity = -1
        most_similar_pair = (0, 1)
        
        for i in range(len(variations)):
            for j in range(i + 1, len(variations)):
                sim = self.calculate_similarity(variations[i], variations[j])
                if sim > max_similarity:
                    max_similarity = sim
                    most_similar_pair = (i, j)
        
        return (most_similar_pair[0], most_similar_pair[1], max_similarity)
    
    def suggest_regeneration(self, variations):
        """
        Suggest which variation to regenerate for better differentiation.
        
        Args:
            variations: List of variation texts
        
        Returns:
            Index of variation to regenerate (or None if all are good)
        """
        validation = self.validate_variations(variations)
        
        if validation['valid']:
            return None
        
        # Count how many problematic pairs each variation is involved in
        involvement_count = [0] * len(variations)
        
        for pair_info in validation['pairs_below_threshold']:
            idx1, idx2 = pair_info['pair']
            involvement_count[idx1 - 1] += 1  # Convert to 0-indexed
            involvement_count[idx2 - 1] += 1
        
        # Suggest regenerating the variation involved in most problematic pairs
        max_involvement = max(involvement_count)
        if max_involvement > 0:
            return involvement_count.index(max_involvement)
        
        return None

