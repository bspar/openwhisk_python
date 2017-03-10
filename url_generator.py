#!/usr/bin/env python3

"""Executable Python script which defines a url generator for the OpenWhisk API
  This script is useful for importing and using in Python scripts to access the
  API endpoints of a local or remote or local OpenWhisk server.  It enables the
  creation, deletion, interrogation, and invocation of OpenWhisk actions,
  activations, packages, rules, and triggers.
  Examples:
     $ python3
     >>> import url_generator
     >>> gen = url_generator.UrlGenerator('openwhisk.ng.bluemix.net')
     >>> print(gen.url(kind='action', name='my_action'))
     >>> print(gen.url('aCtIoNs', 'my_action', verb='invoke', 'message'='Hi!'))
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

try:
    from urllib.parse import urlencode  # Python 3
except ImportError:
    from urllib import urlencode        # Python 2


class UrlGenerator(dict):
    """https://console.ng.bluemix.net/docs/openwhisk/openwhisk_reference.html
       https://console.ng.bluemix.net/apidocs/98-ibm-bluemix-openwhisk"""

    def __init__(self, api_host='localhost'):
        self.url_base = 'https://{}/api/v1/namespaces/_'.format(api_host)
        self.url_whisk_system = self.url_base + '/whisk.system/packages'
        self.url_whisk_utils = self.url_base + '/whisk.system/actions/utils'
        self._package = ''
        self.kinds = {'action': self._actions,
                      'activation': self._activations,
                      'package': self._packages,
                      'rule': self._rules,
                      'trigger': self._triggers}

    # Dynamic URLs that change as self.package changes
    def url(self, kind, name='', verb='', **kwargs):
        kind = str(kind or '').strip().lower().rstrip('s')
        try:
            url = self.kinds[kind]()  # lookup the method and then call it
        except KeyError as e:
            print(kind + ' is not supported.')
            print(e)
            raise
        name = str(name or '').strip()
        if name:
            url += '/{}'.format(name)
            verb = str(verb or '').strip().lower()
            if verb in 'create delete invoke update'.split():
                url += '/{}'.format(verb)
        if kwargs:
            url += '?' + urlencode(kwargs)
        return url

    @property
    def package(self):
        """Append '/packages/{package}' to URLs only if self.package is set."""
        return ('/packages/' + self._package) if self._package else ''

    @package.setter
    def package(self, package_name):
        self._package = str(package_name or '').strip()

    # @property
    def _current_package(self):
        """URL is built dynamically using the current self.namespace.
           https://{host}/api/v1/namespaces/-[/packages/{package}]"""
        return self.url_base + self.package

    # @property
    def _actions(self):
        """URL is built dynamically using url_current_package.
           https://{host}/api/v1/namespaces/-/[/packages/{package}]/actions"""
        return self._current_package() + '/actions'

    # @property
    def _activations(self):
        """URL is built dynamically using url_current_package.
           https://{host}/api/v1/namespaces/-/[/packages/{package}]/activations
           """
        return self._current_package() + '/activations'

    # @property
    def _packages(self):
        """URL is built dynamically using url_current_package.
               https://{host}/api/v1/namespaces/-/packages"""
        return self.url_base + '/packages'

    # @property
    def _rules(self):
        """URL is built dynamically using url_current_package.
           https://{host}/api/v1/namespaces/-/[/packages/{package}]/rules"""
        return self._current_package() + '/rules'

    # @property
    def _triggers(self):
        """URL is built dynamically using url_current_package.
           https://{host}/api/v1/namespaces/-/[/packages/{package}]/triggers"""
        return self._current_package() + '/triggers'


if __name__ == '__main__':
    kinds = 'AcTiOnS action ACTIVATION packages RULESSS rule tRiGgErSs'.split()
    gen = UrlGenerator()
    print('\n'.join('{:>10}: {}'.format(k, gen.url(k)) for k in kinds))

    print(gen.package)
    gen.package = 'PaCkAgE'
    print(gen.package)
    print('\n'.join('{:>10}: {}'.format(k, gen.url(k)) for k in kinds))

    print('')
    gen.package = 'name_test'
    print(gen.package)
    print('\n'.join('{:>10}: {}'.format(k, gen.url(k, 'name')) for k in kinds))

    print('')
    gen.package = 'args_test'
    print(gen.package)
    print('\n'.join('{:>10}: {}'.format(k, gen.url(kind=k, name='args', a=-1.2,
                                                   b=False, c='Open ?/& Whisk',
                                                   d={'e': 'Hi', 'f': [0, 1]}))
                    for k in kinds))

    print('')
    gen.package = 'invoke_test'
    print(gen.package)
    print('\n'.join('{:>10}: {}'.format(k, gen.url(k, 'name', verb='InVoKe',
                                                   a=69, b=True, c='OpenWhisk',
                                                   d={'e': 'Hi', 'f': [0, 1]}))
                    for k in kinds))
