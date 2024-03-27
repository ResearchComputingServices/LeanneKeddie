import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import textwrap
from scipy.stats import gaussian_kde

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_scatter(file_path) -> tuple:
    x = []
    y = []
    labels = []
    input_file = open(file_path,'r')
    for line in input_file.readlines():
        split = line.split('^')
        x.append(float(split[0]))
        y.append(float(split[1]))
        labels.append(textwrap.fill(split[2], 50))
               
    return x,y,labels

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def plot_density_map(x,
                     y,
                     title = '',
                     slope = 0.,
                     y_int = -1.):
    
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    _, ax = plt.subplots()

    ax.set_xlim([-0.1,1.1])
    ax.set_ylim([-0.1,1.1])
    ax.set_title(title)
    
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    
    ax.scatter(x, y, c=z, s=100)

    db_x = np.linspace(-2, 2, 100)
    db_y = slope*db_x + y_int
    ax.plot(db_x, db_y)
    
    return ax  

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#input_path = 'dat/SOCENV_INC/'
#input_path = 'dat/COMP_CON/'
input_path = './'

train_topic_1_x, train_topic_1_y, train_topic_1_labels = load_scatter(input_path+'train_topic_2.dat')
train_topic_2_x, train_topic_2_y, train_topic_2_labels = load_scatter(input_path+'train_topic_1.dat')
# train_topic_3_x, train_topic_3_y, train_topic_3_labels = load_scatter(input_path+'train_topic_3.dat')

verify_topic_1_x, verify_topic_1_y, verify_topic_1_labels = load_scatter(input_path+'verify_topic_2.dat')
verify_topic_2_x, verify_topic_2_y, verify_topic_2_labels = load_scatter(input_path+'verify_topic_1.dat')
# verify_topic_3_x, verify_topic_3_y, verify_topic_3_labels = load_scatter(input_path+'verify_topic_3.dat')


print(f'# of Training pts: {len(train_topic_1_x)+len(train_topic_2_x)}')
print(f'# of Verification pts: {len(verify_topic_1_x)+len(verify_topic_2_x)}')

slope = -2.612991302664114
y_int = 1.7734350251627455

plot_density_map(train_topic_1_x,
                 train_topic_1_y,
                 title = 'Training Data (COMP_CON)',
                 slope=slope,
                 y_int = y_int)

plot_density_map(train_topic_2_x,
                 train_topic_2_y,
                 title = 'Training Data (Irrelevant)',
                 slope=slope,
                 y_int = y_int)

plot_density_map(verify_topic_1_x,
                 verify_topic_1_y,
                 title = 'Verification Data (COMP_CON)',
                 slope=slope,
                 y_int = y_int)

plot_density_map(verify_topic_2_x,
                 verify_topic_2_y,
                 title = 'Verification Data (Irrelevant)',
                 slope=slope,
                 y_int = y_int)

plt.show()

fig, axs = plt.subplots(2, 2)

for ax in axs:
    for a in ax:
        a.set_xlim([-0.1,1.1])
        a.set_ylim([-0.1,1.1])

axs[0,0].set_title('Topic 1 (COMP_CON)')
axs[0,0].scatter(train_topic_1_x,train_topic_1_y,facecolors='none', edgecolors='r',marker='o',sizes=[7])
axs[0,0].scatter(verify_topic_1_x,verify_topic_1_y,facecolors='none', edgecolors='g',marker='o',sizes=[7])
# mplcursors.cursor(axs[0,0]).connect( "add", lambda sel: sel.annotation.set_text(train_topic_1_labels[sel.index]))


axs[0,1].set_title('Topic 2 (Irrelevant)')
axs[0,1].scatter(train_topic_2_x,train_topic_2_y,facecolors='none', edgecolors='r',marker='o',sizes=[7])
axs[0,1].scatter(verify_topic_2_x,verify_topic_2_y,facecolors='none', edgecolors='g',marker='o',sizes=[7])
#mplcursors.cursor(axs[0,1]).connect( "add", lambda sel: sel.annotation.set_text(verify_topic_2_labels[sel.index]))

#axs[1,1].set_title('Topic 3 (SOCENV_INC)')
#axs[1,1].scatter(train_topic_3_x,train_topic_3_y,facecolors='none', edgecolors='r',marker='o',sizes=[7])
#axs[1,1].scatter(verify_topic_3_x,verify_topic_3_y,facecolors='none', edgecolors='g',marker='o',sizes=[7])
#mplcursors.cursor(axs[1,1]).connect( "add", lambda sel: sel.annotation.set_text(train_topic_3_labels[sel.index]))

# axs[1,0].set_title('Compare')
# axs[1,0].scatter(train_topic_1_x,train_topic_1_y,facecolors='none', edgecolors='r',marker='o',sizes=[7])
# axs[1,0].scatter(verify_topic_2_x,verify_topic_2_y,facecolors='none', edgecolors='g',marker='o',sizes=[7])
plt.show()