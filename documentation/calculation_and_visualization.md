# Calculations and visualization by Bettina Pölzleitner

This document explains the following file: [cals_preds.ipynb](../notebooks/calc_preds.ipynb)

## Data Loading

The data is stored in images which are annotated, therefore information about each image needs to be loaded. The information about each image loaded is:

1. habitat
1. species
1. count
1. mean_variance
1. uncertainty_weight
1. weighted_counts

The latter information is due to the Monte-Carlo dropout and used to add that information in the calculation of the probabilities.

## Probabilities

Since the habitats have some classifications we do not need in the calculations, the habitats are merged to result in dense, open and sparse.

### P(species|habitat)

This probability is calculated since we want to know what species in the habitats appear. 

![P(species|habitat)](imgs/p(sh).png)


### P(habitat|species)

This probability is calculated to figure out where the animals are seen and to what extend. 

![P(habitat|species)](imgs/p(hs).png)

### Distribution of Deer


To get more insight into similar species and where they appear, a normal distribution for each species in the same graph is plotted.
![Normaldistribution deer](imgs/normdeer.png)



*Note to Jonas: In the presentation for me less text and more pictures, also if you think it is too little, we can talk about it. :)*