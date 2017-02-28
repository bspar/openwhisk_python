#!/usr/bin/env python

"""
    Required
        Define environment variable
            OPENWHISK_TOKEN ~100 character authorization token with a colon ':'
            can be found at https://console.ng.bluemix.net/openwhisk/learn/cli
            or by doing `wsk property get`

    CCC 2017-02-28-0549

    (C) COPYRIGHT International Business Machines Corp. 2017
"""

import getpass
import time
import webbrowser


def get_auth(url='https://console.ng.bluemix.net/openwhisk/learn/cli'):
    """Help the user to obtain their wsk auth from the Bluemix website"""
    wsk_auth = os.getenv('OPENWHISK_TOKEN')
    if wsk_auth:
        return wsk_auth
    try:
        import wsk_auth
        return wsk_auth.wsk_auth
    except ImportError:
        pass

    print("""No authorization token ('wsk auth') was provided or was found in
    the $OPENWHISK_TOKEN environment variable.  Please login at this website
    and copy your 'wsk auth', then return here and paste it in...""")
    time.sleep(2)  # provide a few seconds for the user to read...
    webbrowser.open(url)
    prompt = 'wsk auth: (~100 character authentication token with a ":" in it)'
    return getpass.getpass(prompt).strip()


if __name__ == '__main__':
    print('wsk auth: {}'.format(get_auth()))
