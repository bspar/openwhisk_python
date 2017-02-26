#!/usr/bin/env python

"""
    WARNING: THIS IS PROOF-OF-CONCEPT LEVEL CODE.
        DO NOT USE IN PRODUCTION YET!!!


    Set of utility functions to communicate with OpenWhisk at Bluemix


    Requires:
        Define environment variable
            OPENWHISK_TOKEN ~100 character authorization token with a colon ':'
            can be found at https://console.ng.bluemix.net/openwhisk/learn/cli
            or by doing `wsk property get`

    Optional:
        Define environment variables
            OPENWHISK_APIHOST or will default to 'openwhisk.ng.bluemix.net'
            OPENWHISK_NAMESPACE or will default to '_' (TOKEN's email address)

    Todo: Clean, organize, and modularize this code.


    AD 2016-0531-1429

    (C) COPYRIGHT International Business Machines Corp. 2016
"""

import collections
import os
import pprint
import requests

DEBUG = False


class OpenWhisk(object):
    """https://console.ng.bluemix.net/docs/openwhisk/openwhisk_reference.html
       https://console.ng.bluemix.net/apidocs/98-ibm-bluemix-openwhisk"""

    def __init__(self, auth=None):
        """See: https://console.ng.bluemix.net/openwhisk/learn/cli  Your ~100
           char auth can be found at that URL or by doing `wsk property get`"""
        try:  # If auth was not provided, then look it up in os.environ
            auth = tuple((auth or os.getenv('OPENWHISK_TOKEN')).split(':'))
        except:
            print('Invocation error: auth must be provided or environment '
                  'variable $OPENWHISK_APIHOST must be defined and must '
                  'contain a colon (":").  See: `wsk property get`')
            raise
        self.session = requests.Session()  # speeds up repeated requests
        self.session.auth = auth           # uses our auth token for all calls
        api_host = os.getenv('OPENWHISK_APIHOST', 'openwhisk.ng.bluemix.net')
        self.url_base = 'https://{}/api/v1'.format(api_host)
        self.url_namespaces = self.url_base + '/namespaces'
        self.url_whisk_system = self.url_namespaces + '/whisk.system/packages'
        self.url_utils = self.url_namespaces + '/whisk.system/actions/utils'
        self._namespace = os.getenv('OPENWHISK_NAMESPACE', '_')
        self._package = ''

    def __del__(self):
        self.session.close()

    # Dynamic URLs that change as self.namespace and self.package change ======
    @property
    def namespace(self):
        """Ensure that when the namespace is falsey, it is repaced with '_'."""
        return str(self._namespace or '_')

    @namespace.setter
    def namespace(self, namespace_name):
        self._namespace = str(namespace_name or '_')

    @property
    def package(self):
        """Append '/packages/{package}' to URLs only if self.package is set."""
        return ('/packages/' + self._package) if self._package else ''

    @package.setter
    def package(self, package_name):
        self._package = str(package_name or '')

    @property
    def url_current_namespace(self):
        """URL is built dynamically using the current self.namespace.
           https://{host}/api/v1/namespaces/{namespace}[/packages/{package}]"""
        return self.url_namespaces + '/' + self.namespace + self.package

    @property
    def url_actions(self):
        """URL is built dynamically using the current self.namespace.
               https://{host}/api/v1/namespaces/{namespace}/actions"""
        return self.url_current_namespace + '/actions'

    @property
    def url_activations(self):
        """URL is built dynamically using the current self.namespace.
               https://{host}/api/v1/namespaces/{namespace}/activations"""
        return self.url_current_namespace + '/activations'

    @property
    def url_packages(self):
        """URL is built dynamically using the current self.namespace.
               https://{host}/api/v1/namespaces/{namespace}/packages"""
        return self.url_current_namespace + '/packages'

    @property
    def url_rules(self):
        """URL is built dynamically using the current self.namespace.
               https://{host}/api/v1/namespaces/{namespace}/rules"""
        return self.url_current_namespace + '/rules'

    @property
    def url_triggers(self):
        """URL is built dynamically using the current self.namespace.
               https://{host}api/v1/namespaces/{namespace}/triggers"""
        return self.url_current_namespace + '/triggers'

    # Actions =================================================================
    """Actions"""
    @property
    def actions(self):
        """Returns a list of all actions in the current namespace."""
        return self.actions_list().json()

    @property
    def action_names(self):
        """Returns a sorted list of the names of all actions."""
        return sorted(action.get('name') for action in self.actions)

    def action_create(self, filename, action_name):
        """Uploads contents of the specified file to the specified action."""
        # Read the file into a string
        with open(filename) as in_file:
            code = in_file.read()
        # print('File ' + filename + ' contents: >>>' + code + '<<<')
        kind = {'py': 'python'}.get(filename.lower().split('.')[-1], 'nodejs')
        payload = {'exec': {'kind': kind, 'code': code}}
        return self._put(self.url_actions + action_name, payload)

    def action_delete(self, action_name):
        """Deletes the specified action."""
        return self._delete(self.url_actions + action_name)

    def action_invoke(self, action_name):
        """Invokes the specified action in blocking mode."""
        url = self.url_actions + action_name + '?blocking=true&result=false'
        return self._post(url)

    def actions_list(self, skip=0, limit=999):
        """Lists the actions defined in openwhisk."""
        return self._get(self.url_actions +
                         '?skip={}&limit={}'.format(skip, limit))

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
        """Returns a list of the ids of all activation."""
        return [activation['activationId'] for activation
                in self.activations_list().json()]

    def activation_info(self, activation_id):
        """Returns a sorted list of the ids of all activation."""
        pass  # TODO

    def activation_logs(self, activation_id):
        """Returns the logs for a given activation id."""
        return self.get(self.url_activations + '/' + activation_id + '/logs')

    def activation_results(self, activation_id):
        """Returns a sorted list of the ids of all activation."""
        return self.get(self.url_activations + '/' + activation_id +
                        '/results')

    def activations_list(self):
        """Lists the activations defined in openwhisk."""
        return self._get(self.url_activations)

    # Namespaces ==============================================================
    @property
    def namespaces(self):  # TODO: namespaces or namespace_names
        """Returns a sorted list of the names of all namespaces."""
        return ['_'] + self.namespaces_list().json()

    def namespaces_list(self):
        """Lists the namespaces defined in openwhisk."""
        return self._get(self.url_namespaces)

    # Packages ================================================================
    @property
    def packages(self):
        """Returns a sorted list of the names of all packages."""
        return sorted(package.get('name') for package
                      in self.packages_list().json())

    def packages_list(self):
        """Lists the packages defined in openwhisk."""
        return self._get(self.url_packages)

    def package_create(self, filename, package_name):
        """Uploads contents of the specified file to the specified package."""
        # Read the file into a string  # TODO
        '''with open(filename) as in_file:
            code = in_file.read()
        # print('File ' + filename + ' contents: >>>' + code + '<<<')
        kind = {'py': 'python'}.get(filename.lower().split('.')[-1], 'nodejs')
        payload = {'exec': {'kind': kind, 'code': code}}
        return self._put(self.url_actions + action_name, payload)'''

    def package_delete(self, package_name):
        """Deletes the specified package."""
        pass  # TODO return self._delete(self.url_actions + action_name)

    def package_info(self, package_name):
        """Deletes the specified package."""
        pass  # TODO return self._delete(self.url_actions + action_name)

    # Rules ===================================================================
    @property
    def rules(self):
        """Returns a sorted list of the names of all rules."""
        return self.rules_list().json()

    def rules_list(self):
        """Lists the rules defined in openwhisk."""
        return self._get(self.url_rules)

    def rule_create(self, filename, rule_name):
        """Uploads contents of the specified file to the specified rule."""
        # Read the file into a string  # TODO
        '''with open(filename) as in_file:
            code = in_file.read()
        # print('File ' + filename + ' contents: >>>' + code + '<<<')
        kind = {'py': 'python'}.get(filename.lower().split('.')[-1], 'nodejs')
        payload = {'exec': {'kind': kind, 'code': code}}
        return self._put(self.url_actions + action_name, payload)'''

    def rule_delete(self, rule_name):
        """Deletes the specified package."""
        pass  # TODO return self._delete(self.url_actions + action_name)

    def rule_info(self, rule_name):
        """Deletes the specified package."""
        pass  # TODO return self._delete(self.url_actions + action_name)

    # Triggers ================================================================
    @property
    def triggers(self):
        """Returns a sorted list of the names of all triggers."""
        return self.triggers_list().json()

    def triggers_list(self):
        """Lists the triggers defined in openwhisk."""
        return self._get(self.url_triggers)

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
        return self._post(self.url_utils + echo, {'message': message}).json()

    def system_utils_invoke(self, action_name, **kwargs):
        """Invokes any action in whisk.system/utils"""
        url = self.url_utils + '/' + action_name
        return self._post(url + '?blocking=true&result=true&', kwargs).json()


if __name__ == '__main__':
    s = ',\n' + ' ' * 14
    whisk = OpenWhisk()  # create an instance of an OpenWhisk object

    print('    actions: {}'.format(whisk.action_names))
    print('activations: [{}]'.format(s.join(whisk.activation_ids)))
    print(' namespaces: {}'.format(whisk.namespaces))
    print('   packages: {}'.format(whisk.packages))
    print('      rules: {}'.format(whisk.rules))
    print('   triggers: {}'.format(whisk.triggers))
    print('')
    print('activation_counts: {}'.format(whisk.activation_counts))
    print('')
    print(whisk.invoke_echo('Anyone home!!'))
    print(whisk.system_utils_invoke('echo', message='my message'))
