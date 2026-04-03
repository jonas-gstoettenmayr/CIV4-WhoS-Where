# Computer vision project of team "Who's where"

A project about finding out the distribution of animals in different forest environments.

## The Team

Maria Helmetsberger (<s2410929013@fhooe.at>)\
Bettina Pölzleitner (<s2410929023@fhooe.at>)\
Andrey Mayev (<s2410929043@fhooe.at>)\
Jonas Gstöttenmayr (<s2410929009@fhooe.at>)

## Data

### Sources

Source data: [https://zenodo.org/records/19034999](https://zenodo.org/records/19034999) \
Annotated data: Made by us, availabe under - \
Ground truth: [https://github.com/bambi-eco/Dataset](https://github.com/bambi-eco/Dataset)

### Folder Structure

From the source files download the images_rgb.zip and labels_matched_rgb.zip, then simply extract them into a data folder from the root directory, the resulting structure should look like:

```text
data/
├── gt_headings.txt
├── gt/
│   └── flight_id.txt...
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
