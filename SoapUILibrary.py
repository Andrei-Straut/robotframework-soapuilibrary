#
# This file is part of SoapUI test library for the Robot Framework
#
# Copyright (c) 2012 by Pavlo Baron (pb[at]pbit[dot]org)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from com.eviware.soapui.tools import (SoapUITestCaseRunner)
from com.eviware.soapui.tools import (SoapUIMockServiceRunner)

from robot.api import logger

import thread
import socket
import os

class SoapUILibrary:
    """ The main class of the library """

    ROBOT_LIBRARY_SCOPE = 'TEST CASE'
    ROBOT_LIBRARY_VERSION = '0.2'

    def __init__(self):
        self.__runner = None
        self.__mockrunner = None
        self._project_properties = []

    def soapui_customize_project(self, project, suite, output_folder, export_all, endpoint):
        """
        Sets the most commonly used values to the project and suite given as parameters
        """
        self.__runner = SoapUITestCaseRunner()
        self.__runner.setProjectFile(project)
        self.__runner.setTestSuite(suite)
        self.soapui_set_output_folder(output_folder)
        self.soapui_set_export_all(export_all)
        self.soapui_set_endpoint(endpoint)
        self.soapui_set_print_report(True)

    def soapui_project(self, prj):
        """ Initialize the runner and set the project string """
        self.__runner = SoapUITestCaseRunner()
        self.__runner.setProjectFile(prj)
        self.soapui_set_print_report(True)

    def soapui_suite(self, s):
        """ Set the suite string """
        self.__runner.setTestSuite(s)

    def soapui_case(self, c):
        """ Set the test case string """
        self.__runner.setTestCase(c)

    def soapui_add_project_property(self, propertyName, propertyValue):
        """
        Adds a project property to properties dictionary.
        This assumes that you have already initialized the project via
        the `SoapUI Project` keyword.
        """
        prop = propertyName + '=' + propertyValue
        self._project_properties.append(prop)
        try:
            self.__runner.setProjectProperties(self._project_properties)
        except AttributeError:
            logger.warn('No project set. Cannot set project properties.')

    def soapui_set_project_property(self, *properties):
        """ Sets project properties for the current test run.
        This assumes that you have already initialized the project via
        the `SoapUI Project` keyword.

        `properites` may contain multiple statements, and each must be specified as: key=value.

        This is useful to data drive your existing SoapUI tests via property expansion.
        For more information see: http://www.soapui.org/Scripting-Properties/property-expansion.html

        Example:
        | SoapUI Project | My Project |
        | SoapUI Set Project Property | ServiceEndpoint=https://staging.company.com | # set a single property |
        | SoapUI Set Project Property | CustomProperty=foo | AnotherProperty=bar | # or set multiple properties |
        """
        for prop in properties:
            if len(prop.split('=')) == 2:
                self._project_properties.append(prop)
            else:
                logger.warn("Skipping property: '%s'. Properties must be specified as: key=value. Equals (=) sign in keys or values is not allowed" % prop)
        try:
            self.__runner.setProjectProperties(self._project_properties)
        except AttributeError:
            logger.warn('No project set. Cannot set project properties.')

    def soapui_run(self):
        """ Run the runner and report to Robot """
        logger.info("Running with the following project properties set: %s" % self._project_properties)
        if not self.__runner.run():
            raise AssertionError('FAIL: failed to run')

        n = self.__runner.getFailedTests().size()
        if n != 0:
            raise AssertionError('FAIL: ' + str(n) + ' tests failed')

    def soapui_start_mock_service(self, p, m):
        """ Runs a mock service """
        try:
            self.__mockrunner = SoapUIMockServiceRunner()
            self.__mockrunner.setProjectFile(p)
            self.__mockrunner.setMockService(m)
            self.__mockrunner.setBlock(False)
            self.__mockrunner.run()
        except Exception, e:
            raise AssertionError('FAIL: Error running the mock service ' + m + '. Reason: ' + str(e))

    def soapui_stop_mock_service(self):
        """ Stops the mock service """
        self.__mockrunner.stopAll()

    def soapui_set_endpoint(self, endpoint):
        self.__runner.setEndpoint(endpoint)

    def soapui_set_host(self, host):
        self.__runner.setHost(host)

    def soapui_set_password(self, password):
        self.__runner.setPassword(password)

    def soapui_set_username(self, username):
        self.__runner.setUsername(username)

    def soapui_set_domain(self, domain):
        self.__runner.setDomain(domain)

    def soapui_set_project_password(self, password):
        self.__runner.setProjectPassword(password)

    def soapui_set_output_folder(self, outputFolder):
        self.__runner.setOutputFolder(outputFolder)

    def soapui_set_export_all(self, exportAll):
        self.__runner.setExportAll(exportAll)

    def soapui_set_print_report(self, printReport):
        """ 
        Set whether a short report should be reported after the execution of each test case
        Return type is Python Boolean (True/False)
        """
        printReport=bool(printReport)
        self.__runner.setPrintReport(printReport)
    
    def soapui_get_test_case(self):
        return self.__runner.getTestCase()
