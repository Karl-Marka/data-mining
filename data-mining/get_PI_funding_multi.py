
def getFunding(DataFrame, db, names, threadNum):
    text = 'Started thread nr. ' + str(threadNum)
    print(text)
    funding = dict()
    for name in names:
        values = []
        totalCost = 0
        noProjects = 0
        for n,i in enumerate(db['PI_NAMEs']):
            if name in str(i):
                noProjects += 1
                if (db['TOTAL_COST'].iloc[n]) > 0:
                    totalCost += int(db['TOTAL_COST'].iloc[n])
        values.append(noProjects)
        values.append(totalCost)
        funding.update({name: values})
    print(len(funding))
    output = DataFrame.from_dict(data = funding, orient = 'index')
    filename = 'NIH_funding_' + str(threadNum) + '.txt'
    output.to_csv(filename, sep = '\t')


            