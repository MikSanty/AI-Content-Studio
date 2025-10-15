"""Citation Validator - Validates source citations and hyperlinks in generated content."""
import re
from typing import Dict, List, Tuple
from utils import read_file


class CitationValidator:
    """Validates that all citations have proper hyperlinks and no URLs are hallucinated."""
    
    def __init__(self):
        """Initialize citation validator."""
        self.issues = []
        self.warnings = []
        self.valid_urls = set()
        
    def extract_urls_from_references(self, references_path: str) -> set:
        """
        Extract all valid URLs from the references file.
        
        Args:
            references_path: Path to references.md file
            
        Returns:
            Set of valid URLs found in references
        """
        references_content = read_file(references_path)
        if not references_content:
            return set()
        
        # Extract URLs from markdown links and plain URLs
        # Match markdown links: [text](url)
        markdown_urls = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', references_content)
        urls = {url for _, url in markdown_urls}
        
        # Also match standalone URLs starting with http/https
        standalone_urls = re.findall(r'https?://[^\s\)]+', references_content)
        urls.update(standalone_urls)
        
        self.valid_urls = urls
        return urls
    
    def extract_citations_from_content(self, content: str) -> List[Dict]:
        """
        Extract all citation patterns from content.
        
        Args:
            content: Article content to analyze
            
        Returns:
            List of citation dictionaries with text, url, and line info
        """
        citations = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Find markdown links
            markdown_links = re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', line)
            for match in markdown_links:
                citations.append({
                    'text': match.group(1),
                    'url': match.group(2),
                    'line': line_num,
                    'full_match': match.group(0),
                    'type': 'linked'
                })
        
        return citations
    
    def find_unlinked_citations(self, content: str) -> List[Dict]:
        """
        Find potential citations that lack hyperlinks.
        
        Args:
            content: Article content to analyze
            
        Returns:
            List of suspected unlinked citations
        """
        unlinked = []
        lines = content.split('\n')
        
        # Patterns that suggest a citation without a hyperlink
        citation_patterns = [
            r'according to ([A-Z][A-Za-z0-9\s&/]+(?:Study|Research|Report|Trends|Analysis|Team|Survey|Data))',
            r'as (?:highlighted|noted|reported|shown) by ([A-Z][A-Za-z0-9\s&/]+)',
            r'\[Source: ([^\]]+)\](?!\()',  # [Source: X] not followed by (url)
            r'- Source: ([^\n]+)(?!http)',
            r'per ([A-Z][A-Za-z0-9\s]+(?:Study|Research|Report|Trends))',
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern in citation_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    # Check if this appears to be part of a markdown link
                    # Look for ]( after the match
                    context_after = line[match.end():match.end()+2]
                    if context_after != '](':
                        unlinked.append({
                            'source_name': match.group(1).strip(),
                            'line': line_num,
                            'context': line.strip()[:100],
                            'type': 'unlinked'
                        })
        
        return unlinked
    
    def validate_urls(self, content: str, references_path: str) -> Dict:
        """
        Validate all URLs in content against references.
        
        Args:
            content: Article content to validate
            references_path: Path to references.md
            
        Returns:
            Validation report dictionary
        """
        self.issues = []
        self.warnings = []
        
        # Extract valid URLs from references
        valid_urls = self.extract_urls_from_references(references_path)
        
        if not valid_urls:
            self.warnings.append({
                'type': 'no_references',
                'message': 'No URLs found in references file'
            })
        
        # Extract citations from content
        citations = self.extract_citations_from_content(content)
        
        # Check each citation URL
        hallucinated_urls = []
        valid_citations = []
        
        for citation in citations:
            url = citation['url'].strip()
            
            # Skip anchor links and relative links
            if url.startswith('#') or not url.startswith('http'):
                continue
            
            if url not in valid_urls:
                hallucinated_urls.append(citation)
                self.issues.append({
                    'type': 'hallucinated_url',
                    'line': citation['line'],
                    'url': url,
                    'text': citation['text'],
                    'message': f"URL not found in references: {url}"
                })
            else:
                valid_citations.append(citation)
        
        # Find unlinked citations
        unlinked = self.find_unlinked_citations(content)
        
        for item in unlinked:
            self.issues.append({
                'type': 'missing_hyperlink',
                'line': item['line'],
                'source': item['source_name'],
                'message': f"Citation lacks hyperlink: '{item['source_name']}'"
            })
        
        # Generate report
        report = {
            'passed': len(self.issues) == 0,
            'total_citations': len(citations),
            'valid_citations': len(valid_citations),
            'hallucinated_urls': len(hallucinated_urls),
            'unlinked_citations': len(unlinked),
            'issues': self.issues,
            'warnings': self.warnings,
            'valid_reference_urls': len(valid_urls)
        }
        
        return report
    
    def format_report(self, report: Dict) -> str:
        """
        Format validation report for display.
        
        Args:
            report: Validation report dictionary
            
        Returns:
            Formatted report string
        """
        lines = []
        lines.append("=" * 70)
        lines.append("CITATION VALIDATION REPORT")
        lines.append("=" * 70)
        lines.append("")
        
        # Summary
        status = "[PASSED]" if report['passed'] else "[FAILED]"
        lines.append(f"Status: {status}")
        lines.append("")
        lines.append(f"Total citations found: {report['total_citations']}")
        lines.append(f"Valid citations: {report['valid_citations']}")
        lines.append(f"Hallucinated URLs: {report['hallucinated_urls']}")
        lines.append(f"Unlinked citations: {report['unlinked_citations']}")
        lines.append(f"Reference URLs available: {report['valid_reference_urls']}")
        lines.append("")
        
        # Issues
        if report['issues']:
            lines.append("ISSUES FOUND:")
            lines.append("-" * 70)
            
            for i, issue in enumerate(report['issues'], 1):
                lines.append(f"\n{i}. {issue['type'].upper()}")
                lines.append(f"   Line: {issue['line']}")
                lines.append(f"   {issue['message']}")
                
                if 'url' in issue:
                    lines.append(f"   Problematic URL: {issue['url']}")
                if 'source' in issue:
                    lines.append(f"   Source: {issue['source']}")
        else:
            lines.append("[OK] No issues found - all citations properly hyperlinked!")
        
        # Warnings
        if report['warnings']:
            lines.append("")
            lines.append("WARNINGS:")
            lines.append("-" * 70)
            for warning in report['warnings']:
                lines.append(f"[WARNING] {warning['message']}")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def validate_and_report(self, content: str, references_path: str) -> Tuple[bool, str]:
        """
        Validate content and return formatted report.
        
        Args:
            content: Article content to validate
            references_path: Path to references.md
            
        Returns:
            Tuple of (passed: bool, report: str)
        """
        report = self.validate_urls(content, references_path)
        formatted_report = self.format_report(report)
        return report['passed'], formatted_report


def validate_citations(content: str, references_path: str) -> Tuple[bool, str]:
    """
    Convenience function to validate citations.
    
    Args:
        content: Article content to validate
        references_path: Path to references.md file
        
    Returns:
        Tuple of (passed: bool, report: str)
    """
    validator = CitationValidator()
    return validator.validate_and_report(content, references_path)

