from tensorflow.keras import layers
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.preprocessing import image_dataset_from_directory as idfd
import matplotlib.pyplot as plot


# Load the images and their labels into a data set
train_ds = idfd(
    directory='data/seg_train/seg_train',
    labels='inferred',
    label_mode='int',
    seed=124
)

val_ds = idfd(
    directory='data/seg_test/seg_test',
    labels='inferred',
    label_mode='int',
    seed=124
)

class_names = train_ds.class_names
print('Classes: ', class_names)

# Visualise the data we're working with
plot.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
    for i in range(9):
        ax = plot.subplot(3, 3, i + 1)
        plot.imshow(images[i].numpy().astype('uint8'))
        plot.title(class_names[labels[i]])
        plot.axis('off')

# >> plot.show()

# Tune the data to not pollute the memory while training
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Standardizing the data before training
normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)
train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds.map(lambda x, y: (normalization_layer(x), y))

# Creating the model
model = Sequential()
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(140, kernel_size=(3, 3), activation='relu'))
model.add(layers.Conv2D(100, kernel_size=(3, 3), activation='relu'))
model.add(layers.Conv2D(60, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(160, activation='relu'))
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(40, activation='relu'))
model.add(layers.Dropout(rate=0.5))
model.add(layers.Dense(6, activation='softmax'))

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

epochs = 20
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

print(model.summary())

# Visualise the model accuracy
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

# Create the graphs
plot.figure(figsize=(10, 10))
plot.subplot(1, 2, 1)
plot.legend(loc='lower right')
plot.title('Training & Validation Acc.')
plot.plot(epochs_range, acc, label='Training Acc.')
plot.plot(epochs_range, val_acc, label='Validation Acc.')

plot.subplot(1, 2, 2)
plot.legend(loc='upper right')
plot.title('Training & Validation Loss')
plot.plot(epochs_range, loss, label='Training Loss')
plot.plot(epochs_range, val_loss, label='Validation Loss')

# ..and show the graphs
plot.show()
