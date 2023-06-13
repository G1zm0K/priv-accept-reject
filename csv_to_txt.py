import csv

domains = []

with open('websites/tranco_lists/tranco_992J2.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        domain = row[1]
        if domain.endswith('.ie'):
            domains.append('https://www.' + domain)

# Write the domains list to a text file
with open('websites/tranco_IE_5000.txt', 'w') as txt_file:
    for domain in domains:
        txt_file.write(domain + '\n')
