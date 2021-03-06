# OpenWhisk Client Python
Python wrapper for the Apache OpenWhisk REST API

Start by instantiating an OpenWhisk object:

`whisk = OpenWhisk(wsk_auth)  # see notes below on how to obtain your wsk_auth`

OpenWhisk has five main concepts:
* Actions
* Activations
* Packages
* Rules
* Triggers

An OpenWhisk object has a property for each of these so you can easily access the current list of each.
```python
print(whisk.actions)  # return a list of json records, one for each whisk action
print(whisk.action_names)  # returns a list of names of the current whisk actions
```
 
See the repl example below to understand how to invoke whisk.systems actions and how to create and then invoke your own Python-based whisk actions.

## Authentiction Tokens
The key prerequisite is an **Open Whisk authentication token** that is generated via the `wsk` command line interface (cli) tool or via a webpage of your Open Whisk server.  This authentication token is a ~100 character string with a ":" in it.  If you have the wsk cli tool, then you can do `wsk property get` to get your “wsk auth”.  Alternatively, if you are on Bluemix, you can get your authentication token by logging into https://console.ng.bluemix.net/openwhisk/learn/cli .

The openwhisk.py script needs a valid Open Whisk authentication token to initialize and will attempt to accept this token in four different ways:
* As a parameter in the `openwhisk.OpenWhisk()` call (unwieldy, but it works)
* From a $OPENWHISK_TOKEN environment variable (recommended)
* By importing a local `wsk_auth.py` which defines a *wsk_auth* variable
* If all of these fail, it opens a webpage to see if the user can login, copy, and paste in their wsk auth

## repl usage example:
`>>>`**import openwhisk** <br>
`>>>`**whisk = openwhisk.OpenWhisk()** <&nbsp;># Assumes that $OPENWHISK_TOKEN environment variable has been set <br>
`>>>`**whisk.namespaces** <br>
['_', 'wendel_p_whisk@whisknamics.org_dev', 'wendel_p_whisk@whisknamics.org']<br>
`>>>`**whisk.action_names**<br>
['Hello World', 'Hello World With Params', 'python_action', 'xyz_action']<br>
`>>>`**whisk.actions**<br>
[{'name': 'python_action', 'publish': False, *[...]*}]<br>
`>>>`**whisk.activations**<br>
['echo', 'python_action']<br>
`>>>`**whisk.activation_counts**<br>
Counter({'echo': 30, 'python_action': 12})<br>
`>>>`**whisk.rules**<br>
[]<br>
`>>>`**whisk.triggers**<br>
[]<br>
`>>>`**whisk.packages**<br>
['Bluemix_Weather Company Data for IBM Bluemix-k6_Credentials-1']<br>
`>>>`**whisk.invoke_echo('Anyone home!!')**<br>
{'message': 'Anyone home!!'}<br>
`>>>`**whisk.system_utils_invoke('echo', message='my message')**<br>
{'message': 'my message'}
`>>>`**whisk.action_create(filename='hello.py', action_name='python_hello')**<br>
`>>>`**whisk.action_invoke('python_hello', name='Wendel')**<br>
{'greeting': 'Hello Wendel!'}

## openwhisk Module
```
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
```

## Data
- `DEBUG = False`

## openwhisk.OpenWhisk Objects

##### `__del__(self)`
> If a requests.Session has been opened, then close() it

##### `__init__(self, auth=None)`
> See: https://console.ng.bluemix.net/openwhisk/learn/cli  Your ~100
>            char auth can be found at that URL or by doing `wsk property get`

##### `action_create(self, filename, action_name)`
> Uploads contents of the specified file to the specified action.

##### `action_delete(self, action_name)`
> Deletes the specified action.

##### `action_invoke(self, action_name)`
> Invokes the specified action in blocking mode.

##### *`abstract property`* `action_names`

##### *`abstract property`* `actions`

##### `actions_list(self, skip=0, limit=999)`
> Lists the actions defined in openwhisk.

##### *`abstract property`* `activation_counts`

##### *`abstract property`* `activation_ids`

##### `activation_info(self, activation_id)`
> Returns a sorted list of the ids of all activation.

##### `activation_logs(self, activation_id)`
> Returns the logs for a given activation id.

##### `activation_results(self, activation_id)`
> Returns a sorted list of the ids of all activation.

##### *`abstract property`* `activations`

##### `activations_list(self)`
> Lists the activations defined in openwhisk.

##### `get_a_url(self, url, payload=None)`

##### `invoke_echo(self, message)`
> Issues a very basic echo request

##### *`abstract property`* `namespace`

##### *`abstract property`* `namespaces`

##### `namespaces_list(self)`
> Lists the namespaces defined in openwhisk.

##### *`abstract property`* `package`

##### `package_create(self, filename, package_name)`
> Uploads contents of the specified file to the specified package.

##### `package_delete(self, package_name)`
> Deletes the specified package.

##### `package_info(self, package_name)`
> Deletes the specified package.

##### *`abstract property`* `packages`

##### `packages_list(self)`
> Lists the packages defined in openwhisk.

##### `post_a_url(self, url, payload=None)`

##### `rule_create(self, filename, rule_name)`
> Uploads contents of the specified file to the specified rule.

##### `rule_delete(self, rule_name)`
> Deletes the specified package.

##### `rule_info(self, rule_name)`
> Deletes the specified package.

##### *`abstract property`* `rules`

##### `rules_list(self)`
> Lists the rules defined in openwhisk.

##### `system_utils_invoke(self, action_name, **kwargs)`
> Invokes any action in whisk.system/utils

##### `trigger_create(self, filename, trigger_name)`
> Uploads contents of the specified file to the specified trigger.

##### `trigger_delete(self, trigger_name)`
> Deletes the specified package.

##### `trigger_info(self, trigger_name)`
> Deletes the specified package.

##### *`abstract property`* `triggers`

##### `triggers_list(self)`
> Lists the triggers defined in openwhisk.

##### *`abstract property`* `url_actions`

##### *`abstract property`* `url_activations`

##### *`abstract property`* `url_current_namespace`

##### *`abstract property`* `url_packages`

##### *`abstract property`* `url_rules`

##### *`abstract property`* `url_triggers`
