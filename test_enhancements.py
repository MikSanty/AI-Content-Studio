"""Test suite for all 6 priority enhancements."""
import unittest
import os
import json
import tempfile
import shutil
from quality_analyzer import QualityAnalyzer
from workflow_memory import WorkflowMemory
from variation_differentiator import VariationDifferentiator


class TestQualityAnalyzer(unittest.TestCase):
    """Test QualityAnalyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = QualityAnalyzer()
        
        self.sample_article = """# Introduction to AI

Artificial Intelligence (AI) is transforming our world. What does this mean for you? 
It means exciting opportunities and important challenges ahead.

## Understanding AI

AI systems can learn from data and make decisions. For example, Netflix uses AI to 
recommend shows you might enjoy. This technology analyzes your viewing patterns and 
preferences to make smart suggestions.

According to recent research, AI adoption has grown by 50% in the last year. Companies 
are investing heavily in this technology.

## Key Benefits

- Increased efficiency
- Better decision making
- Improved user experiences
- Cost savings

## Conclusion

The future of AI is bright. Understanding these technologies will help you navigate 
the changing landscape of work and technology."""

        self.sample_template = """# Introduction

## Section 1

## Section 2

## Conclusion"""

        self.sample_references = """AI adoption statistics from Gartner 2024.
Machine learning examples from industry reports.
Netflix recommendation algorithm documentation."""
    
    def test_readability_analysis(self):
        """Test readability scoring."""
        scores = self.analyzer.analyze(self.sample_article)
        
        self.assertIn('readability', scores)
        self.assertIn('score', scores['readability'])
        self.assertGreater(scores['readability']['score'], 0)
        self.assertLessEqual(scores['readability']['score'], 100)
        self.assertIn('grade_level', scores['readability'])
        self.assertIn('complexity', scores['readability'])
    
    def test_seo_analysis(self):
        """Test SEO scoring."""
        scores = self.analyzer.analyze(self.sample_article)
        
        self.assertIn('seo', scores)
        self.assertIn('score', scores['seo'])
        self.assertIn('word_count', scores['seo'])
        self.assertIn('headings_count', scores['seo'])
        self.assertGreater(scores['seo']['headings_count'], 0)
    
    def test_engagement_analysis(self):
        """Test engagement scoring."""
        scores = self.analyzer.analyze(self.sample_article)
        
        self.assertIn('engagement', scores)
        self.assertIn('questions', scores['engagement'])
        self.assertIn('examples', scores['engagement'])
        self.assertGreater(scores['engagement']['questions'], 0)
    
    def test_structure_analysis(self):
        """Test structure adherence."""
        scores = self.analyzer.analyze(self.sample_article, self.sample_template)
        
        self.assertIn('structure', scores)
        self.assertIn('template_match', scores['structure'])
        self.assertGreater(scores['structure']['template_match'], 0)
    
    def test_factual_consistency(self):
        """Test factual consistency checking."""
        scores = self.analyzer.analyze(
            self.sample_article, 
            self.sample_template, 
            self.sample_references
        )
        
        self.assertIn('factual', scores)
        self.assertIn('reference_citations', scores['factual'])
    
    def test_overall_score(self):
        """Test overall score calculation."""
        scores = self.analyzer.analyze(
            self.sample_article,
            self.sample_template,
            self.sample_references
        )
        
        self.assertIn('overall_score', scores)
        self.assertGreater(scores['overall_score'], 0)
        self.assertLessEqual(scores['overall_score'], 100)
    
    def test_format_summary(self):
        """Test score summary formatting."""
        scores = self.analyzer.analyze(self.sample_article)
        summary = self.analyzer.format_score_summary(scores)
        
        self.assertIsInstance(summary, str)
        self.assertIn('QUALITY ANALYSIS REPORT', summary)
        self.assertIn('Overall Score', summary)


class TestWorkflowMemory(unittest.TestCase):
    """Test WorkflowMemory functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.memory = WorkflowMemory(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_add_feedback(self):
        """Test adding feedback."""
        self.memory.add_feedback('writer', 'Great draft!', approved=True)
        
        self.assertEqual(len(self.memory.feedback_history), 1)
        self.assertEqual(self.memory.feedback_history[0]['stage'], 'writer')
        self.assertEqual(self.memory.feedback_history[0]['feedback'], 'Great draft!')
        self.assertTrue(self.memory.feedback_history[0]['approved'])
    
    def test_add_approval(self):
        """Test adding approval."""
        quality_scores = {'overall_score': 85}
        self.memory.add_approval('llmon', quality_scores)
        
        self.assertEqual(len(self.memory.feedback_history), 1)
        self.assertTrue(self.memory.feedback_history[0]['approved'])
        self.assertEqual(self.memory.feedback_history[0]['quality_scores'], quality_scores)
    
    def test_rejection_tracking(self):
        """Test rejection pattern tracking."""
        self.memory.add_feedback('writer', 'Too technical', approved=False)
        self.memory.add_feedback('writer', 'Lacks examples', approved=False)
        
        self.assertEqual(len(self.memory.rejection_patterns['writer']), 2)
    
    def test_extract_preferences(self):
        """Test preference extraction."""
        self.memory.add_feedback('writer', 'Too technical jargon complex', approved=False)
        self.memory.add_feedback('writer', 'Too formal technical', approved=False)
        
        preferences = self.memory.extract_preferences()
        
        self.assertIn('common_rejections', preferences)
        self.assertIn('writer', preferences['common_rejections'])
    
    def test_get_context_for_agent(self):
        """Test context compilation."""
        self.memory.add_feedback('writer', 'Good structure', approved=True)
        self.memory.add_feedback('writer', 'Too long', approved=False)
        
        context = self.memory.get_context_for_agent('writer')
        
        self.assertIsInstance(context, str)
        if context:  # Context may be empty if not enough data
            self.assertIn('writer', context.lower())
    
    def test_save_and_load(self):
        """Test memory persistence."""
        self.memory.add_feedback('writer', 'Test feedback', approved=True)
        self.memory._save_memory()
        
        # Create new memory instance and load
        new_memory = WorkflowMemory(self.temp_dir)
        
        self.assertEqual(len(new_memory.feedback_history), 1)
        self.assertEqual(new_memory.feedback_history[0]['feedback'], 'Test feedback')
    
    def test_session_stats(self):
        """Test session statistics tracking."""
        self.memory.add_feedback('writer', 'Feedback 1', approved=True)
        self.memory.add_feedback('llmon', 'Feedback 2', approved=False)
        
        stats = self.memory.get_session_summary()
        
        self.assertIn('writer_approvals', stats)
        self.assertIn('llmon_rejections', stats)
        self.assertEqual(stats['writer_approvals'], 1)
        self.assertEqual(stats['llmon_rejections'], 1)


class TestVariationDifferentiator(unittest.TestCase):
    """Test VariationDifferentiator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.differentiator = VariationDifferentiator(min_difference=0.3)
        
        self.variation1 = """AI is transforming businesses. Companies are adopting 
machine learning to improve efficiency and make better decisions."""
        
        self.variation2 = """Artificial intelligence revolutionizes organizations. 
Enterprises leverage deep learning for enhanced productivity and superior choices."""
        
        self.variation3 = """Technology powered by AI changes how we work. Businesses 
use intelligent systems to streamline operations and optimize outcomes."""
        
        # Very similar variation for testing
        self.similar_variation = """AI is transforming businesses. Organizations are 
adopting machine learning to improve efficiency and make better decisions."""
    
    def test_calculate_similarity(self):
        """Test similarity calculation."""
        similarity = self.differentiator.calculate_similarity(
            self.variation1, self.variation2
        )
        
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
    
    def test_calculate_difference(self):
        """Test difference calculation."""
        difference = self.differentiator.calculate_difference(
            self.variation1, self.variation2
        )
        
        self.assertIsInstance(difference, float)
        self.assertGreaterEqual(difference, 0.0)
        self.assertLessEqual(difference, 1.0)
        self.assertAlmostEqual(
            difference,
            1.0 - self.differentiator.calculate_similarity(self.variation1, self.variation2),
            places=5
        )
    
    def test_validate_variations_valid(self):
        """Test validation with sufficiently different variations."""
        variations = [self.variation1, self.variation2, self.variation3]
        validation = self.differentiator.validate_variations(variations)
        
        self.assertIn('valid', validation)
        self.assertIn('min_difference', validation)
        self.assertIn('avg_difference', validation)
        self.assertIsInstance(validation['valid'], bool)
    
    def test_validate_variations_too_similar(self):
        """Test validation with similar variations."""
        variations = [self.variation1, self.similar_variation]
        validation = self.differentiator.validate_variations(variations)
        
        # These should be too similar
        self.assertFalse(validation['valid'])
        self.assertGreater(len(validation['pairs_below_threshold']), 0)
    
    def test_differentiation_report(self):
        """Test report generation."""
        variations = [self.variation1, self.variation2, self.variation3]
        report = self.differentiator.get_differentiation_report(variations)
        
        self.assertIsInstance(report, str)
        self.assertIn('DIFFERENTIATION REPORT', report)
        self.assertIn('Minimum Difference', report)
    
    def test_least_different_pair(self):
        """Test finding least different pair."""
        variations = [self.variation1, self.variation2, self.variation3]
        result = self.differentiator.identify_least_different_pair(variations)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)  # (idx1, idx2, similarity)
        self.assertIsInstance(result[2], float)
    
    def test_suggest_regeneration(self):
        """Test regeneration suggestion."""
        variations = [self.variation1, self.similar_variation, self.variation3]
        suggestion = self.differentiator.suggest_regeneration(variations)
        
        # Should suggest regenerating one of the similar variations
        if suggestion is not None:
            self.assertIn(suggestion, [0, 1, 2])


class TestIntegration(unittest.TestCase):
    """Integration tests for combined functionality."""
    
    def test_quality_and_memory_integration(self):
        """Test quality scoring with memory storage."""
        temp_dir = tempfile.mkdtemp()
        try:
            analyzer = QualityAnalyzer()
            memory = WorkflowMemory(temp_dir)
            
            article = "# Test Article\n\nThis is a test."
            scores = analyzer.analyze(article)
            
            # Store approval with scores
            memory.add_approval('writer', scores)
            
            # Verify storage
            self.assertEqual(len(memory.feedback_history), 1)
            self.assertIsNotNone(memory.feedback_history[0]['quality_scores'])
            
        finally:
            shutil.rmtree(temp_dir)
    
    def test_differentiator_with_variations(self):
        """Test differentiator with multiple variations."""
        differentiator = VariationDifferentiator(min_difference=0.2)
        
        variations = [
            "The quick brown fox jumps over the lazy dog.",
            "A fast brown canine leaps above the sleepy hound.",
            "Technology advances rapidly in modern society.",
        ]
        
        validation = differentiator.validate_variations(variations)
        
        self.assertIsNotNone(validation)
        self.assertIn('valid', validation)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestQualityAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowMemory))
    suite.addTests(loader.loadTestsFromTestCase(TestVariationDifferentiator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)

