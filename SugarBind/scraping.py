import time
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import sys

link_header = 'https://sugarbind.expasy.org'
def agent_list():
    print("GET: agents")
    target_link = link_header + '/agents?n=407'
    file = open('data/agent_list.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(['Agent ID', 'Agent Name', 'Agent Type', 'taxonomy ID', 'taxonomy level', 'Lineage', 'Agent properties', 'HAMAP', 'Viralzone', 'Viralzone Link', 'GOLD'])
    list_html = requests.get(target_link)
    list_soup = BeautifulSoup(list_html.content, "html.parser")
    list_elements = list_soup.find('tbody').find_all('tr')
    for element in list_elements:
        name = element.find_all('td')[0].find('a')
        agent_id = name.get('href')[8:]
        agent_type_link = element.find_all('td')[2].find('a')
        agent_type = element.find_all('td')[2].find('a').get_text()
        taxonomy_id_link = element.find_all('td')[3].find('a')
        taxonomy_id = element.find_all('td')[3].find('a').get_text()
        num_asterisk = taxonomy_id.count('*')
        taxonomy_id = taxonomy_id.replace('*', '')

        element_html = requests.get(link_header + name.get('href'))
        element_soup = BeautifulSoup(element_html.content, "html.parser")
        info = element_soup.find_all('div', class_='info')
        if len(info) == 10:
        # 10 count
            # 0: References
            # 1: Glycan Structure Format
            # 2: Lineage・Type
            # 3: Agent properties
            # 4: HAMAP proteome
            # 5: Viralzone
            # 6: GOLD
            # 7: Ligands
            # 8: Biological Associations
            # 9: Diseases
            lineage = info[2].find_all('p')[0].find_all('a') if info[2].find_all('p')[0].find_all('a') else None
            agent_properties = info[3].find_all('p') if info[3].find_all('p') else None
            hamap = info[4].find('p').get_text() if info[4].find('p') else None
            viralzone = info[5].find('p').get_text() if info[5].find('p') else None
            if viralzone:
                # print(info[5].find('p').find('a'))
                viralzone_link = info[5].find('p').find('a').get('href')

            else:
                viralzone_link = None
            gold = info[6].find_all('p') if info[6].find_all('p') else None
            writer.writerow([agent_id, name.get_text(), agent_type, taxonomy_id, num_asterisk, lineage, agent_properties, hamap, viralzone, viralzone_link, gold])
        elif len(info) == 9:
        # 9 count
            # 0: References
            # 1: Glycan Structure Format
            # 2: Lineage・Type
            # 3: Agent properties
            # 4: HAMAP proteome
            # 5: GOLD
            # 6: Ligands
            # 7: Biological Associations
            # 8: Diseases
            lineage = info[2].find_all('p')[0].find_all('a') if info[2].find_all('p')[0].find_all('a') else None
            agent_properties = info[3].find_all('p') if info[3].find_all('p') else None
            hamap = info[4].find('p').get_text() if info[4].find('p') else None
            viralzone = None
            viralzone_link = None
            gold = info[5].find_all('p') if info[5].find_all('p') else None
            writer.writerow([agent_id, name.get_text(), agent_type, taxonomy_id, num_asterisk, lineage, agent_properties, hamap, viralzone, viralzone_link, gold])
        time.sleep(0.75)
    file.close()

def lectin_list():
    print("GET: lections")
    target_link = link_header + '/lectins?n=739'                                                                            # set scraping target link
    file = open('data/lectin_list.csv', 'w')                                                                               # open file named "lectin_list.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Lectin ID', 'Lectin name','Lectin link','Uniprot ID', 'Uniprot link', 'N/S'])                         # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find_all 'tr' elements from got html content
    for tr in tr_elements:
        a_tag_element = tr.find_all('td')[0].find('a')                                                                      # find a tag element in a tr element
        lectin_id = a_tag_element.get('href')[9:]                                                                             # extracting lectin id
        lectin_name = a_tag_element.get_text()                                                                                # extracting lectin name
        html_of_individual_lectin = requests.get(link_header + a_tag_element.get('href'))                                     # set scraping target link 
        soup_of_individual_lectin = BeautifulSoup(html_of_individual_lectin.content, "html.parser")                         # get html content as Beautiful Soup object
        uniprot = soup_of_individual_lectin.find_all(class_ = 'span4')[0].find_all(class_ = 'info')[2].find('p')            # find all uniprot related information
        if lectin_name == 'N/S':                                                                                # if lectin name is named 'N/S'
            if uniprot:                                                                                                     # if uniprot information is found
                uniprot = uniprot.find('a')
                writer.writerow([lectin_id, lectin_name, link_header + a_tag_element.get('href'),\
                                uniprot.get_text(), uniprot.get('href'), 1])                                                # inserting extracted lectin id, lectin name, lectin link, uniprot id, uniprot link, identifier of N/S
            else:                                                                                                           # if uniprot information is not found
                writer.writerow([lectin_id, lectin_name,\
                                link_header + a_tag_element.get('href'), None,None, 1])                                     # inserting extracted lectin id, lectin name, lectin link, None, None, identifier of N/S
        else:                                                                                                   # if lectin name is named other than 'N/S'
            if uniprot:
                uniprot = uniprot.find('a')
                writer.writerow([lectin_id, lectin_name, link_header + a_tag_element.get('href'),\
                                uniprot.get_text(), uniprot.get('href'), 0])
            else:
                writer.writerow([lectin_id, lectin_name,\
                                link_header + a_tag_element.get('href'), None, None, 0])
        time.sleep(0.5)                                                                                                     # stop processing for avoiding continues request for server
    file.close()                                                                                                            # close file

def disease_list():
    print("GET: diseases")
    target_link = link_header + '/diseases'                                                                                 # set scraping target link
    file = open('data/disease_list.csv', 'w')                                                                              # open file named "disease_list.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Disease ID', 'Disease Name', 'DOID'])                                                                         # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                            # find_all 'tr' elements from got html content
    for tr in tr_elements:
        disease = tr.find_all('td')[0]                                                                                      # find a tag element in a tr element
        disease_link = link_header + disease.find('a').get('href')
        disease_html = requests.get(disease_link)                                                                                        # get html via request
        disease_soup = BeautifulSoup(disease_html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
        disease_id = disease.find('a').get('href')[10:]
        disease_name = disease_soup.find("h1").get_text()
        try:
            disease_doid = disease_soup.find("h4").find("a").get_text()
        except:
            doid = ""
        writer.writerow([disease_id, disease_name, disease_doid])
    file.close()                                                                                                            # close file

def area_list():
    print("GET: area")
    target_link = link_header + '/affectedAreas'                                                                        # set scraping target link
    file = open('data/area_list.csv', 'w')                                                                                 # open file named "area_list.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Affected Area ID', 'Area Name',\
                        'Area Type', 'Host organism'])                                                                                       # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find all 'tr' elements from got html content
    for tr in tr_elements:
        sub_target_link = link_header + tr.find_all('td')[0].find('a').get('href')
        sub_html = requests.get(sub_target_link)
        sub_soup = BeautifulSoup(sub_html.content, "html.parser")
        area_sidebar = sub_soup.find("div", class_="sidebar")
        area_detail = area_sidebar.find_all("div")[1].find_all("p")
        assert area_detail is not None
        area_id = tr.find_all('td')[0].find('a').get('href')[15:]
        area_name = sub_soup.find('h1').get_text()
        try:
            writer.writerow([area_id,
                             area_name,
                             area_detail[1].get_text().replace(" ", ""),
                             area_detail[2].get_text().replace(" ", "")])                                         # inserting extracted area id, area name, and area type index
        except:
            writer.writerow([area_id, area_name, area_detail[1].get_text().replace(" ",""), "-"])                                                           # inserting extracted area id, area name, and area type index


    file.close()                                                                                                            # file close

def lectin_pubmed():
    print("GET: lections")
    file = open('data/lectin_pubmed.csv', 'w')                                                                             # open file named "lectin_pubmed.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Lectin ID', 'Pubmed ID','Pubmed link', 'Pubmed Year', 'Pubmed Authors', 'Pubmed Title'])              # describe header title
    with open('data/lectin_list.csv') as lectin_file:
        reader = csv.reader(lectin_file)                                                                                    # set csv reader
        _ = next(reader)                                                                                                    # pass_header_row
        _html = requests.get('https://sugarbind.expasy.org/references?n=183')
        _soup = BeautifulSoup(_html.content, "html.parser")
        _table_tr = _soup.find('tbody').find_all('tr')
        for row in reader:
            html = requests.get(row[2])                                                                                     # get html via request
            soup = BeautifulSoup(html.content, "html.parser")                                                               # get html content as Beautiful Soup object
            references = soup.find('tbody').find_all('tr')                                                                  # find all 'tr' elements from individual lectin page
            for reference in references:
                if reference.find_all('td')[3].find('a'):
                    pmlink = reference.find_all('td')[3].find('a').get('href')
                    pmid = reference.find_all('td')[3].find('a').get_text()                                                 # if there are any reference
                    pmy = None
                    pma = None
                    pmt = None
                    for tr in _table_tr:
                        if tr.find_all('td')[4] == pmid:
                            pmy = tr.find_all('td')[1]
                            pma = tr.find_all('td')[2]
                            pmt = tr.find_all('td')[0]
                    writer.writerow([row[0], pmid, pmlink, pmy, pma, pmt])                      # inserting extracted lectin id, pubmed id, pubmed link
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close                                                                                                              # file close

def lectin_ligand():
    print("GET: lection ligans")
    file = open('data/lectin_ligand.csv', 'w')                                                                             # open file named "lectin_ligand.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Lectin ID', 'Ligand ID'])                                                                             # describe header title
    with open('data/lectin_list.csv') as lectin_file:
        reader = csv.reader(lectin_file)                                                                                    # set csv reader
        _ = next(reader)                                                                                                    # pass_header_row
        for row in reader:                                                                                                  
            html = requests.get(row[2])                                                                                     # get html via request
            soup = BeautifulSoup(html.content, "html.parser")                                                               # get html content as Beautiful Soup object
            for ligand in soup.find(id = 'more-ligand0ligand').find_all('li'):
                writer.writerow([row[0], ligand.find('a').get('href')[9:]])                                                 # inserting extracted lectin id, ligand id
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def ligand_glycoconjugate():
    print("GET: ligand Glycoconjugate")
    file = open('data/ligand_glycoconjugate.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(['Liogand ID', 'Glycoconjugate URL', 'Glycoconjugate Name'])
    url = 'https://sugarbind.expasy.org/ligands?n=204'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    table = soup.find('tbody')
    trs = table.find_all('tr')
    for tr in trs:
        # print(tr.find_all('td')[1])
        try:
            ligand = tr.find_all('td')[0].find('ul').find_all('li')[0].find('a').get('href')[9:]
            link = tr.find_all('td')[1].find('a').get('href')
            name = tr.find_all('td')[1].find('a').get_text()
            writer.writerow([ligand, link_header + link, name])
        except:
            pass
    file.close()

    

def lectin_agent():
    print("GET: lectin agent")
    file = open('data/lectin_agent.csv', 'w')                                                                              # open file named "lectin_ligand.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Lectin ID', 'Agent ID'])                                                                              # describe header title
    with open('data/lectin_list.csv') as lectin_file:
        reader = csv.reader(lectin_file)                                                                                    # set csv reader
        _ = next(reader)                                                                                                    # pass_header_row
        for row in reader:
            html = requests.get(row[2])                                                                                     # get html via request
            soup = BeautifulSoup(html.content, "html.parser")                                                               # get html content as Beautiful Soup object
            for agent in soup.find(id = 'more-taxonomy0bioassociations').find_all('li'):
                writer.writerow([row[0], agent.find('a').get('href')[8:]])                                                  # inserting extracted lectin id, agent id
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def lectin_area():
    print("GET: lectin area")
    file = open('data/lectin_affect.csv', 'w')                                                                             # open file named "lectin_affect.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Lectin ID', 'Affect ID'])                                                                             # describe header title
    with open('data/lectin_list.csv') as lectin_file:
        reader = csv.reader(lectin_file)                                                                                    # set csv reader
        _ = next(reader)                                                                                                    # pass_header_row
        for row in reader:
            html = requests.get(row[2])                                                                                     # get html via request
            soup = BeautifulSoup(html.content, "html.parser")                                                               # get html content as Beautiful Soup object
            for area in soup.find(id = 'more-source0bioassociations').find_all('li'):
                writer.writerow([row[0], area.find('a').get('href')[15:]])                                                  # inserting extracted lectin id, agent id
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def structure_ligand():
    print("GET: structure ligand")
    target_link = link_header + '/ligands?n=204'                                                                            # set scraping target link
    file = open('data/ligand_names.csv', 'w')                                                                              # open file named "ligand_names.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Ligand ID', 'Ligand name', 'Unnamed'])                                                                # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find all 'tr' elements from got html content
    for tr in tr_elements:
        if tr.find_all('td')[0].find('ul'):                                                                     # if there are more than 1 ligand or not
            for ligand in tr.find('ul').find_all('li'):
                writer.writerow([ligand.find('a').get('href')[9:], ligand.find('a').get_text(), 0])                         # inserting extracted ligand id, ligand name, and identifier wheather 'Unnamed'
        else:
            ligand_id = tr.find('a').get('href')[9:]
            if tr.find('a').get_text() == 'Unnamed':                                                            # if ligand name is named as 'Unnamed' or not
                writer.writerow([ligand_id, tr.find('a').get_text(), 1])                                                    # inserting extracted ligand id, ligand name, and identifier wheather 'Unnamed'
            else:
                writer.writerow([ligand_id, tr.find('a').get_text(), 0])                                                    # inserting extracted ligand id, ligand name, and identifier wheather 'Unnamed'
    file.close()                                                                                                            # file close

    file = open('data/structure_ligand.csv', 'w')                                                                          # open file named "structure_ligand.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Ligand ID', 'Structure ID', 'Structure link', 'Glytoucan ID', 'Glytoucan link'])                      # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find all 'tr' elements from got html content
    for tr in tr_elements:
        ligand_id = tr.find('a').get('href')[9:]                                                                            # extracting ligand id
        structure_link = tr.find_all('td')[4].find('a').get('href')                                                         # extracting structure link
        structure_id = structure_link[12:]                                                                                  # extracting structure id
        if structure_link:                                                                                      # if structure link exist
            structure_html = requests.get('https://sugarbind.expasy.org' + structure_link)                                  # get structure html via request 
            structure_soup = BeautifulSoup(structure_html.content, "html.parser")                                           # get structure html content as Beautiful Soup object
            glytoucan = structure_soup.find_all(class_ = 'info')[2]                                                         # find all 'info' elements, related to glytoucan, from got html content
            if glytoucan.find('a'):
                glytoucan_link = glytoucan.find('a').get('href')                                                                    # extracting glytoucan link
                glytoucan_id = glytoucan.find('a').get_text()                                                                       # extracting glytoucan id
                writer.writerow([ligand_id, structure_id, link_header + structure_link, glytoucan_id, glytoucan_link])      # inserting extracted ligand id, structure id, structure link, glytoucan id, glytoucan link
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def agent_disease():
    print("GET: agent disease")
    target_link = link_header + '/agents?n=407'                                                                             # set scraping target link
    file = open('data/agent_disease.csv', 'w')                                                                             # open file named "agent_disease.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Agent ID','Agent Name','Disease ID','Disease Name'])                                                  # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find all 'tr' elements from got html content
    for row in tr_elements:
        agent = row.find_all('td')[0].find('a')                                                                             # find all 'td, a' elements, related to agent, from got html content
        agent_id = agent.get('href')[8:]                                                                                    # extracting agent id
        agent_name = agent.get_text()                                                                                       # extracting agent name
        agent_html = requests.get(link_header + agent.get('href'))                                                          # get agent html via request
        agent_soup = BeautifulSoup(agent_html.content, "html.parser")                                                       # get agent html content as Beautiful Soup object
        for disease in agent_soup.find(id = 'more-disease0disease').find_all('li'):                                         
            disease_id = disease.find('a').get('href')[10:]                                                                 # extracting disease id
            disease_name = disease.find('a').get_text()                                                                     # extracting disease name
            writer.writerow([agent_id, agent_name, disease_id, disease_name])                                               # inserting extracted agent id, agent name, disease id, and disease name
        time.sleep(0.5)                                                                                                     # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def area_disease():
    print("GET: area disease")
    target_link = link_header + '/affectedAreaTypes'                                                                        # set scraping target link
    file = open('data/area_disease.csv', 'w')                                                                              # open file named "area_disease.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Affected Area ID', 'Affected Area Name', 'Disease ID', 'Disease Name'])                               # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find all 'tr' elements from got html content
    for row in tr_elements:
        for area in row.find_all('td')[1].find('ul').find_all('li'):
            area_id = area.find('a').get('href')[15:]                                                                       # extracting area id
            area_name = area.find('a').get_text()                                                                           # extracting area name
            area_html = requests.get(link_header + area.find('a').get('href'))                                              # get area html via request
            area_soup = BeautifulSoup(area_html.content, "html.parser")                                                     # get area html content as Beautiful Soup object
            for disease in area_soup.find( id = "more-disease0disease").find_all('li'):
                disease_id = disease.find('a').get('href')[10:]                                                             # extracting disease id
                disease_name = disease.find('a').get_text()                                                                 # extracting disease name
                writer.writerow([area_id, area_name, disease_id, disease_name])                                             # inserting extracted area id, area name, disease id, and disease name
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def agent_area():
    target_link = link_header + '/affectedAreaTypes'                                                                        # set scraping target link
    file = open('data/agent_affected_area.csv', 'w')                                                                       # open file named "agent_affected_area.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Agent ID', 'Agent Name', 'Affected Area ID', 'Affected Area Name', 'Area Type'])                      # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                          # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                            # find all 'tr' elements from got html content

    index = 1                                                                                                               # set area type identifier
    for row in tr_elements:
        for agent in row.find_all('td')[2].find('ul').find_all('li'):
            agent_a = agent.find('a')                                                                                       # extracting agent a tag element
            agent_html = requests.get(link_header + agent_a.get('href'))                                                    # get agent html via request
            agent_soup = BeautifulSoup(agent_html.content, "html.parser")                                                   # get agent html content as Beautiful Soup object
            for agent_area in agent_soup.find(id = 'more-source0bioassociations').find_all('li'):
                area_id = agent_area.find('a').get('href')[15:]                                                             # extracting area id
                area_name = agent_area.find('a').get_text()                                                                 # extracting area name
                writer.writerow([agent_a.get('href')[8:], agent_a.get_text(), area_id, area_name, index])                   # inserting extracted agent id, agent name, area id, area name, and type identifier
            time.sleep(0.5)                                                                                                 # stop precessing for avoiding continues request for server
            index += 1                                                                                                      # incrementing identifier
    file.close()                                                                                                            # file close


if __name__ == "__main__":
    ### scraping from sugarbind ( https://sugarbind.expasy.org )
    agent_list()
    # creating agent_list.csv
    lectin_list()
    # creating lectin_list.csv
    disease_list()
    # creating disease_list.csv
    area_list()
    # creating area_list.csv
    lectin_pubmed()
    # creating lectin_pubmed.csv
    lectin_ligand()
    # creating lectin_ligand.csv
    structure_ligand()
    # creating ligand_names.csv, structure_ligand
    area_disease()
    # creating area_disease.csv
    agent_area()
    # creating agent_affected_area.csv
    agent_disease()
    # creating agent_disease.csv
    lectin_area()
    # creating lectin_area.csv
    lectin_agent()
    # creating lectin_agent.csv
