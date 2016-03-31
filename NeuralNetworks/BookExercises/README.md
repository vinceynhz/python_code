# Book Exercises

### Contents
1. **HodgkinHuxley.py**: implementation of the HodgkinHuxley model of the giant squid neuron
2. **LinearSeparability.py**: code that calculates the number of logical functions that are linearly separable for 2, 3 and 4 variables
3. **EdgeDetector.py**: first attempt of an image edge detector using a perceptron.

### About...
While studying multiple models of neural networks, I found the book [Neural Networks - A Systematic Introduction](http://page.mi.fu-berlin.de/rojas/neural/) by Raul Rojas, and I started studying and doing some of the exercises mentioned in the book, currently I'm on chapter 3.

### Hodgkin Huxley module
[TODO: Move this text to the blog post about the HH model]

Aside the book description of the HH model, I found [this](http://icwww.epfl.ch/~gerstner/SPNM/node14.html) lecture quite helpful. This module uses VPython for the graphics generation.

In 1952, Hodgkin and Huxley were studying the giant axon of the squid and after several weeks working with heavy hot computers (Wikipedia has a nice story of this era), they came with an electronic circuit that models the excitation and activation of the neuron by means of the electrochemical components surrounding the real axon. It took me some time to understand the model, the biological implications and how to represent it in a computer program. I'll explain it to the best of my understanding.

First is convenient to understand that the cell is excitable, meaning that there is an *input signal* that upon its value and the cell's state, can generate a reaction. When an input signal (current) is passed through the cell, it can either increase current into the membrane or leak through one of the environment channels: *sodium (Na)* at the outside of the cell, *potasium (K)* at the inside and a *leak (L)* current for other unspecified channels. 

The three channels are characterized within the model by their conductance *g*. The conductance of the leakage channel (L) is voltage-independent while the other conductance of the other two (Na and K) is both, time and voltage dependent. Said that, if all the channels are open at a given time, they will transmit currents with maximum conductance *g<sub>Na</sub>* and *g<sub>K</sub>* respectively, however, normally some of the channels are blocked.

The probability that a channel is open is described by three additional coeficients *m*, *n* and *h*. The combined action of *m* and *h* controls the *Na* channel, while *n* controls the *K* one. Since we mention that the gates Na and K are time dependent, the coeficients *m*, *n* and *h* evolve according to some differential equations allowing us to model exactly the time variation of these three coeficients.

In fact, we can observe how these coeficients change in time using the model. Being *x* a generic name for *m*, *n*, or *h*, for a fixed voltage *u*, the coeficients (described by *x*) approach an equilibrium value *x<sub>0</sub>(u)* and a time constant *T<sub>x</sub>(u)*. The following charts describe these two functions.

![HodgkinHuxley - Equilibrium Functions](https://raw.githubusercontent.com/vinceynhz/python_code/master/NeuralNetworks/BookExercises/img/hodgkin-huxley-x0(n%2Cm%2Ch).png)

![HodgkinHuxley - Time Constant](https://raw.githubusercontent.com/vinceynhz/python_code/master/NeuralNetworks/BookExercises/img/hodgkin-huxley-T(n%2Cm%2Ch).png)

Putting all the pieces together and letting the model run over time, we can observe some interesting dynamics.

**Membrane potential**

What we are doing on this model is to change current over time and measure the membrane potential (E) that shows the activation of the cell. The green curve describes the current applied to the model while the blue represents the response from the cell:

![HodgkinHuxley - Membrane Potential](https://raw.githubusercontent.com/vinceynhz/python_code/master/NeuralNetworks/BookExercises/img/hodgkin-huxley-example1.png)

**Spike generation**

In this case, we are applying a high current to the cell and letting it get back to it's rest state with current 0:

![HodgkinHuxley - Spike Generation](https://raw.githubusercontent.com/vinceynhz/python_code/master/NeuralNetworks/BookExercises/img/hodgkin-huxley-example2.png)

The following classes are defined:

* *channel*: this one is more like an enum than a class and just to give names to the three channels of the cell: potasium (K), sodium (Na), leakage (L).
* *coeficient*: similarly, this one is an enum for *m*, *n*, and *h*.

The following methods are described:

**Model functions**

* *alpha*: this function is used in the differential equations to calculate the change of the coeficients over time.
* *beta*: second function for the differential equations to calculate the change of the coeficients over time.
* *rest*: to calculate the values of the coeficients at rest current.
* *x0*: equilibrium function depending on voltage.
* *Tx*: time constant depending on voltage.
* *partial_coeficient*: to calculate the differential equation of the coeficients respect time.
* *current*: to calculate the current at each gate depending on the voltage.
* *model*: this applies the two functions above to calculate the differential values for the next *dt*.

**Examples**

* *spikeA*: to create a spike curve applying a high current at time < 0.
* *multiple_current*: to display the behavior of the cell at current value changes on time.
* *displayx0*: to show the equilibrium function of the coeficients.
* *displayT*: to show the time constant function of the coeficients.

### Linear Separability module