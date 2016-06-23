from fetch_xml import fetch_xml

output = fetch_xml('pubmed', 'whitfield m[author]', 'Count')
print(output)