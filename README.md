# openwhisk_python
Python wrapper for the Apache OpenWhisk REST API

# openwhisk Module
> WARNING: THIS IS PROOF-OF-CONCEPT LEVEL CODE.
>     DO NOT USE IN PRODUCTION YET!!!
>
>
> Set of utility functions to communicate with OpenWhisk at Bluemix
>
>
> Requires:
>     Define environment variable
>         OPENWHISK_TOKEN ~100 character authorization token with a colon ':'
>         can be found at https://console.ng.bluemix.net/openwhisk/learn/cli
>         or by doing `wsk property get`
>
> Optional:
>     Define environment variables
>         OPENWHISK_APIHOST or will default to 'openwhisk.ng.bluemix.net'
>         OPENWHISK_NAMESPACE or will default to '_' (TOKEN's email address)
>


## Data
- `DEBUG = False`

## openwhisk.OpenWhisk Objects



##### `__del__(self)`



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
