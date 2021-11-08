# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rand
from html_movie import movie

width = 100                        #set the width of the box
center = int((width+2)/2)          #set the origin of generating the points
countStationary = 0    #set up the counts for the number of stationary points plotted
numberOfDot = 1000     #set up the total number of stationary points
step=10             #set the number of new stationary dots needed everytime to create an image

xcum = np.zeros(numberOfDot)  #set up an array to store x coordinate position of the stationary points
ycum = np.zeros(numberOfDot)  #set up an array to store y coordinate position of the stationary points


boundaryArray = np.ones((width+2, width+2))    #setup the background plot for the points to be all 1
boundaryArray[1:-1,1:-1] = 0                   #set only the boundary region to be 1

#set up the function to determine if the stationary point is going to touch the boundary or other points
def ifNearOne (y,a,b):
    xFinal = a + rand.choice([-1,0,1])
    yFinal = b + rand.choice([-1,0,1])
    if xFinal < (width+2) and yFinal < (width+2):
        if (y[xFinal][yFinal] == 1):
            return True

'center to boundary'
boundaryArray[center][center] = 0          #set the center to be 0
count = 0        #set the count to determine whether the center has been filled with a point
#set up the loop to generate the points
plt.figure()
while countStationary < numberOfDot:
    #the initial position of the points
    xFinal = center
    yFinal = center
    #random walk for the points
    while boundaryArray[xFinal][yFinal] == 0: 
        xFinal += rand.choice([-1,0,1])
        yFinal += rand.choice([-1,0,1])
        #determine whether the point is stationary and count the number of stationary point
        if ifNearOne(boundaryArray,xFinal,yFinal):
            boundaryArray[xFinal][yFinal] = 1
            xcum[countStationary] = xFinal
            ycum[countStationary] = yFinal
            countStationary += 1
            print(str(countStationary) + ' dots counted')
            if(countStationary%step==0):
                file_name = "{:03d}_movie.jpg"
                plt.plot(xcum,ycum,".")
                plt.title('DLA from center to boundary')
                plt.savefig(file_name.format(int((countStationary)/step)))
        #break out the loop if the center is filled with a point
        if boundaryArray[center][center] == 1:
            count = 1
            break
    if count == 1:
        break
movie(input_files = '*.jpg', output_file = 'movie.html')  #create a clipbook with the saved images


'distribution'
'''
the following codes plot the distribution of the dots inside a bounded region expanding from center
to the boundary.
'''
length = int(width/2)+1                #setup the length of the array that store the count
region = np.arange(0,length)           #create the region in which the graph is being plotted
boxDistribution = np.zeros(length)     #create an array to store the count of dots in bounded region
centerboundRX = center                 #setup the right bound of the bounded region
centerboundLX = center - 1             #setup the left bound of the bounded region
centerboundDY = center                 #setup the lower bound of the bounded region
centerboundUY = center - 1             #setup the upper bound of the bounded region
#count the number of dots in bounded region and store them into the boxDistribution array
for i in range(0,length):
    for j in range(0,numberOfDot):
        if xcum[j]<=centerboundRX and xcum[j]>=centerboundLX and ycum[j]<=centerboundDY and ycum[j]>=centerboundUY:
            boxDistribution[i] = boxDistribution[i] + 1
    centerboundRX += 1
    centerboundLX -= 1
    centerboundDY += 1
    centerboundUY -= 1
#In order to calculate the exponential equation, need to eliminate the zero
#values in the boxDistribution array
b = 0   
for i in range(0,length):
    if boxDistribution[i] != 0:
        b = i
        break
#calculate coefficient of exponential equation using nonzero values in the array
expo = np.polyfit(region[b:], np.log(boxDistribution[b:]), 1, w=np.sqrt(boxDistribution[b:]))
#plot the distribution of the dot and the fitted exponential curve
plt.figure()
plt.bar(np.arange(0,length), boxDistribution,label = 'distribution')
plt.plot(region,np.exp(expo[1])*np.exp(expo[0]*region),'r',label = 'fitted exponential curve')
plt.title('distribution of the dots from center to boundary')
plt.xlabel('width of the box located at center')
plt.ylabel('number of dots')
plt.legend()
plt.show()
