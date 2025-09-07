import os
import requests
from urllib.parse import urlparse
from pathlib import Path

def fetch_image():
    # Prompt the user for a URL
    url = input("Enter the image URL: ").strip()

    # Create the Fetched_Images directory if it doesn't exist
    save_dir = Path("Fetched_Images")
    save_dir.mkdir(exist_ok=True)

    try:
        # Send GET request to fetch the image
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # If no filename, generate one
        if not filename:
            filename = "downloaded_image.jpg"

        save_path = save_dir / filename

        # Save image in binary mode
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Image successfully saved as: {save_path}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    fetch_image()

