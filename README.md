# ✨ PaperScraper ✨ <p align="center">
  [![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=30&pause=1000&color=16A3B2FF&width=440&height=60&lines=PaperScraper)](https://git.io/typing-svg)
</p>

A Python script for scraping and downloading wallpapers from WallpaperCave categories.

[![Built with Python](https://img.shields.io/badge/Built%20with-Python-1f425f.svg)](https://www.python.org/)

---

## 📖 Overview

`PaperScraper` is a straightforward command-line tool in Python designed to streamline the download of wallpapers from specific categories on WallpaperCave. It intelligently navigates the website's listing pages, accesses individual wallpaper pages, extracts the direct image download links, and efficiently saves the wallpapers to your preferred local directory, while preventing duplicate downloads.

---

## ✨ Features

-   **Targeted Scraping:** Extracts wallpaper links from a specified WallpaperCave category URL.
-   **Smart Navigation:** Visits individual wallpaper pages linked from the main list.
-   **Download Handling:** Identifies and follows the unique download button links to retrieve high-resolution images.
-   **Automated Saving:** Organizes and saves downloaded images to a designated local folder (`~/Pictures/wallpapers` by default).
-   **Duplicate Prevention:** Skips downloading images that already exist in the target directory.
-   **Server Politeness:** Includes built-in delays and a standard User-Agent header to make requests resemble browser traffic and avoid overwhelming the server.

---

## 🎬 Demo

*(Suggestion: Add an animated GIF or a screenshot here showing the script running or showing the downloaded files in the wallpapers directory.)*

To add a GIF or image:
1.  Create your animated GIF or take a screenshot.
2.  Upload it to your repository (e.g., in a folder named `assets`).
3.  Reference it in the README like this: `![Alt text describing the image](path/to/your/image.gif)`

---

## 🚀 Requirements

-   Python 3.7+
-   `requests` library
-   `beautifulsoup4` library

Utilizing a Python [virtual environment](https://docs.python.org/3/library/venv.html) is highly recommended to isolate the project's dependencies.

---

## 🛠️ Installation and Setup

1.  **Obtain the Script:**
    * If storing in a Git repository: Clone it - `git clone <your-repo-url>` and `cd <your-repo-name>`.
    * Otherwise: Simply place the `wallpaper_scraper.py` file in your desired project directory.

2.  **Set up a Python Virtual Environment:**
    Create an isolated environment for dependencies. We'll use the name `PaperScraper`.
    ```bash
    python -m venv PaperScraper
    ```

3.  **Activate the Virtual Environment:**
    You need to activate the environment in each terminal session you use to run the script.
    * On Linux/macOS (Bash, Zsh, etc.): `source PaperScraper/bin/activate`
    * On Windows (Command Prompt): `PaperScraper\Scripts\activate.bat`
    * On Windows (PowerShell): `PaperScraper\Scripts\Activate.ps1`
    * On Fish shell: `source PaperScraper/bin/activate.fish`
    Your prompt should show `(PaperScraper)` when the environment is active.

4.  **Install Dependencies:**
    With the environment active, install the required libraries:
    ```bash
    (PaperScraper) pip install requests beautifulsoup4
    ```

5.  **Verify CSS Selectors (Potential Troubleshooting Step):**
    Websites can change their structure. The script relies on finding elements using CSS selectors specific to WallpaperCave's HTML (`a.wpinkw`, `a#tdownload`, etc.). If the script fails to find links or images, the website's structure may have changed, and you'll need to:
    * Inspect the website's HTML using browser developer tools.
    * Update the corresponding `soup.select()` and `soup.find()` calls in `wallpaper_scraper.py`.

---

## 💻 Usage

1.  **Activate your virtual environment:**
    ```bash
    source PaperScraper/bin/activate.fish # Or your shell's equivalent
    ```

2.  **Run the script:**
    Make sure your terminal is in the directory containing `wallpaper_scraper.py`.
    ```bash
    (PaperScraper) python wallpaper_scraper.py
    ```

The script will proceed to fetch the listing page, process links, and download wallpapers to the configured directory.

---

## ⚙️ Configuration

Modify the following variables at the beginning of the `wallpaper_scraper.py` file to customize behavior:

-   `LISTING_URL`: Specify the starting URL for the WallpaperCave category.
-   `DOWNLOAD_DIR`: Define the local path where downloaded wallpapers will be saved.
-   `HEADERS`: Customize the `User-Agent` string if needed (rarely necessary).
-   `time.sleep()`: Adjust delays to control the rate of requests (important for politeness and stability).

---

## ⚠️ Disclaimer and Terms of Service

Please be aware that automated scraping may be restricted by the terms of service of the target website. WallpaperCave's terms should be reviewed. This script is intended for educational purposes and personal use where you have the necessary authorization to download the content. Always scrape responsibly and avoid causing undue load on the website's servers.

---

## ✨ Future Improvements

-   **Pagination:** Extend the script to automatically traverse and download from all pages within a category.
-   **Command-Line Interface:** Add support for command-line arguments to specify URL, download path, etc., without editing the script file.
-   **More Robust Parsing:** Enhance selectors and error handling for greater resilience to minor website changes.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

-   Powered by the excellent `requests` and `beautifulsoup4` Python libraries.
