import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import time  # Import the time module for adding delays

# The URL of the WallpaperCave listing page
# You can change this to other 5120x1440 categories or other resolutions
LISTING_URL = "https://wallpapercave.com/5120x1440-wallpapers"

# The directory to save the downloaded wallpapers
# The os.path.expanduser('~') part gets your home directory
DOWNLOAD_DIR = os.path.expanduser("~/Pictures/wallpapers")

# Define a User-Agent header to make requests look like they come from a browser
# This helps avoid being blocked by the website
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"  # Example User-Agent
}

# Ensure the download directory exists
# Creates the directory if it doesn't already exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_image(image_url, download_path):
    """Downloads an image from a given URL."""
    print(f"Attempting to download: {os.path.basename(download_path)}")
    try:
        # Use stream=True to handle potentially large files efficiently
        # Include headers in the download request as well
        response = requests.get(image_url, headers=HEADERS, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (like 404, 500)

        # Open the local file in binary write mode
        with open(download_path, "wb") as f:
            # Write the file content in chunks
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Successfully downloaded: {os.path.basename(download_path)}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {image_url}: {e}")
    except IOError as e:
        print(f"Error saving file to {download_path}: {e}")


def get_image_url_from_wallpaper_page(page_url):
    """Visits a wallpaper page and finds the direct image URL,
    handling the download button link specifically for WallpaperCave."""
    print(f"  Visiting wallpaper detail page: {page_url}")
    try:
        # Fetch the individual wallpaper page, include headers
        response = requests.get(page_url, headers=HEADERS)
        response.raise_for_status()  # Check for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")

        # --- Strategy to find the main image URL ---
        # Based on inspecting WallpaperCave structure:
        # 1. Find the download button by its ID.
        # 2. Get its href attribute.
        # 3. Make a request to that href, which should redirect to the image.

        # Attempt 1: Find the download button by its ID and follow its href
        # Based on inspection: <a href="/download/..." id="tdownload">
        download_button = soup.find(
            "a", id="tdownload"
        )  # Look for the tag with id="tdownload"
        if download_button is not None:  # Check if the button element was found
            href = download_button.get("href")  # Get the value of the 'href' attribute
            if href:  # Check if the 'href' attribute exists and has a value
                # Construct the full URL for the download link (e.g., https://wallpapercave.com/download/...)
                download_link_url = urljoin(page_url, href)
                print(f"    Found download link URL: {download_link_url}")

                # Now, make a request to this download link.
                # Use allow_redirects=True to automatically follow redirects to the actual image file.
                try:
                    # Use the same headers for the download link request
                    download_response = requests.get(
                        download_link_url, headers=HEADERS, allow_redirects=True
                    )
                    download_response.raise_for_status()  # Check for errors on the download link request

                    # The final URL after any redirects should be the direct image URL
                    image_url = download_response.url
                    # Basic check to ensure it looks like an image URL (ends with common image extensions)
                    if image_url and (
                        image_url.lower().endswith(
                            (".jpg", ".jpeg", ".png", ".gif", ".webp")
                        )
                        or "/get/" in image_url
                        or "/download/" in image_url
                    ):
                        print(f"    Followed redirect to actual image URL: {image_url}")
                        return image_url
                    else:
                        print(
                            f"    Download link did not redirect to a recognizable image URL: {image_url}"
                        )
                        # Fall through to other attempts if the URL doesn't look like an image

                except requests.exceptions.RequestException as e:
                    print(f"    Error following download link {download_link_url}: {e}")
                    # Continue to other attempts if following the download link failed

        # Attempt 2: (Fallback) Find the main image tag directly
        # Look for a large <img> tag that is likely the main wallpaper
        # Example: <img id="wallpaper" src="...">
        main_image = soup.find(
            "img", id="wallpaper"
        )  # !! VERIFY/ADJUST THIS ID/CLASS NAME if needed as a fallback !!
        if main_image is not None:  # Check if the image element was found
            src = main_image.get("src")  # Get the value of the 'src' attribute
            if src:  # Check if the 'src' attribute exists and has a value
                # Use urljoin to handle relative or absolute URLs correctly
                image_url = urljoin(page_url, src)
                print(f"    (Fallback) Found potential main image URL: {image_url}")
                return image_url

        # Attempt 3: (Fallback) Look for a meta tag (like Open Graph)
        # Example: <meta property="og:image" content="...">
        og_image_tag = soup.find(
            "meta", property="og:image"
        )  # !! VERIFY/ADJUST if needed as a fallback !!
        if og_image_tag is not None:  # Check if the meta tag was found
            content = og_image_tag.get(
                "content"
            )  # Get the value of the 'content' attribute
            if content:  # Check if the 'content' attribute exists and has a value
                # Use urljoin even for meta tag content, just in case it's a relative path
                image_url = urljoin(page_url, content)
                print(f"    (Fallback) Found potential og:image URL: {image_url}")
                return image_url

        # If none of the attempts found a URL after checking all methods
        print(
            f"    Could not find a direct image or download URL using defined selectors on {page_url}"
        )
        return None

    # This except block handles requests-related errors when trying to access the detail page ITSELF
    except requests.exceptions.RequestException as e:
        print(f"Error accessing wallpaper page {page_url}: {e}")
        return None


# --- Main Script Execution ---
# This block runs the main logic of the script
print(f"Starting wallpaper scraping from: {LISTING_URL}")

try:
    # Fetch the main listing page, include headers
    print(f"Fetching listing page: {LISTING_URL}")
    response = requests.get(LISTING_URL, headers=HEADERS)
    response.raise_for_status()  # Check for bad status codes (will raise HTTPError)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find links to individual wallpaper pages.
    # BASED ON INSPECTION: Links to individual wallpapers are <a> tags with class="wpinkw"
    # Example: <a href="/w/wpXXXXXXX" class="wpinkw">
    # This selector finds all such links.
    wallpaper_links = soup.select(
        "a.wpinkw"
    )  # **CONFIRMED SELECTOR for listing page links**

    if not wallpaper_links:
        print(
            "Error: No wallpaper links found on the listing page using the CSS selector 'a.wpinkw'."
        )
        print("The website's HTML structure for links may have changed.")
    else:
        print(
            f"Found {len(wallpaper_links)} potential wallpaper links on the listing page."
        )

        # Loop through each found link to a wallpaper page
        # You might want to limit this loop for testing, e.g., wallpaper_links[:10]
        for index, link in enumerate(wallpaper_links):
            # Add a small delay between requests to be polite and avoid overwhelming the server
            time.sleep(
                0.5
            )  # Adjust delay as needed (e.1 to 1.0 seconds is usually good)

            # Get the 'href' attribute from the link element
            # Use .get() which returns None if the attribute doesn't exist
            href = link.get("href")

            # Check if href is not None and is a valid link
            if href:
                # Construct the full URL for the individual wallpaper page
                # urljoin handles cases where href is a relative path (like /w/wpXXXXXXX)
                wallpaper_page_url = urljoin(LISTING_URL, href)

                # Visit the individual wallpaper page and find the image URL
                image_url = get_image_url_from_wallpaper_page(wallpaper_page_url)

                if image_url:
                    # Extract filename from the image URL
                    # os.path.basename gets the part after the last slash (e.g., "image.jpg")
                    image_filename = os.path.basename(image_url)
                    # Construct the full path where the image will be saved
                    download_path = os.path.join(DOWNLOAD_DIR, image_filename)

                    # Check if the file already exists locally before downloading
                    if not os.path.exists(download_path):
                        # Download and save the image
                        # A short delay before downloading the image file itself
                        time.sleep(0.2)  # Adjust as needed
                        download_image(image_url, download_path)
                    else:
                        print(f"  Image already exists: {image_filename}")
                else:
                    # Message already printed by get_image_url_from_wallpaper_page if URL wasn't found
                    pass  # Skip if no image URL was found on the detail page

            else:
                # This happens if a link element was found by the selector but had no 'href' attribute
                print(
                    f"  Skipping a link element found without an 'href' attribute: {link}"
                )
                pass  # Skip links that don't have an href

    # --- Handle Pagination (if necessary) ---
    # Wallpaper listing pages often have pagination (e.g., Page 1, Page 2, Next >>).
    # This script CURRENTLY only processes the first page (the LISTING_URL).
    # To download from subsequent pages, you would need to:
    # 1. Inspect the HTML of the listing page to find the links for pagination (e.g., class='next-page', class='page-link').
    # 2. Add logic here to find the URL of the "Next" page.
    # 3. Create a loop that fetches each subsequent page, finds its wallpaper links, and processes them,
    #    until there are no more "Next" pages.
    print("\nNote: Pagination is not implemented in this script.")
    print(f"Only images from the initial page ({LISTING_URL}) were processed.")


# This except block handles requests-related errors when trying to access the main listing page
except requests.exceptions.RequestException as e:
    print(f"\nError accessing the main listing page {LISTING_URL}: {e}")
# This catches any other unexpected errors during the main script execution
except Exception as e:
    print(f"\nAn unexpected error occurred during script execution: {e}")


print("\nWallpaper download process finished.")
