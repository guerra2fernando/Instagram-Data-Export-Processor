import logging
import argparse
import yaml
from pathlib import Path
from src.file_processor import process_html_and_media

def load_config(config_path):
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)

def main():
    parser = argparse.ArgumentParser(description='Process Instagram data export files.')
    parser.add_argument('base_dir', type=str, help='Base directory of the Instagram data export')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration file')
    parser.add_argument('--log-level', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level')
    args = parser.parse_args()

    config = load_config(args.config)

    log_level = args.log_level or config.get('log_level', 'INFO')
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    base_dir = Path(args.base_dir)
    content_dir = base_dir / config['content_dir']
    media_dir = base_dir / config['media_dir']

    html_files = config['html_files']

    total_stats = {
        'total_links': 0,
        'files_processed': 0,
        'files_updated': 0,
        'files_not_found': 0
    }

    for html_file, media_folder in html_files.items():
        html_file_path = content_dir / html_file
        media_directory = media_dir / media_folder

        if html_file_path.exists() and media_directory.exists():
            try:
                links, processed, updated, not_found = process_html_and_media(html_file_path, media_directory)
                total_stats['total_links'] += links
                total_stats['files_processed'] += processed
                total_stats['files_updated'] += updated
                total_stats['files_not_found'] += not_found
            except Exception as e:
                logger.error(f"Error processing {html_file}: {str(e)}")
        else:
            logger.warning(f"Skipping {html_file} as either HTML file or media directory not found.")

    logger.info("\nOverall Processing Summary:")
    logger.info(f"Total links in all HTML files: {total_stats['total_links']}")
    logger.info(f"Total files processed: {total_stats['files_processed']}")
    logger.info(f"Total files updated successfully: {total_stats['files_updated']}")
    logger.info(f"Total files not found: {total_stats['files_not_found']}")
    logger.info(f"Total files not updated correctly: {total_stats['files_processed'] - total_stats['files_updated']}")

if __name__ == "__main__":
    main()