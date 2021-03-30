'''
Created on 29.03.2021

@author: HD
'''

import os
import requests
from pyenzyme.enzymeml.tools import EnzymeMLReader

class NBHelper:

    _workspace = None
    _apiUrl = None
    _enzmldoc = None

    def __init__(self, apiURL):
        '''
        Helper Class for general notebook functions 
        '''
        self._apiUrl = apiURL

    def getWorkspace(self):
        return self._workspace

    def getEnzymeMLDoc(self):
        return self._enzmldoc

    def setWorkspace(self, ws):
        if not(ws is None):
            self._workspace=ws

    def convertSpreadsheet(self, path, name):
        if len(name)==0:
            name = os.path.splitext(os.path.basename(path))[0]
        if not name.lower().endswith('.omex'):
            name = name + '.omex'
        excelBinary = self.readBinary(path)
        newOmex = self.reqUnknown(excelBinary)
        if newOmex[0] == 200:
            self.writeBinary(os.path.join(self._workspace,name),newOmex[1])
            #self._enzmldoc = EnzymeMLReader().readFromFile(os.path.join(self._workspace,name))
            # TODO 
            # MOCKUP - start
            self._enzmldoc = EnzymeMLReader().readFromFile('./datasets/Rother/ApPDC.omex')
            # MOCKUP - end
        return newOmex[0]
            


    def readBinary(self, inPath):
        '''
        Reads binary files 

        Args:
            inPath (string): Path to binary file
        Returns:
            FileIO TODO
        '''
        if os.path.exists(inPath):
            return open(inPath, 'rb').read()

    def writeBinary(self, outPath, inBinary):
        '''
        Writes binary files 

        Args:
            outPath (string): Path to store binary file
            inBinary (string): String with binary content
        '''
        f = open(outPath, 'wb')
        f.write(inBinary)
        f.close()

    def writeText(self, outPath, inText):
        '''
        Writes text file

        Args:
            outPath (string): Path to store text file
            inBinary (string): String with content
        '''
        f = open(outPath, 'w')
        f.write(inText)
        f.close()

    def reqRead(self, omexPath):
        '''
        Sends read request to EnzymeML-API

        Args:
            omexPath (string): path to omex
        Returns:
            response_status_code (string): status code of response, 200 everything fine, 500 Error
            response_content (string): json-formated EnzymeML document
        '''
        endpoint_read = f"{self._apiUrl}/read"
        payload={}
        name = os.path.split(omexPath)[1]
        files=[
            ('omex',(name,open(omexPath,'rb'),'application/octet-stream'))
        ]
        headers = {}
        response = requests.request("GET", endpoint_read, headers=headers, data=payload, files=files)
        return [response.status_code,response.content]

    def reqUnknown(self, excelBinary):
        '''
        Sends unknown request to EnzymeML-API

        Args:
            excelBinary (string): excel content
        Returns:
            response_status_code (string): status code of response, 200 everything fine, 500 Error
            response_content (string): json-formated EnzymeML document
        '''
        #TODO replace MOCKUP
        # MOCKUP - start
        endpoint_create = f"{self._apiUrl}/create"
        payload = open('./datasets/API-Test-Fantasy.json', 'r').read()
        headers = {
        'Content-Type': 'text/plain'
        }

        response = requests.request("POST", endpoint_create, headers=headers, data=payload)
        return [response.status_code,response.content]
        # MOCKUP - end