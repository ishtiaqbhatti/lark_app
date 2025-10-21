# core/page_classifier.py
import re
from typing import Dict, Any
from urllib.parse import urlparse


class PageClassifier:
    """
    Categorizes a webpage based on its URL, domain, title, and other attributes.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("page_classification", {})
        self.forum_domains = self.config.get("forum_domains", [])
        self.ecommerce_domains = self.config.get("ecommerce_domains", [])
        self.news_domains = self.config.get("news_domains", [])

        # Pre-compile regex for efficiency
        self.blog_patterns = [
            re.compile(p) for p in self.config.get("blog_url_patterns", [])
        ]
        self.forum_patterns = [
            re.compile(p) for p in self.config.get("forum_url_patterns", [])
        ]

    def classify(self, url: str, domain: str, title: str) -> str:
        """
        Classifies the given URL into a specific page type.

        Args:
            url: The full URL of the page.
            domain: The domain of the page.
            title: The title of the page.

        Returns:
            A string representing the classified page type.
        """
        if domain in self.ecommerce_domains:
            return "E-commerce"
        if domain in self.forum_domains:
            return "Forum"
        if domain in self.news_domains:
            return "News"

        # Check URL patterns for more specific types
        parsed_url = urlparse(url)
        path = parsed_url.path

        for pattern in self.forum_patterns:
            if pattern.search(path) or pattern.search(title.lower()):
                return "Forum"

        for pattern in self.blog_patterns:
            if pattern.search(path):
                return "Blog/Article"

        # Check for homepage/landing page (short path)
        if len(path.strip("/").split("/")) <= 1:
            return "Homepage/Landing Page"

        return "Blog/Article"  # Default category
