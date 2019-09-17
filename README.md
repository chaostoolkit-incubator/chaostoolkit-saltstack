# Chaos Toolkit Extension for SaltStack

[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-saltstack.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-saltstack)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-saltstack.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit]. 

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org
[saltstack]: https://www.saltstack.com/

Generally [SaltStack][saltstack] runs minion agents in machine level, and minions are under management of one or more SaltMaster machines.
On the SaltMaster or via API, SaltMaster can run bulk commands or scripts or other actions on any connected minion.
The biggest advantage of SaltSatck is adapting cross cloud solutions on VM level chaos experiments.
If you are working on hybrid cloud and have network tunnelled, one SaltMaster could control all VMs across multiple clouds, e.g. Azure, AWS, etc.

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U chaostoolkit-saltstack
```


## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "type": "action",
    "name": "burn_cpu",
    "provider": {
        "type": "python",
        "module": "chaossaltstack.machines.actions",
        "func": "burn_cpu",
        "secrets": ["saltstack"],
        "arguments": {
            "parameters": {
                "execution_duration": "300"
            }
        }
    }
}
```

That's it!

Please explore the code to see existing probes and actions.



## Configuration

### Credentials
    0. Salt Master URL
        * SALTMASTER_HOST

    1. Useranme & Password.
       -d username='salt' -d password='abcd1234' -d eauth='pam'
       Then a token in obrained via <salt_url>/login

    2. Token
       A token directly, same with the backend of 1.

    3. Key, only from Salt Master
        * SALTMASTER_HOST: Salt Master API address

        You can authenticate with user / password via:
        * SALTMASTER_USER: the user name
        * SALTMASTER_PASSWORD: the password

        Or via a token:
        * SALTMASTER_TOKEN


There are two ways of doing this:

* you can either pass the name of the environment variables to the experiment definition as follows (recommended):

    ```json
    {
        "saltstack": {
            "SALTMASTER_HOST": {
                "type": "env",
                "key": "SALTMASTER_HOST"
            },
            "SALTMASTER_USER": {
                "type": "env",
                "key": "SALTMASTER_USER"
            },
            "SALTMASTER_PASSWORD": {
                "type": "env",
                "key": "SALTMASTER_PASSWORD"
            }
        }
    }
    ```

    ```json
    {
        "saltstack": {
            "SALTMASTER_HOST": {
                "type": "env",
                "key": "SALTMASTER_HOST"
            },
            "SALTMASTER_TOKEN": {
                "type": "env",
                "key": "SALTMASTER_TOKEN"
            }
        }
    }
    ```
    
* or you inject the secrets explicitly to the experiment definition:

    ```json
    {
        "saltstack": {
            "SALTMASTER_HOST": "https://172.10.20.666",
            "SALTMASTER_USER": "username",
            "SALTMASTER_PASSWORD": "password"
        }
    }
    ```

    ```json
    {
        "saltstack": {
            "SALTMASTER_HOST": "https://172.10.20.666",
            "SALTMASTER_TOKEN": "abcd1234abcd1234abcd1234"
        }
    }
    ```
    
    Additionally you may directly use if you are on the SaltMaster


### Putting it all together

Here is a full example:

```json
{
  "version": "1.0.0",
  "title": "...",
  "description": "...",
  "tags": [
    "azure",
    "kubernetes",
	"aks",
	"node"
  ],
  "configuration": {
    "saltstack": {
        "environment": "azure"
	}
  },
  "secrets": {
   "saltstack": {
       "SALTMASTER_HOST": "https://172.20.1.172:8000",
       "SALTMASTER_USER": "saltuser",
       "SALTMASTER_PASSWORD": "asfasfasdfa"
    }
   },
  "steady-state-hypothesis": {
    "title": "Services are all available and healthy",
    "probes": [
      {
        "type": "probe",
        "name": "check_minions_online",
        "provider": {
          "type": "python",
          "module": "chaossaltstack.machine.probes",
          "func": "is_minion_online",
          "arguments": {
              "instance_ids": [ "PABCDEFGS0016","PABCDEFGS0666" ]
          },
          "secrets": ["saltstack"]
        }
      }
    ]
  },
  "method": [
    {
        "type": "action",
        "name": "stress_cpu",
        "provider": {
            "type": "python",
          "module": "chaossaltstack.machine.probes",
            "module": "saltstack.machine.actions",
            "func": "stress_cpu",
            "arguments": {
                "execution_duration": "300",
                "instance_ids": [ "PABCDEFGS0016","PABCDEFGS0666" ]
            },
            "secrets": ["saltstack"]
        }
    }
  ],
  "rollbacks": [
    
  ]
}
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt 
```

Then, point your environment to this directory:

```console
$ pip install -e .
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```
