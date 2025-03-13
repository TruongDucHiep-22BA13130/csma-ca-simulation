#! /usr/bin/bash

file="main"
dir="NSFinalProject"

nNodes=7
packetSize=512
serverNode=$(echo $(($nNodes / 2)))
maxPackets=10
interval=1
verbose="false"
pcap="false"
collectData="true"
param="--nNodes=$nNodes --verbose=$verbose --pcap=$pcap --collectData=$collectData --packetSize=$packetSize --maxPackets=$maxPackets --interval=$interval"

storeDir="/svmid-ps$packetSize"

if [ "$collectData" == "false" ]
then
echo "Running $file with $nNodes nodes...";
storeDir="/"
fi

if [ -d $dir/flowData$storeDir -a $collectData == "true" ]
then
	echo "Experiment has already been done. Results are stored at $storeDir."
	exit 0
fi

cp $dir/$file.cc scratch/
./ns3 run "scratch/$file $param"

mkdir -p $dir/flowData$storeDir
mkdir -p $dir/animData$storeDir

mv final*.xml $dir/flowData$storeDir
mv anim*.xml $dir/animData$storeDir
