
#
import re
import datetime as dt
#
import Globals as glb


class Record:
    def __init__(self, x=0, y=0, id=-1):
        self.__x = x
        self.__y = y
        self.__id = id

    def __repr__(self):
        return "Record( id: " + str(self.__id) + ", x: " + str(self.x) + ", y: " + str(self.y) + ")"

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def id(self):
        return self.__id


class FileWorker:

    def __init__(self, citiesFilepath=glb.CITIES_FILEPATH, optTourFilepath=glb.OPTIMAL_TOUR_FILEPATH):
        self.__citiesFilepath = citiesFilepath
        self.__citiesFileMetadata = dict()
        self.__citiesCoordsList = list()
        self.__optTourFilepath = optTourFilepath
        self.__optTourFileMetadata = dict()
        self.__optTourPointIdList = list()
        self.__strContainsDigitsOnlyRegExp = r'^[-?\d+(\s+?)]+$'
        self.__strContainsDigitsOnlyPattern = re.compile(self.__strContainsDigitsOnlyRegExp)
        self.__fileHeaderSep = ':'
        self.__filePayloadSep = " "

    @property
    def getCitiesFileMetadata(self):
        return self.__citiesFileMetadata

    @property
    def getOptTourFileMetadata(self):
        return self.__optTourFileMetadata

    @property
    def getCitiesCoordsList(self):
        return self.__citiesCoordsList

    @property
    def getOptTourPointIdList(self):
        return self.__optTourPointIdList

    def parseMetadata(self, f):
        pass

    def saveCitiesFileMetadata(self):
        with open(self.__citiesFilepath, "r") as f:
            lines = [line.rstrip('\n') for line in f]
            for line in lines:
                if (not self.__strContainsDigitsOnlyPattern.fullmatch(line)) and (line != "EOF"):
                    parts = line.split(self.__fileHeaderSep)
                    nParts = len(parts)
                    if nParts == 2:
                        prop = parts[0]
                        val = parts[1]
                        self.__citiesFileMetadata.update({prop: val})
                    if nParts == 1:
                        prop = parts[0]
                        val = None
                        self.__citiesFileMetadata.update({prop: val})

    def saveOptTourFileMetadata(self):
        with open(self.__optTourFilepath, "r") as f:
            #content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            #lines = [x.strip() for x in content]
            lines = [line.rstrip('\n') for line in f]
            for line in lines:
                if (not self.__strContainsDigitsOnlyPattern.fullmatch(line)) and (line != "EOF"):
                    parts = line.split(self.__fileHeaderSep)
                    nParts = len(parts)
                    if nParts == 2:
                        prop = parts[0]
                        val = parts[1]
                        self.__optTourFileMetadata.update({prop: val})
                    if nParts == 1:
                        prop = parts[0]
                        val = None
                        self.__optTourFileMetadata.update({prop: val})

    def readFileHeader(self, isPerfectFile=False):
        if not isPerfectFile:
            self.saveCitiesFileMetadata()
        else:
            self.saveOptTourFileMetadata()

    def findRecordByPointId(self, pointId):
        for record in self.__citiesCoordsList:
            if(int(pointId) == record.id):
                return record
        return None

    def saveCitiesFilePayload(self):
        with open(self.__citiesFilepath, "r") as f:
            lines = [line.rstrip('\n') for line in f]
            for line in lines:
                if self.__strContainsDigitsOnlyPattern.fullmatch(line):
                    parts = line.split(self.__filePayloadSep)
                    nParts = len(parts)
                    if nParts == 3:
                        pointId = parts[0]
                        x = parts[1]
                        y = parts[2]
                        record = Record(x=int(x), y=int(y), id=int(pointId))
                        self.__citiesCoordsList.append(record)

    def saveOptTourFilePayload(self):
        with open(self.__optTourFilepath, "r") as f:
            lines = [line.rstrip('\n') for line in f]
            for line in lines:
                if self.__strContainsDigitsOnlyPattern.fullmatch(line):
                    parts = line.split(self.__filePayloadSep)
                    nParts = len(parts)
                    if nParts == 1:
                        pointId = parts[0]
                        record = self.findRecordByPointId(pointId)
                        if record is not None:
                            x = 0
                            y = 0
                            if record is not None:
                                x = record.x
                                y = record.y
                                point = Record(x=int(x), y=int(y), id=int(pointId))
                                self.__optTourPointIdList.append(point)

    def readPayload(self, isPerfectFile=False):
        if not isPerfectFile:
            self.saveCitiesFilePayload()
        else:
            self.saveOptTourFilePayload()

    def read(self):
        self.readFileHeader(isPerfectFile=False)
        self.readPayload(isPerfectFile=False)
        self.readFileHeader(isPerfectFile=True)
        self.readPayload(isPerfectFile=True)

    def run(self):
        #try:
            self.read()
            return self.__citiesFileMetadata, self.__optTourFileMetadata, \
                   self.__citiesCoordsList, self.__optTourPointIdList
        #except Exception as e:
        #    print("[", dt.datetime.now(), ", LOG] ", e)