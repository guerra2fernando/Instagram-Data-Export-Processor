import os
import time
import logging
from pathlib import Path
from datetime import datetime
from PIL import Image
import piexif

logger = logging.getLogger(__name__)

def update_file_metadata(file_path: Path, new_date: datetime) -> tuple[Path, bool]:
    try:
        # Update file modification time
        os.utime(file_path, (time.mktime(new_date.timetuple()),) * 2)
        
        # Update file creation time (platform-specific)
        if os.name == 'nt':  # Windows
            from win32_setctime import setctime
            setctime(str(file_path), time.mktime(new_date.timetuple()))
        else:  # Unix-based systems
            stat = os.stat(file_path)
            os.utime(file_path, (new_date.timestamp(), stat.st_mtime))

        # Update file name
        new_file_name = new_date.strftime("%Y%m%d_%H%M%S") + file_path.suffix
        new_file_path = file_path.with_name(new_file_name)
        
        # Rename the file
        file_path.rename(new_file_path)
        
        logger.info(f'Successfully updated {file_path} to {new_file_path} with date {new_date}')
        return new_file_path, True
    except Exception as e:
        logger.error(f"Error updating {file_path}: {e}")
        return file_path, False

def update_image_exif(image_path: Path, new_date: datetime) -> bool:
    try:
        # Update EXIF data for images (jpg, jpeg, webp)
        if image_path.suffix.lower() in ('.jpg', '.jpeg', '.webp'):
            with Image.open(image_path) as img:
                exif_dict = piexif.load(img.info.get('exif', b''))
                
                # Update date in EXIF
                date_str = new_date.strftime("%Y:%m:%d %H:%M:%S")
                exif_dict['0th'][piexif.ImageIFD.DateTime] = date_str
                exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_str
                exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date_str
                
                exif_bytes = piexif.dump(exif_dict)
                
                # Save the updated EXIF data
                img.save(image_path, exif=exif_bytes)

            logger.info(f"Successfully updated EXIF for {image_path}")
            return True
        else:
            logger.info(f"Skipping EXIF update for non-supported file type: {image_path}")
            return False
    except Exception as e:
        logger.error(f"Error updating EXIF for {image_path}: {e}")
        return False