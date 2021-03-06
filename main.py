from tensorflow.keras import layers as layers
import tensorflow as tf
from tensorflow.keras import Sequential
from sklearn.utils import shuffle
import tensorflow.keras.optimizers as Optimizer
import matplotlib.pyplot as plot
import numpy as np
import os

# Check the GPU
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))


# Load the images and their labels into a data set
def getImages(dataset_dir, img_size):
    dataset_array = []
    dataset_labels = []

    class_counter = 0

    class_names = os.listdir(dataset_dir)
    for current_class_name in class_names:
        # Get class directory
        class_dir = os.path.join(dataset_dir, current_class_name)

        # Keep track of the class that is being extracted
        images_in_class = os.listdir(class_dir)
        print("Class index", class_counter, ", ", current_class_name, ":", len(images_in_class))

        for image_file in images_in_class:
            if image_file.endswith(".jpg"):
                image_file_dir = os.path.join(class_dir, image_file)

                img = tf.keras.preprocessing.image.load_img(image_file_dir, target_size=(img_size, img_size))
                img_array = tf.keras.preprocessing.image.img_to_array(img)

                img_array = img_array / 255.0

                dataset_array.append(img_array)
                dataset_labels.append(class_counter)

        # Increase the counter when we're done with a class
        class_counter += 1

    # Shuffle both lists the same way
    dataset_array, dataset_labels = shuffle(dataset_array, dataset_labels, random_state=817328462)

    # Transform to a numpy array
    dataset_array = np.array(dataset_array)
    dataset_labels = np.array(dataset_labels)
    return dataset_array, dataset_labels, class_names


# Get the training data set
train_ds, train_classes, class_names = getImages('./data/seg_train/seg_train/', 150)

print("Training Data Array Shape :", train_ds.shape)
print('Classes Shape: ', train_classes.shape)

# Visualise the data we're working with
plot.figure(figsize=(10, 10))
for i in range(9):
    img = train_ds[i]
    img_label = class_names[train_classes[i]]

    # Create a subplot for the image on the canvas
    ax = plot.subplot(3, 3, i + 1)
    plot.imshow(img)
    plot.title(img_label)
    plot.axis('off')

# >> plot.show()

# Creating the model
# Creating the model
model = Sequential()
model.add(layers.Conv2D(200, kernel_size=(3, 3), activation='relu'))
model.add(layers.Conv2D(180, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPool2D(5, 5))
model.add(layers.Conv2D(180, kernel_size=(3, 3), activation='relu'))
model.add(layers.Conv2D(140, kernel_size=(3, 3), activation='relu'))
model.add(layers.Conv2D(100, kernel_size=(3, 3), activation='relu'))
model.add(layers.Conv2D(50, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPool2D(5, 5))
model.add(layers.Flatten())
model.add(layers.Dense(180, activation='relu'))
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(50, activation='relu'))
model.add(layers.Dropout(rate=0.5))
model.add(layers.Dense(6, activation='softmax'))

# Compile the model
model.compile(optimizer=Optimizer.Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Fit the model
trained = model.fit(train_ds, train_classes, epochs=35, validation_split=0.30)
model.summary()

# Visualise the model accuracy
# Visualise the model accuracy
acc = trained.history['accuracy']
val_acc = trained.history['val_accuracy']
loss = trained.history['loss']
val_loss = trained.history['val_loss']

epochs_range = range(35)

# Create the graphs
plot.figure(figsize=(10, 10))
plot.subplot(1, 2, 1)
plot.title('Training & Validation Acc.')
plot.plot(epochs_range, acc, label='Training Acc.')
plot.plot(epochs_range, val_acc, label='Validation Acc.')
plot.legend(['Train', 'Test'], loc='lower right')

plot.subplot(1, 2, 2)
plot.title('Training & Validation Loss')
plot.plot(epochs_range, loss, label='Training Loss')
plot.plot(epochs_range, val_loss, label='Validation Loss')
plot.legend(['Train', 'Test'], loc='upper right')

# ..and show the graphs
# >> plot.show()
