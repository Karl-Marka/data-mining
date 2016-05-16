import requests
import xml.etree.ElementTree as ET

def main(database, term, retmode, type, tag1 = 'Count', eutils = True, tag2 = None, tag3 = None):
    try:
        if eutils == True:
            urlFirstHalf = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db='
        else:
            urlFirstHalf = 'http://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db='
            tag4 = 'Entrezgene'
        URL = urlFirstHalf + str(database) + '&retmode=' + str(retmode) + '&' + str(type) + '=' + str(term)
        request = requests.get(URL)
        result = request.content
        root = ET.fromstring(result)
        if tag2 == None:
            path = './/' + str(tag1)
        elif tag3 == None:
            path = './/' + str(tag1) + '//' + str(tag2)
        else:
            path = './/' + str(tag4) + '//' + str(tag1) + '//' + str(tag2) + '//' + str(tag3)
        id = root.find(path).text
        return id
    except:
        return 'Not found'

if __name__ == "__main__":
    print(main('gene', 'NM_006291[Nucleotide+Accession]', 'xml', 'term', 'IdList', True, 'Id'))
    print(main('gene', 7127, 'xml', 'id', 'Entrezgene_gene', False, 'Gene-ref', 'Gene-ref_desc'))