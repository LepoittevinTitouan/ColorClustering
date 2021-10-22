from PIL.Image import new
import utils
import random
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count

class KMeans():
    def __init__(self, k, euclidienne):
        self.k = k
        self.euclidienne = euclidienne

    def getDistances(self, data):
        distances = []
        for c in self.centroids :
                    a = [int(i) for i in data]
                    b = [int(i) for i in self.centroids[c]]
                    distance = utils.distanceEuclidienne(a, b) if self.euclidienne else utils.distanceManhattan(a, b)
                    distances.append(distance)
        return distances

    def getClassification(self, sample):
        distances = self.getDistances(sample)
        # distances = [np.linalg.norm(np.array(x)-np.array(self.centroids[centroid])) for centroid in self.centroids]
        classification = distances.index(min(distances))
        self.classifications[classification].append(sample)

    def getClassificationMultiP(self, sample):
        distances = self.getDistances(sample)
        # distances = [np.linalg.norm(np.array(x)-np.array(self.centroids[centroid])) for centroid in self.centroids]
        classification = distances.index(min(distances))
        return classification

    def fit(self, data, maxIter = 200):
        self.centroids = {}

        flatData = [item for sublist in data for item in sublist]

        print(len(flatData))

        for i in range(self.k):
            self.centroids[i] = flatData[random.randint(0,len(flatData))]

        iter = 0
        
        optimized = False

        while(iter < maxIter and not optimized):
            print("Iteration " + str(iter))
            print(self.centroids)

            self.classifications = {}

            for n in range(self.k) :
                self.classifications[n] = []

            # #Pour chaque pixel, on calcul et selectionne la distance au centroid le plus proche
            # for x in flatData :
            #     self.getClassification(x)

            p = Pool(processes = cpu_count()-1 or 1)
            classification = p.map(self.getClassificationMultiP, flatData)
            p.close()

            for i in range(len(classification)) :
                self.classifications[classification[i]].append(flatData[i])

            oldCentroids = dict(self.centroids)

            for n in self.classifications :
                if len(self.classifications[n]) > 0 :
                    self.centroids[n] = np.average(self.classifications[n], axis=0)
                    self.centroids[n] = self.centroids[n].tolist()
                    self.centroids[n] = [int(i) for i in self.centroids[n]]

            # On verifie que les centroids sont optimisés, en regardant la différence entre deux itérations
            optimized = True

            for c in self.centroids :
                if (abs(oldCentroids[c][0] - self.centroids[c][0]) + abs(oldCentroids[c][1] - self.centroids[c][1]) + abs(oldCentroids[c][2] - self.centroids[c][2]) > 4 ):
                    optimized = False

            X = [self.centroids[i][0] for i in self.centroids]
            Y = [self.centroids[i][1] for i in self.centroids]
            Z = [self.centroids[i][2] for i in self.centroids]

            C = [self.centroids[i] for i in self.centroids]
            C = [[color[0]/255, color[1]/255, color[2]/255] for color in C]

            fig = plt.figure()
            ax = fig.add_subplot(111, projection = '3d')
            ax.set_xlabel('Red')
            ax.set_ylabel('Green')
            ax.set_zlabel('Blue')
            
            ax.set_xlim([0,255])
            ax.set_ylim([0,255])
            ax.set_zlim([0,255])

            ax.scatter(X, Y, Z, c = C)
            ax.set_title("k = " + str(self.k) + " (iteration n° " + str(iter) + ")")
            plt.savefig("./centroidsSRC/plot" + str(iter) + ".png")
            plt.close()

            iter += 1

    def predict(self, x):
        distances = self.getDistances(x)
        classification = distances.index(min(distances))

        return classification
            
def process(filename,k,euclidienne = True):

    data = utils.getPixels(filename)

    kMeans = KMeans(k, euclidienne)
    kMeans.fit(data)    

    data = [tuple(kMeans.centroids[kMeans.predict(x)]) for sublist in data for x in sublist]

    return data


    

    



    
