# %%
import requests
from bs4 import BeautifulSoup
import json

# %%
def scrap():
    # URL for the TPCODL Website 
    url = 'https://kavach.tpodisha.com/(S(k5jbomhuadjjihxbbzfl4lqj))/Reports/PSDCases?discom=CODL'

    # %%
    # Fetch the data from the website 
    try:
        page = requests.get(url)
    except Exception as e:
        print("Error getting the data", e)

    # %%

    soup = BeautifulSoup(page.text,'html.parser')

    # %%
    # Target the Suraksha Kavach Table
    suraksha_table = soup.find('table',{'id':"MainContent_GV_SurakshaKavach"})

    # %%
    # Check the table content
    if suraksha_table is None:
        pass
    else:
        table_rows = suraksha_table.find_all('tr') # type: ignore
        
        # Each td has a format of id="MainContent_GV_SurakshaKavach_div2_<row number>"
        
        final_block =[]
        heading_block=[]
        # Check if div3 has a value of BCDD-II, BBSR and div4 has a value of CS PUR-2
        for idx,tr in enumerate(table_rows):
            # Get the heading separately in a array
            
            # find all the th
            headings =tr.findAll('th',{"class":"text-nowrap"})
            if headings is not None:
                for heading in headings:
                    heading_block.append(heading.text)
            # print(heading_block)
            
            # print(td)
            td_division_field = tr.find("div")
            
            if td_division_field is not None and "div3" in td_division_field['id']:
                td_gss_field = td_division_field.find_next("div")
                if "BCDD-II, BBSR" in td_division_field.text and "CS PUR-2" in td_gss_field.text:
                    # Get all the field for the TR in the JSON format 
                    all_div = tr.findAll('div')
                    temp_block={}
                    for idx,div in enumerate(all_div):
                        temp_block[heading_block[idx]] = div.text
                    final_block.append(temp_block)
                    
                        
        with open('sample_data.json', 'w', encoding='utf-8') as f:
                json.dump(final_block, f, ensure_ascii=False, indent=4)
        
    print('Operation Complete!')

