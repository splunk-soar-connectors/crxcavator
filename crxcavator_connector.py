# File: crxcavator_connector.py
#
# Copyright (c) 2020 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

# Usage of the consts file is recommended
from crxcavator_consts import *
import requests
import json
from bs4 import BeautifulSoup
import re
from bs4 import UnicodeDammit
import sys


class RetVal(tuple):

    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class CrxcavatorConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(CrxcavatorConnector, self).__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None

    def _handle_py_ver_compat_for_input_str(self, input_str):
        """
        This method returns the encoded|original string based on the Python version.
        :param input_str: Input string to be processed
        :return: input_str (Processed input string based on following logic 'input_str - Python 3; encoded input_str - Python 2')
        """

        try:
            if input_str and self._python_version == 2:
                input_str = UnicodeDammit(input_str).unicode_markup.encode('utf-8')
        except:
            self.debug_print("Error occurred while handling python 2to3 compatibility for the input string")

        return input_str

    def _get_error_message_from_exception(self, e):
        """ This method is used to get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """
        try:
            if e.args:
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_msg = e.args[1]
                elif len(e.args) == 1:
                    error_code = ERR_CODE_MSG
                    error_msg = e.args[0]
            else:
                error_code = ERR_CODE_MSG
                error_msg = ERR_MSG_UNAVAILABLE
        except:
            error_code = ERR_CODE_MSG
            error_msg = ERR_MSG_UNAVAILABLE

        try:
            error_msg = self._handle_py_ver_compat_for_input_str(error_msg)
        except TypeError:
            error_msg = TYPE_ERR_MSG
        except:
            error_msg = ERR_MSG_UNAVAILABLE

        try:
            if error_code in ERR_CODE_MSG:
                error_text = "Error Message: {0}".format(error_msg)
            else:
                error_text = "Error Code: {0}. Error Message: {1}".format(error_code, error_msg)
        except:
            self.debug_print("Error occurred while parsing error message")
            error_text = PARSE_ERR_MSG

        return error_text

    def _dictify(self, data, key, prev_key=None):
        if isinstance(data, dict):
            for k in data.keys():
                data[k] = self._dictify(data[k], k, key)
            return data
        elif isinstance(data, list):
            for i, v in enumerate(data):
                data[i] = self._dictify(v, None, key)
            return data
        else:
            if prev_key is not None:
                new_key = (prev_key[0:-1] if (prev_key.endswith('s') and len(prev_key) > 1) else prev_key)
                return {new_key: data}
            else:
                return data

    def replace_dict(self, d):
        new = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = self.replace_dict(v)
            new[k.replace('.', '_')] = v
        return new

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(
            action_result.set_status(
                phantom.APP_ERROR, "Status code: {0}. Empty response and no information in the header".format(response.status_code)
            ), None
        )

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            # Remove the script, style, footer and navigation part from the HTML message
            for element in soup(["script", "style", "footer", "nav"]):
                element.extract()
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code, self._handle_py_ver_compat_for_input_str(error_text))

        message = message.replace('{', '{{').replace('}', '}}')
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".format(err)
                ), None
            )

        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        message = "Error from server. Status Code: {0} Data from server: {1}".format(
            r.status_code,
            self._handle_py_ver_compat_for_input_str(r.text.replace('{', '{{').replace('}', '}}'))
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        # Process a json response
        if 'json' in r.headers.get('Content-Type', ''):
            return self._process_json_response(r, action_result)

        if 'html' in r.headers.get('Content-Type', ''):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
            r.status_code,
            self._handle_py_ver_compat_for_input_str(r.text.replace('{', '{{').replace('}', '}}'))
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, method="get", **kwargs):
        # **kwargs can be any additional parameters that requests.request accepts

        config = self.get_config()

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(
                action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)),
                resp_json
            )

        # Create a URL to connect to
        url = self._base_url + endpoint

        try:
            r = request_func(
                url,
                verify=config.get('verify_server_cert', False),
                **kwargs
            )
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, "Error Connecting to server. {0}".format(err)
                ), resp_json
            )

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Connecting to endpoint")
        # make rest call
        ret_val, _ = self._make_rest_call('/', action_result, params=None, headers=None)
        if phantom.is_fail(ret_val):
            self.save_progress("Test Connectivity Failed")
            return action_result.get_status()

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def major_minor_micro_patch(self, version):
        # pad the numbers
        if not re.search(r'(\d+)\.', version):
            version += '.0.0.0'
        elif not re.search(r'(\d+)\.(\d+)\.', version):
            version += '.0.0'
        elif not re.search(r'(\d+)\.(\d+)\.(\d+)\.', version):
            version += '.0'
        major, minor, micro, patch = re.search(r'(\d+)\.(\d+)\.(\d+)\.(\d+)', version).groups()
        return int(major), int(minor), int(micro), int(patch)

    def _handle_extension_metadata(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        extension_id = param['extension_id']
        versions = []
        version_list = []
        endpoint = '/metadata/{}'.format(extension_id)

        ret_val, response = self._make_rest_call(endpoint, action_result)

        if phantom.is_fail(ret_val):
            return action_result.get_status()
        if response is None:
            return action_result.set_status(phantom.APP_ERROR, "Received unexpected response from the server. Please try again by providing a valid input")
        endpoint = '/report/{}'.format(extension_id)

        ret_val, response2 = self._make_rest_call(endpoint, action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        if response2 is None:
            return action_result.set_status(phantom.APP_ERROR, "Received unexpected response from the server. Please try again by providing a valid input")
        try:
            for data in response2:
                version_list.append({"version": data['version']})
                versions.append(data['version'])
                latest = max(versions, key=self.major_minor_micro_patch)
            response.update({"versions": version_list})
            action_result.add_data(response)
            name = response['name']
            rating = response['rating']
            short_description = response['short_description']
            action_result.update_summary({"extension_id": extension_id, "name": name, "rating": rating,
                                        "short_description": short_description, "total_versions": len(versions),
                                        "latest_version": latest})
        except:
            return action_result.set_status(phantom.APP_ERROR, "Error occurred while processing response from the server")

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_report(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        extension_id = param['extension_id']
        version = param.get('version')
        if version:
            endpoint = '/report/{}/{}'.format(extension_id, version)
        else:
            # Get latest version
            endpoint = '/report/{}'.format(extension_id)
            ret_val, response = self._make_rest_call(endpoint, action_result)
            if response is None:
                return action_result.set_status(phantom.APP_ERROR, "Received unexpected response from the server. Please try again by providing a valid input")
            versions = []
            try:
                for data in response:
                    versions.append(data['version'])
            except Exception as e:
                err = self._get_error_message_from_exception(e)
                return action_result.set_status(phantom.APP_ERROR, "Error occurred while processing response for version from the server. {}".format(err))

            latest = max(versions, key=self.major_minor_micro_patch)
            endpoint = '/report/{}/{}'.format(extension_id, latest)

        ret_val, response = self._make_rest_call(endpoint, action_result)

        if phantom.is_fail(ret_val):
            return action_result.get_status()
        if response is None:
            return action_result.set_status(phantom.APP_ERROR, "Received unexpected response from the server. Please try again by providing a valid input")

        try:
            # Scrub dots from field names
            response = self.replace_dict(response)
            data = response['data']
            data.update({"extension_id": response['extension_id']})
            data.update({"version": response['version']})
            action_result.add_data(data)
            total_risk = data['risk']['total']
            action_result.update_summary({"extension_id": extension_id, "version": response['version'], "total_risk": total_risk})
        except:
            return action_result.set_status(phantom.APP_ERROR, "Error occurred while processing response from the server for given extension ID")

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_submit_extension(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        extension_id = param['extension_id']
        data = json.dumps({"extension_id": extension_id})

        ret_val, response = self._make_rest_call('/submit', action_result, data=data, method='post')
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        elif response.get('error'):
            return action_result.set_status(phantom.APP_ERROR, response['error'])

        action_result.add_data(response)
        version = response.get('version')
        code = response.get('code')

        action_result.update_summary({"code": code, "extension_id": extension_id, "version": version})
        msg = response.get("message", "Successfully submitted extension")
        return action_result.set_status(phantom.APP_SUCCESS, msg)

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)
        elif action_id == 'extension_metadata':
            ret_val = self._handle_extension_metadata(param)
        elif action_id == 'get_report':
            ret_val = self._handle_get_report(param)
        elif action_id == 'submit_extension':
            ret_val = self._handle_submit_extension(param)

        return ret_val

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()

        self._base_url = config.get('base_url').strip("/")
        # Fetching the Python major version
        try:
            self._python_version = int(sys.version_info[0])
        except:
            return self.set_status(phantom.APP_ERROR, "Error occurred while fetching the phantom server's python major version.")

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = CrxcavatorConnector._get_phantom_base_url() + '/login'

            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = CrxcavatorConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)


if __name__ == '__main__':
    main()
