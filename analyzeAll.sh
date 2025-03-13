#! /usr/bin/bash

mkdir -p analyzedData 
mkdir -p summarizedData

if [ -z $1 ]
then
	echo "You have to provide a configuration (e.g.: sv0-ps512)"
	exit 1
fi

if [ ! -d "flowData/$1" ]
then
	echo "$1 is invalid"
	exit 1
fi

if [ -d "analyzedData/$1" ]
then
	echo "Result is already in analyzedData/$1"
	exit 0
fi

mkdir analyzedData/$1

for nNodes in {2..30}
do
echo $nNodes/30
python3 analyze.py flowData/$1/final-$nNodes-nodes.xml $1> analyzedData/$1/$nNodes-nodes.txt
done
echo "Results are stored in analyzedData/$1 and summarizedData/$1"
echo Done
