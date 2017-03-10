#!/usr/bin/env python3

"""Executable Python script which defines a url generator for the OpenWhisk API
  This script is useful for importing and using in Python scripts to access the
  API endpoints of a local or remote or local OpenWhisk server.  It enables the
  creation, deletion, interrogation, and invocation of OpenWhisk actions,
  activations, packages, rules, and triggers.
  Examples:
     $ python3
     >>> import url_generator
     >>> gen = url_generator.UrlGenerator(api_host='openwhisk.ng.bluemix.net')
     >>> print(gen.url_action('my_action'))
     >>> gen.package = 'my_package'
     >>> print(gen.url_action('my_action', blocking=True, result=True))
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


def url_finish(*args, **kwargs):
    """completes the right side of a url.
       URLs for REST APIs are composed of three parts:
       1. Base URL: https://openwhisk.ng.bluemix.net/api/v1/namespaces/_
       2. Path Parameters (args) separated by /'s
       3. Query Parameters (kwargs) started with a ? and then urlencoded
       args are a tuple of unnamed values that go on the left of the ?
       kwargs are a dict of named values that are urlencoded to right of ?"""
    s = ''
    if args:
        s = '/' + '/'.join(str(arg) for arg in args)
    if kwargs:
        s += '?' + urlencode(kwargs)
    return s


class UrlGenerator(object):
    """https://console.ng.bluemix.net/docs/openwhisk/openwhisk_reference.html
       https://console.ng.bluemix.net/apidocs/98-ibm-bluemix-openwhisk"""

    def __init__(self, api_host='localhost'):
        self.url_base = 'https://{}/api/v1/namespaces/_'.format(api_host)
        self.url_whisk_system = self.url_base + '/whisk.system/packages'
        self.url_whisk_utils = self.url_base + '/whisk.system/actions/utils'
        self._package = ''

    @property
    def package(self):
        return self._package

    @package.setter
    def package(self, package_name):
        self._package = str(package_name or '').strip()

    @property
    def _curr_package(self):
        """URL is built dynamically using the current self.namespace.
           https://{host}/api/v1/namespaces/-[/packages/{package}]"""
        return self.url_base + ('/packages/' +
                                self._package) if self._package else ''

    def url_package(self, *args, **kwargs):
        return self.url_base + '/packages' + url_finish(*args, **kwargs)

    def url_action(self, *args, **kwargs):
        return self._curr_package + '/actions' + url_finish(*args, **kwargs)

    def url_activation(self, *args, **kwargs):
        return self._curr_package + '/activations' + url_finish(*args,
                                                                **kwargs)

    def url_rule(self, *args, **kwargs):
        return self._curr_package + '/rules' + url_finish(*args, **kwargs)

    def url_trigger(self, *args, **kwargs):
        return self._curr_package + '/triggers' + url_finish(*args, **kwargs)


if __name__ == '__main__':
    gen = UrlGenerator()
    print(url_finish('0', 1, 2.0, a=0, b=1, c=2.0))

    kinds = {'action': gen.url_action,
             'activation': gen.url_activation,
             'package': gen.url_package,
             'rule': gen.url_rule,
             'trigger': gen.url_trigger}

    print('\n'.join('{:>10}: {}'.format(key, func())
                    for key, func in kinds.items()))

    print(gen.package)
    gen.package = 'PaCkAgE'
    print(gen.package)
    print('\n'.join('{:>10}: {}'.format(key, func())
                    for key, func in kinds.items()))

    print('')
    gen.package = 'name_test'
    print(gen.package)
    print('\n'.join('{:>10}: {}'.format(key, func('name'))
                    for key, func in kinds.items()))

    print('')
    gen.package = 'args_test'
    print(gen.package)
    print('\n'.join('{:>10}: {}'.format(key, func('path0', 'path1', 'path2',
                                                  query0=-1.2, query1=False,
                                                  query2='Open ?/& Whisk',
                                                  d={'e': 'Hi', 'f': [0, 1]}))
                    for key, func in kinds.items()))
