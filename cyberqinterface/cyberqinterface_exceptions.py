"""
Exceptions for use with libary for BBQ Guru's CyberQ Temperature Control System

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

class ResponseValidationException(Exception):
    """The response from the CyberQ web service was invalid."""
    def __init__(self, message=None, errors=None):
        Exception.__init__(self, message)
        if errors != None:
            self.errors = errors

class ParameterValidationException(Exception):
    """An invalid parameter was passed to the interface"""
    def __init__(self, message=None, errors=None):
        Exception.__init__(self, message)
        if errors != None:
            self.errors = errors

class ResponseHTTPException(Exception):
    """The HTTP response was invalid"""
    def __init__(self, message=None, errors=None):
        Exception.__init__(self, message)
        if errors != None:
            self.errors = errors

class LookupException(Exception):
    """The lookup failed"""
    def __init__(self, message=None, errors=None):
        Exception.__init__(self, message)
        if errors != None:
            self.errors = errors