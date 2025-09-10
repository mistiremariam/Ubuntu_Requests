import requests
import os
from urllib.parse import urlparse
import hashlib

def generate_filename(url, content=None):
    """Generate a filename from the URL or content hash if missing."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    if not filename:  # If the URL doesn't end with a file
        if content:
            # Generate hash-based filename for uniqueness
            file_hash = hashlib.md5(content).hexdigest()[:8]
            filename = f"image_{file_hash}.jpg"
        else:
            filename = "downloaded_image.jpg"
    return filename


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Get URLs from user (support single or multiple, comma-separated)
    urls = input("Please enter the image URL(s) (comma-separated if multiple): ").split(",")

    # Create directory if it doesn't exist
    os.makedirs("Fetched_Images", exist_ok=True)

    for url in urls:
        url = url.strip()
        if not url:
            continue
        
        try:
            # Fetch the image with timeout
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            # Check if content type is image
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"✗ Skipped (not an image): {url}")
                continue

            # Get content for filename hashing and duplicate check
            content = response.content
            filename = generate_filename(url, content)

            filepath = os.path.join("Fetched_Images", filename)

            # Avoid duplicate downloads
            if os.path.exists(filepath):
                print(f"⚠ Duplicate skipped: {filename}")
                continue

            # Save the image in binary mode
            with open(filepath, 'wb') as f:
                f.write(content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error while fetching {url}: {e}")
        except Exception as e:
            print(f"✗ An error occurred with {url}: {e}")

    print("\nConnection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
