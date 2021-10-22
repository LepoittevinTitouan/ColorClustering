from PIL.Image import init
import utils
import numpy as np

class DBScan():
    def __init__(self, eps, minPts, euclidienne):
        self.eps = eps
        self.minPts = minPts
        self.euclidienne = euclidienne

    def fit(self, data):
        self.core = {}
        cluster = 0

        data = [item for sublist in data for item in sublist]
        self.markedData = [[x, False, None] for x in data]

        # On parcours les points non marqués pour chercher leurs voisins
        for x in self.markedData :
            if not x[1] :
                x[1] = True
                neighborPts = self.getNeighbors(x[0])
                print("voisins de " + str(x) + " : " + str(len(neighborPts)))

                # Si le point a plus de minPts voisins, c'est un point "core" qui forme un cluster
                if len(neighborPts) >= self.minPts :
                    x[2] = cluster
                    print("New Cluster n°" + str(cluster) + " !\n")
                    self.expandCluster(x, cluster, neighborPts)
                    cluster += 1

        self.coreCentroids = {}
        for cluster in self.core :
            colors = [x[0] for x in self.core[cluster]]
            self.coreCentroids[cluster] = np.average(colors,axis=0)
            self.coreCentroids[cluster].tolist()
            self.coreCentroids[cluster] = [int(i) for i in self.coreCentroids[cluster]]


    def expandCluster(self, core, cluster, initNeighbor):
        self.core[cluster] = []
        self.core[cluster].append(core)
        for p in self.markedData :
            if p in initNeighbor :
                # Si on a jamais testé les voisins de ce points, on les cherche
                if not p[1] :
                    p[1] = True
                    neighborPts = self.getNeighbors(p[0])

                    # print("voisins de " + str(p) + " : " + str(len(neighborPts)))

                    # Si la taille du voisinage est supérieur à la limite, c'est un "core" et on ajoute son voisinage a la file
                    if len(neighborPts) >= self.minPts :
                        for v in neighborPts :
                            if v not in initNeighbor :
                                initNeighbor.append(v)
                        # print("Taille du voisinage : " + str(len(initNeighbor)))
                        # initNeighbor.extend(neighborPts)

                # Si le point a déjà été testé mais n'est pas attribué a un cluster, on l'ajoute simplement au cluster actuel
                if p[2] == None :
                    self.core[cluster].append(p)
                    p[2] = cluster

        print("Taille du cluster " + str(cluster) + " : " + str(len(self.core[cluster])) )


    def getNeighbors(self, b):
        neighbors = []
        for ptA in self.markedData :
            a = [int(i) for i in ptA[0]]
            b = [int(i) for i in b]
            distance = utils.distanceEuclidienne(a, b) if self.euclidienne else utils.distanceManhattan(a, b)
            if distance <= self.eps :
                neighbors.append(ptA)
        
        return neighbors

    def predict(self, data) :
        distances = []
        for c in self.coreCentroids :
                    a = [int(i) for i in data]
                    b = [int(i) for i in self.coreCentroids[c]]
                    distance = utils.distanceEuclidienne(a, b) if self.euclidienne else utils.distanceManhattan(a, b)
                    distances.append(distance)

        classification = distances.index(min(distances))

        return classification



def process(filename, eps, minPts, euclidienne = True):

    data = utils.getPixels(filename)

    dBscan = DBScan(eps, minPts, euclidienne)
    dBscan.fit(data)

    data = [tuple(dBscan.coreCentroids[dBscan.predict(x)]) for sublist in data for x in sublist]

    return data