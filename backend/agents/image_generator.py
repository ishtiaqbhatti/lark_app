import logging
import os
from typing import Dict, Any, Tuple, Optional, List

from backend.external_apis.pexels_client import PexelsClient, download_image_from_url
from backend.core import utils

from PIL import Image, ImageDraw, ImageFont, ImageColor


class ImageGenerator:
    """
    Agent for finding featured and in-article images from Pexels.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

        self.pexels_client = None
        if self.config.get("pexels_api_key"):
            try:
                self.pexels_client = PexelsClient(self.config["pexels_api_key"])
            except ValueError as e:
                self.logger.warning(
                    f"Pexels client could not be initialized: {e}. Image generation will be skipped."
                )

    def _add_text_overlay(self, image_path: str, text: str) -> str:
        """Adds a text overlay to the image based on configured settings."""
        if not self.config.get("overlay_text_enabled", False):
            return image_path  # If disabled, return original path

        try:
            image = Image.open(image_path).convert(
                "RGBA"
            )  # Convert to RGBA for alpha channel in overlay background
            draw = ImageDraw.Draw(image)

            text_color = ImageColor.getrgb(
                self.config.get("overlay_text_color", "#FFFFFF")
            )
            bg_color_hex = self.config.get("overlay_background_color", "#00000080")
            # Extract RGB and alpha from RGBA hex
            bg_color = ImageColor.getrgb(
                bg_color_hex
            )  # This returns (R,G,B) for #RRGGBB or (R,G,B,A) for #RRGGBBAA
            # Ensure bg_color is (R,G,B,A) if alpha is specified
            if len(bg_color) == 3 and len(bg_color_hex) == 9:  # #RRGGBBAA format
                bg_alpha = int(bg_color_hex[7:9], 16)
                bg_color = bg_color + (bg_alpha,)
            elif len(bg_color) == 3:  # default to some alpha if only RGB is given
                bg_color = bg_color + (128,)  # Default 50% opacity

            font_size = self.config.get("overlay_font_size", 40)

            try:
                # Use a reliable path to a bundled font file.
                # Assumes a `resources/fonts` directory exists relative to the project root.
                font_path = os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "..",
                    "resources",
                    "fonts",
                    "DejaVuSans-Bold.ttf",
                )
                if not os.path.exists(font_path):
                    raise IOError("Bundled font file not found.")
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                self.logger.warning(
                    f"Could not load the bundled font at {font_path}. "
                    "Falling back to default bitmap font. Text quality will be poor. "
                    "Ensure the font file exists."
                )
                font = ImageFont.load_default()

            # Use textbbox (or textsize for older PIL versions)
            # draw.textbbox is preferred
            try:
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
            except (
                AttributeError
            ):  # Fallback for older PIL where textbbox might not exist
                text_width, text_height = draw.textsize(text, font=font)

            # Position the text based on configuration
            position = self.config.get("overlay_position", "bottom_center")
            padding = 20  # Padding around text

            x, y = 0, 0
            if "center" in position:
                x = (image.width - text_width) / 2
            elif "left" in position:
                x = padding
            elif "right" in position:
                x = image.width - text_width - padding

            if "bottom" in position:
                y = image.height - text_height - padding
            elif "top" in position:
                y = padding
            elif "center" in position:  # Vertical center
                y = (image.height - text_height) / 2

            # Create a transparent layer for the background
            overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
            draw_overlay = ImageDraw.Draw(overlay)

            # Draw semi-transparent background
            draw_overlay.rectangle(
                (
                    x - padding / 2,
                    y - padding / 2,
                    x + text_width + padding / 2,
                    y + text_height + padding / 2,
                ),
                fill=bg_color,
            )

            image = Image.alpha_composite(image, overlay)  # Composite the background
            draw = ImageDraw.Draw(image)  # Re-get draw object for updated image

            draw.text((x, y), text, font=font, fill=text_color)

            # Save the modified image
            new_image_path = image_path.replace(".jpeg", "-overlay.jpeg")
            image.convert("RGB").save(new_image_path)
            return new_image_path
        except Exception as e:
            self.logger.error(f"Failed to add text overlay to image: {e}")
            return image_path

    def generate_featured_image(
        self, opportunity: Dict[str, Any]
    ) -> Tuple[Optional[Dict[str, Any]], float]:
        """
        Finds and saves the featured image for the article from Pexels.
        """
        if not self.pexels_client:
            self.logger.warning(
                "Pexels client not initialized. Cannot generate featured image."
            )
            return None, 0.0

        search_query = opportunity["keyword"]
        self.logger.info(f"Searching Pexels for featured image for '{search_query}'...")

        pexels_photos, cost = self.pexels_client.search_photos(
            query=search_query, orientation="landscape", size="large", per_page=1
        )

        if not pexels_photos:
            self.logger.warning(
                f"No suitable featured image found on Pexels for '{search_query}'."
            )
            return None, cost

        best_photo = pexels_photos[0]
        best_photo_url = (
            best_photo["src"].get("landscape")
            or best_photo["src"].get("large2x")
            or best_photo["src"].get("original")
        )

        if not best_photo_url:
            self.logger.warning(
                f"Pexels photo found, but no usable URL for '{search_query}'."
            )
            return None, cost

        image_dir = "generated_images"
        os.makedirs(image_dir, exist_ok=True)
        file_path = os.path.join(
            image_dir,
            f"pexels-featured-{utils.slugify(search_query)}-{best_photo['id']}.jpeg",
        )

        local_path = download_image_from_url(best_photo_url, file_path)

        if not local_path:
            self.logger.error(
                f"Failed to download featured image from Pexels: {best_photo_url}"
            )
            return None, cost

        # Add text overlay
        meta_title = opportunity.get("ai_content", {}).get(
            "meta_title", opportunity["keyword"]
        )
        local_path = self._add_text_overlay(local_path, meta_title)

        self.logger.info(
            f"Successfully sourced featured image from Pexels: {local_path}"
        )
        return {
            "type": "featured",
            "search_query": search_query,
            "local_path": local_path,
            "remote_url": best_photo_url,  # Store Pexels URL directly
            "alt_text": best_photo["alt"],
            "source_id": best_photo["id"],
            "source": "Pexels",
        }, cost

    def _simplify_prompt_for_pexels(self, descriptive_prompt: str) -> str:
        """
        Uses an LLM to extract 3-5 high-impact keywords suitable for a stock photo search
        from a more descriptive AI image prompt.
        """
        if not descriptive_prompt or not self.openai_client:
            return descriptive_prompt  # Fallback to original if no client or prompt

        self.logger.info(
            f"Refining image prompt for Pexels search: '{descriptive_prompt}'"
        )

        prompt_messages = [
            {
                "role": "system",
                "content": "You are a concise keyword extractor for stock photo sites. Extract 3-5 key nouns, adjectives, or short phrases from the user's descriptive image prompt that would be most effective for searching a stock photo library like Pexels. Return only a comma-separated list of keywords.",
            },
            {"role": "user", "content": f"Descriptive prompt: '{descriptive_prompt}'"},
        ]

        # Use a low temperature for predictable, factual output
        extracted_keywords_str, error = self.openai_client.call_chat_completion(
            messages=prompt_messages,
                            model=self.config.get("default_model", "gpt-5-nano"),  # Use a cost-effective model for this            temperature=0.1,
            max_completion_tokens=50,  # Keep output very short
            schema={
                "name": "extract_keywords",
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Comma-separated keywords.",
                    }
                },
                "required": ["keywords"],
                "additionalProperties": False
            },
        )

        if error or not extracted_keywords_str:
            self.logger.warning(
                f"Failed to extract keywords for Pexels. Falling back to original prompt. Error: {error}"
            )
            return descriptive_prompt  # Fallback to original prompt

        # The AI should return a dictionary with a 'keywords' key
        if (
            isinstance(extracted_keywords_str, dict)
            and "keywords" in extracted_keywords_str
        ):
            return extracted_keywords_str["keywords"]
        elif isinstance(
            extracted_keywords_str, str
        ):  # Fallback if AI doesn't follow schema perfectly
            return extracted_keywords_str

        return descriptive_prompt  # Final fallback

    # In class ImageGenerator, replace the generate_images_from_prompts method
    def generate_images_from_prompts(
        self, prompts: List[str]
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Finds and saves in-article images from Pexels based on a list of specific prompts.
        """
        if not self.pexels_client:
            self.logger.warning(
                "Pexels client not initialized. Cannot generate images from prompts."
            )
            return [], 0.0

        images_data = []
        total_cost = 0.0

        for i, prompt in enumerate(prompts):
            search_query = self._simplify_prompt_for_pexels(prompt)
            self.logger.info(
                f"Searching Pexels for in-article image with simplified query: '{search_query}' (from prompt: '{prompt}')..."
            )

            pexels_photos, cost = self.pexels_client.search_photos(
                query=search_query, orientation="landscape", size="large", per_page=1
            )
            total_cost += cost

            if pexels_photos:
                photo = pexels_photos[0]
                photo_url = photo["src"].get("large") or photo["src"].get("original")

                if photo_url:
                    image_dir = "generated_images"
                    os.makedirs(image_dir, exist_ok=True)
                    file_path = os.path.join(
                        image_dir,
                        f"pexels-in-article-{utils.slugify(search_query)}-{photo['id']}.jpeg",
                    )
                    local_path = download_image_from_url(photo_url, file_path)

                    if local_path:
                        images_data.append(
                            {
                                "type": f"in_article_{i + 1}",
                                "search_query": search_query,
                                "original_prompt": prompt,
                                "local_path": local_path,
                                "remote_url": photo_url,
                                "alt_text": photo.get("alt") or prompt,
                                "source_id": photo["id"],
                                "source": "Pexels",
                            }
                        )
                        self.logger.info(
                            f"Successfully sourced in-article image from Pexels: {local_path}"
                        )
                        continue

            self.logger.warning(
                f"Could not find a suitable Pexels image for prompt: '{prompt}'."
            )

        return images_data, total_cost
