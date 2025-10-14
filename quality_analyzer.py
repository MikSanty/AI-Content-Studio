"""Quality Analyzer - Multi-dimensional content quality scoring."""
import re
import textstat
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class QualityAnalyzer:
    """Analyzes content quality across multiple dimensions."""
    
    def __init__(self):
        """Initialize quality analyzer."""
        pass
    
    def analyze(self, article, template=None, references=None):
        """
        Perform comprehensive quality analysis.
        
        Args:
            article: The article text to analyze
            template: Optional template text for structure comparison
            references: Optional reference materials for factual checking
        
        Returns:
            Dictionary with quality scores across all dimensions
        """
        scores = {
            'overall_score': 0,
            'readability': self._analyze_readability(article),
            'seo': self._analyze_seo(article),
            'engagement': self._analyze_engagement(article),
            'structure': self._analyze_structure(article, template),
            'factual': self._analyze_factual_consistency(article, references)
        }
        
        # Calculate overall score (weighted average)
        weights = {
            'readability': 0.25,
            'seo': 0.15,
            'engagement': 0.25,
            'structure': 0.20,
            'factual': 0.15
        }
        
        overall = sum(
            scores[key]['score'] * weights[key]
            for key in weights.keys()
        )
        scores['overall_score'] = round(overall, 1)
        
        return scores
    
    def _analyze_readability(self, text):
        """Analyze readability metrics."""
        try:
            flesch_score = textstat.flesch_reading_ease(text)
            grade_level = textstat.flesch_kincaid_grade(text)
            
            # Convert Flesch score to 0-100 scale
            # Flesch: 90-100=very easy, 0-30=very difficult
            readability_score = max(0, min(100, flesch_score))
            
            # Determine complexity
            if grade_level < 8:
                complexity = 'easy'
            elif grade_level < 12:
                complexity = 'moderate'
            elif grade_level < 16:
                complexity = 'challenging'
            else:
                complexity = 'advanced'
            
            # Additional metrics
            words = text.split()
            sentences = text.split('.')
            
            avg_word_length = sum(len(w) for w in words) / max(len(words), 1)
            avg_sentence_length = len(words) / max(len(sentences), 1)
            
            return {
                'score': round(readability_score, 1),
                'grade_level': round(grade_level, 1),
                'complexity': complexity,
                'avg_word_length': round(avg_word_length, 1),
                'avg_sentence_length': round(avg_sentence_length, 1),
                'flesch_score': round(flesch_score, 1)
            }
        except Exception as e:
            return {
                'score': 50,
                'grade_level': 0,
                'complexity': 'unknown',
                'error': str(e)
            }
    
    def _analyze_seo(self, text):
        """Analyze SEO-related metrics."""
        # Count headings
        h1_count = len(re.findall(r'^# [^#]', text, re.MULTILINE))
        h2_count = len(re.findall(r'^## [^#]', text, re.MULTILINE))
        h3_count = len(re.findall(r'^### [^#]', text, re.MULTILINE))
        total_headings = h1_count + h2_count + h3_count
        
        # Extract potential keywords (words 4+ chars, appearing 2+ times)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        word_freq = Counter(words)
        keywords = [word for word, count in word_freq.most_common(10) if count >= 2]
        
        # Calculate word count
        word_count = len(text.split())
        
        # Scoring logic
        score = 0
        
        # Heading structure (30 points)
        if h1_count == 1:
            score += 15
        if h2_count >= 3:
            score += 10
        if total_headings >= 5:
            score += 5
        
        # Word count (30 points)
        if 800 <= word_count <= 2500:
            score += 30
        elif 500 <= word_count < 800 or 2500 < word_count <= 3500:
            score += 20
        elif word_count >= 300:
            score += 10
        
        # Keyword presence (20 points)
        score += min(20, len(keywords) * 2)
        
        # Content organization (20 points)
        has_intro = bool(re.search(r'(introduction|overview)', text.lower()))
        has_conclusion = bool(re.search(r'(conclusion|summary|takeaway)', text.lower()))
        
        if has_intro:
            score += 10
        if has_conclusion:
            score += 10
        
        return {
            'score': min(100, score),
            'word_count': word_count,
            'headings_count': total_headings,
            'h1_count': h1_count,
            'h2_count': h2_count,
            'h3_count': h3_count,
            'keywords': keywords[:5],
            'has_intro': has_intro,
            'has_conclusion': has_conclusion
        }
    
    def _analyze_engagement(self, text):
        """Analyze engagement and storytelling elements."""
        # Count questions
        questions = len(re.findall(r'\?', text))
        
        # Count storytelling elements
        personal_pronouns = len(re.findall(
            r'\b(you|your|we|our|I|my)\b', text, re.IGNORECASE
        ))
        
        # Count examples and case studies
        examples = len(re.findall(
            r'\b(example|for instance|such as|like|imagine)\b', 
            text, re.IGNORECASE
        ))
        
        # Count action words
        action_verbs = len(re.findall(
            r'\b(discover|learn|explore|achieve|create|build|transform)\b',
            text, re.IGNORECASE
        ))
        
        # Count emotional/power words
        emotional_words = len(re.findall(
            r'\b(amazing|powerful|essential|critical|important|significant|incredible)\b',
            text, re.IGNORECASE
        ))
        
        # Lists and bullet points
        lists = len(re.findall(r'^\s*[-*+]\s', text, re.MULTILINE))
        
        # Scoring
        score = 0
        score += min(15, questions * 5)
        score += min(20, personal_pronouns * 0.5)
        score += min(20, examples * 3)
        score += min(15, action_verbs * 2)
        score += min(15, emotional_words * 2)
        score += min(15, lists * 1)
        
        return {
            'score': min(100, round(score)),
            'questions': questions,
            'personal_pronouns': personal_pronouns,
            'examples': examples,
            'action_verbs': action_verbs,
            'emotional_words': emotional_words,
            'lists': lists
        }
    
    def _analyze_structure(self, text, template):
        """Analyze adherence to template structure."""
        if not template:
            return {
                'score': 50,
                'template_match': 0,
                'sections_complete': False,
                'note': 'No template provided for comparison'
            }
        
        # Extract sections from template and article
        template_sections = re.findall(r'^##\s+(.+)$', template, re.MULTILINE)
        article_sections = re.findall(r'^##\s+(.+)$', text, re.MULTILINE)
        
        # Calculate match percentage
        if not template_sections:
            template_match = 100
            sections_complete = True
        else:
            matched = 0
            for template_section in template_sections:
                # Fuzzy matching - check if similar section exists
                template_words = set(template_section.lower().split())
                for article_section in article_sections:
                    article_words = set(article_section.lower().split())
                    overlap = len(template_words & article_words)
                    if overlap > 0 or template_section.lower() in article_section.lower():
                        matched += 1
                        break
            
            template_match = round((matched / len(template_sections)) * 100)
            sections_complete = matched == len(template_sections)
        
        # Check for proper hierarchy
        h1_count = len(re.findall(r'^# [^#]', text, re.MULTILINE))
        has_proper_h1 = h1_count == 1
        
        # Overall structure score
        score = 0
        score += template_match * 0.6
        score += (20 if sections_complete else 10)
        score += (20 if has_proper_h1 else 0)
        
        return {
            'score': min(100, round(score)),
            'template_match': template_match,
            'sections_complete': sections_complete,
            'template_sections_count': len(template_sections),
            'article_sections_count': len(article_sections),
            'has_proper_h1': has_proper_h1
        }
    
    def _analyze_factual_consistency(self, text, references):
        """Analyze factual consistency with references."""
        if not references:
            return {
                'score': 50,
                'reference_citations': 0,
                'note': 'No references provided for comparison'
            }
        
        # Count potential citations or references
        citations = len(re.findall(
            r'(according to|research shows|studies indicate|data suggests|source:|cited)',
            text, re.IGNORECASE
        ))
        
        # Extract key terms from references
        ref_words = re.findall(r'\b[a-zA-Z]{5,}\b', references.lower())
        ref_freq = Counter(ref_words).most_common(20)
        ref_keywords = {word for word, count in ref_freq if count >= 2}
        
        # Check how many reference keywords appear in article
        article_words = set(re.findall(r'\b[a-zA-Z]{5,}\b', text.lower()))
        keyword_overlap = len(ref_keywords & article_words)
        
        # Scoring
        score = 0
        score += min(40, citations * 10)
        score += min(60, keyword_overlap * 3)
        
        return {
            'score': min(100, score),
            'reference_citations': citations,
            'keyword_overlap': keyword_overlap,
            'reference_keywords_found': sorted(list(ref_keywords & article_words))[:10]
        }
    
    def format_score_summary(self, scores):
        """Format quality scores for display."""
        summary = f"\n{'='*60}\n"
        summary += f"QUALITY ANALYSIS REPORT\n"
        summary += f"{'='*60}\n\n"
        summary += f"Overall Score: {scores['overall_score']}/100\n\n"
        
        summary += f"[READABILITY] Readability: {scores['readability']['score']}/100\n"
        summary += f"   Grade Level: {scores['readability'].get('grade_level', 'N/A')}\n"
        summary += f"   Complexity: {scores['readability'].get('complexity', 'N/A')}\n\n"
        
        summary += f"[SEO] SEO: {scores['seo']['score']}/100\n"
        summary += f"   Word Count: {scores['seo']['word_count']}\n"
        summary += f"   Headings: {scores['seo']['headings_count']}\n\n"
        
        summary += f"[ENGAGEMENT] Engagement: {scores['engagement']['score']}/100\n"
        summary += f"   Questions: {scores['engagement']['questions']}\n"
        summary += f"   Examples: {scores['engagement']['examples']}\n\n"
        
        summary += f"[STRUCTURE] Structure: {scores['structure']['score']}/100\n"
        summary += f"   Template Match: {scores['structure'].get('template_match', 'N/A')}%\n\n"
        
        summary += f"[OK] Factual Consistency: {scores['factual']['score']}/100\n"
        summary += f"   Citations: {scores['factual']['reference_citations']}\n"
        
        summary += f"\n{'='*60}\n"
        
        return summary

