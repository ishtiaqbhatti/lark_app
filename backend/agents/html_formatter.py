import logging
from typing import Dict, Any, List, Optional
import os
import re
import markdown
from bs4 import BeautifulSoup
from datetime import datetime
from backend.core import utils


class HtmlFormatter:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def _convert_markdown_tables_to_html(self, html_body: str) -> str:
        """Converts Markdown tables to HTML using markdown library directly."""
        return markdown.markdown(html_body, extensions=["tables", "fenced_code"])

    def _insert_internal_links(
        self, soup: BeautifulSoup, internal_links: List[Dict[str, str]]
    ) -> None:
        """
        Inserts internal links into the BeautifulSoup object based on specific contextual suggestions from an AI agent.
        """
        if not internal_links:
            return

        linked_anchors = set()

        for link_data in internal_links:
            anchor_text = link_data.get("anchor_text")
            url = link_data.get("url")
            context_paragraph = link_data.get("context_paragraph_text")

            if (
                not all([anchor_text, url, context_paragraph])
                or anchor_text.lower() in linked_anchors
            ):
                continue

            # Find all paragraphs that contain the exact context text
            potential_paragraphs = soup.find_all(
                "p", string=re.compile(re.escape(context_paragraph))
            )

            for p_tag in potential_paragraphs:
                # Find the text node within this paragraph that contains the anchor
                text_node = p_tag.find(
                    string=re.compile(re.escape(anchor_text), re.IGNORECASE)
                )

                if text_node and not text_node.find_parent(
                    "a"
                ):  # Ensure it's not already linked
                    match = re.search(
                        re.escape(anchor_text), str(text_node), re.IGNORECASE
                    )
                    if match:
                        before_text = str(text_node)[: match.start()]
                        matched_text = match.group(0)
                        after_text = str(text_node)[match.end() :]

                        link_tag = soup.new_tag("a", href=url)
                        link_tag.string = matched_text

                        new_content = []
                        if before_text:
                            new_content.append(before_text)
                        new_content.append(link_tag)
                        if after_text:
                            new_content.append(after_text)

                        text_node.replace_with(*new_content)
                        linked_anchors.add(anchor_text.lower())
                        break  # Move to the next link suggestion once placed

    def _generate_toc(self, soup: BeautifulSoup) -> None:
        """Generates and inserts a Table of Contents from H2 tags into the BeautifulSoup object."""
        toc_list = soup.new_tag("ul", **{"class": "toc-list"})
        h2_tags = soup.find_all("h2")

        if len(h2_tags) < 2:
            return  # No TOC needed for less than 2 headings

        # Add unique IDs to H2 tags and build TOC
        for i, h2 in enumerate(h2_tags):
            slug = utils.slugify(h2.text)
            if not slug:  # Fallback for empty/unsluggable H2s
                slug = f"section-{i + 1}"
            h2["id"] = slug  # Add ID to H2 for linking

            toc_item = soup.new_tag("li")
            toc_link = soup.new_tag("a", href=f"#{slug}")
            toc_link.string = h2.text
            toc_item.append(toc_link)
            toc_list.append(toc_item)

        toc_header = soup.new_tag("h2")
        toc_header.string = "Table of Contents"
        toc_header["id"] = "table-of-contents"  # Give TOC its own ID

        first_h2 = soup.find("h2")
        if first_h2:
            first_h2.insert_before(toc_list)
            first_h2.insert_before(toc_header)
        else:
            # Fallback if no H2s exist, place it after the first paragraph or at the start
            first_p = soup.find("p")
            if first_p:
                first_p.insert_after(toc_header)
                first_p.insert_after(toc_list)
            else:
                soup.insert(0, toc_list)
                soup.insert(0, toc_header)

    def _generate_schema_org(
        self, soup: BeautifulSoup, opportunity: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Dynamically generates Schema.org JSON-LD from the final HTML soup.
        """
        schema_graph: List[Dict[str, Any]] = []
        client_cfg = opportunity.get("client_cfg", {})
        slug = opportunity.get("blueprint", {}).get("slug", "default-slug")

        domain = client_cfg.get("target_domain", "")
        article_url = f"https://{domain}/{slug}" if domain else slug
        publisher_name = domain or "Publisher Name"

        h1_tag = soup.find("h1")
        article_headline = (
            h1_tag.get_text(strip=True)
            if h1_tag
            else opportunity.get("keyword", "Article")
        )

        article_schema = {
            "@type": "BlogPosting",
            "@id": f"{article_url}#article",
            "mainEntityOfPage": {"@id": article_url},
            "headline": article_headline,
            "author": {
                "@type": client_cfg.get("schema_author_type", "Organization"),
                "name": client_cfg.get("default_author_name", "Author"),
            },
            "publisher": {"@type": "Organization", "name": publisher_name},
            "datePublished": datetime.now().isoformat(),
            "dateModified": datetime.now().isoformat(),
            "additionalProperties": False,
        }
        schema_graph.append(article_schema)

        # Dynamic HowTo Schema
        how_to_headings = soup.find_all(
            ["h2", "h3"], string=re.compile(r"how to", re.IGNORECASE)
        )
        for heading in how_to_headings:
            ol = heading.find_next("ol")
            if ol:
                steps = [
                    {"@type": "HowToStep", "text": li.get_text(strip=True)}
                    for li in ol.find_all("li")
                ]
                if steps:
                    schema_graph.append(
                        {
                            "@type": "HowTo",
                            "name": heading.get_text(strip=True),
                            "step": steps,
                        }
                    )

        return {"@context": "https://schema.org", "@graph": schema_graph}

    def _replace_image_placeholders(
        self, soup: BeautifulSoup, in_article_images_data: List[Dict[str, Any]]
    ) -> None:
        """Replaces [[IMAGE: ...]] placeholders with actual <img> tags."""
        if not in_article_images_data:
            return

        image_data_map = {
            item["original_prompt"]: item for item in in_article_images_data
        }

        for p_tag in soup.find_all("p", string=re.compile(r"\[\[IMAGE: (.*?)\]\]")):
            placeholder_text = p_tag.get_text()
            match = re.search(r"\[\[IMAGE: (.*?)\]\]", placeholder_text)
            if not match:
                continue

            prompt = match.group(1).strip()
            image_info = image_data_map.get(prompt)

            if image_info and image_info.get("local_path"):
                relative_path = f"/api/images/{os.path.basename(image_info['local_path'])}"
                img_tag = soup.new_tag(
                    "img",
                    src=relative_path,
                    alt=image_info.get("alt_text", prompt),
                    **{"class": "in-article-image"},
                )
                # Replace the entire paragraph with the image
                p_tag.replace_with(img_tag)
            else:
                # If no image was found, remove the placeholder paragraph to keep the HTML clean
                p_tag.decompose()

    def format_final_package(
        self,
        opportunity: Dict[str, Any],
        internal_linking_suggestions: Optional[List[Dict[str, str]]] = None,
        in_article_images_data: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Constructs the final content package, now including schema generation.
        """
        ai_content = opportunity.get("ai_content", {})
        client_cfg = opportunity.get("client_cfg", {})
        html_body_str = ai_content.get("article_body_html", "")
        soup = BeautifulSoup(f"<div>{html_body_str}</div>", "html.parser")

        if internal_linking_suggestions:
            self._insert_internal_links(soup, internal_linking_suggestions)

        if client_cfg.get("generate_toc", True):
            self._generate_toc(soup)

        if in_article_images_data:
            self._replace_image_placeholders(soup, in_article_images_data)

        article_html_final = (
            str(soup.body.decode_contents()) if soup.body else str(soup)
        )

        # --- NEW: Call the schema generator ---
        schema_org_json = self._generate_schema_org(soup, opportunity)

        featured_image = opportunity.get("featured_image_data", {})
        featured_image_relative_path = (
            f"/api/images/{os.path.basename(featured_image.get('local_path'))}"
            if featured_image and featured_image.get("local_path")
            else None
        )

        return {
            "meta_title": ai_content.get("meta_title", "No Title"),
            "meta_description": ai_content.get("meta_description", ""),
            "article_html_final": article_html_final,
            "schema_org_json": schema_org_json,
            "featured_image_path": featured_image.get("local_path"),
            "featured_image_relative_path": featured_image_relative_path,
            "social_media_posts": opportunity.get("social_media_posts_json", []),
        }
