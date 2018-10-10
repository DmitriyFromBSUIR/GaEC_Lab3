
#
import sys
import os
import datetime as dt
import re
import tokenize as tok
#
import Globals as glb


class AlgoDeclListParser:
    def __init__(self, scriptFilepath=glb.ALGORITHMS_DECL_LIST_SCRIPT_FILEPATH, isDebug=False):
        self.__scriptFilepath = scriptFilepath
        self.__algorithmsParams = dict()
        self.__paramNameRexExp = r'[A-Z_][A-Z_0-9]*'
        self.__paramNamePattern = re.compile(self.__paramNameRexExp)
        self.__isDebug = isDebug

    @property
    def scriptFilepath(self):
        return self.__scriptFilepath

    @property
    def algorithmsParams(self):
        return self.__algorithmsParams

    def specialTokenize(self):
        print(glb.ALGORITHMS_DECL_LIST_SCRIPT_FILEPATH)
        enumName = None
        with open(glb.ALGORITHMS_DECL_LIST_SCRIPT_FILEPATH, 'rb') as f:
            for tokInfo in tok.tokenize(f.readline):
                if self.__isDebug:
                    print(tokInfo.type)
                    print(tokInfo.string)
                    print(tokInfo.start)
                    print(tokInfo.end)
                    print(tokInfo.line)
                if tokInfo.type == 1 and tokInfo.string == "class":
                    leftAndRightStmtParts = tokInfo.line.split(" ")
                    rightStmtPart = leftAndRightStmtParts[1]
                    enumName = rightStmtPart.split("(Enum)")[0]
                    if self.__isDebug:
                        print(" === enum name: ", enumName)
                    self.__algorithmsParams.update({enumName: list()})
                if tokInfo.type == 1 and self.__paramNamePattern.fullmatch(tokInfo.string):
                    self.__algorithmsParams[enumName].append(tokInfo.string)
                    if self.__isDebug:
                        print("param name: ", tokInfo.string)

    def printAlgoParamsInReadableView(self, t, s):
        if not isinstance(t, dict) and not isinstance(t, list):
            print("\t" * s + str(t))
        else:
            for key in t:
                print("\t" * s + str(key))
                if not isinstance(t, list):
                    self.printAlgoParamsInReadableView(t[key], s + 1)
            print()

    def run(self):
        try:
            self.specialTokenize()
            print("algorithmsParams: ")
            self.printAlgoParamsInReadableView(self.__algorithmsParams, 0)
        except Exception as e:
            print("[", dt.datetime.now(), "], LOG: ", e)


if __name__ == '__main__':
    algoDeclListParser = AlgoDeclListParser(scriptFilepath=glb.ALGORITHMS_DECL_LIST_SCRIPT_FILEPATH, isDebug=False)
    algoDeclListParser.run()