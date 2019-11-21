# -*- coding: utf-8 -*-
from typing import List

from chaoslib.types import Configuration, Secrets
from chaoslib.exceptions import FailedActivity


from .. import saltstack_api_client
from ..types import SaltStackResponse
from .actions import __default_salt_experiment__

__all__ = ["is_minion_online", "is_iproute_tc_installed", "grep_process_exist"]


def grep_process_exist(instance_ids: List[str],
                       process_name: str,
                       configuration: Configuration = None,
                       secrets: Secrets = None) -> SaltStackResponse:
    """
    grep_process_exist will run
    ps -ef | grep $process_name | grep -v 'grep' | awk '{ print $2 }'

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    process_name : str
        process name
    configuration : Configuration
        Chaostoolkit Configuration
    secrets : Secrets
        Chaostoolkit Secrets
    """

    param = dict()
    param["param"] = process_name

    return __default_salt_experiment__(instance_ids=instance_ids,
                                       execution_duration=1,
                                       param=param,
                                       configuration=configuration,
                                       secrets=secrets)


def is_minion_online(instance_ids: List[str],
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """
        test.ping salt minions

        Parameters
        ----------
        instance_ids : str or List
            same as
                salt --list ['client1','client2','client3'] test.ping
        api return a dict {'client1': True, 'client2': False}
        this function will return dict otherwise raise exception
            {'client1': 'Online', 'client2': 'Offline',
                'client3':'Not a Salt Minion' }
    """
    try:
        client = saltstack_api_client(secrets)
        machines = client.run_cmd(instance_ids, 'test.ping')

        result = dict()

        for k in instance_ids:
            if k not in machines:
                result[k] = "Not a Salt Minion"
            else:
                if machines[k] is False:
                    result[k] = "Offline"
                else:
                    result[k] = "Online"

        return result

    except Exception as x:
        raise FailedActivity(
            "failed issuing a execute of shell script via salt API {}".format(
                str(x)
            )
        )


def is_iproute_tc_installed(instance_ids: List[str],
                            configuration: Configuration = None,
                            secrets: Secrets = None):
    """
        cmd.run tc -help

        Parameters
        ----------
        instance_ids : str or List
            same as
                salt --list ['client1','client2','client3'] cmd.run tc -help
        api return a dict {'client1': 'xxxxxx', 'client2': 'xxxxxx'}
        this function will return dict otherwise raise execption
            {'PCNCMCNSA0018': 'Usage: tc [ OPTIONS ] OBJECT { COMMAND | help }
            tc [-force] -batch filename where  OBJECT := { qdisc | class | filter | action | monitor | exec }
            OPTIONS := { -s[tatistics] | -d[etails] | -r[aw] | -p[retty] | -b[atch] [filename] | -n[etns] name |
            -nm | -nam[es] | { -cf | -conf } path }', 'PCNCMCNSA0016': 'Usage: tc [ OPTIONS ] OBJECT { COMMAND | help }
            tc [-force] -batch filename where  OBJECT := { qdisc | class | filter | action | monitor | exec }
            OPTIONS := { -s[tatistics] | -d[etails] | -r[aw] | -p[retty] | -b[atch] [filename] | -n[etns] name |
            -nm | -nam[es] | { -cf | -conf } path }'}
    """  # noqa: E501
    try:
        client = saltstack_api_client(secrets)
        machines = client.run_cmd(instance_ids, 'cmd.run', 'tc -help')

        result = dict()

        for k in instance_ids:
            if k not in machines:
                result[k] = "Not a Salt Minion"
            else:
                if machines[k].startswith("Usage: tc"):
                    result[k] = "Installed"
                else:
                    result[k] = "Not Installed"

        return result

    except Exception as x:
        raise FailedActivity(
            "failed issuing a execute of shell script via salt API {}".format(
                str(x)
            )
        )
