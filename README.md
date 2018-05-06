# POLYSEM_1.0
POLYSEM 1.0 is a programme for disambiguating spoken restrictive relatives and quoted vs unquoted expressions. The naive Bayesian classifier (currently implemented) yields a succcess recognition rate of ca 85% (according to my tests with a native speaker of BrE). The Multi-layer Perceptron Classifier (not implemented) yields a success rate of ca 95% (tested on the durations of silent intervals in the senteces produced by the BrE speaker).

The programme works if you have all the necessary Python packages installed. It doesn't work without the free software Praat used in speech research. It is still a prototype version and will be significantly improved in the future. For now, it is just code that worked for the purposes of my MPhil thesis. I intend to make a standalone version soon.

There is also an auxiliary tool, MLP Optimiser, which is still under development, but it already works for the two datasets (i.e., relative clauses and (un)quoted strings). It was used to search for the best parameters for the Multilayer Perceptron Classifier. A general version for any dataset will be released very soon.
