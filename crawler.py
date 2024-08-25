import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from PIL import Image
import io

def crawl_website(url, replace_patterns=False, compress_images=False):
    visited_urls = set()
    image_urls = set()
    
    def crawl(url):
        if url in visited_urls:
            return
        visited_urls.add(url)
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all images
        for img in soup.find_all('img'):
            img_url = urljoin(url, img.get('src'))
            image_urls.add((img_url, urlparse(url).path))
        
        # Find all links and crawl them
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith(url):
                crawl(href)
    
    crawl(url)
    
    # Download and process images
    for img_url, page_path in image_urls:
        download_and_process_image(img_url, page_path, replace_patterns, compress_images)

def download_and_process_image(img_url, page_path, replace_patterns, compress_images):
    response = requests.get(img_url)
    if response.status_code == 200:
        # Create directory based on page path
        dir_path = os.path.join('downloaded_images', page_path.strip('/'))
        os.makedirs(dir_path, exist_ok=True)
        
        # Get filename from URL
        filename = os.path.basename(urlparse(img_url).path)
        
        if replace_patterns:
            filename = re.sub(r'[^a-zA-Z0-9\.]', '_', filename)
        
        file_path = os.path.join(dir_path, filename)
        
        # Check if file already exists (to avoid duplicates)
        if not os.path.exists(file_path):
            if compress_images:
                # Open the image using PIL
                img = Image.open(io.BytesIO(response.content))
                # Save with compression
                img.save(file_path, optimize=True, quality=85)
            else:
                with open(file_path, 'wb') as f:
                    f.write(response.content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python crawler.py <url> [replace_patterns] [compress_images]")
        sys.exit(1)
    
    url = sys.argv[1]
    replace_patterns = len(sys.argv) > 2 and sys.argv[2].lower() == 'true'
    compress_images = len(sys.argv) > 3 and sys.argv[3].lower() == 'true'
    
    crawl_website(url, replace_patterns, compress_images)