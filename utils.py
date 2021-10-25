from PIL import Image
from math import sqrt

width = 100

def getPixels(filename):
    img = Image.open(filename, 'r')
    w, h = img.size
    # w, h = width , int((h*width)/w)
    img.thumbnail((w,h),Image.ANTIALIAS)
    pix = list(img.getdata())
    print(img.size)
    return [pix[n:n+w] for n in range(0, w*h, w)]

def getSize(filename):
    img = Image.open(filename, 'r')
    w, h = img.size
    # w, h = width , int((h*width)/w)
    img.thumbnail((w,h),Image.ANTIALIAS)
    return img.size

def distanceEuclidienne(a, b):
    return sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2 )

def distanceManhattan(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1]) + abs(b[2] - a[2])

if __name__ == "__main__":
    rouge = tuple([255,0,0])
    bleu = tuple([0,0,255])

    print(distanceEuclidienne(rouge,bleu))
    print(distanceManhattan(rouge,bleu))