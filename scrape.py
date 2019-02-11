import csv
import re
import sys
import urllib.request
from bs4 import BeautifulSoup
"""
    Scrapes pokemon statistics from PokemonDB

    Notes: 
    - Working output but can still be simplified/improved
    - URL handling is problematic
    - Add try and except where applicable
"""
def get_page(url):
    "Retrieve the page response parsed by BeautifulSoup"
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}
    request=urllib.request.Request(url,None,headers)
    page_response = BeautifulSoup(urllib.request.urlopen(request), 'html.parser')
    return page_response

def process_htmltable_data(page):
    "Process the raw page response data into a workable list"
    table = page.find_all('tr')
    data_list = []
    for row in table:
        column = row.find_all('td')
        processed_row = []
        for entry in column:
            entry_text = entry.getText().replace('\n','')
            processed_row.append(entry_text)
        data_list.append(processed_row)
    return data_list

def get_pokemondata(url, output_file):
    "Writes the pokemon statistic"
    raw_page_data = get_page(url)
    pokemon_data = process_htmltable_data(raw_page_data)

    with open(output_file, 'w') as out:
        filewriter = csv.writer(out)
        filewriter.writerows(pokemon_data)

    out.close()

def get_filename(arguments):
    "Check if proper script usage and returns filename for output"
    if (len(arguments) == 1):
        sys.exit('         ERROR: Not enough command line arguments. \n \
        Usage: python scrape.py <output-filename>.csv')
    else:
        return arguments[1]

if __name__ == '__main__':
    url = "https://pokemondb.net/pokedex/all"
    filename = get_filename(sys.argv)
    get_pokemondata(url, filename)

