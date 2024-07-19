from bs4 import BeautifulSoup
import os
import re

def sanitize_filename(filename):
    return re.sub(r'[^\w\-\. ]', '', filename)

def get_image_name(alt_text):
    alt_map = {
        "logo": ("logo", "webp"),
        "flag": ("flag", "webp"),
        "ticbullet": ("ticbullet", "webp"),
        "tikbullet": ("ticbullet", "webp"),
        "toptesti": ("toptesti", "webp"),
        "shipping": ("shipping", "webp"),
        "support team icon": ("support team icon", "webp"),
        "happy customers icon": ("happy customers icon", "webp"),
        "firstp": ("firstp", "webp"),
        "secondp": ("secondp", "webp"),
        "big money back": ("big money back", "webp"),
        "trustpilotbig": ("trustpilotbig", "webp"),
        "verifiedcompany": ("verifiedcompany", "webp"),
        "testi1": ("testi1", "webp"),
        "testi2": ("testi2", "webp"),
        "testi3": ("testi3", "webp"),
        "testi4": ("testi4", "webp"),
        "faq side": ("FAQ side", "webp"),
        "pricewill": ("pricewill", "webp"),
        "30 days warranty icon": ("30 days warranty icon", "webp"),
        "5 stars": ("5 stars", "svg"),
        "small trust pilot": ("small trust pilot", "svg"),
        "grades": ("grades", "webp"),
        "thirdp": ("thirdp", "webp"),
    }
    cleaned_alt = alt_text.lower().strip()
    return alt_map.get(cleaned_alt, (cleaned_alt, "webp"))

def update_image_paths(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    image_counter = 1
    image_map = {}

    img_tags = soup.find_all('img')
    print(f"Total img tags found: {len(img_tags)}")

    for img in img_tags:
        print(f"\nOriginal tag: {img}")
        
        # Remove crossorigin attribute
        if img.has_attr('crossorigin'):
            del img['crossorigin']

        # Find data-srcset or src
        old_src = img.get('data-srcset') or img.get('src')
        alt_text = img.get('alt', '')
        
        if old_src:
            if ' ' in old_src:  # Remove any size specifier (like '1x')
                old_src = old_src.split()[0]
            
            new_filename, extension = get_image_name(alt_text)
            new_filename = f"{new_filename}.{extension}"
            image_map[old_src] = (new_filename, alt_text)
            
            new_src = f'./pics/{new_filename}'
            
            # Update src attribute, remove data-srcset and data-src
            img['src'] = new_src
            if img.has_attr('data-srcset'):
                del img['data-srcset']
            if img.has_attr('data-src'):
                del img['data-src']
            
            print(f"Updated to: {img}")
            print(f"Changed: {old_src} -> {new_src}")
            print(f"Alt text: {alt_text}")
        else:
            print("No source found, skipping this tag")

    # Write the updated content back to the file
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"\nUpdated {html_file}")
    print(f"Total unique images renamed: {len(image_map)}")

    # Print out the image mapping for reference
    print("\nImage name mapping:")
    for old, (new, alt) in image_map.items():
        print(f"{old} -> {new} (Alt: {alt})")

html_file = 'index.html'
update_image_paths(html_file)