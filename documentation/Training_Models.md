## Files: train_mode.ipynb and train_model_efficientnetv2-s.ipynb + everything in /notebooks/models

### Trained two different models, one pretrained with MobileNetV3 and one pretrained with EfficientNetV2

#### Architecture

[Pretrained ImageNet backbone]   ← all layers, fully trainable
        ↓
  Global Average Pooling
        ↓
  [New classifier head]          ← randomly initialized, fits your NUM_CLASSES
        ↓
   Output (9 classes)

(At least I believe this is how it should look like)

We are training the final linear layer, everything before comes from the pretrained weights. 

#### Differences

MobileNetV3-Small has a more complex head: Conv → HardSwish → AdaptiveAvgPool → Conv → HardSwish → Dropout → Linear. The dropout lives inside this structure.

EfficientNetV2-S has a simpler head: AdaptiveAvgPool → Dropout → Linear. The drop_rate we pass in applies to that single dropout before the linear.


#### Decisions

There is a Batch size of 32 for now, it worked with out first try good which had a smaller size and for now it is still this size. 

The learning rate is 1e-4, which is pretty standard and based on the val loss and accuracy works good. 

It also includes a dropout rate of 0.2.

A random seed (42) is also included for reproducability.  

#### What we save

We save for each model the metadata, the model to load it again, the predictions for the habitats (name of picture and prediction) and the training_history. 

#### Further uses

We have in both train_model files Grad-CAM to check what the model looks at, a confusion Matrix to check if it makes sense what it misclassifies and where the biggest confusions are and a potential Monte Carlo Dropout usecase, if we have the time/want to look into that. 


#### Setup

Setting all the starting parts (all of the decisions + model), including also a part for potential Fashion_Mnist testing purposes, just to see if everything works before having the data ready. 

#### Model definition

Building the model, based on our setup + checking out a quick model summary to see if it looks correct.

#### Data Loading

Getting the Data we are about to use from the data_loading_augmentation file. Checking for the length of them and for the classes to see if everything was loaded correctly.

#### Training Helpers

Includes the functions: 
- for training one Epoch, gives us back the loss and the accuracy.
- for evaluation on the validation set, gives also back the loss and the accuracy
- for testing the model, which runs on the test set. It gives back the accuracy, balanced accuracy, the predictions and the labels for the data. 
- a function for plotting the the loss and the accuracy after training. 

#### Training Loop

Gets the criterion and the optimizer (in our case CrossEntropyLoss and Adam), goes through the training epoch and evaluation functions to train the layer. 
Prints for us to see the Epochs + the loss and accuracy for both the train and validation dataset.

#### Results

Plots the Accuracy and Loss of the model, also tests the model on the testset. It then prints the test and the balanced accuracy. 

#### Save Model & History

Saves:
- full `state_dict` (the model itself)
- per-epoch loss & accuracy in a csv
- the predictions for the habitat on the test set in a csv
- metadata of the model for reproducability as json


#### Grad Cam

Firstly calculating how correct we where and how many samples we did wrong based on the test labels and the test predictions. 

Then getting the target layer to work with with GradCam and GradCamPlusPlus. Here we need to Convert our normalizzed tensor from the target layer back to display an RGB Image.

THen a function to show us the images with the predictions and the actual labels to see which parts where mostly looked at and if it makes sense. We once have it for misclassified pictures and once for correctly classified ones

#### Confusion Matrix

very simple, just a Confusion Matrix to check what it classifies as what. To check if our misclassifications make sense or if they do not make sense. Again based on the test set. 

### Mobile Net V3 Small results

![alt text](imgs\mobilenetv3_loss_accuracy.png)

Last Epoch: Epoch 50/50  train_loss=0.0616  train_acc=0.979  val_loss=0.5282  val_acc=0.912


Test Accuracy : 92.92%

Test Balanced Accuracy : 93.53%

![alt text](imgs\mobilenetv3_grad_cam_missclassification.png)

![alt text](imgs\mobilenetv3_grad_cam_correct.png)


Based on test set:

Correct: 1155, Misclassified: 88 (7.1%)


![alt text](imgs\mobilenetv3_confusion_matrix.png)


### Efficient Net V2 Small results

![alt text](imgs\efficientnetv2_loss_accuracy.png)

Last Epoch: Epoch 50/50  train_loss=0.0272  train_acc=0.994  val_loss=0.4317  val_acc=0.910

Test Accuracy : 92.52%

Test Balanced Accuracy : 90.46%

![alt text](imgs\efficientnetv2_grad_cam_missclassification.png)

![alt text](imgs\efficientnetv2_grad_cam_correct.png)

Based on test set:

Correct: 1150, Misclassified: 93 (7.5%)

![alt text](imgs\efficientnetv2_confusion_matrix.png)


### General Conclusion

If one looks at the confusion matrices, it makes sense why the model misclassified certain images. The confusion happens between the open/sparse classes or sparse/dense classes which are easy to confuse in my opinion. There is no confusion that is not understandable.