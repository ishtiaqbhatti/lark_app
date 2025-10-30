import logging
import textstat
from typing import Dict, Any, List, Optional  # ADD List
from bs4 import BeautifulSoup  # ADD this for HTML parsing
import re  # ADD this for regex checks
import requests


class ContentAuditor:
    """
    Audits the generated content for SEO and readability metrics,
    and checks for "publish-readiness" issues.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def _check_for_broken_links(self, soup: BeautifulSoup, max_links: int = 20) -> List[Dict[str, str]]:
        """
        Checks external <a> tags for 4xx or 5xx status codes.
        Limited to max_links to prevent performance issues and potential DoS of target sites.
        Uses async-style concurrent requests for better performance.
        """
        issues = []
        links = soup.find_all("a", href=True)
        
        external_links = []
        for link in links:
            href = link["href"]
            # Skip internal/anchor links and javascript links
            if (
                not href
                or href.startswith("#")
                or href.startswith("/")
                or href.startswith("javascript:")
                or href.startswith("mailto:")
                or href.startswith("tel:")
            ):
                continue
            external_links.append(href)
        
        # Limit the number of links to check
        if len(external_links) > max_links:
            self.logger.warning(
                f"Article contains {len(external_links)} external links. "
                f"Only checking first {max_links} to avoid performance issues."
            )
            external_links = external_links[:max_links]
        
        # Check links with shorter timeout to prevent blocking
        for href in external_links:
            try:
                # Use a HEAD request for efficiency with reduced timeout
                response = requests.head(href, timeout=3, allow_redirects=True)
                if response.status_code >= 400:
                    issues.append(
                        {
                            "issue": "broken_link",
                            "context": f"URL '{href}' returned status {response.status_code}.",
                        }
                    )
            except requests.exceptions.Timeout:
                # Don't flag timeouts as errors - the link might still be valid
                self.logger.debug(f"Link check timeout for '{href}' - skipping validation.")
            except requests.RequestException as e:
                issues.append(
                    {
                        "issue": "unreachable_link",
                        "context": f"Could not connect to URL '{href}': {str(e)[:100]}",
                    }
                )
        
        return issues

    def audit_content(
        self,
        article_html: str,
        primary_keyword: str,
        blueprint: Dict[str, Any],
        client_cfg: Dict[str, Any],
        avg_competitor_readability: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Audits the HTML content and returns a dictionary of metrics.
        """
        # Extract plain text for text-based analysis
        soup = BeautifulSoup(article_html, "html.parser")
        plain_text = soup.get_text(separator=" ", strip=True)
        html_issues = self._check_html_publish_readiness(article_html)
        if html_issues is None:
            html_issues = []

        # Add broken link check results
        broken_link_issues = self._check_for_broken_links(soup)
        html_issues.extend(broken_link_issues)

        word_count = len(plain_text.split())
        target_word_count = blueprint.get("ai_content_brief", {}).get(
            "target_word_count", 0
        )
        if target_word_count > 0:
            deviation = abs(word_count - target_word_count) / target_word_count
            if deviation > 0.20:
                html_issues.append(
                    {
                        "issue": "word_count_deviation",
                        "context": f"Actual count ({word_count}) deviates from target ({target_word_count}) by more than 20%.",
                    }
                )

        readability_score = textstat.flesch_kincaid_grade(plain_text)
        # Calculate additional metrics for comprehensive audit (Task 9.1)
        smog_score = textstat.smog_index(plain_text)
        coleman_liau_score = textstat.coleman_liau_index(plain_text)

        persona = blueprint.get("ai_content_brief", {}).get(
            "target_audience_persona", "General audience"
        )

        # W13 FIX: Determine Readability Mismatch and Required Refinement Command
        refinement_command = None
        readability_assessment = f"Flesch-Kincaid Grade Level: {readability_score:.1f}."

        if avg_competitor_readability is not None:
            readability_assessment += (
                f" (Avg. Competitor F-K: {avg_competitor_readability:.1f})."
            )
            if (
                abs(readability_score - avg_competitor_readability) > 3.0
            ):  # If our score is more than 3 grades off
                if readability_score < avg_competitor_readability:
                    readability_assessment += " Assessment: CRITICAL: Content is significantly simpler than competitors. Consider increasing complexity."
                    refinement_command = f"Increase the complexity to match competitor average of Flesch-Kincaid Grade Level {avg_competitor_readability:.1f}."
                else:
                    readability_assessment += " Assessment: CRITICAL: Content is significantly more complex than competitors. Consider simplifying."
                    refinement_command = f"Simplify the content to match competitor average of Flesch-Kincaid Grade Level {avg_competitor_readability:.1f}."
            else:
                readability_assessment += (
                    " Assessment: Readability is consistent with top competitors."
                )
        else:
            # Fallback to persona-based assessment if no competitor average is provided
            if "expert" in persona.lower() or "planner" in persona.lower():
                if readability_score < 9.5:
                    readability_assessment += " Assessment: CRITICAL: Content is likely oversimplified (Grade < 9.5)."
                    refinement_command = "Increase the complexity and authoritative tone of the writing to target a Flesch-Kincaid Grade Level of 10 or higher."
                else:
                    readability_assessment += (
                        " Assessment: Appropriate complexity for an expert audience."
                    )
            else:
                if readability_score > 12 or smog_score > 10.0:
                    readability_assessment += " Assessment: CRITICAL: Content is too academic or complex (Grade > 12 or SMOG > 10.0)."
                    refinement_command = "Simplify the complexity and reduce sentence length to target a Flesch-Kincaid Grade Level between 7 and 9, and a SMOG Index under 8."
                else:
                    readability_assessment += (
                        " Assessment: Appropriate complexity for a general audience."
                    )

        entity_metrics = self._check_entity_coverage(plain_text, blueprint)
        if entity_metrics.get("score", 100) < 75.0 and entity_metrics.get(
            "missing"
        ):  # Only flag if there are actually missing entities
            missing_entities_str = ", ".join(entity_metrics.get("missing", []))
            html_issues.append(
                {
                    "issue": "critical_entity_gap",
                    "context": f"Entity coverage is below 75%. Missing: {missing_entities_str}",
                }
            )

        # Ensure the final return object from audit_content includes all new data:
        return {
            "flesch_kincaid_grade": readability_score,
            "smog_index": smog_score,
            "coleman_liau_index": coleman_liau_score,
            "readability_assessment": readability_assessment,
            "refinement_command": refinement_command,
            "entity_coverage_score": entity_metrics.get("score", 0),
            "missing_entities": entity_metrics.get("missing", []),
            "covered_sections": None,
            "publish_readiness_issues": html_issues,  # This now includes broken links and critical entity gaps
        }

    def _check_entity_coverage(
        self, article_text: str, blueprint: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Checks if the key entities from the blueprint are present in the article text.
        """
        # ... (existing logic)
        entities = blueprint.get("ai_content_brief", {}).get(
            "key_entities_to_mention", []
        )
        if not entities:
            return {"score": 100, "missing": []}

        missing_entities = []
        for entity in entities:
            # Heuristic check: Look for exact match or simple pluralization (Task 11.1)
            if entity.endswith("s"):
                # If entity is already plural (e.g., 'tools'), check for exact match only
                pattern = r"\b" + re.escape(entity) + r"\b"
            else:
                # Check for singular or plural form (e.g., 'tool' or 'tools')
                pattern = r"\b" + re.escape(entity) + r"s?\b"
            if not re.search(pattern, article_text, re.IGNORECASE):
                missing_entities.append(entity)

        coverage_score = (
            100 - (len(missing_entities) / len(entities) * 100) if entities else 100
        )
        return {
            "score": coverage_score,
            "missing": missing_entities,
            "found_count": len(entities) - len(missing_entities),
            "total_expected": len(entities),
        }

    def _check_html_publish_readiness(self, article_html: str) -> List[Dict[str, Any]]:
        """
        Performs specific checks on the final HTML for publish-readiness, returning structured issues.
        """
        issues = []
        soup = BeautifulSoup(article_html, "html.parser")

        # Check for unresolved image placeholders
        placeholder_pattern = r"\[\[IMAGE_ID:\s*(.*?)\s*PROMPT:\s*(.*?)\s*\]\]"
        placeholders_found = re.findall(placeholder_pattern, article_html)
        if placeholders_found:
            issues.append(
                {
                    "issue": "unresolved_placeholder",
                    "context": f"{len(placeholders_found)} image placeholders remain in the text.",
                }
            )

        # Check for empty headings
        for h_tag in soup.find_all(re.compile(r"^h[1-6]$")):
            if not h_tag.get_text(strip=True):
                issues.append({"issue": "empty_heading", "context": str(h_tag)})

        # Check for extremely short paragraphs
        for p_tag in soup.find_all("p"):
            text = p_tag.get_text(strip=True)
            if 0 < len(text.split()) < 5:
                issues.append({"issue": "short_paragraph", "context": str(p_tag)})

        return issues
