# Data annotation and augmentation by Andrej Majev

Table of contents:

- [Annotation process](#annotation-process)
- [Augmentation](#augmentation)

## Annotation process

The classes that we chose are the varying degrees of tree density - open, sparse and dense.

||Open|Sparse|Dense|
|---|---|---|---|
|Original image|![](../data/cut_images/classified/open/119_1805_g0_1b.jpg)|![](../data/cut_images/classified/sparse/104_862_g0_2b.jpg)|![](../data/cut_images/classified/dense/29_4841_g0_2k.jpg)|
|Trees highlighted|![](imgs/open.jpg)|![](imgs/sparse.jpg)|![](imgs/dense.jpg)|

Open - no trees visible in image <br>
Sparse - few trees are visible mostly from one side (one tree / one group of trees) <br>
Dense - a lot of trees are visible from multiple sides (surrounded by trees) <br>


The classes are additionally each split into regular, leafless and snowy subtypes 

|Regular|Leafless|Snowy|
|---|---|---|
|![](../data/cut_images/classified/sparse/27_1532_g0_1k.jpg)|![](../data/cut_images/classified/sparse_leafless/140_242_g0_1k.jpg)|![](../data/cut_images/classified/sparse_snow/18_7457_g0_1b.jpg)



For image annotation annotator.py was used

## Augmentation

The loadign, augmentation and splitting can be found in [data_loading_augmentation.py](../notebooks/data_loading_augmentation.py)


All splits are resised and transformed to tensors:

``` python
transforms.Resize((224, 224)),
transforms.ToTensor()
```

The training dataset is also augmented:

``` python
transforms.RandomHorizontalFlip(),
transforms.RandomRotation(10),
transforms.ColorJitter(brightness = 0.2)
```

|Original image|Augmented 1|Augmented 2|
|---|---|---|
|![](imgs/sample.jpg)|![](imgs/aug_1.jpg)|![](imgs/aug_2.jpg)

