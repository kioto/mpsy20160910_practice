#!/bin/sh

if [ ! -d ../mnist ]; then
    cd ..
    mkdir mnist
    cd mnist
    wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
    wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
    wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
    wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
    gunzip *.gz
    cd ../hirahara
    
fi

imgdir='img_mnist_logistic'
if [ ! -d $imgdir ]; then
    mkdir $imgdir
fi
    
python3 ./mnist_learn.py  10 010_res.npz
python3 ./mnist_learn.py  50 050_res.npz
python3 ./mnist_learn.py 100 100_res.npz

# end of file
