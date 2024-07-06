import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import time
import webbrowser
import platform

def download_resource(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

def download_website(url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for css in soup.find_all('link', rel='stylesheet'):
        css_url = urljoin(url, css.get('href'))
        css_path = os.path.join(output_dir, os.path.basename(urlparse(css_url).path))
        download_resource(css_url, css_path)
        css['href'] = os.path.basename(css_path)

    for script in soup.find_all('script', src=True):
        script_url = urljoin(url, script.get('src'))
        script_path = os.path.join(output_dir, os.path.basename(urlparse(script_url).path))
        download_resource(script_url, script_path)
        script['src'] = os.path.basename(script_path)

    for img in soup.find_all('img', src=True):
        img_url = urljoin(url, img.get('src'))
        img_path = os.path.join(output_dir, os.path.basename(urlparse(img_url).path))
        download_resource(img_url, img_path)
        img['src'] = os.path.basename(img_path)

    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as file:
        file.write(str(soup))

def check_website(url, interval=60, max_attempts=None):
    attempts = 0
    while max_attempts is None or attempts < max_attempts:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"Success! Website {url} is now accessible.")
                download_website(url, 'downloaded_website')
                open_local_file(os.path.join('downloaded_website', 'index.html'))
                return True
        except requests.RequestException:
            print(f"Attempt {attempts + 1}: Website {url} is still not accessible. Retrying in {interval} seconds.")

        attempts += 1
        time.sleep(interval)

    print(f"Max attempts reached. Website {url} is still not accessible.")
    return False

def open_local_file(file_path):
    """Open the local file in the default web browser"""
    webbrowser.open('file://' + os.path.realpath(file_path))

if __name__ == "__main__":
    website_url = "https://www.aadl3inscription2024.dz/AR/Inscription-desktop.php"  
    check_interval = 300  
    max_attempts = None attempts, or None for infinite attempts

    check_website(website_url, check_interval, max_attempts)