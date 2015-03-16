#! /bin/sh

MODE=$1
PATH_TO_SCRATCH_FOLDER=$2
LIST_OF_FILES=$3
OUTPUT_FILE=$4

if [ $MODE = "-extract" ]
then
  lib/./mirex_extract $LIST_OF_FILES.mf $PATH_TO_SCRATCH_FOLDER/features.arff
fi

if [ $MODE = "-train" ]
then
  python src/main.py -train $PATH_TO_SCRATCH_FOLDER/features.arff $LIST_OF_FILES ./data/train.arff
  java -Xms1024M -Xmx1024M -classpath ./lib/weka.jar weka.classifiers.meta.MultiBoostAB -W weka.classifiers.trees.J48 -t ./data/train.arff -i -d $PATH_TO_SCRATCH_FOLDER/classifier > ./results/train.txt
fi

if [ $MODE = "-classify" ]
then
  python src/main.py -test $PATH_TO_SCRATCH_FOLDER/features.arff $LIST_OF_FILES ./data/test.arff
  java -Xms1024M -Xmx1024M -classpath ./lib/weka.jar weka.classifiers.meta.MultiBoostAB -W weka.classifiers.trees.J42L8 -T ./data/test.arff -i -o -p 0 -l $PATH_TO_SCRATCH_FOLDER/classifier > ./results/test.txt
  python src/main.py -output $OUTPUT_FILE
fi