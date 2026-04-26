# Imports
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import splitfolders

def make_loaders():
    # Defining augmentations
    train_aug = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness = 0.2),
        transforms.ToTensor()
    ])
    val_test_aug = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    # Making datasets
    data_path = r"C:/Users/tipka/Desktop/uni/Semester4/Computer Vision/Project/CIV4-WhoS-Where/data"
    splitfolders.ratio(input = f"{data_path}/cut_images/merged", output = f"{data_path}/cut_images/split", ratio=(.6, .2, .2))
        #Uniformly split images are in cut_images/split/.


    train_dataset = ImageFolder(f"{data_path}/cut_images/split/train", transform = train_aug)
    val_dataset = ImageFolder(f"{data_path}/cut_images/split/val", transform = val_test_aug)
    test_dataset = ImageFolder(f"{data_path}/cut_images/split/test", transform = val_test_aug)
    #print(train_dataset.class_to_idx)

    # Making loaders
    train_loader = DataLoader(train_dataset, batch_size = 32, shuffle = True)
    val_loader = DataLoader(val_dataset, batch_size = 32, shuffle = False)
    test_loader = DataLoader(test_dataset, batch_size = 32, shuffle = False)

    return train_loader, val_loader, test_loader