import csv

def init_print_csv_file(nameFile):
    """
    Function which create a file descriptor.
    """
    csvfile = open(nameFile, 'w', newline='')
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['iteration', 'timer', 'id', 'active_te', 'silent_te'] )
    return csvfile

def print_csv_file(csvfile,times,listGenome,iteration):
    """
    Function which save the genomes datas 
    """
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
    id = 0
    for genome in listGenome:
        spamwriter.writerow([iteration, times, id, genome.cptETactive, genome.cptETinactive])
        id += 1