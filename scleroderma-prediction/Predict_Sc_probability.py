from pandas import read_csv, concat, DataFrame, Series

gene_exp = read_csv('./datasets/test_noduplicate_scores_top10pc.txt', header = 0, index_col = 0, sep = '\t')
gene_data = read_csv('./datasets/gene_data.txt', header = 0, index_col = 0, sep = '\t')

up = dict()
down = dict()

for i in gene_data.index:
    condition = gene_data.loc[i,'condition']
    value = gene_data.loc[i,'value']
    if condition == 'UP':
        up.update({i : value})
    elif condition == 'DOWN':
        down.update({i : value})

for patient in gene_exp.columns:
    score = 0
    data = gene_exp[patient]
    for gene in data.index:
        if gene in up.keys():
            if data.ix[gene] > up.get(gene):
                score += 1
        elif gene in down.keys():
            if data.ix[gene] < down.get(gene):
                    score += 1
    probability = (score/65)*100
    print(patient,probability)
    
    
