# Computer vision project of team "Who's where"

A project about finding out the distribution of animals in different forest environments.

## The Team

Maria Helmetsberger (<s2410929013@fhooe.at>)\
Bettina Pölzleitner (<s2410929023@fhooe.at>)\
Andrey Mayev (<s2410929043@fhooe.at>)\
Jonas Gstöttenmayr (<s2410929009@fhooe.at>)

## Repo structure

[Notebooks](notebooks): Holds the notebooks and code for the project
[Documentation](documentation): Holds the explenation files of the different Parts of the project
[Data](data): The folder that holds the required data for the notbooks to work

### Documentation timeline

Order to view Documentation in:

1. [Data preperation](documentation/Data_preperation.md) (By Jonas Gstöttenmayr): explains code and decisions from: utils.py, view_images.ipynb, prototyping.ipyinb, cut_images.ipynb, match_lables_with_gt.ipynb
2. 

## Data

### Sources

Source data: [https://zenodo.org/records/19034999](https://zenodo.org/records/19034999) \
Annotated data: Made by us, availabe under - [data/cut_images](data/cut_images)
Ground truth: [https://github.com/bambi-eco/Dataset](https://github.com/bambi-eco/Dataset)

### Cutouts

The naming convention of the cutouts consists of `flight_frame_group_countAnimalid.jpg`

### Folder Structure

#### Data folder

From the source files download the images_rgb.zip and labels_matched_rgb.zip, then simply extract them into a data folder from the root directory, the resulting structure should look like:

```text
data/
├── gt_headings.txt
├── gt/
│   └── flight_id.txt...
├── cut_images/
│   ├── classified/
│   │   ├── dense/
│   │   │     ├──frame_id_.jpg
│   │   │     ├──...
│   │   ├── ...
├── labels_matched_rgb/
│   ├── test/
│   │   ├──frame_id.txt
│   │   ├──...
│   ├── train.../
│   └── val.../
└── rgb_images/
    ├── test.../
    ├── train/
    │   ├──frame_id.txt
    │   ├──...
    └── val.../
```
