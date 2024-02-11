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

from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')
# options.add_argument("--window-size=1920,1080")
driver = webdriver.Remote(
command_executor='http://localhost:4444/wd/hub',
options=options
)
print(driver)
driver.get("https://allduniv.ac.in/about-uoa/tender")
# driver.find_element_by_link_text("Get started free").click()
driver.close()
driver.quit()