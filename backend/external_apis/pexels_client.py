import requests
import logging
import os
from typing import List, Dict, Any, Optional, Tuple


class PexelsClient:
    """
    Manages communication with the Pexels API for free stock photos and videos.
    """

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Pexels API key is required.")
        self.base_url_photos = "https://api.pexels.com/v1/"
        self.base_url_videos = "https://api.pexels.com/videos/"  # Not used in this plan, but included for completeness
        self.headers = {"Authorization": api_key}
        self.logger = logging.getLogger(self.__class__.__name__)

    def search_photos(
        self,
        query: str,
        orientation: Optional[str] = None,
        size: Optional[str] = None,
        per_page: int = 1,
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Searches for photos on Pexels based on a query.
        Returns a list of photo dicts (simplified for direct use) and a dummy cost (Pexels is free).
        """
        endpoint = f"{self.base_url_photos}search"
        params = {
            "query": query,
            "per_page": per_page,
        }
        if orientation:
            params["orientation"] = orientation
        if size:
            params["size"] = size

        try:
            response = requests.get(
                endpoint, headers=self.headers, params=params, timeout=10
            )
            response.raise_for_status()
            data = response.json()

            photos = []
            for photo in data.get("photos", []):
                # Simplify the photo data to what's immediately useful
                photos.append(
                    {
                        "id": photo["id"],
                        "url": photo["url"],
                        "photographer": photo["photographer"],
                        "photographer_url": photo["photographer_url"],
                        "src": photo["src"],  # Contains different sizes
                        "alt": photo.get(
                            "alt", f"Photo by {photo['photographer']} on Pexels"
                        ),
                    }
                )

            self.logger.info(
                f"Found {len(photos)} photos on Pexels for query '{query}'."
            )
            return photos, 0.0  # Pexels is free, so cost is 0

        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"Error searching Pexels photos for '{query}': {e}", exc_info=True
            )
            return [], 0.0
        except Exception as e:
            self.logger.error(
                f"Unexpected error in Pexels photo search for '{query}': {e}",
                exc_info=True,
            )
            return [], 0.0


def download_image_from_url(image_url: str, save_path: str) -> Optional[str]:
    """
    Downloads an image from a given URL and saves it locally.
    Returns the local file path on success, None on failure.
    """
    try:
        response = requests.get(image_url, stream=True, timeout=30)
        response.raise_for_status()

        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)

        logging.getLogger(__name__).info(
            f"Downloaded image from {image_url} to {save_path}"
        )
        return save_path
    except requests.exceptions.RequestException as e:
        logging.getLogger(__name__).error(
            f"Failed to download image from {image_url}: {e}", exc_info=True
        )
        return None
    except Exception as e:
        logging.getLogger(__name__).error(
            f"An unexpected error occurred during image download: {e}", exc_info=True
        )
        return None
