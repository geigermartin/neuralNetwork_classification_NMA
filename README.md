# **Course project: Neural Network for Classification (Computational Neuroscience - Neuromatch Academy)**
We analyzed calcium imaging data provided within the [Allen Institute dataset](https://compneuro.neuromatch.io/projects/neurons/README.html) from visual cortices of transgenic mice in a go and no-go task where the animal had to respond to changes in image identity. In the *detectingExpectations.ipynb* we used supervised learning for expectation classification. Specifically, we implemented a feedforward neural network to classify the presented stimuli, which were 8 images and an omitted image (no-go trials). The goal was then to compare classification accuracies for excitatory and inhibitory populations.

Network structure:	
- Shape: [268(exc) / 66(inh), 64, 32, 9]
- Fully-Connected Layers
- ReLU

Regularization: 	
- SGD via batching
- Dropout = 0.35
- Weight decay = 0.2

Looking at the classifier output, there was an issue with overfitting. We’re overfitting because each training sample is not independent and we didn’t have enough data to make the test set independent from the training set.

The classification accuracy was much higher for excitatory compared to inhibitory cells. There are 2 possible explanations. Inhibitory cells could be less predictive of the stimuli. Alternatively, this may result from the fact that this neuron population was only 1/4 the size, so the features are less predictive because there’s less information. 

This analysis is inconclusive due to the very restricted time for the project. Nevertheless, it was a great learning opportunity to work with calcium imaging data and to implement & train a deep neural network with PyTorch.

*Curriculum of the summer school*: https://compneuro.neuromatch.io/tutorials/intro.html
