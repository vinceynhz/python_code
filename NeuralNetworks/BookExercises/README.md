# Book Exercises

### Contents
1. **HodgkinHuxley.py**: implementation of the HodgkinHuxley model of the giant squid neuron
2. **LinearSeparability.py**: code that calculates the number of logical functions that are linearly separable for 2, 3 and 4 variables
3. **EdgeDetector.py**: first attempt of an image edge detector using a perceptron.

### About...
While studying multiple models of neural networks, I found the book [Neural Networks - A Systematic Introduction](http://page.mi.fu-berlin.de/rojas/neural/) by Raul Rojas, and I started studying and doing some of the exercises mentioned in the book, currently I'm on chapter 3.

### HodkinHuxley module
Aside the book description of the HH model, I found [this](http://icwww.epfl.ch/~gerstner/SPNM/node14.html) lecture quite helpful. 

In 1952, Hodgkin and Huxley were studying the giant axon of the squid and after several weeks working with heavy hot computers (Wikipedia has a nice story of this era), they came with an electronic circuit that models the excitation and activation of the neuron by means of the electrochemical components surrounding the real axon. It took me some time to understand the model, the biological implications and how to represent it in a computer program. I'll explain it to the best of this understanding.

First, is convenient to understand that the cell is excitable, meaning that there is an input signal that upon its value and the cell's state, can generate a reaction from the cell.