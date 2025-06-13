import re
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Extracting Titles
def titlesExt(soup):
    page_title = soup.find('title').get_text(strip=True) if soup.find('title') else 'No Title Found'
    title_column_data = {"Topic/Subject": page_title}

    return title_column_data

# Extracting Images
def imagesExt(soup):
    images = []
    for img_tag in soup.find_all('img'):
        img_src = img_tag.get('src')
        if img_src and img_src.startswith(('http://', 'https://')):
            images.append(img_src)
        elif img_src:
            # Handle relative URLs by trying to construct an absolute URL
            from urllib.parse import urljoin
            abs_img_src = urljoin(url, img_src)
            images.append(abs_img_src)

    images_data = [", ".join(images)]
    images_column_data = {"Images": images_data}

    return images_column_data

# EXtracting Location
def locationEXT(soup):
    regex_pattern = r'<p\s+class="mantine-focus-auto m_b6d8b162 mantine-Text-root"\s+style="[^"]*font-weight:\s*600;[^"]*">(.*?)</p>'

    # Search for the pattern in the provided whole_soup_content
    match = re.search(regex_pattern, soup, re.DOTALL)

    extracted_location = ""
    if match:
        full_content_from_tag = match.group(1).strip() # Remove outer leading/trailing whitespace

        extracted_location = full_content_from_tag.replace('•', '').strip()
    extracted_location = extracted_location.replace("<!-- -->","")
    location_column_data = {"Location": extracted_location}
    #print(f"\nResulting column: {location_column_data}")

    return location_column_data


# Extracting Content
def contentExt(soup):
    content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'li', 'ol', 'ul'])

    extracted_texts = []
    seen_texts = set()

    for element in content_elements:
        if element.name in ['script', 'style', 'meta', 'link']: # Added more tags to skip
            continue

        text = element.get_text(strip=True)

        if text and text not in seen_texts and len(text) > 10: # Filter short, potentially irrelevant texts
            extracted_texts.append(text)
            seen_texts.add(text)

    article_content = "\n\n".join(extracted_texts)
    content_column_data = {"Collection": article_content}

    return content_column_data



# Extracting Categories
def CategoriesExt(soup):
    regex_pattern = r'<span class="m_1e0e6180 mantine-Pill-label">(.*?)</span>'
    raw_extracted_contents = re.findall(regex_pattern, soup)

    extracted_categories = [content.strip() for content in raw_extracted_contents]

    Categories_column_data = {"Categories": extracted_categories}

    return Categories_column_data



# Extracting Author Names
def extract_author_with_regex(soup_content):
    html_string = soup_content

    author_pattern = r'<div[^>]*class="[^"]*mantine-Stack-root[^"]*"[^>]*>.*?<p[^>]*>Author</p>.*?<a[^>]*href="[^"]*authorName=[^"]*"[^>]*>([^<]+)</a>'
    author_pattern_alt = r'<div[^>]*>.*?<p[^>]*>Author</p>.*?<span><a[^>]*href="[^"]*authorName=[^"]*"[^>]*>([^<]+)</a></span>'
    author_pattern_flexible = r'<p[^>]*>Author</p>.*?<a[^>]*href="[^"]*authorName=([^"&]+)"[^>]*>([^<]+)</a>'

    match = re.search(author_pattern, html_string, re.DOTALL | re.IGNORECASE)
    if match:
        extracted_author_name = match.group(1).strip()
        Author_column_data = {"Author": extracted_author_name}
        return Author_column_data

    match = re.search(author_pattern_alt, html_string, re.DOTALL | re.IGNORECASE)
    if match:
        extracted_author_name = match.group(1).strip()
        Author_column_data = {"Author": extracted_author_name}
        return Author_column_data

    match = re.search(author_pattern_flexible, html_string, re.DOTALL | re.IGNORECASE)
    if match:
        extracted_author_name = match.group(2).strip()
        Author_column_data = {"Author": extracted_author_name}
        return Author_column_data


    return ""



# Main Function
def main(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        Title = titlesExt(soup)
        Images = imagesExt(soup)
        Collection =contentExt(soup)


        soup = str(soup)
        Location = locationEXT(soup) #locationExt(soup)
        Author = extract_author_with_regex(soup)  #AuthorName(soup) #Authorname(soup)
        Categories = CategoriesExt(soup)

        return Title,Location,Collection, Author,Categories,Images

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "","","","","",""

# Execution Starts from here
if __name__ == "__main__":
    #url = "https://ruralindiaonline.org/article/my-mother-was-not-a-dayan" #"https://ruralindiaonline.org/article/beyond-disaster-and-wildlife-in-the-sundarbans"
    urls_excel_file = 'Rural_India_articles.xlsx'

    all_articles_dfs = []

    df_urls = pd.read_excel(urls_excel_file)

    for index, row in df_urls.iterrows():
        print(index,end=" ")
        article_url = row[0]

        if article_url:
            title, loc, collection,auth, categ, images  = main(article_url)
            combined_data = {}
            combined_data.update(title)
            combined_data.update(loc)
            combined_data.update(collection)
            combined_data.update({"Story link":article_url})
            combined_data.update(auth)
            combined_data.update(categ)
            combined_data.update(images)
            data_for_df = {key: [value] for key, value in combined_data.items()}

            df = pd.DataFrame(data_for_df)

            if not df.empty:
                all_articles_dfs.append(df)


merged_df = pd.concat(all_articles_dfs, ignore_index=True)
excel_file_name = "Rural_India_Articles_data.xlsx"

merged_df.to_excel(excel_file_name, index=False)