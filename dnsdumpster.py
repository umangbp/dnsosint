
import requests

from columnar import columnar
from click import style
from bs4 import BeautifulSoup

from colors import CTitle,CEND,CSubTitle

DOMAIN_DNSDUMPSTER = "https://dnsdumpster.com/"
DNSDUMPSTER_CSRF = ""

DUMPSTER_DNS_SERVERS = []
DUMPSTER_MX_SERVERS = []
DUMPSTER_HOSTS = []

def parseDnsServers(dns_servers_table_rows):
    
    # iterating over each row of table and getting cells
    for row in dns_servers_table_rows:

        dns_server = []

        # finding all cells from table row
        cells = row.find_all("td")

        #iterating over each cell of row
        for cell in cells:
            
            # removing all child nodes from cell
            for child in cell.findChildren():
                child.decompose()

            # appending cell values to dns_server list
            dns_server.append(cell.get_text(' | ',strip=True))

        DUMPSTER_DNS_SERVERS.append(dns_server)

    if not len(DUMPSTER_DNS_SERVERS) == 0:

        dns_table = columnar(DUMPSTER_DNS_SERVERS, no_borders=True, min_column_width=2)
        print(dns_table)

    else:
        print("No DNS Server Found")


def parseMxServers(mx_servers_table_rows):

    # iterating over each row of table and getting cells
    for row in mx_servers_table_rows:

        mx_server = []

        # finding all cells from table row
        cells = row.find_all("td")

        #iterating over each cell of row
        for cell in cells:
            
            # removing all child nodes from cell
            for child in cell.findChildren():
                child.decompose()

            # appending cell values to dns_server list
            mx_server.append(cell.get_text(strip=True))


        DUMPSTER_MX_SERVERS.append(mx_server)    
        

    # checking if any mx server found 
    if not len(DUMPSTER_MX_SERVERS) == 0:

        mx_table = columnar(DUMPSTER_MX_SERVERS, no_borders=True, min_column_width=2, row_sep='-')
        print(mx_table)

    else:

        print("No MX Server Found")

# function to parse TXT records
def parseTxtRecords(txt_record_table_rows):

    # iterate on each txt_record_table rows
    for row in txt_record_table_rows:

        # find td element in each tr element of txt_record_table
        column = row.find("td")

        print(column.get_text(strip=True),'\n')

# function for parsing hosts 
def parsHosts(hosts_table_rows):

    # iterating over each row of table and getting cells
    for row in hosts_table_rows:

        host = []

        # finding all cells from table row
        cells = row.find_all("td")

        #iterating over each cell of row
        for cell in cells:
            
            # removing all child nodes from cell
            for child in cell.findChildren():
                child.decompose()

            # appending cell values to dns_server list
            host.append(cell.get_text(' | ',strip=True))

        DUMPSTER_HOSTS.append(host)

    if not len(DUMPSTER_HOSTS) == 0:

        dns_table = columnar(DUMPSTER_HOSTS, no_borders=True, min_column_width=2)
        print(dns_table)

    else:
        print("No Host Found")

# function parse html from DNSDumpster
def parseDnsDumpster(html_text):
    
    # parsing html
    parser = BeautifulSoup(html_text, 'html.parser')

    print(CSubTitle + "DNS Servers" + CEND)
    print("------------------------------------------------------------------------------\n")
    
    # getting html block where DNS servers are listed using 'Table' tag
    dns_server_block = parser.find("a", {"name":"dnsanchor"})
    
    if dns_server_block != None:

        dns_server_block = dns_server_block.find_next()
        
        if dns_server_block != None:
            
            dns_servers_table_rows = dns_server_block.find('table')

            if dns_servers_table_rows != None:
                
                dns_servers_table_rows = dns_servers_table_rows.find_all('tr')
                parseDnsServers(dns_servers_table_rows)
            
            else:

                print("No DNS Server Found")    

        else:

            print("No DNS Server Found")

    else:

        print("No DNS Server Found")
    

    print(CSubTitle + "\n\nMX Servers" + CEND)
    print("------------------------------------------------------------------------------\n")

    mx_server_block = parser.find("a", {"name":"mxanchor"}).parent
    
    # if tag with name=mxanchor exist in the html
    if mx_server_block != None:

        #find next div element
        mx_server_block = mx_server_block.find_next("div")
        
        # if div element exists
        if mx_server_block != None:
            
            # find table in the div element
            mx_servers_table_rows = mx_server_block.find('table')

            # if table exists
            if mx_servers_table_rows != None:
                
                mx_servers_table_rows = mx_servers_table_rows.find_all('tr')
                parseMxServers(mx_servers_table_rows)
            
            else:
                print("No MX Server Found")    

        else:
            print("No MX Server Found")

    else:
        print("No MX Server Found")


    print(CSubTitle + "\n\nTXT Records" + CEND)
    print("------------------------------------------------------------------------------\n")

    txt_record_block = parser.find("a", {"name":"txtanchor"})

    if txt_record_block != None:
        
        txt_record_block = txt_record_block.find_next("div")

        if txt_record_block != None:
            
            txt_record_table = txt_record_block.find("table")

            if txt_record_table != None:
                
                txt_record_table_rows = txt_record_table.find_all('tr')

                if txt_record_table_rows != None and len(txt_record_table_rows) > 0:

                    parseTxtRecords(txt_record_table_rows)

                else:
                    print("No TXT Record Found")

            else:
                print("No TXT Record Found")

        else:
            print("No TXT Record Found")

    else:
        print("No TXT Record Found")


    print("\n\nHost (A) Records")
    print("------------------------------------------------------------------------------\n")
    
    hosts_block = parser.find("a", {"name":"hostanchor"}).parent

    if hosts_block != None:

        #find next div element
        hosts_block = hosts_block.find_next("div")
        
        # if div element exists
        if hosts_block != None:
            
            # find table in the div element
            hosts_table_rows = hosts_block.find('table')

            # if table exists
            if hosts_table_rows != None:
                
                hosts_table_rows = hosts_table_rows.find_all('tr')
                parsHosts(hosts_table_rows)
            
            else:
                print("No Host Found")    

        else:
            print("No Host Found")

    else:
        print("No Host Found")

#function to get dnsDumpster html
def getDnsDumpster(domain):

    print(CTitle + "[*] Gathering Information From DNSDumpster\n\n"+ CEND)

    # making GET requests to dnsdumpster website
    dnsdumpster_req_get = requests.get(DOMAIN_DNSDUMPSTER)
    
    # reading response cookies
    cookies = dnsdumpster_req_get.cookies.get_dict()

    # read csrf token from cookies dictionary
    DNSDUMPSTER_CSRF = cookies['csrftoken']


    payload = {
        'csrfmiddlewaretoken': DNSDUMPSTER_CSRF,
        'targetip': domain
    }

   
    headers = {
        'Referer': 'https://dnsdumpster.com/',
        'Cookie': 'csrftoken='+DNSDUMPSTER_CSRF
    }

    dnsdumpster_response_post = requests.request("POST", DOMAIN_DNSDUMPSTER, headers=headers, data = payload)
    
    if dnsdumpster_response_post.status_code==200:
        
        parseDnsDumpster(dnsdumpster_response_post.text) 

    else:
        print("Can't reach www.dnsdumpster.com at the moment")
        exit()
    #soup = BeautifulSoup(dnsDumpster_req.text, 'html.parser')