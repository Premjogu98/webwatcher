# from difflib import SequenceMatcher
# from bs4 import BeautifulSoup

# # Example usage:
# OLD_HTML = """<div id="datatable-1_wrapper" class="dataTables_wrapper" role="grid"><div id="datatable-1_length" class="dataTables_length"><label>Show <select size="1" name="datatable-1_length" aria-controls="datatable-1"><option value="10" selected="selected">10</option><option value="25">25</option><option value="50">50</option><option value="100">100</option></select> entries</label></div><div class="dataTables_filter" id="datatable-1_filter"><label>Search: <input type="text" aria-controls="datatable-1"></label></div><table class="table table-bordered table-striped admin-custom-table sticky-enabled datatables-processed dataTable" id="datatable-1" aria-describedby="datatable-1_info"> <thead><tr role="row"><th class="sorting_asc" role="columnheader" tabindex="0" aria-controls="datatable-1" rowspan="1" colspan="1" aria-sort="ascending" aria-label="Sl.No: activate to sort column descending" style="width: 41px;">Sl.No</th><th class="sorting" role="columnheader" tabindex="0" aria-controls="datatable-1" rowspan="1" colspan="1" aria-label="Start Date: activate to sort column ascending" style="width: 91px;">Start Date</th><th class="sorting" role="columnheader" tabindex="0" aria-controls="datatable-1" rowspan="1" colspan="1" aria-label="End Date: activate to sort column ascending" style="width: 91px;">End Date</th><th style="width: 682px;" class="sorting" role="columnheader" tabindex="0" aria-controls="datatable-1" rowspan="1" colspan="1" aria-label="Description: activate to sort column ascending">Description</th><th class="sorting" role="columnheader" tabindex="0" aria-controls="datatable-1" rowspan="1" colspan="1" aria-label="View &amp;amp; Download: activate to sort column ascending" style="width: 144px;">View &amp; Download</th></tr></thead> <tbody role="alert" aria-live="polite" aria-relevant="all"><tr class="odd"><td class=" sorting_1">1</td><td class=" ">31-08-2023</td><td class=" ">22-09-2023</td><td class=" ">Procurement of 80 Denier 75 Denier 34-36 Filaments Highly Intermingled (HIM) Semi Dull Grade-I Texturised Polyester Filament Yarn</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1693564449Tender Notice.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="even"><td class=" sorting_1">2</td><td class=" ">31-07-2023</td><td class=" ">11-08-2023</td><td class=" ">Submission of Price Quotation for the supply of VArious Stationery items</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1690786094Notice for supply of stationery items.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="odd"><td class=" sorting_1">3</td><td class=" ">19-05-2023</td><td class=" ">26-05-2023</td><td class=" ">Security audit of product matrix software hosted in WB-SDC -- extended for 7 days.</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1684992876Dir20230525_0076.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="even"><td class=" sorting_1">4</td><td class=" ">12-05-2023</td><td class=" ">19-05-2023</td><td class=" ">Security audit of product matrix software hosted in WB-SDC</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1684231816Final PDF NIQ AND SCOPE.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="odd"><td class=" sorting_1">5</td><td class=" ">20-04-2023</td><td class=" ">02-05-2023</td><td class=" ">ADVERTISEMENT FOR WALK-IN-INTERVIEW FOR THE POST OF HEAD OF STATE LEVEL PMU</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1682006744WBBCCS_PMU_Notice for Walk in interview.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="even"><td class=" sorting_1">6</td><td class=" ">31-01-2023</td><td class=" ">09-02-2023</td><td class=" ">Setting up Textile and Apparel manufacturing units in West Bengal</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1675165128Date_Corrigendum - Textiles.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="odd"><td class=" sorting_1">7</td><td class=" ">20-01-2023</td><td class=" ">24-02-2023</td><td class=" ">RFP for setting up Textile &amp; Apparel Manufacturing units in West Bengal -- RAIGANJ Drawing</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1674281258Raiganj (1).pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="even"><td class=" sorting_1">8</td><td class=" ">20-01-2023</td><td class=" ">24-02-2023</td><td class=" ">RFP for setting up Textile &amp; Apparel Manufacturing units in West Bengal -- KALYANI Drawing</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1674281310Kalyani (1).pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="odd"><td class=" sorting_1">9</td><td class=" ">20-01-2023</td><td class=" ">24-02-2023</td><td class=" ">RFP for setting up Textile &amp; Apparel Manufacturing units in West Bengal -- ASHOKNAGAR Drawing</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1674281369Ashoknagar (1).pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="even"><td class=" sorting_1">10</td><td class=" ">20-01-2023</td><td class=" ">24-02-2023</td><td class=" ">RFP for setting up Textile &amp; Apparel Manufacturing units in West Bengal </td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1674280994RFP307.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr></tbody></table><div class="dataTables_info" id="datatable-1_info">Showing 1 to 10 of 1,457 entries</div><div class="dataTables_paginate paging_two_button" id="datatable-1_paginate"><a class="paginate_disabled_previous" tabindex="0" role="button" id="datatable-1_previous" aria-controls="datatable-1">Previous</a><a class="paginate_enabled_next" tabindex="0" role="button" id="datatable-1_next" aria-controls="datatable-1">Next</a></div></div>"""
# NEW_HTML = """<div id="datatable-sss1_wrapper" class="dataTables_wrapper" role="grid"><div id="datatable-1_length" class="dataTables_length"><label>Shows <select size="1" name="datatable-1_length" aria-controls="datatable-1"><option value="10" selected="selected">10</option><option value="25">25</option><option value="50">50</option><option value="100">100</option></select> entries</label></div><div class="dataTables_filter" id="datatable-1_filter"><label>Search: <input type="text" aria-controls="datatable-1"></label></div><table class="table table-bordered table-striped admin-custom-table sticky-enabled datatables-processed dataTable" id="datatable-1" aria-describedby="datatable-1_info"> <thead><tr role="row"><th class="sorting_asc" role="columnheader" tabindex="0" aria-controls="datatable-1" rowspan="1" colspan="1" aria-sort="ascending" aria-label="Sl.No: activate to sort column descending" style="width: 41px;">Sl.No</th><th class="sorting" role="columnheader" tabindex="0" aria-controls="datatable-1" rowspan="1" colspan="1" aria-label="Start Date: activate to sort column ascending" style="width: 91px;">Start Date</th><th class="sorting" role="columnheader" tabindex="0" aria-controls="datatable-1" rowspan="1" colspan="1" aria-label="End Date: activate to sort column ascending" style="width: 91px;">End Date</th><th style="width: 682px;" class="sorting" role="columnheader" tabindex="0" aria-controls="datatable-1" rowspan="1" colspan="1" aria-label="Description: activate to sort column ascending">Description</th><th class="sorting" role="columnheader" tabindex="0" aria-controls="datatable-1" rowspan="1" colspan="1" aria-label="View &amp;amp; Download: activate to sort column ascending" style="width: 144px;">View &amp; Download</th></tr></thead> <tbody role="alert" aria-live="polite" aria-relevant="all"><tr class="odd"><td class=" sorting_1">1</td><td class=" ">31-08-2023</td><td class=" ">22-09-2023</td><td class=" ">Procurement of 80 Denier 75 Denier 34-36 Filaments Highly Intermingled (HIM) Semi Dull Grade-I Texturised Polyester Filament Yarn</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1693564449Tender Notice.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="even"><td class=" sorting_1">2</td><td class=" ">31-07-2023</td><td class=" ">11-08-2023</td><td class=" ">Submission of Price Quotation for the supply of VArious Stationery items</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1690786094Notice for supply of stationery items.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="odd"><td class=" sorting_1">3</td><td class=" ">19-05-2023</td><td class=" ">26-05-2023</td><td class=" ">Security audit of product matrix software hosted in WB-SDC -- extended for 7 days.</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1684992876Dir20230525_0076.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="even"><td class=" sorting_1">4</td><td class=" ">12-05-2023</td><td class=" ">19-05-2023</td><td class=" ">Security audit of product matrix software hosted in WB-SDC</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1684231816Final PDF NIQ AND SCOPE.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="odd"><td class=" sorting_1">5</td><td class=" ">20-04-2023</td><td class=" ">02-05-2023</td><td class=" ">ADVERTISEMENT FOR WALK-IN-INTERVIEW FOR THE POST OF HEAD OF STATE LEVEL PMU</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1682006744WBBCCS_PMU_Notice for Walk in interview.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="even"><td class=" sorting_1">6</td><td class=" ">31-01-2023</td><td class=" ">09-02-2023</td><td class=" ">Setting up Textile and Apparel manufacturing units in West Bengal</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1675165128Date_Corrigendum - Textiles.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="odd"><td class=" sorting_1">7</td><td class=" ">20-01-2023</td><td class=" ">24-02-2023</td><td class=" ">RFP for setting up Textile &amp; Apparel Manufacturing units in West Bengal -- RAIGANJ Drawing</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1674281258Raiganj (1).pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="even"><td class=" sorting_1">8</td><td class=" ">20-01-2023</td><td class=" ">24-02-2023</td><td class=" ">RFP for setting up Textile &amp; Apparel Manufacturing units in West Bengal -- KALYANI Drawing</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1674281310Kalyani (1).pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="odd"><td class=" sorting_1">9</td><td class=" ">20-01-2023</td><td class=" ">24-02-2023</td><td class=" ">RFP for setting up Textile &amp; Apparel Manufacturing units in West Bengal -- ASHOKNAGAR Drawing</td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1674281369Ashoknagar (1).pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr><tr class="even"><td class=" sorting_1">10</td><td class=" ">20-01-2023</td><td class=" ">24-02-2023</td><td class=" ">RFP for setting up Textile &amp; Apparel Manufacturing units in West Bengal </td><td class=" "><a href="http://wbmsme.gov.in/sites/default/files/cms/tenderpdf/1674280994RFP307.pdf" target="_blank"><img src="http://wbmsme.gov.in//sites/all/themes/anonymous/images/view_btm.jpg"></a></td> </tr></tbody></table><div class="dataTables_info" id="datatable-1_info">Showing 1 to 10 of 1,457 entries</div><div class="dataTables_paginate paging_two_button" id="datatable-1_paginate"><a class="paginate_disabled_previous" tabindex="0" role="button" id="datatable-1_previous" aria-controls="datatable-1">Previous</a><a class="paginate_enabled_next" tabindex="0" role="button" id="datatable-1_next" aria-controls="datatable-1">Next</a></div></div>"""  # Your old HTML content

# def extract_inner_text(html_string):
#     soup = BeautifulSoup(html_string, 'html.parser')
#     inner_text = soup.get_text(separator=' ', strip=True)
#     return inner_text

# def calculate_percentage_difference(old_text, new_text):
#     sequence_matcher = SequenceMatcher(None, extract_inner_text(old_text), extract_inner_text(new_text))
#     similarity_ratio = sequence_matcher.ratio()
#     percentage_change = (1 - similarity_ratio) * 100
#     return percentage_change


# percentage_change = calculate_percentage_difference(OLD_HTML, NEW_HTML)
# print(round(percentage_change,2))
# print(f"Percentage of Change: {percentage_change:.2f}%")

# from html_diff import diff

# def calculate_html_percentage_difference(old_html, new_html):
#     # Calculate the difference between the two HTML strings
#     difference = diff(old_html, new_html)

#     # Calculate the length of the changes
#     total_changes = len(difference)
#     total_old = len(old_html)

#     # Calculate the percentage change
#     percentage_change = (total_changes / total_old) * 100

#     return percentage_change


# percentage_change = calculate_html_percentage_difference(OLD_HTML, NEW_HTML)
# print(f"Percentage of Change: {percentage_change:.2f}%")


# import re
# from parsel import Selector

# def extract_inner_text(html_content):
#     selector = Selector(text=html_content)
#     xpath_expression = "//text()"
#     inner_text_list = selector.xpath(xpath_expression).extract()
#     inner_text = ' '.join(inner_text_list).strip()
#     inner_text_cleaned = re.sub(r'[\n\t]+', ' ', inner_text)
#     inner_text_cleaned = re.sub(r'\s+', ' ', inner_text_cleaned)  # Replace multiple spaces with a single space
#     return inner_text_cleaned

# # Example HTML content
# html_content = '''
# <html>
#     <head>
#         <title>Example HTML</title>
#     </head>
#     <body>
#         <h1>Hello, world!</h1>
#         <p>This is an example HTML string.</p>
#     </body>
# </html>
# '''

# cleaned_inner_text = extract_inner_text(html_content)
# print(cleaned_inner_text)


# from parsel import Selector

# def extract_html_elements(html_content, xpath_expression):
#     # Create a Selector object with the HTML content
#     selector = Selector(text=html_content)

#     # Use the provided XPath expression to select specific HTML elements
#     selected_elements = selector.xpath(xpath_expression).extract()
#     joined_html = ' '.join(selected_elements)
#     return joined_html

# # Example HTML content
# html_content = '''
# <html>
#     <body>
#         <div class="container">
#             <h1>Hello, world!</h1>
#             <p>This is a paragraph.</p>
#             <ul>
#                 <li>Item 1</li>
#                 <li>Item 2</li>
#                 <li>Item 3</li>
#             </ul>
#         </div>
#     </body>
# </html>
# '''

# # Example XPath expression to extract specific elements (div with class="container")
# xpath_expr = "//div[@class='container']"

# # Extract HTML elements using XPath
# selected_html_elements = extract_html_elements(html_content, xpath_expr)
# print(selected_html_elements)


# import mysql.connector

# # Establish a connection to MySQL
# connection = mysql.connector.connect(
#     host='your_host',
#     user='your_username',
#     password='your_password',
#     database='your_database',
#     connection_timeout=10  # Set connection timeout (optional)
# )

# # Create a cursor object to execute queries
# cursor = connection.cursor()

# # Set query timeout
# query = "SELECT * FROM your_table"
# cursor.execute(query, params=None, operation_timeout=5)  # Set query timeout to 5 seconds

# # Fetch results
# results = cursor.fetchall()
# for row in results:
#     print(row)

# # Close the cursor and connection
# cursor.close()
# connection.close()


# import cupy as cp
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Sample text data
# text1 = "This is the first text sample."
# text2 = "Here is the second text example."

# # Create a TF-IDF Vectorizer and transform the texts
# vectorizer = TfidfVectorizer()
# tfidf_matrix = vectorizer.fit_transform([text1, text2])

# # Convert the TF-IDF matrix to a Cupy array for GPU computation
# tfidf_matrix_cupy = cp.sparse.csr_matrix(tfidf_matrix.astype(cp.float32))

# # Compute cosine similarity on the GPU
# similarity = cosine_similarity(tfidf_matrix_cupy, dense_output=False)

# print(f"Cosine Similarity Matrix (GPU):\n{similarity}")

# from playwright.sync_api import sync_playwright


# def main():
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         context = browser.new_context()
#         page = context.new_page()

#         # Navigate to different websites
#         websites = ['https://allduniv.ac.in/about-uoa/tender']

#         for website in websites:
#             page.goto(website,wait_until="load")

#             # Wait for a specific timeout (adjust the timeout based on your needs)
#             page.wait_for_timeout(10000)  # Wait for 5 seconds

#             # Extract the HTML content after the page has loaded
#             html_content = page.content()

#             # Process the HTML content as needed
#             print(html_content[:200])  # Print the first 200 characters for illustration

#         # Close the browser
#         browser.close()

# if __name__ == "__main__":
#     main()

# from selenium import webdriver
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-ssl-errors=yes')
# options.add_argument('--ignore-certificate-errors')
# # options.add_argument('--disable-gpu')
# # options.add_argument('--headless')
# # options.add_argument("--window-size=1920,1080")
# driver = webdriver.Remote(
# command_executor='http://localhost:4444/wd/hub',
# options=options
# )
# print(driver)
# driver.get("https://allduniv.ac.in/about-uoa/tender")
# # driver.find_element_by_link_text("Get started free").click()
# driver.close()
# driver.quit()

# import os
# from bs4 import BeautifulSoup


# # Define a function to process HTML files
# def process_html_file(
#     file_path="/home/gts/web-watcher/htmldocs/74223-oldhtmlfile.html",
# ):
#     with open(file_path, "r", encoding="utf-8") as file:
#         html_string = file.read().replace("\n", " ")
#         print(html_string)
#     # Parse HTML with BeautifulSoup
#     soup = BeautifulSoup(html_string, "html.parser")

#     # Find all Blockquote elements
#     blockquote_elements = soup.find_all("blockquote")
#     print(blockquote_elements)
#     # Create a set to keep track of unique text content of Blockquote elements
#     unique_blockquotes = set()

#     # Iterate through Blockquote elements
#     for blockquote in blockquote_elements:
#         # Check if the text content is unique
#         if blockquote.text not in unique_blockquotes:
#             unique_blockquotes.add(blockquote.text)
#         else:
#             # If it's a duplicate, remove the element from the soup
#             blockquote.extract()

#     # Write the modified HTML back to the same file
#     print(soup)
#     # with open(file_path, "w", encoding="utf-8") as file:
#     #     file.write(str(soup))


# process_html_file()
# # Iterate through files in the directory tree
# for root, dirs, files in os.walk("/home/gts/web-watcher", topdown=True):
#     print(dirs)
#     for file in files:
#         file_path = os.path.join(root, file)
#         # Process HTML file if it has a .html extension
#         if "Tender Document-new.html" in file_path:
#             print(file_path)
#             # process_html_file(file_path)
#         break

from playwright.async_api import async_playwright
import asyncio

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, re
from selenium.webdriver.chrome.options import Options
import os


async def playwright_extract_outer_html(url, xpath_expression):
    try:
        async with async_playwright() as playwrigh:
            browser = await playwrigh.chromium.launch(
                channel="chrome",
                handle_sighup=False,
                headless=True,
                chromium_sandbox=False,
            )
            context = await browser.new_context(
                ignore_https_errors=True, bypass_csp=True
            )
            page = await context.new_page()
            # page.set_default_timeout(40000)
            print(url)
            await page.goto(url, timeout=30000)

            # proceed_selector = 'button[onclick*="proceed"]'  # Example selector, adjust based on actual page
            # if await page.is_visible(proceed_selector):
            #     await page.click(proceed_selector)
            # order_sent = page.locator(xpath_expression)
            # await order_sent.wait_for(timeout=5)
            # await page.wait_for_selector(xpath_expression)
            # Query for element using XPath
            element = await page.query_selector(xpath_expression)

            if element:

                # Extract outer HTML using JavaScript evaluation
                outer_html = await page.evaluate(
                    "(element) => element.outerHTML", element
                )
                print("Outer HTML:", outer_html)
            else:
                print("No element found with the given XPath expression.")

            # await browser.close()
    except TimeoutError:
        await browser.close()
    except Exception as e:
        print(e)


def selenium_extract_outer_html(url, xpath_expression):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.page_load_strategy = (
        "eager"  # WebDriver waits until DOMContentLoaded event fire is returned.
    )
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    # Start a Selenium WebDriver session
    chromedriver_path = "/home/gts/web-watcher/chromedriver"
    driver = webdriver.Chrome(chromedriver_path, options=chrome_options)
    try:

        driver.set_page_load_timeout(15)
        driver.get(url)
        # Wait for 5 seconds for the page to load
        time.sleep(5)

        # Find the element by XPath
        for element in driver.find_elements(By.XPATH, '//*[@id="skipCont"]'):
            print(element)
            print(element.get_attribute("outerHTML"))
            element = re.sub(
                "\s\s+",
                " ",
                element.get_attribute("outerHTML")
                .strip()
                .replace("\n", " ")
                .replace("\t", " "),
            )
            print(element)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_expression))
        )

        # Extract outer HTML
        outer_html = element.get_attribute("outerHTML")
        print("Outer HTML:", outer_html)
    except TimeoutException:
        print("TimeoutException")
    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        # Close the WebDriver session
        driver.quit()


# Example usage
url = "http://asdma.gov.in/notice_detail.html"
xpath_expression = "//html[1]/body[1]"

asyncio.run(playwright_extract_outer_html(url, xpath_expression))
# selenium_extract_outer_html(url, xpath_expression)


# import os, re
# from lxml import html
# from bs4 import BeautifulSoup
# import html as _html


## Define a function to process HTML files
# def process_html_file(
#     file_path="/home/gts/web-watcher/Tender Document-new.html",
# ):
#     with open(file_path, "r", encoding="utf-8") as file:
#         html_content = file.read()
#     tree = html.fromstring(html_content)
#     elements = tree.xpath("/html/body/blockquote")[0]
#     element_html = html.tostring(elements, encoding="unicode")
#     soup = BeautifulSoup(element_html, "html.parser")
#     for tag in soup.find_all("blockquote"):
#         tag.unwrap()
#     modified_html = str(soup)
#     inner_text_cleaned = re.sub(r"[\n\t]+", " ", modified_html)
#     inner_text_cleaned = re.sub(r"\s+", " ", modified_html)
#     modified_html = _html.unescape(inner_text_cleaned).strip()
# if (
#     (
#         "</blockquote>" not in modified_html
#         and modified_html.find("</blockquote>") == -1
#     )
#     and (
#         "<blockquote" not in modified_html
#         and modified_html.find("<blockquote") == -1
#     )
# ):
# if not modified_html.endswith("</blockquote>") and not modified_html.startswith(
#     "<blockquote"
# ):
#     print(f" {file_path} => Not found")
# else:
#     print(f" {file_path} => Found")
#     exit()
# print(inner_text_cleaned)
# with open(file_path, "w", encoding="utf-8") as file:
#     file.write(modified_html)
# print(file_path, "=> DONE")


# process_html_file()

# for root, dirs, files in os.walk("/home/gts/web-watcher/htmldocs", topdown=True):
#     # print(len(files))
#     for file in files:
#         file_path = os.path.join(root, file)
#         # Process HTML file if it has a .html extension
#         process_html_file(file_path)
