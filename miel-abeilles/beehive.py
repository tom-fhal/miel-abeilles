import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

#les abeilles partent d'une ruche,elles ont on position commune 
class Bee:
    def __init__(self):
        self.genome = []
        self.fitness = 0
        self.bees = []

    #on lit le fichier csv qui contient les coordonnées des fleurs et ensuite on la stocke en array
    def read_csv(self):
        df = pd.read_csv('fleursabeilles.csv')
        df = df.to_numpy()      
        return df
    
    #fonction qui va random l'ordre des déplacements des abeilles dans le tableau de fleurs
    def random_bee(self):
        df = self.read_csv()
        np.random.shuffle(df)
        #chaque déplacement de l'abeille est stocké dans le tableau flowers_visited
        for i in range(len(df)):
            self.genome.append(df[i])
        # Vérifier s'il y a des doublons dans le génome et s'assurer qu'il y a bien 50 fleurs
        if len(set(map(tuple, self.genome))) != len(self.genome) or len(self.genome) != 50:
            self.genome = []
            self.random_bee()
        return self.genome
    
    #fonction qui va calculer la distance en soustrayant pour chaque x le prochain x et pour chaque y le prochain y et ensuite les additionner au carré
    def distance(self):
        total_distance = 0
        for i in range(len(self.genome)-1):
            x1, y1 = self.genome[i]
            x2, y2 = self.genome[i + 1]
            total_distance += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            self.fitness = total_distance
        return total_distance
    
    #fonction accouplement qui va prendre les 50 meilleures abeilles et les faire se reproduire pour créer une nouvelle génération de 100 abeilles
    def accouplement(self, best_bees):
        nouvelles_abeilles = []
        
        #faire une boucle for qui va parcourir le dataframe des 50 meilleures abeilles
        for i in range(0, len(best_bees), 2):
            bee1 = best_bees.iloc[i]['genome']
            bee2 = best_bees.iloc[i+1]['genome']
            enfant1 = bee1[:2] + bee2[2:]
            baby1 = Bee()
            baby1.genome = enfant1
            enfant2 = bee2[:2] + bee1[2:]
            baby2 = Bee()
            baby2.genome = enfant2
            nouvelles_abeilles.append(baby1)
            nouvelles_abeilles.append(baby2)
        if not any(np.array_equal(child.genome, baby1.genome) for child in nouvelles_abeilles):
            nouvelles_abeilles.append(baby1)
        if not any(np.array_equal(child.genome, baby2.genome) for child in nouvelles_abeilles):
            nouvelles_abeilles.append(baby2)
        return nouvelles_abeilles
    
    def mutate(self, depth=0, max_depth=100):
        if depth >= max_depth:
            return self.genome
        # Choisir deux positions aléatoires dans la séquence de déplacements aléatoires
        i, j = np.random.choice(len(self.genome), size=2, replace=False)
        # Échanger les positions
        self.genome[i], self.genome[j] = self.genome[j], self.genome[i]
        # Vérifier s'il y a des doublons dans le génome et s'assurer qu'il y a bien 50 fleurs
        if len(set(map(tuple, self.genome))) != len(self.genome) or len(self.genome) != 50:
            self.mutate(depth=depth+1, max_depth=max_depth)
        return self.genome

    
    def generate_bees(self):
        self.bees = [Bee() for _ in range(100)]
        genomes = [bee.random_bee() for bee in self.bees]
        return self.bees, genomes
    
    def run_algorithm(self):  
        df = pd.DataFrame(columns=['Fitness'])
        #ajouter les données de chaque abeille dans le dataframe
        #créer une boucle qui répète ce processus 5 fois
        average_fitness_scores = []
        self.bees, genomes = self.generate_bees()

        for generation in range(50):
            #genomes = [bee.random_bee() for bee in bees]
            if generation % 30 == 0:
                for i in range(10):
                    index = np.random.randint(0, len(self.bees))
                    self.bees[index].mutate()
            fitness_scores = [bee.distance() for bee in self.bees]
            avg = df['Fitness'].mean()

            average_fitness_scores.append(avg)
            
            df = pd.DataFrame({'Fitness': fitness_scores, 'genome': genomes})
            best_bees = df.sort_values(by='Fitness').head(50)
            df.drop(df.tail(50).index, inplace=True)        

            children = Bee().accouplement(best_bees)
            child_genomes = [bee.genome for bee in children]
            child_fitness_scores = [bee.distance() for bee in children]
            child_df = pd.DataFrame({'Fitness': child_fitness_scores, 'genome': [bee.genome for bee in children]})
            child_df = child_df.sort_values(by='Fitness').head(50)

            # Ajouter les nouvelles abeilles au dataframe
            df = pd.concat([best_bees, child_df])
            df = df.sort_values(by='Fitness')
            genomes = [bee.genome for bee in children] + list(best_bees['genome']) 
            for i in range(50):
                self.bees[i].genome = genomes[i]      # Sélectionner les 50 premières lignes

        plt.plot(range(50), average_fitness_scores)
        plt.xlabel('Génération')
        plt.ylabel('Score de fitness moyen')
        plt.show()
        print("Le meilleur chemin est : ", df['genome'].iloc[0])

generate_bees, run_algorithm = Bee().generate_bees(), Bee().run_algorithm()