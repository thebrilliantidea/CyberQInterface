#!/usr/bin/python
"""
Class to interface with BBQ Guru's CyberQ Temperature Control System

**ChangeLog:**

=== ========== ========== ======================================================
Ver Date       Editor     Notes
=== ========== ========== ======================================================
0.1 09/29/2012 Bryan Kemp Initial Commit
0.9 11/03/2012 Bryan Kemp Added distools functionality
1.0 03/29/2013 Bryan Kemp First release
=== ========== ========== ======================================================
"""

__author__ = "Bryan Kemp <bryan@thebrilliantidea.com>"
__version__ = "1.0"
__date__ = '03/29/2013'
__license__ = "BSD New"
__license_text__ = """
Copyright (c) 2013, The Brilliant Idea
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 * Neither the name of the The Brilliant Idea, LLC. nor the names of its
   contributors may be used to endorse or promote products derived from this
   software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import requests
from lxml import objectify

from cyberqinterface_exceptions import *

class CyberQInterface:
    """
    Web Interface to BBQ Guru's CyberQ Temperature Controller System.
    """

    def __init__(self, host=None, headers=None):
        """
        **Description:**
        Initialiazer

        ** Keyword arguments:**
        * **<String>**  The hostname or IP of the CyberQ
        * (optional) **<Dictionary>** Header Name: Header Value

        Returns:
        <object> CyberQInterface

        **Example Usage:**
        .. code-block:: python
        cqi = CyberQInterface("10.0.1.5", {
                            "Content-type": "application/x-www-form-urlencoded",
                            "Accept": "text/plain"} )
        """
        self.validParameters = ["COOK_NAME", "COOK_SET", "FOOD1_NAME",
                                "FOOD1_SET", "FOOD2_NAME", "FOOD2_SET",
                                "FOOD3_NAME", "FOOD3_SET", "_COOK_TIMER",
                                "COOK_TIMER", "COOKHOLD", "TIMEOUT_ACTION",
                                "ALARMDEV", "COOK_RAMP", "OPENDETECT",
                                "CYCTIME", "PROPBAND", "MENU_SCROLLING",
                                "LCD_BACKLIGHT", "LCD_CONTRAST", "DEG_UNITS",
                                "ALARM_BEEPS", "KEY_BEEPS"]

        if headers == None:
            self.headers = {"Content-type": "application/x-www-form-urlencoded",
                            "Accept": "text/plain"}
        else:
            self.headers = headers
            
        self.host = host
        self.url = "http://"+host+"/"

    def sendUpdate(self, parameters):
        """
        **Description:** 
        sendUpdate validates new parameters and sends update to CyberQ

        **Possible parameters:**
    
        ==============  ========================================================
        Parameter Name  Definition 
        ==============  ========================================================
        COOK_NAME       Pit Sensor name in plain text
        COOK_SET        Pit probe target temp in current units
        FOOD1_NAME      Food 1 name in plain text
        FOOD1_SET       Food probe 1 target temp in current units
        FOOD2_NAME      Food 2 name in plain text
        FOOD2_SET       Food probe 2 target temp in current units
        FOOD3_NAME      Food 3 name in plain text
        FOOD3_SET       Food probe 3 target temp in current units
        _COOK_TIMER     Set the countdown timer HH:MM:SS (must use urlencoded
                        colons - \%3A
        COOK_TIMER      Same as above - looks like you need to set both to keep
                        changes across refresh?
        COOKHOLD        Cook and hold target temp in current units if timer is
                        set to HOLD
        TIMEOUT_ACTION  What to do when timer hits 00:00:00 (0: No Action, 1:
                        HOLD, 2: Alarm, 3:Shutdown) See 8.3.2 in manual
        ALARMDEV        Alarm deviation setpoint in current units (see 8.3.3 in
                        Manual)
        COOK_RAMP       Which probe to use for Ramp mode (0: Off, 1: Food 1, 2:
                        Food 2, 3:Food 3)
        OPENDETECT      Enable/Disable Lid Open detection (0: Off, 1:On)
        CYCTIME         Fan Cycle time in s (between 4 and 10 seconds)
        PROPBAND        Proportional band size (between 5-100 degF)
        MENU_SCROLLING  Enable/Disable LCD scrolling (0: Off, 1:On)
        LCD_BACKLIGHT   Enable/Disable LCD backlight (0: Off, 1:On)
        LCD_CONTRAST    Contrast percent?
        DEG_UNITS       Master Switch for degC/degF (0:degC, 1:degF)
        ALARM_BEEPS     Alarm beeps (0-5)
        KEY_BEEPS       Enable/Disable key beeps (0: Off, 1:On)
        ==============  ========================================================
        
        **Keyword arguments:**
        *<dictionary>* Dictionary of values to be updated. Note: will be validated against list of known values

        **Returns:**
        *<Boolean>* True if successful / False if not successful

        **Example Usage:**

    .. code-block:: python

            cqi.sendUpdate({'FOOD1_NAME' : "Tri-Tip Roast",
                            'FOOD1_SET': '140',
                            'COOK_SET' : '300'})
        """
        results = self._validateParameters(parameters)
        if results != {}:
            raise ParameterValidationException("Bad parameters passed", results)
        response = requests.post(self.url, data=parameters,
                                 headers=self.headers)
        if response.status_code == 200:
            return True
        else:
            raise ResponseHTTPException("%s Error: %s %s" %
                                        (response.status_code, response.url,
                                         response.reason),response)

    def _validateParameters(self, parameters):
        """
        Test all parameters against known set of keys
        #TODO: Provide better tests for values

        Keyword arguments:
        <dictionary> parameters - Key/Value pairs for CyberQ settings

        Returns:
        <string> {} - returns dictionary of all invalid parameters with reason

        Example Usage:
        self._validateParameters({'FOOD1_NAME' : "Tri-Tip Roast", 'FOOD1_SET': '140',
                        'COOK_SET' : '300'})
        """
        badParameters = {}
        for key in parameters.keys():
            if key not in self.validParameters:
                badParameters[key] = "Not a valid parameter"
        return badParameters

    def _getResponseObject(self, xml):
        """
        get data from CyberQ and return as an object

        Keyword arguments:
        <string> objectType

        Returns:
        Object of specifiedtype

        Example Usage:
        private
        """
        try:
            return objectify.fromstring(xml)
        except(Exception):
            raise ResponseValidationException("Invalid XML from CyberQ",
                                              xml)

    def _getResponseXML(self, objectURI):
        """
        get data from CyberQ and return an XML

        Keyword arguments:
        <string> objectType

        Returns:
        XML

        Example Usage:
        private
        """
        response = requests.get(self.url+objectURI)
        if response.status_code == 200:
            return response.text
        else:
            raise ResponseHTTPException("%s Error: %s %s" %
                                        (response.status_code, response.url,
                                         response.reason),response)

    def getConfig(self):
        """
        Get Configuration from CyberQ

        Keyword arguments:
        None

        Returns:
        Config Object

        Example Usage:
        print cqi.getConfig().FOOD1_TEMP
        """
        return self._getResponseObject(self.getConfigXML())

    def getStatus(self):
        """
        Get Status from CyberQ

        Keyword arguments:
        None

        Returns:
        Status Object

        Example Usage:
        print cqi.getStatus().FOOD1_TEMP
        """
        return self._getResponseObject(self.getStatusXML())

    def getAll(self):
        """
        Get All parameters from CyberQ

        Keyword arguments:
        None

        Returns:
        All Object

        Example Usage:
        cqi.getAll()
        """
        return self._getResponseObject(self.getAllXML())

    def getConfigXML(self):
        """
        Get ConfigXML from CyberQ

        Keyword arguments:
        None

        Returns:
        Config Object in XML

        Example Usage:
        cqi.getStatus()
        """
        return self._getResponseXML("config.xml")

    def getStatusXML(self):
        """
        Get StatusXML from CyberQ

        Keyword arguments:
        None

        Returns:
        Status Object

        Example Usage:
        cqi.getStatusXML()
        """
        return self._getResponseXML("status.xml")

    def getAllXML(self):
        """
        Get AllXML from CyberQ

        Keyword arguments:
        None

        Returns:
        All Xml

        Example Usage:
        cqi.getAllXML()
        """
        return self._getResponseXML("all.xml")

    def _lookup(self, table, code):
        """
        Lookup internal values by code. There are several values in the API
        returned as Integers. This provides a means to look up a more useful
        text reprentation

        Keyword arguments:
        <String> table - name of the table to find the code
        <int> code - number of the code returned by the API.
        Returns:
        String
        
        Raises: LookupException

        Example Usage:
        private
        """
        codes = {
        "status" : ["OK", "HIGH", "LOW", "DONE", "ERROR", "HOLD", "ALARM",
                      "SHUTDOWN"],
        "temperature" : ["CELSIUS", "FAHRENHEIT"],
        "ramp" : ["OFF", "FOOD1", "FOOD2", "FOOD3"]
            }
        if isinstance(code, objectify.IntElement):
            code = int(code)
        
        if not codes.has_key(table):
            raise LookupException("No lookup table for: %s", table)
        try:
            return codes[table][code]
        except IndexError as e:
            raise LookupException("No value for code %s in lookup table %s" %
                                  (code, table), e)
        
    def statusLookup(self, code):
        """
        Provides a text meaning for a given status code
        "status" : ["OK", "HIGH", "LOW", "DONE", "ERROR", "HOLD", "ALARM",
                      "SHUTDOWN"],
                      
        ============== ============
        Value from API String Value
        ============== ============
        0              OK
        1              HIGH
        2              LOW
        3              DONE
        4              ERROR
        5              HOLD
        6              ALARM
        7              SHUTDOWN
        ============== ============

        Keyword arguments:
        <int> code - the code returned in the object or the XML.

        Returns:
        <String> Meaning behind the code

        Example Usage:
        cqi.statusLookup(cqi.getConfig().FOOD1_STATUS)
        """
        return self._lookup("status", code)

    def temperatureLookup(self, code):
        """
        Provides a text meaning for the temperature scale in use
        temperature" : ["CELSIUS", "FAHRENHEIT"]
        
        ============== ============
        Value from API String Value
        ============== ============
        0              CELSIUS
        1              FAHRENHEIT
        ============== ============
        
        Keyword arguments:
        <int> code - the code returned in the object or XML.

        Returns:
        <String> 'Celsius' or 'Fahrenheit'

        Example Usage:
        cqi.temperatureLookup(cqi.getStatus().DEG_UNITS)
        """
        return self._lookup("temperature", code)

    def rampLookup(self, code):
        """
        Provides a text representation of the food that is monitored for ramping

        ============== ============
        Value from API String Value
        ============== ============
        0              OFF
        1              FOOD1
        2              FOOD2
        3              FOOD3
        ============== ============

        Keyword arguments:
        <int> code - the code from the object or xml

        Returns:
        <String> Which food, if any, is being monitored for ramping

        Example Usage:
        cqi.rampLookup(cqi.getStatus().COOK_RAMP)
        """
        return self._lookup("ramp", code)

if __name__ == "__main__": # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(
        description="""CyberQ Interface class. No real executable code""",
        epilog=
        """
        Lets go grillin'
        """)

    parser.add_argument(
        '-d', "--docs",
        action='store_true',
        help="""display the pydoc documentation""")

    parser.add_argument(
        '-v', "--version",
        action='store_true',
        help="""get version information for this file""")

    parser.add_argument(
        '-l', "--license",
        action='store_true',
        help="""display license information for this file""")

    args = parser.parse_args()

    if args.docs == True:
        help(CyberQInterface)

    if args.version == True:
        print "Version: %s" % __version__
        print "Last Modified: %s" % __date__

    if args.license == True:
        print "License: %s" % __license__
        print __license_text__
