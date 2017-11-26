import glob

import numpy as np
import math

from keras.models import load_model
import h5py


class TensorFlowCNN(object):
    def __init__(self):
        self.model = None

    def create(self):
        self.model = load_model('model.h5')

    def predict(self, samples):
        resp = self.model.predict(samples)
        return resp.argmax(-1)


model = TensorFlowCNN()
model.create()

# load training data
image_array = np.zeros((1, 38400))
label_array = np.zeros((1, 4), 'float')
training_data = glob.glob('temp_tensor_data/*.npz')

for single_npz in training_data:
    with np.load(single_npz) as data:
        print data.files
        train_temp = data['train']
        train_labels_temp = data['train_labels']
        print train_temp.shape
        print train_labels_temp.shape
    image_array = np.vstack((image_array, train_temp))
    label_array = np.vstack((label_array, train_labels_temp))

train = image_array[1:, :]
train_labels = label_array[1:, :]

prediction = model.predict(train)
print prediction
true_labels = train_labels.argmax(-1)
print true_labels
print 'Testing...'
train_rate = np.mean(prediction == true_labels)
print 'Train rate: %f:' % (train_rate * 100)

