#/usr/bin/env python3

import sys
sys.path.append('..')

from matplotlib import pyplot as plt
from nn.networks import Classifier
from datasets import MnistTrainingDataset, MnistTestDataset, MnistTrainingDataset1000
from helpers import training, test, draw_W_histories, draw_mean_se_history, draw_cpr_history
import numpy as np

MNIST_PATH = '../mnist'

if __name__ == '__main__':
    # get args
    if len(sys.argv) != 3:
        print('Usage: %s <lean_num> <out_file>' % (sys.argv[0]))
        exit()
    learn_num = int(sys.argv[1])
    filename = sys.argv[2]
    with open(filename, 'w') as f:
        pass
    
    # Load MNIST dataset
    training_dataset = MnistTrainingDataset(MNIST_PATH, 1, -1)
    test_dataset = MnistTestDataset(MNIST_PATH, 1, 0)

    # Create Deep Neural Network for nmist classification
    classifier = Classifier('logistic', training_dataset.img_size, 'se', 0.15)
    classifier.add_layer('logistic', 200)
    classifier.add_layer('logistic', 10)
    np.savez(filename, classifier)

    # Training network and obtain histories
    W_histories, mean_se_history, cpr_history = training(classifier,
                                                         training_dataset,
                                                         learn_num)

    # Draw training histories
    data_name = '%d_%s' % (learn_num, training_dataset.name)
    draw_W_histories(W_histories, classifier.name, data_name)
    draw_mean_se_history(mean_se_history, classifier.name, data_name)
    draw_cpr_history(cpr_history, classifier.name, data_name)

    # Test network and print mean SE and CPR
    print(test(classifier, test_dataset))
    np.savez(filename, classifier)

    #plt.show()

# end of file
