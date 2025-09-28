class Individual:
    """
    Class of individual.
    An individual is a genome and this class includes all the functions and variables that a genome needs
    """

    def __init__(self,ET,bh,dh,αh,φ,bt,dt,pa,rng):
        """
        Builder
        Put the number of ETs in the genome.
        Then a function will resolve the disparity between active and inactive.
        """
        self.bh = bh
        self.dh = dh
        self.αh = αh
        self.φ = φ
        self.bt = bt
        self.dt = dt
        self.p_a = pa

        self.rates = [0,0,0,0]

        self.ET = 0 # Gi
        self.cptETactive = 0
        self.cptETinactive = 0

        for i in range(ET): # For each ET, choice betwen active or inactive
            self.ET += 1
            self.add_actif_or_inactif_ET(rng)

    def add_actif_or_inactif_ET(self,rng):
        """
        Add an ET active or inactive with the p_a rate.
        """
        if self.cptETactive == 0 and self.cptETinactive == 0: # initialisation. If the genome don't have any ET. 
            n = rng.random()
            if n <= 0.5:
                self.cptETactive += 1
            if n > 0.5:
                self.cptETinactive += 1
        else:
            choice1 = self.cptETactive / self.ET   # add inactif
            choice2 = (self.cptETactive+1) / self.ET # add actif
            if abs(self.p_a - choice1) < abs(self.p_a - choice2):
                self.cptETinactive += 1
            else:
                self.cptETactive += 1

    def delete_actif_or_inactif_ET(self):
        """
        Delete an ET active or inactive with the p_a rate.
        """
        if self.cptETactive == 0: # If the genome don't have active ET.
            self.cptETinactive -= 1
        elif self.cptETinactive == 0: # If the genome don't have inactive ET.
            self.cptETactive -= 1
        else:
            choice1 = self.cptETactive / self.ET   # delete inactif
            choice2 = (self.cptETactive-1) / self.ET # delete active
            if abs(self.p_a - choice1) < abs(self.p_a - choice2):
                self.cptETinactive -= 1
            else:
                self.cptETactive -= 1

    def delete_ET(self):
        self.ET -= 1
        self.delete_actif_or_inactif_ET() # Delete an active or inactive

    def add_ET(self,rng):
        self.ET += 1
        self.add_actif_or_inactif_ET(rng) # Add an active or inactive

    def ET_is_empty(self):
        """
        Function which looks if the genome have an or several ET
        """
        if self.ET == 0:
            return True
        else:
            return False

    def calcul_rates(self,numberOfGenomes):
        """
        Function which gives a rate to each genome with their 4 event rates
        """
        self.rates = [self.bh, self.αh*numberOfGenomes + self.dh + self.φ*self.ET ,self.ET*self.dt, self.bt*self.cptETactive]
