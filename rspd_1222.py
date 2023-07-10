


'''Data Handling & Linear Algebra'''
import numpy as np
import pandas as pd

'''Visualisation'''
import matplotlib.pyplot as plt
import matplotlib as mpl
from pylab import rcParams
import seaborn as sns

'''Data Analysis'''
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import confusion_matrix

'''Manipulating Data and Model Building'''
from keras.layers import Conv2D
from keras.layers import Dense
from keras.layers import GlobalMaxPooling2D
from keras.layers import MaxPooling2D
from keras.layers import BatchNormalization
from keras.layers import Add
from keras.models import Sequential

"""###Importing Google Drive for Dataset Access

- Download [this dataset](https://drive.google.com/drive/folders/1gYqNXkQb13-c-pDXO5AUX9TqzTSQWD3z?usp=share_link) to your system.
- Upload this 'data' folder directly in your 'Main Drive'.
"""

# from google.colab import drive
from google.colab import drive
drive.mount('/content/drive')

DIR_TRAIN_IMAGES = "/content/drive/MyDrive/data/training/"
DIR_TRAIN_LABELS = "/content/drive/MyDrive/data/labels_training.csv"

# define dataset directories - th/content/drive/MyDrive/data/training/e below links won't work if you haven't placed 'data' folder in your 'Main Drive'
# DIR_TRAIN_IMAGES = "D:\solar-panel-detection-master\data\\training\\"
# DIR_TRAIN_LABELS = "D:\solar-panel-detection-master\data\labels_training.csv"

"""#Exploratory Analysis & Data Scaling<a name ="h4"></a>



"""

pd.read_csv(DIR_TRAIN_LABELS).head()

pwd

# LOADING DATA AND PREPROCESSING

def load_data(dir_data, dir_labels):
    '''
    dir_data: Data directory
    dir_labels: Respective csv file containing ids and labels
    returns: Array of all the image arrays and its respective labels
    '''
    labels_pd = pd.read_csv(dir_labels)                         # Read the csv file with labels and ids as we saw above
    ids = labels_pd.id.values                                   # Extracting ids from the csv file
    data = []                                                   # Initiating the empty list to store each image as numpy array
    for identifier in ids:                                      # Looping into the desired folder
        fname = dir_data + identifier.astype(str) + '.tif'      # Generating the file name
        image = mpl.image.imread(fname)                         # Reading image as numpy array using matplotlib
        data.append(image)                                      # Appending this array into the empty list and repeat the above cycle
    data = np.array(data)                                       # Now, convert the data list into data array
    labels = labels_pd.label.values                             # Extract labels from the csv file
    return data, labels                                                # Return the array of data and respective labels

# load train data - time consuming code cell
X, y = load_data(DIR_TRAIN_IMAGES, DIR_TRAIN_LABELS)

# import cv2

# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.preprocessing import image



# display the images with and without solar panels
plt.figure(figsize = (13,8))                         # Adjust the figure size
for i in range(6):                                   # For first 6 images in the data
  plt.subplot(2, 3, i+1)                             # Create subplots
  plt.imshow(X[i])                                   # Show the respective image in respective postion
  if y[i] == 0:                                      # If label is 0
    title = 'No Solar Panels in this image'          # Set this as the title
  else:                                              # Else label is 1
    title = 'Solar Panels in this image'             # Set this as the title
  plt.title(title, color = 'r', weight = 'bold')     # Adding title to each images in the subplot
plt.tight_layout()                                   # Automatically adjusts the width and height between images in subplot
plt.show()                                           # Display the subplot

# print data shape
print('X shape:\n', X.shape)

"""- 1500 total images in the training data
- Each image is of shape (101 x 101 x 3)
"""

# check number of samples
print('Distribution of y', np.bincount(y))

"""- Out of 1500 images:
  - 995 images are without any solar panels
  - 505 images are with solar panels
"""

# scale pixel values between 0 and 1
X = X / 255.0

"""#Building the CNN Model<a name ="h5"></a>



# define CNN
def build_model():
    '''
    Returns a Keras CNN model
    '''

    # define image dimensions
    IMAGE_HEIGHT = 101
    IMAGE_WIDTH = 101
    IMAGE_CHANNELS = 3

    # define a straightforward sequential neural network
    model = Sequential()

    # layer-1
    #filter is convolutional matrix which is applied across the image = 32 filters
    #kernal size is 3x3 matrix(filter)
    #relu positive kept as it is, negative is taken out
    model.add(Conv2D(filters=32,
                     kernel_size=3,
                     activation='relu',
                     input_shape=(IMAGE_HEIGHT,
                                  IMAGE_WIDTH,
                                  IMAGE_CHANNELS)))

    #adding normalizing layer to improve the speed of training
    model.add(BatchNormalization())

    # As we move forword in the layers pattern gets more complex,
    # to capture the maximum combinations in subsequent layers
    # layer-2
    model.add(Conv2D(filters=64,
                     kernel_size=3,
                     activation='relu'))
    model.add(BatchNormalization())

    # layer-3
    model.add(Conv2D(filters=128,
                     kernel_size=3,
                     activation='relu'))
    model.add(BatchNormalization())

    # Pooling layer is to reduce dimentions of feature map by summerizing presence of features
    # max-pool - sends only imp data to next layer - here 2x2 matrix
    model.add(MaxPooling2D(pool_size=2))

    # layer-4
    model.add(Conv2D(filters=64,
                     kernel_size=3,
                     activation='relu'))
    model.add(BatchNormalization())

    # layer-5
    model.add(Conv2D(filters=128,
                     kernel_size=3,
                     activation='relu'))
    model.add(BatchNormalization())

    # max-pool
    model.add(MaxPooling2D(pool_size=2))

    # layer-6
    model.add(Conv2D(filters=64,
                     kernel_size=3,
                     activation='relu'))
    model.add(BatchNormalization())

    # layer-7
    model.add(Conv2D(filters=128,
                     kernel_size=3,
                     activation='relu'))
    model.add(BatchNormalization())

    # gobal-max-pool- performs downsampling by computing the maximum of the height and width dimensions of the input
    # using it as a substitute of Flatten before passing it to the final layer
    model.add(GlobalMaxPooling2D())

    # output layer
    model.add(Dense(1, activation='sigmoid'))

    # compile model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model

"""##Checking the Performance of our CNN Model"""

# cross-validate CNN model
def cv_performance_assessment(X, y, num_folds, clf, random_seed=1):
    '''
    Cross validated performance assessment

    Input:
        X: training data
        y: training labels
        num_folds: number of folds for cross validation
        clf: classifier to use

    Divide the training data into k folds of training and validation data.
    For each fold the classifier will be trained on the training data and
    tested on the validation data. The classifier prediction scores are
    aggregated and output.
    '''

    prediction_scores = np.empty(y.shape[0], dtype='object')

    # establish the num_folds folds
    kf = StratifiedKFold(n_splits=num_folds, shuffle=True, random_state=random_seed)

    for train_index, val_index in kf.split(X, y):
        # extract the training and validation data for this fold
        X_train, X_val = X[train_index], X[val_index]
        y_train = y[train_index]

        # give more weight to minority class based on the target class distribution
        class_weight = {0: 505/1500, 1: 995/1500}

        # train the classifier
        training = clf.fit(x=X_train,
                           y=y_train,
                           class_weight=class_weight,
                           batch_size=32,
                           epochs=10,
                           shuffle=True,
                           verbose=1)

        # test the classifier on the validation data for this fold
        y_val_pred_probs = clf.predict(X_val).reshape((-1, ))

        # save the predictions for this fold
        prediction_scores[val_index] = y_val_pred_probs

    return prediction_scores

# number of subsets of data, where k subsets are used as test set and other k-1 subsets are used for the training purpose
num_folds = 3

# seed value is the previous value number generated by the random function
random_seed = 1

# build_model() function returns the predefined sequential model
cnn = build_model()

# lets look at summary of the model
cnn.summary()

# generate the probabilities (y_pred_prob)
cnn_y_hat_prob = cv_performance_assessment(X, y, num_folds, cnn, random_seed=random_seed)

"""Looking at the True Positives, False Negatives, False Positives & True Negatives -


"""

df = pd.read_csv(DIR_TRAIN_LABELS)                                              # Create a data frame of labels
df["predicted_class"] = [1 if pred >= 0.5 else 0 for pred in cnn_y_hat_prob]    # Add a column to it for predicted class

# Get the values for FN, FP, TP, TN
fn = np.array(df[(df['label'] == 1) & (df['predicted_class'] == 0)]['id'])      # False Negative
fp = np.array(df[(df['label'] == 0) & (df['predicted_class'] == 1)]['id'])      # False Positive
tp = np.array(df[(df['label'] == 1) & (df['predicted_class'] == 1)]['id'])      # True Positive
tn = np.array(df[(df['label'] == 0) & (df['predicted_class'] == 0)]['id'])      # True Negative

# Visuals of TP, TN, FP, and FN
def show_images(image_ids, num_images, title, color):
    '''
    Display a subset of images from the image_ids data
    '''
    rcParams['figure.figsize'] = 20, 4                                          # Adjusting figure size
    plt.figure()                                                                # Generating figure
    n = 1                                                                       # index where plot should apear in subplot
    for i in image_ids[0:num_images]:                                           # Run a loop for total number of images to display
        plt.subplot(1, num_images, n)                                           # Generate a subplot
        plt.imshow(X[i, :, :, :])                                               # Display the image
        plt.title('Image id: ' + str(i))                                        # Add title
        plt.axis('off')                                                         # Turn off the axis
        n+=1                                                                    # Incrememting index by 1
    plt.suptitle('\n'+title, fontsize=15, color = color, weight = 'bold')       # Adding main title to subplot
    plt.show()                                                                  # Display the final output

num_images = 7  # number of images to look at
show_images(tp, num_images, 'Examples of True Positives - Predicted solar panels if they were present', 'g')
show_images(fp, num_images, 'Examples of False Positives - Predicted solar panels even if they were not present', 'r')
show_images(tn, num_images, 'Examples of True Negatives - Predicted no solar panels when they were not present', 'g')
show_images(fn, num_images, 'Examples of False Negatives - Predicted no solar panels even if they were present', 'r')

"""# Model Evaluation & Results<a name ="h6"></a>

## Understanding ROC Curves -

An ROC curve (receiver operating characteristic curve) is a graph showing the performance of a classification model at all classification thresholds. This curve plots two parameters:

*   True Positive Rate
*   False Positive Rate

<center>True Positive Rate (TPR) is a synonym for recall and is therefore defined as follows:

![Screenshot 2023-01-20 at 5.27.02 PM.png](data:image/png;base64,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)

False Positive Rate (FPR) is defined as follows:

![Screenshot 2023-01-20 at 5.27.08 PM.png](data:image/png;base64,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)

An ROC curve plots TPR vs. FPR at different classification thresholds.

Lowering the classification threshold classifies more items as positive, thus increasing both False Positives and True Positives.</center>

####AUC: Area Under the ROC Curve -
AUC stands for "Area under the ROC Curve." That is, AUC measures the entire two-dimensional area underneath the entire ROC curve from 0 to 1.
AUC provides an aggregate measure of performance across all possible classification thresholds. One way of interpreting AUC is as the **probability that the model ranks a random positive example more highly than a random negative example**. AUC ranges in value from 0 to 1. A model whose predictions are 100% wrong has an AUC of 0.0; one whose predictions are 100% correct has an AUC of 1.0.
"""

# ROC - AUC
def plot_roc(y_true, y_pred_cnn):
    '''
    Plots ROC curves for the CNN models.
    '''
    plt.figure(figsize=(8, 8))

    # ROC of CNN
    fpr, tpr, _ = roc_curve(y_true, y_pred_cnn, pos_label=1)
    auc = roc_auc_score(y_true, y_pred_cnn)
    legend_string = 'CNN Model - AUC = {:0.3f}'.format(auc)
    plt.plot(fpr, tpr, color='red', label=legend_string)

    # ROC of chance
    plt.plot([0, 1], [0, 1], '--', color='gray', label='Chance - AUC = 0.5')

    # plot aesthetics
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.grid('on')
    plt.axis('square')
    plt.legend()
    plt.tight_layout()
    plt.title('ROC Curve', fontsize=10)
    pass

# plot ROC
y_pred = [1 if pred >= 0.5 else 0 for pred in cnn_y_hat_prob]
plot_roc(y,  cnn_y_hat_prob)
plot_roc(y, y_pred)

"""**CONFUSION MATRIX**         
<img src = 'https://miro.medium.com/max/1218/1*jMs1RmSwnYgR9CsBw-z1dw.png'>
"""

plt.figure(figsize=(5,5))
sns.heatmap(confusion_matrix(y, y_pred), annot = True, cbar = False, fmt='.0f')
plt.show()

"""## Task for you <mark>(Your chance to earn a certificate on completion!)</mark><a name ="h7"></a>

- Use data augmentation to increase the size of the training data and train the model again.
- If you are familar with transfer learning do try to implement and see if you get even better results.
- In either of the cases write your conclusion based on what you changed and how you try it.

<b>Submit your solution notebook using [this](https://forms.gle/Yz4mm4Lq29zA1WhF9) form! All the Best!
"""

