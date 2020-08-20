import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from matplotlib.mlab import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Load Doc2Vec model
model= Doc2Vec.load("d2v.model")

# Names for tags
names = ['Admiral_Ackbar', 'Ahsoka_Tano', 'Aragorn', 'Arwen', 'Asajj_Ventress', 'BB-8', 'Bail_Organa', 'Barliman_Butterbur', 'Beechbone', 'Beregond_and_Bergil', 'Bergil', 'Bilbo_Baggins', 'Boba_Fett', 'Boromir', 'Bregalad', 'C-3PO', 'Cad_Bane', 'Captain_Phasma', 'Celeborn', 'Chewbacca', 'Clone_trooper', 'Count_Dooku', 'Círdan', 'Darth_Maul', 'Darth_Vader', 'Denethor', 'Droid_(Star_Wars)', 'Déagol', 'Dúnhere', 'Elfhelm', 'Elladan_and_Elrohir', 'Elrond', 'Erestor', 'Erkenbrand', 'Faramir', 'Farmer_Maggot', 'Finn_(Star_Wars)', 'Forlong_the_Fat', 'Fredegar_Bolger', 'Frodo_Baggins', 'Galadriel', 'Gamling', 'Gandalf', 'General_Hux', 'Ghân-buri-Ghân', 'Gildor_Inglorion', 'Gimli_(Middle-earth)', 'Glorfindel', 'Goldberry', 'Gollum', 'Gothmog_(Third_Age)', 'Grand_Admiral_Thrawn', 'Grand_Moff_Tarkin', 'Grimbold', 'Gríma_Wormtongue', 'HK-47',
'Haldir_of_Lórien', 'Hamfast_Gamgee', 'Han_Solo', 'Háma_(Middle-earth)', 'Húrin_the_Tall', 'Isildur', 'Jango_Fett', 'K-2SO', 'Kylo_Ren', 'L3-37', 'Lando_Calrissian', 'Legolas', 'Lieutenant_Connix', 'List_of_Star_Wars_Legends_characters', 'Luke_Skywalker', 'Mace_Windu', 'Mandalorian', 'Mara_Jade', 'Max_Rebo_Band', 'Meriadoc_Brandybuck', 'Mouth_of_Sauron', 'Nazgûl', 'Nien_Nunb', 'Old_Man_Willow', 'Orophin', 'Orson_Krennic', 'Padmé_Amidala', 'Peregrin_Took', 'Princess_Leia', 'Qui-Gon_Jinn', 'R2-D2', 'Radagast', 'Rey_(Star_Wars)', 'Rogue_Squadron', 'Rose_Tico', 'Samwise_Gamgee', 'Saruman', 'Sauron', 'Saw_Gerrera', 'Shelob', 'Skywalker_family', 'Solo_family', 'Starkiller', 'Stormtrooper_(Star_Wars)', 'Tag_and_Bink', 'Théoden', 'Théodred', 'Tom_Bombadil', 'Treebeard', 'Tusken_Raiders', 'Wedge_Antilles', 'Witch-king_of_Angmar', 'Éomer', 'Éomund', 'Éothain', 'Éowyn']

# Subset needed for tags
tagnames = ['Éomer', 'Elfhelm', 'Théoden', 'General_Hux', 'Lieutenant_Connix', 'Starkiller', 'HK-47', 'Samwise_Gamgee', 'Legolas', 'Aragorn', 'Darth_Vader', 'Gandalf', 'C-3PO', 'Darth_Maul', 'Beechbone', 'Count_Dooku', 'Bilbo_Baggins' , 'Cad_Bane']

# Take vector embeddings and do PCA analysis
data = [model.docvecs[i] for i in range(len(model.docvecs))]
dataMatrix = np.array(data) 
myPCA = PCA(dataMatrix)


'''
# This part plots all tags
for i in range(len(names)):
    x = myPCA.Y[i,0]
    y = myPCA.Y[i,1]
    plt.plot(x, y, 'bo')
    plt.text(x * (1 + 0.01), y * (1 + 0.01) , names[i], fontsize=8)
'''

#This part only plots a subset of tags.
for i in range(len(names)):
    x = myPCA.Y[i,0]
    y = myPCA.Y[i,1]
    plt.plot(x, y, 'bo')

for name in tagnames:
    i = names.index(name)
    x = myPCA.Y[i,0]
    y = myPCA.Y[i,1]
    plt.text(x * (1 + 0.01), y * (1 + 0.01) , names[i], fontsize=10)

j = names.index('R2-D2')
x = myPCA.Y[j,0]
y = myPCA.Y[j,1]
plt.text(x * (1 + 0.01), y * (1 - 0.2) , names[j], fontsize=10)


# Give plot title and axes
plt.title('Doc2Vec document embeddings plotted in 1. and 2. principal components')
plt.xlabel('First principal component')
plt.ylabel('Second principal component')

#Plot plot
plt.show()

