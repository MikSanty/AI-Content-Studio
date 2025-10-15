"""Test script for citation validator."""
from citation_validator import CitationValidator, validate_citations
import os


def test_citation_validator():
    """Test the citation validator with sample content."""
    
    print("=" * 70)
    print("CITATION VALIDATOR TEST")
    print("=" * 70)
    print()
    
    # Test 1: Content with proper hyperlinks
    print("TEST 1: Content with proper hyperlinks")
    print("-" * 70)
    
    good_content = """
# Article Title

According to [Miquido UI/UX Trends](https://www.miquido.com/blog/ui-ux-design-trends/), 
speed is critical in 2025. The [Userpilot SaaS Research](https://userpilot.com/blog/saas-landing-pages/) 
shows that conversion rates average 5.89%.
"""
    
    references_path = os.path.join("templates", "references.md")
    
    validator = CitationValidator()
    report = validator.validate_urls(good_content, references_path)
    print(validator.format_report(report))
    print()
    
    # Test 2: Content with missing hyperlinks
    print("\nTEST 2: Content with unlinked citations")
    print("-" * 70)
    
    bad_content = """
# Article Title

According to Miquido UI/UX Trends, speed is critical in 2025. 
The data from various SaaS Landing Page Studies shows conversion rates vary.
"""
    
    report = validator.validate_urls(bad_content, references_path)
    print(validator.format_report(report))
    print()
    
    # Test 3: Content with hallucinated URLs
    print("\nTEST 3: Content with hallucinated/invented URLs")
    print("-" * 70)
    
    hallucinated_content = """
# Article Title

According to [Miquido UI/UX Trends](https://miquido.com/fake-url), 
speed is critical. The [Fake Source](https://invented-url.com/article) agrees.
"""
    
    report = validator.validate_urls(hallucinated_content, references_path)
    print(validator.format_report(report))
    print()
    
    # Test 4: Test with actual output file if it exists
    output_path = "outputs/20251015_102405/01_writer_draft.md"
    if os.path.exists(output_path):
        print("\nTEST 4: Validating actual output file")
        print("-" * 70)
        
        with open(output_path, 'r', encoding='utf-8') as f:
            draft_content = f.read()
        
        passed, report_text = validate_citations(draft_content, references_path)
        print(report_text)
        print()
        
        if passed:
            print("[OK] The draft passes citation validation!")
        else:
            print("[FAILED] The draft has citation issues that need fixing.")
    
    print("\n" + "=" * 70)
    print("TESTS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    test_citation_validator()

