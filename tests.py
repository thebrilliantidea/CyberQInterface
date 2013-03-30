#!/usr/bin/python
"""
Test Cases for the CyberQInterface Library

ChangeLog:
A00 - 11/04/2012 - Bryan Kemp - Initial release
"""

__author__ = "Bryan Kemp <bryan@thebrilliantidea.com>"
__version__ = "A00"
__date__ = '11/04/2012'
__license__ = "BSD New"
__license_text__ = """
Copyright (c) 2012, The Brilliant Idea
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 * Neither the name of the The Brilliant Idea, LLC. nor the names of its contributors may
   be used to endorse or promote products derived from this software without
   specific prior written permission.

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

import unittest
import requests
from mock import patch
from cyberqinterface.cyberqinterface import CyberQInterface
from cyberqinterface.cyberqinterface_exceptions import *
TestCyberQInterfaceSuite = unittest.TestLoader()

class TestCyberQInterfaceInit(unittest.TestCase):
    """Test that the initializer works and gets all of the needed variables"""
    def setUp(self):
        pass

    def tearDown(self):
        """None"""
        pass

    def testProperInit(self):
        """Test host property is set to proper value"""
        cqi = CyberQInterface("localhost")
        self.assertEqual(cqi.host, "localhost")

    def testInitWithHeaders(self):
        """Test supplying custom headers"""
        cqi = CyberQInterface("localhost", {"Test-Header": "Test"})
        self.assertEqual(cqi.headers["Test-Header"], "Test")

TestCyberQInterfaceSuite.loadTestsFromTestCase(TestCyberQInterfaceInit)

class TestCyberQInterfaceValidateParameters(unittest.TestCase):
    """Test to make sure that the validate parameters function is working"""
    def setUp(self):
        """Setup: None"""

    def tearDown(self):
        """TearDown: None"""
        pass

    def testAllParameters(self):
        """Test the full set of parameters are correct"""
        cqi = CyberQInterface("127.0.0.1")
        assert cqi._validateParameters( {"COOK_NAME": 1, "COOK_SET": 1,
                                         "FOOD1_NAME": 1, "FOOD1_SET": 1,
                                         "FOOD2_NAME": 1, "FOOD2_SET": 1,
                                         "FOOD3_NAME": 1, "FOOD3_SET": 1,
                                         "_COOK_TIMER": 1, "COOK_TIMER": 1,
                                         "COOKHOLD": 1, "TIMEOUT_ACTION": 1,
                                         "ALARMDEV": 1, "COOK_RAMP": 1,
                                         "OPENDETECT": 1, "CYCTIME": 1,
                                         "PROPBAND": 1, "MENU_SCROLLING": 1,
                                         "LCD_BACKLIGHT": 1, "LCD_CONTRAST": 1,
                                         "DEG_UNITS": 1, "ALARM_BEEPS": 1,
                                         "KEY_BEEPS": 1}) == {}

    def testBadParameters(self):
        """Test parameters with 3 bad parameters"""
        cqi = CyberQInterface("127.0.0.1")
        assert len(cqi._validateParameters( {"COK_NAME": 1, "COOK_SET": 1,
                                             "FOOD1_NAME": 1, "FOOD1_SET": 1,
                                             "FOOD2_NAME": 1, "FOOD2_SET": 1,
                                             "FOOD3_NAME": 1, "FOOD3_SET": 1,
                                             "_COOK_TIMER": 1, "COOK_TIMER": 1,
                                             "COOKHOLD": 1, "TIEOUT_ACTION": 1,
                                             "ALARMDEV": 1, "COOK_RAMP": 1,
                                             "OPENDETECT": 1, "CYCTIME": 1,
                                             "PROPBAND": 1, "MNU_SCROLLING": 1,
                                             "LCD_BACKLIGHT": 1,
                                             "LCD_CONTRAST": 1, "DEG_UNITS": 1,
                                             "ALARM_BEEPS": 1,
                                             "KEY_BEEPS": 1})) == 3
TestCyberQInterfaceSuite.loadTestsFromTestCase(
    TestCyberQInterfaceValidateParameters)

class TestCyberQInterfaceRequests(unittest.TestCase):
    """
    Test the interaction with the CyberQ web interface and XML to object
    translation
    """

    def setUp(self):
        """Setup: None"""

    def tearDown(self):
        """TearDown: None"""

    def testInvalidReturnCode(self):
        """
        Test that the proper exception is thrown if the server returns bad
        status code
        """
        with patch.object(requests, 'get') as mockMethod:
            with self.assertRaises(ResponseHTTPException):
                cqi = CyberQInterface("127.0.0.1")
                mockMethod.return_value.status_code = 500
                cqi.getConfigXML()

    def testValidReturnCode(self):
        """Test that a 200 code returns a string"""
        with patch.object(requests, 'get') as mockMethod:
            mockMethod.return_value.status_code = 200
            mockMethod.return_value.text = "testcase"
            xml = CyberQInterface("127.0.0.1").getConfigXML()
            self.assertEqual(xml, "testcase")

    def testGetStatusWithBadXML(self):
        """Test that the correct Object is returned"""
        with patch.object(requests, 'get') as mockMethod:
            with self.assertRaises(ResponseValidationException):
                mockMethod.return_value.status_code = 200
                mockMethod.return_value.text = """
<nutcstatus>
<!--all temperatures are displayed in tenths F, regardless of setting of unit-->
<!--all temperatures sent by browser to unit should be in F.  you can send-->
<!--tenths F with a decimal place, ex: 123.5-->
<OUTPUT_PERCENT>100</OUTPUT_PERCENT>
<TIMER_CURR>00:00:00</TIMER_CURR>
<COOK_TEMP>3343</COOK_TEMP>
<FOOD1_TEMP>823</FOOD1_TEMP>
<FOOD2_TEM2_TEMP>
<FOOD3_TEMP>OPEN</FOOD3_TEMP>
<COOK_STATUS>0</COOKTUS>
<FOOD1_STATUS>0</FOOD1_STATUS>
<FOOD2_STATUS>4</FOOD2_STATUS>
<FOOD3_STATUS>4</FOOD3_STATUS>
<TIMER_STATUS>0</TIMER_STATUS>
<DEG_UNITS>1</DEG_UNITS>
<COOK_CYCTIME>6</COOK_CYCTIME>
<COOK_PROPBAND>500</COOK_PROPBAND>
<COOK_RAMP>0</COOK_RAMP>
</nutcstatus>"""
                CyberQInterface("127.0.0.1").getStatus()

    def testGetStatus(self):
        """Test that the correct Object is returned"""
        with patch.object(requests, 'get') as mockMethod:
            mockMethod.return_value.status_code = 200
            mockMethod.return_value.text = """
<nutcstatus>
<!--all temperatures are displayed in tenths F, regardless of setting of unit-->
<!--all temperatures sent by browser to unit should be in F.  you can send-->
<!--tenths F with a decimal place, ex: 123.5-->
<OUTPUT_PERCENT>100</OUTPUT_PERCENT>
<TIMER_CURR>00:00:00</TIMER_CURR>
<COOK_TEMP>3343</COOK_TEMP>
<FOOD1_TEMP>823</FOOD1_TEMP>
<FOOD2_TEMP>OPEN</FOOD2_TEMP>
<FOOD3_TEMP>OPEN</FOOD3_TEMP>
<COOK_STATUS>0</COOK_STATUS>
<FOOD1_STATUS>0</FOOD1_STATUS>
<FOOD2_STATUS>4</FOOD2_STATUS>
<FOOD3_STATUS>4</FOOD3_STATUS>
<TIMER_STATUS>0</TIMER_STATUS>
<DEG_UNITS>1</DEG_UNITS>
<COOK_CYCTIME>6</COOK_CYCTIME>
<COOK_PROPBAND>500</COOK_PROPBAND>
<COOK_RAMP>0</COOK_RAMP>
</nutcstatus>"""
            status = CyberQInterface("127.0.0.1").getStatus()
            self.assertEqual(status.tag, "nutcstatus")

    def testGetAll(self):
        """Test that the All Object is returned"""
        with patch.object(requests, 'get') as mockMethod:
            with self.assertRaises(AttributeError):
                mockMethod.return_value.status_code = 200
                mockMethod.return_value.text = """
<nutcallstatus>
<!--this is similar to status.xml, but with more values-->
<!--all temperatures are displayed in tenths F, regardless of setting of unit-->
<!--all temperatures sent by browser to unit should be in F.  you can send-->
<!--tenths F with a decimal place, ex: 123.5-->
<COOK>
  <COOK_NAME>Big Green Egg</COOK_NAME>
  <COOK_TEMP>3216</COOK_TEMP>
  <COOK_SET>4000</COOK_SET>
  <COOK_STATUS>0</COOK_STATUS>
</COOK>
<FOOD1>
  <FOOD1_NAME>Chicken Quarters</FOOD1_NAME>
  <FOOD1_TEMP>1482</FOOD1_TEMP>
  <FOOD1_SET>1750</FOOD1_SET>
  <FOOD1_STATUS>0</FOOD1_STATUS>
</FOOD1>
<FOOD2>
  <FOOD2_NAME>Food2</FOOD2_NAME>
  <FOOD2_TEMP>OPEN</FOOD2_TEMP>
  <FOOD2_SET>1000</FOOD2_SET>
  <FOOD2_STATUS>4</FOOD2_STATUS>
</FOOD2>
<FOOD3>
  <FOOD3_NAME>Food3</FOOD3_NAME>
  <FOOD3_TEMP>OPEN</FOOD3_TEMP>
  <FOOD3_SET>1000</FOOD3_SET>
  <FOOD3_STATUS>4</FOOD3_STATUS>
</FOOD3>
<OUTPUT_PERCENT>100</OUTPUT_PERCENT>
<TIMER_CURR>00:00:00</TIMER_CURR>
<TIMER_STATUS>0</TIMER_STATUS>
<DEG_UNITS>1</DEG_UNITS>
<COOK_CYCTIME>6</COOK_CYCTIME>
<COOK_PROPBAND>500</COOK_PROPBAND>
<COOK_RAMP>0</COOK_RAMP>
</nutcallstatus>
"""
                allObj = CyberQInterface("127.0.0.1").getAll()
                self.assertNotEqual(allObj.CONTROL.OPENDETECT, 1)

    def testGetConfig(self):
        """Test that the config Object is returned"""
        with patch.object(requests, 'get') as mockMethod:
            mockMethod.return_value.status_code = 200
            mockMethod.return_value.text = """
<nutcallstatus>
<!--this is similar to all.xml, but with more values-->
<!--all temperatures are displayed in tenths F, regardless of setting of unit-->
<!--all temperatures sent by browser to unit should be in F.  you can send-->
<!--tenths F with a decimal place, ex: 123.5-->
<COOK>
  <COOK_NAME>Big Green Egg</COOK_NAME>
  <COOK_TEMP>3220</COOK_TEMP>
  <COOK_SET>4000</COOK_SET>
  <COOK_STATUS>0</COOK_STATUS>
</COOK>
<FOOD1>
  <FOOD1_NAME>Chicken Quarters</FOOD1_NAME>
  <FOOD1_TEMP>1493</FOOD1_TEMP>
  <FOOD1_SET>1750</FOOD1_SET>
  <FOOD1_STATUS>0</FOOD1_STATUS>
</FOOD1>
<FOOD2>
  <FOOD2_NAME>Food2</FOOD2_NAME>
  <FOOD2_TEMP>OPEN</FOOD2_TEMP>
  <FOOD2_SET>1000</FOOD2_SET>
  <FOOD2_STATUS>4</FOOD2_STATUS>
</FOOD2>
<FOOD3>
  <FOOD3_NAME>Food3</FOOD3_NAME>
  <FOOD3_TEMP>OPEN</FOOD3_TEMP>
  <FOOD3_SET>1000</FOOD3_SET>
  <FOOD3_STATUS>4</FOOD3_STATUS>
</FOOD3>
<OUTPUT_PERCENT>100</OUTPUT_PERCENT>
<TIMER_CURR>00:00:00</TIMER_CURR>
<TIMER_STATUS>0</TIMER_STATUS>
<SYSTEM>
  <MENU_SCROLLING>1</MENU_SCROLLING>
  <LCD_BACKLIGHT>47</LCD_BACKLIGHT>
  <LCD_CONTRAST>10</LCD_CONTRAST>
  <DEG_UNITS>1</DEG_UNITS>
  <ALARM_BEEPS>0</ALARM_BEEPS>
  <KEY_BEEPS>0</KEY_BEEPS>
</SYSTEM>
<CONTROL>
  <TIMEOUT_ACTION>0</TIMEOUT_ACTION>
  <COOKHOLD>2000</COOKHOLD>
  <ALARMDEV>500</ALARMDEV>
  <COOK_RAMP>0</COOK_RAMP>
  <OPENDETECT>1</OPENDETECT>
  <CYCTIME>6</CYCTIME>
  <PROPBAND>500</PROPBAND>
</CONTROL>
<WIFI>
  <IP>10.0.1.30</IP>
  <NM>255.255.255.0</NM>
  <GW>10.0.1.1</GW>
  <DNS>10.0.1.1</DNS>
  <WIFIMODE>0</WIFIMODE>
  <DHCP>0</DHCP>
  <SSID>Wireless Network</SSID>
  <WIFI_ENC>6</WIFI_ENC>
  <WIFI_KEY>SsecretKey</WIFI_KEY>
  <HTTP_PORT>80</HTTP_PORT>
</WIFI>
<SMTP>
  <SMTP_HOST>smtp.hostname.com</SMTP_HOST>
  <SMTP_PORT>0</SMTP_PORT>
  <SMTP_USER></SMTP_USER>
  <SMTP_PWD></SMTP_PWD>
  <SMTP_TO>destination@someplace.com</SMTP_TO>
  <SMTP_FROM>source@someplace.com</SMTP_FROM>
  <SMTP_SUBJ>Temperature Controller Status E-Mail</SMTP_SUBJ>
  <SMTP_ALERT>0</SMTP_ALERT>
</SMTP>
</nutcallstatus>
"""
            configObj = CyberQInterface("127.0.0.1").getConfig()
            self.assertEqual(configObj.CONTROL.OPENDETECT, 1)

    def testSendUpdate(self):
        """
        Test the ability to send a message to the CyberQ with good parameters
        """
        with patch.object(requests, 'post') as mockMethod:
            mockMethod.return_value.status_code = 200
            cqi = CyberQInterface("127.0.0.1")
            self.assertEqual(cqi.sendUpdate({'FOOD1_NAME' : "Tri-Tip Roast",
                                             'FOOD1_SET': '140',
                                             'COOK_SET' : '300'}),True)

    def testSendUpdateWithBadParameters(self):
        """
        Test the ability to send a message to the CyberQ with bad parameters
        """
        with patch.object(requests, 'post') as mockMethod:
            with self.assertRaises(ParameterValidationException):
                mockMethod.return_value.status_code = 200
                cqi = CyberQInterface("127.0.0.1")
                cqi.sendUpdate({'FOOD1_NME' : "Tri-Tip Roast",
                                'FOOD1_SET': '140', 'COOK_SET' : '300'})

    def testSendUpdateWithBadResponse(self):
        """
        Test the ability to send a message to the CyberQ with good parameters
        but a bad response
        """
        with patch.object(requests, 'post') as mockMethod:
            with self.assertRaises(ResponseHTTPException):
                mockMethod.return_value.status_code = 500
                cqi = CyberQInterface("127.0.0.1")
                cqi.sendUpdate({'FOOD1_NAME' : "Tri-Tip Roast",
                                'FOOD1_SET': '140', 'COOK_SET' : '300'})

TestCyberQInterfaceSuite.loadTestsFromTestCase(TestCyberQInterfaceRequests)

class TestCyberQInterfaceLookups(unittest.TestCase):
    """Test the lookup functionality for temperature, status, and ramp"""
    def setUp(self):
        """Setup: None"""
        pass

    def tearDown(self):
        """TearDown: None"""
        pass

    def testRampLookups(self):
        """Test that all known ramp codes work"""
        cqi = CyberQInterface("127.0.0.1")
        rampCodes = ["OFF", "FOOD1", "FOOD2", "FOOD3"]
        for code in range (0, len(rampCodes)-1):
            self.assertEqual(cqi.rampLookup(code), rampCodes[code])

    def testStatusLookups(self):
        """Test that all known status codes work"""
        cqi = CyberQInterface("127.0.0.1")
        statusCodes = ["OK", "HIGH", "LOW", "DONE", "ERROR", "HOLD", "ALARM",
                      "SHUTDOWN"]
        for code in range (0, len(statusCodes)-1):
            self.assertEqual(cqi.statusLookup(code), statusCodes[code])

    def testTemperatureLookups(self):
        """Test that all known temperature codes work"""
        cqi = CyberQInterface("127.0.0.1")
        temperatureCodes = ["CELSIUS", "FAHRENHEIT"]
        for code in range (0, len(temperatureCodes)-1):
            self.assertEqual(cqi.temperatureLookup(code),
                             temperatureCodes[code])

    def testBadTableName(self):
        """Test that an unknown table produces a known exception"""
        with self.assertRaises(LookupException):
            cqi = CyberQInterface("127.0.0.1")
            cqi._lookup("badtable", 0)

    def testInvalidCodeNumber(self):
        """Test that an index out of range is handled"""
        with self.assertRaises(LookupException):
            cqi = CyberQInterface("127.0.0.1")
            cqi._lookup("temperature", 4)
            
    def testLookupFromStatusObject(self):
        """Test that the code from an actual status object works properly"""
        with patch.object(requests, 'get') as mockMethod:
            mockMethod.return_value.status_code = 200
            mockMethod.return_value.text = """
<nutcstatus>
<!--all temperatures are displayed in tenths F, regardless of setting of unit-->
<!--all temperatures sent by browser to unit should be in F.  you can send-->
<!--tenths F with a decimal place, ex: 123.5-->
<OUTPUT_PERCENT>100</OUTPUT_PERCENT>
<TIMER_CURR>00:00:00</TIMER_CURR>
<COOK_TEMP>3343</COOK_TEMP>
<FOOD1_TEMP>823</FOOD1_TEMP>
<FOOD2_TEMP>OPEN</FOOD2_TEMP>
<FOOD3_TEMP>OPEN</FOOD3_TEMP>
<COOK_STATUS>0</COOK_STATUS>
<FOOD1_STATUS>0</FOOD1_STATUS>
<FOOD2_STATUS>4</FOOD2_STATUS>
<FOOD3_STATUS>4</FOOD3_STATUS>
<TIMER_STATUS>0</TIMER_STATUS>
<DEG_UNITS>1</DEG_UNITS>
<COOK_CYCTIME>6</COOK_CYCTIME>
<COOK_PROPBAND>500</COOK_PROPBAND>
<COOK_RAMP>0</COOK_RAMP>
</nutcstatus>"""
            cqi = CyberQInterface("127.0.0.1")
            status = cqi.getStatus()
            self.assertEqual(cqi.statusLookup(status.FOOD1_STATUS),"OK")
  
TestCyberQInterfaceSuite.loadTestsFromTestCase(TestCyberQInterfaceLookups)

if __name__ == '__main__':
    import nose
    nose.main()
