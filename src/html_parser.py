import logging
from pathlib import Path
from bs4 import BeautifulSoup
from dateutil import parser
from typing import List, Tuple

logger = logging.getLogger(__name__)

def extract_dates_from_html(html_file_path: Path) -> Tuple[List[Tuple[str, datetime]], int]:
    if not html_file_path.exists():
        logger.error(f"Error: HTML file not found at {html_file_path}")
        return [], 0

    with html_file_path.open('r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    date_image_pairs = []
    entries = soup.find_all(class_='pam _3-95 _2ph- _a6-g uiBoxWhite noborder')
    total_links = 0
    
    for entry in entries:
        img_elem = entry.find('img') or entry.find('video')
        date_elem = entry.find('div', class_='_a6-q', string='Date taken') or entry.find('div', class_='_a6-q', string='Creation time')
        
        if img_elem:
            total_links += 1
            image_path = img_elem.get('src')
            image_name = Path(image_path).name
            
            if date_elem:
                date_str = date_elem.find_next('div', class_='_a6-q').text.strip()
            else:
                date_elem = entry.find('div', class_='_3-94 _a6-o')
                if date_elem:
                    date_str = date_elem.text.strip()
                else:
                    logger.warning(f"No date found for file: {image_name}")
                    continue
            
            try:
                date = parser.parse(date_str)
                date_image_pairs.append((image_name, date))
            except ValueError:
                logger.error(f"Error parsing date: {date_str} for file: {image_name}")
        else:
            logger.warning("Missing img or video element in an entry")
    
    return date_image_pairs, total_links