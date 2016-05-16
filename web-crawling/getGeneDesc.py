import fetch_xml_2 as fx
import pandas as pd

name = 'names_matched_10.txt'
def main(file):
    result = []
    for i in file[1]:
        if i != 'nan' :
            query = str(i) + '[Nucleotide+Accession]'
            id = fx.main('gene', query, 'xml', 'term', 'IdList', True, 'Id')
            desc = fx.main('gene', str(id), 'xml', 'id', 'Entrezgene_gene', False, 'Gene-ref', 'Gene-ref_desc')
            result.append(str(desc))
        else:
            desc = 'Not available'
            result.append(str(desc))
    col1 = file[0].tolist()
    col2 = file[1].tolist()
    col4 = file[2].tolist()
    output = pd.DataFrame(data = [col1, col2, result, col4], index = None, columns = None)
    output = output.T
    output.to_csv("gene_descriptions.txt", sep = '\t')

if __name__ == "__main__":
    name = input('Specify the input file path: ')
    file = pd.read_csv(name, sep = '\t', header = None)
    main(file)
