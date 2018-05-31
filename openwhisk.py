#!/usr/bin/env python3

"""Executable Python script which defines an OpenWhisk API interface
  This script is useful for importing and using in Python scripts to access the
  API endpoints of a local or remote or local OpenWhisk server.  It enables the
  creation, deletion, interrogation, and invocation of OpenWhisk actions,
  activations, packages, rules, and triggers.
  Examples:
     $ python3
     >>> import openwhisk
     >>> whisk = openwhisk.OpenWhisk()
     >>> print(whisk.action_names)
     >>> print(whisk.action_invoke('submit_order'))
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
"""


import collections
import os
import sys
import pprint
import requests
import base64

from url_generator import UrlGenerator

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEBUG = False


class OpenWhisk(object):
    """https://console.ng.bluemix.net/docs/openwhisk/openwhisk_reference.html
       https://console.ng.bluemix.net/apidocs/98-ibm-bluemix-openwhisk"""

    def __init__(self, wsk_auth, apihost='localhost', verify=True):
        """See: https://console.ng.bluemix.net/openwhisk/learn/cli  Your ~100
           char auth can be found at that URL or by doing `wsk property get`"""
        self.session = None
        # print(get_wsk_auth())
        # If wsk_auth token was not provided, then look it up in os.environ...
        wsk_auth = wsk_auth
        try:
            wsk_auth = tuple(wsk_auth.split(':'))
        except:
            print('Invocation error: auth must be provided or environment '
                  'variable $OPENWHISK_APIHOST must be defined and must '
                  'contain a colon (":").  See: `wsk property get`\n')
            raise
        self.session = requests.Session()  # speeds up repeated requests
        self.session.verify = verify              # verify SSL certs (bool)
        self.session.auth = wsk_auth       # uses our auth token for all calls
        self.gen = UrlGenerator(apihost)

    def __del__(self):
        self.session.close()

    # Dynamic URLs that change as self.package changes
    @property
    def package(self):
        """Append '/packages/{package}' to URLs only if self.package is set."""
        return self.gen.package

    @package.setter
    def package(self, package_name):
        self.gen.package = package_name

    # Actions =================================================================
    """Actions"""
    @property
    def actions(self):
        """Returns a list of all actions in url_current_package."""
        return self.actions_list()

    @property
    def action_names(self):
        """Returns a sorted list of the names of all actions."""
        return sorted(action.get('name', 'Can\'t get action name') for action in self.actions)

    def action_create(self, filename, action_name, runtime='python3', *args, **kwargs):
        """Uploads contents of the specified file to the specified action."""
        # Read the file into a string
        with open(filename, 'rb') as in_file:
            code = in_file.read()
        if filename.lower().split('.')[-1] == 'zip':
            code = base64.b64encode(code)
        code = code.decode('utf-8')
        # TODO: Support more languages beyond Python or NodeJS
        image = 'bspar/openwhisk-runtime-python:{}-latest'.format(runtime)
        payload = {'exec': {'kind':'blackbox', 'code':code, 'image':image}}
        url = self.gen.url_action(action_name, *args, **kwargs)
        return self._put(url, payload).json()

    def sequence_create(self, sequence_name, action_names, *args, **kwargs):
        payload = { 'exec': { 'kind' : 'sequence', 'components' : action_names }}
        url = self.gen.url_action(sequence_name, *args, **kwargs)
        return self._put(url, payload).json()

    def action_delete(self, action_name, *args, **kwargs):
        """Deletes the specified action."""
        url = self.gen.url_action(action_name, *args, **kwargs)
        return self._delete(url).json()

    def action_invoke(self, action_name, *args, **kwargs):
        """Invokes the specified action in blocking mode."""
        '''url = (self.url_actions + '/' + action_name +
               '?blocking=true&result=false')'''
        payload = kwargs.pop('payload') if 'payload' in kwargs else {}
        url = self.gen.url_action(action_name, *args, **kwargs)
        return self._post(url, payload).json()

    def action_get(self, action_name, *args, **kwargs):
        return self.actions_list(action_name, *args, **kwargs)

    def actions_list(self, *args, **kwargs):
        """Lists the actions defined in openwhisk."""
        url = self.gen.url_action(*args, **kwargs)
        return self._get(url).json()

    # Activations =============================================================
    @property
    def activations(self):
        """Returns a sorted list of the names of all activation."""
        # TODO: remove set()
        return sorted(set(activation.get('name') for activation
                          in self.activations_list().json()))

    @property
    def activation_counts(self):
        """Returns dict of how many times current actions have been invoked."""
        return collections.Counter(activation.get('name') for activation
                                   in self.activations_list().json())

    @property
    def activation_ids(self):
        """Returns a sorted list of the ids of all activation."""
        return sorted(activation['activationId'] for activation
                      in self.activations_list().json())

    def activation_info(self, activation_id):
        """Returns info on the activation."""
        url = self.gen.url_activation(activation_id)
        return self._get(url).json()

    '''
    def activation_logs(self, activation_id):
        """Returns the logs for a given activation id."""
        return self.get(self.url_activations + '/' + activation_id + '/logs')
    '''
    def activation_results(self, activation_id):
        """Returns a sorted list of the ids of all activation."""
        url = self.gen.url_activation(activation_id, 'result')
        return self._get(url).json()

    def activations_list(self):
        """Lists the activations defined in openwhisk."""
        return self._get(self.gen.url_activation())

    '''
    # Namespaces ==============================================================
    @property
    def namespaces(self):  # TODO: namespaces or namespace_names
        """Returns a sorted list of the names of all namespaces."""
        return self.namespaces_list().json()

    def namespaces_list(self):
        """Lists the namespaces defined in openwhisk."""
        return self._get(self.url_namespaces)
    '''

    # Packages ================================================================
    @property
    def packages(self):
        """Returns a sorted list of the names of all packages."""
        return sorted(package.get('name') for package
                      in self.packages_list().json())

    def packages_list(self):
        """Lists the packages defined in openwhisk."""
        return self._get(self.gen.url_package())

    def package_create(self, filename, package_name):
        """Uploads contents of the specified file to the specified package."""
        pass  # TODO

    def package_delete(self, package_name):
        """Deletes the specified package."""
        pass  # TODO

    def package_info(self, package_name):
        """Returns info on the specified package."""
        pass  # TODO

    # Rules ===================================================================
    @property
    def rules(self):
        """Returns a sorted list of the names of all rules."""
        return self.rules_list().json()

    def rules_list(self):
        """Lists the rules defined in openwhisk."""
        return self._get(self.gen.url_rule())

    def rule_create(self, filename, rule_name):
        """Uploads contents of the specified file to the specified rule."""
        pass  # TODO

    def rule_delete(self, rule_name):
        """Deletes the specified rule."""
        pass  # TODO

    def rule_info(self, rule_name):
        """Returns info on the specified rule."""
        pass  # TODO

    # Triggers ================================================================
    @property
    def triggers(self):
        """Returns a sorted list of the names of all triggers."""
        return self.triggers_list().json()

    def triggers_list(self):
        """Lists the triggers defined in openwhisk."""
        return self._get(self.gen.url_trigger())

    def trigger_create(self, filename, trigger_name):
        """Uploads contents of the specified file to the specified trigger."""
        # Read the file into a string  # TODO
        '''with open(filename) as in_file:
            code = in_file.read()
        # print('File ' + filename + ' contents: >>>' + code + '<<<')
        kind = {'py': 'python'}.get(filename.lower().split('.')[-1], 'nodejs')
        payload = {'exec': {'kind': kind, 'code': code}}
        return self._put(self.url_actions + action_name, payload)'''

    def trigger_delete(self, trigger_name):
        """Deletes the specified package."""
        pass  # TODO return self._delete(self.url_actions + action_name)

    def trigger_info(self, trigger_name):
        """Deletes the specified package."""
        pass  # TODO return self._delete(self.url_actions + action_name)

    # Debugging: ==============================================================
    #   These methods will be removed from the final API ======================
    # get_a_url('https://openwhisk.ng.bluemix.net/api/v1/namespaces/_/actions/x')
    def get_a_url(self, url, payload=None):
        x = self._get(url, payload).json()
        pprint.pprint(x)
        return x

    # post_a_url('https://openwhisk.ng.bluemix.net/api/v1/namespaces/_/actions/x')
    def post_a_url(self, url, payload=None):
        return self._post(url, payload).json()

    @classmethod
    def _print_request(cls, req_type, url, payload=None):
        if not DEBUG:
            return
        msg = 'Issuing {} request: url={}'.format(req_type, url)
        if payload:
            msg += ' payload={!r}'.format(payload)
        print(msg)

    @classmethod
    def _print_response(cls, response):
        if not DEBUG:
            return response
        print('Response.status_code={}\n{}'.format(response.status_code,
                                                   response.text))
        return response

    def _delete(self, url, payload=None):
        self._print_request('delete', url, payload)
        return self._print_response(self.session.delete(url, json=payload))

    def _get(self, url, payload=None):
        self._print_request('get', url, payload)
        return self._print_response(self.session.get(url, json=payload))

    def _post(self, url, payload=None):
        self._print_request('post', url, payload)
        return self._print_response(self.session.post(url, json=payload))

    def _put(self, url, payload=None):
        self._print_request('put', url, payload)
        return self._print_response(self.session.put(url, json=payload))

    # Misc utils ==============================================================
    def invoke_echo(self, message):
        """Issues a very basic echo request"""
        echo = '/echo?blocking=true&result=true'
        return self._post(self.gen.url_whisk_utils + echo,
                          payload={'message': message}).json()

    def system_utils_invoke(self, action_name, **kwargs):
        """Invokes any action in whisk.system/utils"""
        url = self.gen.url_whisk_utils + '/' + action_name
        return self._post(url + '?blocking=true&result=true&', kwargs).json()


if __name__ == '__main__':
    s = ',\n' + ' ' * 14    # array separation
    if len(sys.argv) <= 1:
        print('-- pls supply api key (try `wsk property get`) --')
        exit(-1)
    whisk = OpenWhisk(sys.argv[1], verify=False)  # create an instance of an OpenWhisk object
    print('\n ### Initial actions on this OpenWhisk ###')
    print(whisk.action_names)
    whisk.action_create('hello/hello_zip.zip', 'hello_python', overwrite=True)

    print('\n ### Testing blocking default hello_python ###')
    print(whisk.action_invoke('hello_python', blocking=True, result=True))
    print('\n ### Should include hello_python now ###')
    print(whisk.action_names)

    print('\n ### Testing params to hello_python ###')
    pprint.pprint(whisk.action_invoke('hello_python', blocking=True,
                                      result=True, payload={'name': 'Wendel'}))

    from time import sleep
    print('\n ### Testing async activation results ###')
    act = whisk.action_invoke('hello_python', payload={'name': 'Wendel P. Whisk'})
    res = whisk.activation_results(act['activationId'])
    while res.get('error', None):
        res = whisk.activation_results(act['activationId'])
        sleep(1)
    pprint.pprint(res)
    print('')

    print('\n ### Testing sequence with params ###')
    whisk.action_create('hello/hello.py', 'hello_python2', overwrite=True)
    whisk.sequence_create('hello_sequence', ['guest/hello_python','guest/hello_python2'])
    print(whisk.action_invoke('hello_sequence', blocking=True, result=True, payload={'name':'testy'}))

    print('\n ### Testing getting code for hello_python2 ###')
    print(whisk.action_get('hello_python2', code=True)['exec']['code'])
    print('\n ### Testing getting metadata for hello_python2 ###')
    print(whisk.action_get('hello_python2', code=False))

    print('\n\n    actions: {}'.format(whisk.action_names))
    print('activations: [{}]'.format(s.join(whisk.activation_ids)))
    print('   packages: {}'.format(whisk.packages))
    print('      rules: {}'.format(whisk.rules))
    print('   triggers: {}'.format(whisk.triggers))
    print('')
    print('activation_counts: {}'.format(whisk.activation_counts))
    print('')
    # print(whisk.invoke_echo('Anyone home!!'))
    # print(whisk.system_utils_invoke('echo', message='my message'))

    print('!!!Deleting all actions!!!')
    whisk.action_delete('hello_python')
    whisk.action_delete('hello_python2')
    whisk.action_delete('hello_sequence')
    print('    actions: {}'.format(whisk.action_names))
    print('activations: [{}]'.format(s.join(whisk.activation_ids)))
    print('   packages: {}'.format(whisk.packages))
    print('      rules: {}'.format(whisk.rules))
    print('   triggers: {}'.format(whisk.triggers))
    print('')
    print('1activation: ')
    pprint.pprint(whisk.activation_info(whisk.activation_ids[0]))
    print('')
    print('activation_counts: {}'.format(whisk.activation_counts))
    print('')
