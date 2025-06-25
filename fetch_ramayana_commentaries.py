#!/usr/bin/env python3
"""
Script to download Sanskrit commentaries from the Valmiki Ramayana website.

This script fetches all available Sanskrit commentaries from https://www.valmiki.iitk.ac.in
and saves them in an organized directory structure. It also creates a master index JSON file
with metadata about each downloaded commentary.
"""

import argparse
import concurrent.futures
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Commentary catalogue mapping IDs to names
COMMENTARIES = {
    14: "Bhusana",
    9: "Dharmakutam",
    8: "Kataka",
    10: "Siromani",
    11: "Tanisloki",
    12: "Tattvadipika",
    13: "Tilaka",
}

# Base URL for the Valmiki Ramayana website
BASE_URL = "https://www.valmiki.iitk.ac.in/ecommentaries"

# Default headers for HTTP requests
DEFAULT_HEADERS = {
    "User-Agent": "RamayanaScraper/1.0",
    "Accept": "text/html,application/xhtml+xml,application/xml",
    "Accept-Language": "en-US,en;q=0.9",
}

# Output directory
OUTPUT_DIR = Path("output")

# Index file path
INDEX_FILE = OUTPUT_DIR / "commentaries_index.json"


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Download Sanskrit commentaries from the Valmiki Ramayana website."
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume downloading from where it left off.",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=1,
        help="Number of parallel threads to use for downloading (default: 1).",
    )
    return parser.parse_args()


def load_index() -> Dict:
    """Load the existing index file if it exists.

    Returns:
        Dict: The loaded index or an empty dictionary if the file doesn't exist
    """
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Invalid index file. Starting with an empty index.")
    return {"commentaries": []}


def save_index(index: Dict) -> None:
    """Save the index to the index file.

    Args:
        index (Dict): The index to save
    """
    INDEX_FILE.parent.mkdir(exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def fetch_page(
    commentary_id: int, kanda: int, sarga: int, session: requests.Session
) -> Tuple[Optional[str], int]:
    """Fetch a commentary page from the website.

    Args:
        commentary_id (int): The ID of the commentary
        kanda (int): The kanda number
        sarga (int): The sarga number
        session (requests.Session): The requests session to use

    Returns:
        Tuple[Optional[str], int]: A tuple containing the HTML content (or None if not found)
                                   and the HTTP status code
    """
    url = f"{BASE_URL}?field_commnetary_tid={commentary_id}&field_kanda_tid={kanda}&field_sarga_value={sarga}"
    
    try:
        response = session.get(url, headers=DEFAULT_HEADERS, timeout=30)
        return response.text, response.status_code
    except requests.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return None, 500


def parse_commentary(html_content: str) -> Optional[str]:
    """Parse the commentary HTML content to extract the sloka list.

    Args:
        html_content (str): The HTML content of the page

    Returns:
        Optional[str]: The extracted commentary HTML or None if not found
    """
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, "html.parser")
    commentary_div = soup.select_one("div.views-field-field-sloka-list")
    
    if not commentary_div:
        return None
    
    # Return the cleaned HTML content of the commentary div
    return str(commentary_div)


def save_html(
    commentary_name: str, kanda: int, sarga: int, content: str
) -> Optional[str]:
    """Save the commentary HTML content to a file.

    Args:
        commentary_name (str): The name of the commentary
        kanda (int): The kanda number
        sarga (int): The sarga number
        content (str): The HTML content to save

    Returns:
        Optional[str]: The absolute path to the saved file or None if saving failed
    """
    directory = OUTPUT_DIR / commentary_name / f"kanda_{kanda}"
    directory.mkdir(parents=True, exist_ok=True)
    
    file_path = directory / f"sarga_{sarga}.html"
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return str(file_path.absolute())
    except IOError as e:
        logger.error(f"Error saving file {file_path}: {e}")
        return None


def process_commentary(
    commentary_id: int,
    resume: bool,
    existing_entries: Set[Tuple[int, int, int]],
    progress_bar: tqdm,
) -> List[Dict]:
    """Process a single commentary across all kandas and sargas.

    Args:
        commentary_id (int): The ID of the commentary to process
        resume (bool): Whether to resume from where it left off
        existing_entries (Set[Tuple[int, int, int]]): Set of already processed (commentary_id, kanda, sarga) combinations
        progress_bar (tqdm): Progress bar to update

    Returns:
        List[Dict]: List of metadata for each saved commentary
    """
    commentary_name = COMMENTARIES[commentary_id]
    results = []
    session = requests.Session()

    for kanda in range(1, 8):  # Iterate kāṇḍa values 1-7
        sarga = 1
        while True:
            # Skip if already processed and resume is enabled
            if resume and (commentary_id, kanda, sarga) in existing_entries:
                sarga += 1
                progress_bar.update(1)
                continue

            # Respect rate limiting
            time.sleep(1)
            
            # Fetch the page
            html_content, status_code = fetch_page(commentary_id, kanda, sarga, session)
            
            # Update progress
            progress_bar.set_description(
                f"Processing {commentary_name} Kanda {kanda} Sarga {sarga}"
            )
            
            # If 4xx status or no content, move to next kanda
            if status_code >= 400 and status_code < 500:
                break
            
            # Parse the commentary
            commentary_html = parse_commentary(html_content)
            
            if not commentary_html:
                logger.warning(
                    f"No commentary found for {commentary_name} Kanda {kanda} Sarga {sarga}",
                    file=sys.stderr,
                )
                sarga += 1
                progress_bar.update(1)
                
                # If we've checked 5 consecutive sargas without content, move to next kanda
                if sarga > 5 and all(
                    not parse_commentary(fetch_page(commentary_id, kanda, s, session)[0])
                    for s in range(sarga - 4, sarga + 1)
                ):
                    break
                
                continue
            
            # Save the HTML content
            file_path = save_html(commentary_name, kanda, sarga, commentary_html)
            
            if file_path:
                # Add to results
                results.append({
                    "commentary_id": commentary_id,
                    "commentary_name": commentary_name,
                    "kanda": kanda,
                    "sarga": sarga,
                    "path": file_path,
                    "timestamp": datetime.now().isoformat(),
                })
            
            sarga += 1
            progress_bar.update(1)

    return results


def main() -> None:
    """Main function to orchestrate the download process."""
    args = parse_arguments()
    
    # Load the existing index if resuming
    index = load_index() if args.resume else {"commentaries": []}
    
    # Extract existing entries if resuming
    existing_entries = set()
    if args.resume:
        for entry in index["commentaries"]:
            existing_entries.add(
                (entry["commentary_id"], entry["kanda"], entry["sarga"])
            )
    
    # Estimate total number of combinations to process
    # Rough estimate: 7 commentaries * 7 kandas * 70 sargas per kanda on average
    total_combinations = len(COMMENTARIES) * 7 * 70
    
    # Create progress bar
    progress_bar = tqdm(
        total=total_combinations,
        desc="Downloading commentaries",
        unit="page",
    )
    
    # Process commentaries, either sequentially or in parallel
    if args.parallel > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
            futures = []
            for commentary_id in COMMENTARIES:
                futures.append(
                    executor.submit(
                        process_commentary,
                        commentary_id,
                        args.resume,
                        existing_entries,
                        progress_bar,
                    )
                )
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(futures):
                index["commentaries"].extend(future.result())
                # Save index after each commentary is processed
                save_index(index)
    else:
        # Process sequentially
        for commentary_id in COMMENTARIES:
            results = process_commentary(
                commentary_id,
                args.resume,
                existing_entries,
                progress_bar,
            )
            index["commentaries"].extend(results)
            # Save index after each commentary is processed
            save_index(index)
    
    progress_bar.close()
    logger.info(f"Download complete. Index saved to {INDEX_FILE}")


if __name__ == "__main__":
    main()
