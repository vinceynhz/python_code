# Experiments on Back-Propagation Neural Networks

### Contents
1. **funcs.py**: miscellaneous functions used in neural network training and execution, since I'm using multiple implementations of the training algorithm, this module is a common place to share code.
2. **experiment.py**:
3. **data.py**:
4. **neurons.py**: Standard back propagation
5. **neurons2.py**: Schmidhuber's version of back propagation
6. **neurons3.py**: Matrix approach for back propagation
7. **neurons4.py**: Fahlman's Quickpropagation 
8. **neurons5.py**: Standard back prop with margin function at each layer (instead of just to the output)

### About...
On my studies on Neural Networks, I started with an implementation of an Feedforward Backpropagation Multilayer Network (what a long name...) mostly by memory from what I had done in college; this is the architecture I started with:

![Experiments - Class Diagram](https://raw.githubusercontent.com/vinceynhz/python_code/master/ColorTheory/img/NeuronsClassDiagram.png)

A network will be composed by a set of layers, a layer will be composed by a set of neurons. From the network we can evaluate layer by layer and each layer can evaluate neuron by neuron; the training is similar, passing an error at the output, each layer will pass the error to each neuron and let them calculate the necessary adjustment and the error for the next layer.

The idea was to try to re-create an old exercise from college (having a robot in a room and deciding its movements with a NN, I have that implementation in another module).

Following my curiosity on what other stuff existed around neural networks and machine learning I found some interesting stuff; first, Scott E. Fahlman papers: *An Empirical Study of Learning Speed in Back Propagation Networks*, which taught me about the methodology and proper way to test learning algorithms, and Michael Nielsen's online book [*Neural Networks and Deep Learning*](http://neuralnetworksanddeeplearning.com/), which taught me about the matrix approach for a neural network and my first glimpse into deep learning.

Having in mind the teachings on Fahlman papers, I started working on the same modifications he suggested and varying the training algorithm. The code in here corresponds to those experiments.

### Common Functions Module *funcs.py*
This module contains a set of different functions used in back-propagation networks; both activation and error (or cost depending on the bibliography) plus binary threshold functions.

The following methods are defined:

**Activation Functions**
* *tanh_prime*: derivative of the hyperbolic tangent function
* *sigmoid*: logistic function form for a [sigmoid function](https://en.wikipedia.org/wiki/Sigmoid_function)
* *sigmoid_prime (standard version)*: derivative of the logistic function
* *sigmoid_prime (Fahlman's version)*: modification to the standard version according to Fahlman's experiments

**Backpropagation Functions**
* *cost_func*: [Mean squared error](https://en.wikipedia.org/wiki/Mean_squared_error)
* *cost_prime (standard version)*: derivative of the quadratic error function
* *cost_prime (Fahlman's version)*: modification to the standard version according to Fahlman's experiments
* *catanh*: modified version of the hyperbolic arc tangent for cost prime as suggested by Fahlman

**Output Margin Functions**
* *margin1*: basic threshold function
* *margin2*: threshold function with marginal values as suggested by Fahlman

**Other**
* *random_weight*: to get a random weight within a given range and precision

### Experiment module *experiments.py*
This module serves as a command line wrapper for multiple configuration of neural networks and allows the execution of a set of experiments at once.

To execute, open a command line console and type:
    
    $ python experiment.py [OPTIONS]

Where [OPTIONS] correspond to a set of multiple parameters to adjust the neural network itself (network type, learning rate, weight range, architecture) but also the experiment execution (boundaries and increasing step for learning rate and weight range, number of trials per combination, maximum number of epochs per training). To see the full list of options execute:

    $ python experiment.py -h

The detailed explanation of the experiments and multiple implementations can be found in this report: [TODO: Add link to my results report...]

When a new experiment is started, a bunch of information about it is printed out to the standard output, a simple stream redirection ( > ) can be used to dump this output to a file. Additionally, all statistic data is dumped to a JSON file to be analyzed with any desired tool. The structure of the JSON file can be found in the report metioned above.

The module includes the following methods:
* *test*: to actually execute a test set given configuration parameters
* *process*: to process command line parameters
* *printhelp*: exaclty that, print the help about the application

Additionally, the module contains a list of predefined test sets a test vector and its corresponding output to validate the extrapolation of results, for different functions; at the bottom can be found the full list of commands executed for the experiments I did for replication purposes.