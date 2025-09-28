import numpy as np
from math import log

from elements_transposables.verbose_mode import *
from elements_transposables.individual import *
from elements_transposables.file_csv import *

def calcul_rates_genome(listGenome,randomGenome,numberOfGenomes,optimization):
    """
    Call function to calculate the rate of each genome, and to get the total rate
    """
    if optimization == False:
        for G in listGenome:
            G.calcul_rates(numberOfGenomes)
    else:
        listGenome[randomGenome].calcul_rates(numberOfGenomes)

def random_choice(rng,listGenome):
    """
    Function which choice a random genome and evenement
    """
    genome = 0
    finish = False

    ratesSum = 0
    genomeAndEvenmentResearch = 0

    for G in listGenome:
        ratesSum += sum(G.rates)

    randomNumber = rng.random() * ratesSum

    for G in listGenome:
        evenment = 0
        for rate in G.rates:
            genomeAndEvenmentResearch += rate
            if genomeAndEvenmentResearch > randomNumber:
                finish = True
                break
            evenment += 1
        if finish == True:
            break
        genome += 1

    return genome, evenment, ratesSum # Genome, evenement

def executed_genome_initialization(distribution,p_a,initPop,initTe,s,bh,dh,αh,φ,bt,dt,rng):
    """
    Function which execut the genome initialisation.
    The 'distribution' parameter is a boolean variable for knowing if there is use distribution.
    The 's' paramater is an array with the TE numbers, if there is a distribution which is choice.
    """
    listGenome = []

    if distribution == False:
        for i in range(initPop):
            genome = Individual(initTe,bh,dh,αh,φ,bt,dt,p_a,rng)
            listGenome.append(genome)
    else:
        for i in s:
            genome = Individual(int(i),bh,dh,αh,φ,bt,dt,p_a,rng)
            listGenome.append(genome)

    return listGenome

def init_list_genome(p_a,initPop,initTe,bh,dh,αh,φ,bt,dt,rng): # Prendre en parametre liste avec Gi et i
    """
    Function which initializes a list of individuals (of genomes), with their number of ETs
    """
    return executed_genome_initialization(False,p_a,initPop,initTe,0,bh,dh,αh,φ,bt,dt,rng)

def init_list_genome_from_a_Poisson_distribution(p_a,initPop,initTe,rng,bh,dh,αh,φ,bt,dt):
    """
    Function which initializes a list of individuals (of genomes), with their number of ETs
    From a Poisson distribution
    """
    s = rng.poisson(initTe,initPop)
    return executed_genome_initialization(True,p_a,initPop,initTe,s,bh,dh,αh,φ,bt,dt,rng)

def init_list_genome_from_a_Gamma_distribution(p_a,initPop,initTe,rng,bh,dh,αh,φ,bt,dt):
    """
    Function which initializes a list of individuals (of genomes), with their number of ETs
    From a Gamma distribution
    """
    shape, scale = initTe, initPop # mean and width
    s = np.ceil(rng.gamma(shape = shape, scale = 1, size = initPop))
    return executed_genome_initialization(True,p_a,initPop,initTe,s,bh,dh,αh,φ,bt,dt,rng)

def init_list_genome_from_a_Negative_Binomial_distribution(p_a,initPop,initTe,rng,bh,dh,αh,φ,bt,dt):
    """
    Function which initializes a list of individuals (of genomes), with their number of ETs
    From a Negative_Binomial distribution
    """
    s = rng.negative_binomial(initTe, 0.55, initPop)
    return executed_genome_initialization(True,p_a,initPop,initTe,s,bh,dh,αh,φ,bt,dt,rng)

def new_population(listGenome, randomGenome, randomEvenement, rng):
    """
    Function which modify the genomes population or the ETs numbers.
    """
    if randomEvenement == 0: # Genome clone
        genomeClone = Individual(listGenome[randomGenome].ET,listGenome[randomGenome].bh,listGenome[randomGenome].dh,listGenome[randomGenome].αh,listGenome[randomGenome].φ,listGenome[randomGenome].bt,listGenome[randomGenome].dt,listGenome[randomGenome].p_a,rng)
        listGenome.append(genomeClone)
        optimization = False

    elif randomEvenement == 1: # Genome death
        del listGenome[randomGenome]
        optimization = False

    elif randomEvenement == 2: # Losing an ET
        if listGenome[randomGenome].ET_is_empty() == False:
            listGenome[randomGenome].delete_ET()
            optimization = True

    elif randomEvenement == 3: # Win an ET
        if listGenome[randomGenome].ET_is_empty() == False:
            listGenome[randomGenome].add_ET(rng)
            optimization = True

    else:
        print("ERROR: calculation new popualtion impossible")
        sys.exit()

    return optimization

def new_time(time,rng,ratesSum):
    """
    Function to have the new time
    """
    r1 = rng.random()
    dt = (1/ratesSum)*(log(1/r1))
    return time + dt

def simulation(duration,paramSeed,p_a,nameFile,initPop,initTe,initSim,bh,dh,αh,φ,bt,dt,verbose):
    """
    Function which is called to start the simulation
    """
    time = 0.0
    iteration = 0
    randomGenome = 0
    optimization = False

    rng = np.random.default_rng(seed=paramSeed) # Random generator with a seed

    # Initialize the genome list with the rate of p_a

    if initSim == 0:
        listGenome = init_list_genome(p_a,initPop,initTe,bh,dh,αh,φ,bt,dt,rng)

    elif initSim > 0 and initSim < 4:
        listGenome = init_list_genome_from_a_Gamma_distribution(p_a,initPop,initTe,rng,bh,dh,αh,φ,bt,dt)

    elif initSim >= 4 and initSim < 7:
        listGenome = init_list_genome_from_a_Poisson_distribution(p_a,initPop,initTe,rng,bh,dh,αh,φ,bt,dt)

    else:
        print("Initialization value unknow")
        sys.exit()

    #listGenome = init_list_genome_from_a_Negative_Binomial_distribution(p_a,initPop,initTe,rng)

    csvfile = init_print_csv_file(nameFile) # To have a file descriptor.

    while time < duration and len(listGenome) > 0:

        if iteration % 10000 == 0:
            print_csv_file(csvfile,time,listGenome,iteration) # Print the genome list in the .csv file

        numberOfGenomes = len(listGenome)

        calcul_rates_genome(listGenome,randomGenome,numberOfGenomes,optimization) # Rates calcul
        randomGenome,randomEvenement, ratesSum = random_choice(rng,listGenome) # Choice an evenment and genome
        time = new_time(time,rng,ratesSum) # New time
        optimization = new_population(listGenome,randomGenome,randomEvenement,rng) # Application of the evenment

        iteration += 1

        if verbose == 1:
            #verbose(time,duration,randomGenome,randomEvenement,numberOfGenomes,iteration)
            print_progress_bar(time, duration, prefix = 'Progress ----- :', suffix = 'Complete', length = 50)

    csvfile.close()
