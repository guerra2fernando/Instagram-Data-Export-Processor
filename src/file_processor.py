import os
import logging
from pathlib import Path
from datetime import datetime
from src.html_parser import extract_dates_from_html
from src.metadata_updater import update_file_metadata, update_image_exif

logger = logging.getLogger(__name__)

def process_html_and_media(html_file_path: Path, media_directory: Path) -> tuple[int, int, int, int]:
    logger.info(f"Processing {html_file_path}...")
    date_file_pairs, total_links = extract_dates_from_html(html_file_path)
    logger.info(f'Found {len(date_file_pairs)} files in HTML out of {total_links} total links.')
    
    if not date_file_pairs:
        logger.warning("No file-date pairs found. Skipping.")
        return 0, 0, 0, 0

    files_processed = 0
    files_updated = 0
    files_not_found = 0

    for file_name, date in date_file_pairs:
        try:
            logger.debug(f'Processing {file_name} with date {date}...')
            file_path = find_file(media_directory, file_name)
            if file_path:
                new_file_path, update_success = update_file_metadata(file_path, date)
                if update_success:
                    files_updated += 1
                    if new_file_path.lower().endswith(('.jpg', '.jpeg', '.webp')):
                        exif_success = update_image_exif(new_file_path, date)
                        if not exif_success:
                            logger.warning(f"Failed to update EXIF for {new_file_path}")
                files_processed += 1
            else:
                logger.warning(f'File {file_name} not found in the directory')
                files_not_found += 1
        except Exception as e:
            logger.error(f"Error processing file {file_name}: {str(e)}")

    return total_links, files_processed, files_updated, files_not_found

def find_file(directory: Path, filename: str) -> Path | None:
    for file_path in directory.rglob(filename):
        return file_path
    return None