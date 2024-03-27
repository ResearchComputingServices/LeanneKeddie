
import numpy as np
import matplotlib.pyplot as plt

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def implicit_function(x,
                      y,
                      coeffs = [0,0,0,0,0]):
         
    return coeffs[0]+ x*coeffs[1] + y*coeffs[2] + x**2*coeffs[3] + x*y*coeffs[4]+y**2*coeffs[5] 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_scatter(file_path) -> tuple:
    x = []
    y = []
    
    input_file = open(file_path,'r')
    for line in input_file.readlines():
        split = line.split(' ')
        x.append(float(split[0]))
        y.append(float(split[1]))
        
    return x,y
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


topic_1_x, topic_1_y = load_scatter('topic_1.dat')
topic_2_x, topic_2_y = load_scatter('topic_2.dat')
topic_3_x, topic_3_y = load_scatter('topic_3.dat')

# coeffs1 = [-8.92474551e-01,  3.23862941e+00,  3.69704265e-01,  5.22651225e+00, 1.62882480e+00, -4.03060270e-03]
# coeffs2 = [ 3.43776076e-01, -2.88064509e+00,  5.79281386e+00, -4.11302209e+00, 1.64449989e+00,  2.64212350e+00]
# coeffs3 = [ 5.48698475e-01, -3.57984314e-01, -6.16251812e+00, -1.11349016e+00, -3.27332469e+00, -2.63809290e+00]


coeffs1 = [1.21747227e-02,  3.51549327e+00,  1.85622619e-01,  5.18131360e+00, 1.48024451e+00, -1.53673274e-01]
coeffs2 = [-9.90457354e-04, -2.88847642e+00,  5.84265286e+00, -3.96349303e+00,1.71840395e+00,  2.81278499e+00]
coeffs3 = [-1.11842653e-02, -6.27016849e-01, -6.02827548e+00, -1.21782057e+00,-3.19864845e+00, -2.65911172e+00]
x_values = np.linspace(-5,5, 1000)
y_values = np.linspace(-5,5, 1000)

x,y = np.meshgrid(x_values, y_values)

z1 = implicit_function(x,y, coeffs=coeffs1)
z2 = implicit_function(x,y, coeffs=coeffs2)
z3 = implicit_function(x,y, coeffs=coeffs3)

plt.contour(x,y,z1,levels=[0],colors='b',)
plt.contour(x,y,z2,levels=[0],colors='r',)
plt.contour(x,y,z3,levels=[0],colors='g',)
plt.scatter(topic_1_x,topic_1_y,c='b')
plt.scatter(topic_2_x,topic_2_y,c='r')
plt.scatter(topic_3_x,topic_3_y,c='g')

plt.grid(True)
plt.axis('equal')

plt.xlim(-2,2)
plt.ylim(-2,2)
plt.show()

