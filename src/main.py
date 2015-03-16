'''
Created on 12.03.2011

Main class for processing raw feature set from bextract

@author: veleslavia
'''

if __name__ == '__main__':
    pass

import decimal
import sys

class FeaturesHandler:
    '''
    Opened files with input raw feature set
    '''
    def init(self, infile, outfile):
        self.inputfile = open(infile)
        self.outputfile = open(outfile, 'w')
        self.currentStr = ''
    '''
    Add value moodClass from moodfile for each feature vector 
    '''
    def addClasses(self, mode, moodfile):
        classfile = open(moodfile)
        moodList = classfile.readlines()
        classLabel = []
        for line in moodList:
            doublelist = line.split() 
            for subline in doublelist:
                if '\n' in subline:
                    if subline[:-1] not in classLabel:
                        classLabel.append(subline[:-1])
        classAttributeStr = '@attribute class {'
        classLabel = ['1','2','3','4','5']
        for label in classLabel:
            classAttributeStr+= (label+',')
        classAttributeStr = classAttributeStr[:-1]
        classAttributeStr += '}\n' 
        self.currentStr = '@'
        while  ('@' in self.currentStr) or ('%' in self.currentStr):
            self.currentStr = self.inputfile.readline()
            if self.currentStr != '\n':
                self.outputfile.write(self.currentStr)
        else:
            self.currentStr = classAttributeStr
            self.outputfile.write(self.currentStr)
            self.currentStr = self.inputfile.readline()
        while '@' not in self.currentStr:
            self.currentStr = self.inputfile.readline()
            self.outputfile.write(self.currentStr)
        self.currentStr = self.inputfile.readline()
        filelist = open('./tmpfilelist.txt','w')
        infilelist = 0
        while self.currentStr:
            if mode == '-train':
                procFile = self.currentStr[self.currentStr.rfind('/')+1:-1]
                for value in moodList:
                    if procFile in value:
                        infilelist = 1
                        currentCluster = value[value.rfind(' ')+1:]
                    else:
		      infilelist = 0
            elif mode == '-test':
                procFile = self.currentStr[self.currentStr.rfind('/')+1:-1]
                for value in moodList:
                    if procFile in value:
                        infilelist = 1
                        currentCluster = '?\n'
                        filelist.write(value[value.find('/'):value.find(' ')]+'\n')
            if (infilelist == 1):
                self.currentStr = self.currentStr[:self.currentStr.rfind(',')+1] + currentCluster
                self.outputfile.write(self.currentStr)
                self.currentStr = self.inputfile.readline()            
        filelist.close()
    def destroy(self):
        self.inputfile.close()
        self.outputfile.close()

def outputHandler(fileout):
    results = open(fileout,'w')
    testres = open('./test.txt')
    tmpfilelist = open('./tmpfilelist.txt').readlines()
    
    tmpstr=' '
    while ('inst#' not in tmpstr):
        tmpstr = testres.readline()
    for samplename in tmpfilelist:
        tmpstr=testres.readline()
        results.write(samplename[:-1]+tmpstr[tmpstr.rfind(':')+1:tmpstr.rfind(' ')])
    results.close()
    testres.close()
    tmpfilelist.close()    

'''
'''
           
if (sys.argv[1] != '-output'):
    featset = FeaturesHandler()
    featset.init(sys.argv[2], sys.argv[4])
    featset.addClasses(sys.argv[1], sys.argv[3])
    featset.destroy()
else:
    outputHandler(sys.argv[2])