Alfred-HipChat
==============

Alfred workflow to interact, and perform various functions with the service [HipChat](http://hipchat.com/).

## Getting started
1. Install alfred-hipchat by visiting the download page in Github or via the [Packal page](http://www.packal.org/workflow/alfred-hipchat)
2. Go to the web interface at [HipChat.com](https://www.hipchat.com/sign_in), sign in, then under user preferences create an API token.
3. Launch alfred and type `hipchat_hostname`, this time followed by your hipchat hostname. Press `enter` to save your token. 
4. Launch alfred and type `hipchat_api_token`, this time followed by your token. Press `enter` to save your token. 
5. If room switching does not work immediately, simply restart HipChat.

## Currently Available Functionality:
* `hc`: Let's you switch easily between rooms, and private IMs.
* `hipchat_api_token`: API token to use.
* `hipchat_api_url`: URL of HipChat API.  Default: https://api.hipchat.com
* `hipchat_hostname`: Hostname of HipChat instance.
* `hipchat_cache_max_age`: Maximum age in seconds to cache results. Default: 180 

This workflow was created in Python with the help of [Dean Jackson's](https://github.com/deanishe/alfred-workflow) Alfred library and the [Requests](http://docs.python-requests.org/en/latest/) library.  It is based heavily on the [Frank Spinillo's slackfred](https://github.com/fspinillo/slackfred).
