# -*- coding: utf-8 -*-
import os
import json
from time import sleep
from typing import List

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from .. import saltstack_api_client
from ..types import SaltStackResponse
from .constants import OS_LINUX, OS_WINDOWS
from .constants import BURN_CPU, FILL_DISK, NETWORK_UTIL, \
    BURN_IO, KILLALL_PROCESSES, KILL_PROCESS


__all__ = ["burn_cpu", "fill_disk", "network_latency", "burn_io",
           "network_loss", "network_corruption", "network_advanced",
           "killall_processes", "kill_process"]


def burn_cpu(instance_ids: List[str] = None,
             execution_duration: str = "60",
             configuration: Configuration = None,
             secrets: Secrets = None) -> SaltStackResponse:
    """
    burn CPU up to 100% at random machines.

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    execution_duration : str, optional
        Duration of the stress test (in seconds) that generates high CPU usage.
        Defaults to 60 seconds.
    configuration : Configuration
        Chaostoolkit Configuration
    secrets : Secrets
        Chaostoolkit Secrets
    """

    logger.debug(
        "Start burn_cpu: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    param = dict()
    param["duration"] = execution_duration

    return __default_salt_experiment__(instance_ids=instance_ids,
                                       execution_duration=execution_duration,
                                       param=param,
                                       experiment_type=BURN_CPU,
                                       configuration=configuration,
                                       secrets=secrets
                                       )


def fill_disk(instance_ids: List[str] = None,
              execution_duration: str = "120",
              size: str = "1000",
              configuration: Configuration = None,
              secrets: Secrets = None) -> SaltStackResponse:
    """
    For now do not have this scenario, fill the disk with random data.

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    execution_duration : str, optional
        Lifetime of the file created. Defaults to 120 seconds.
    size : str
        Size of the file created on the disk. Defaults to 1GB.
    configuration : Configuration
        Chaostoolkit Configuration
    secrets : Secrets
        Chaostoolkit Secrets
    """

    logger.debug(
        "Start fill_disk: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    param = dict()
    param["execution_duration"] = execution_duration
    param["size"] = size

    return __default_salt_experiment__(instance_ids=instance_ids,
                                       execution_duration=execution_duration,
                                       param=param,
                                       experiment_type=FILL_DISK,
                                       configuration=configuration,
                                       secrets=secrets
                                       )


def burn_io(instance_ids: List[str] = None,
            execution_duration: str = "60",
            configuration: Configuration = None,
            secrets: Secrets = None) -> SaltStackResponse:
    """
    Increases the Disk I/O operations per second of the virtual machine.

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    execution_duration : str, optional
        Lifetime of the file created. Defaults to 120 seconds.
    configuration : Configuration
        Chaostoolkit Configuration
    secrets : Secrets
        Chaostoolkit Secrets
    """

    logger.debug(
        "Start burn_io: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    param = dict()
    param["duration"] = execution_duration

    return __default_salt_experiment__(instance_ids=instance_ids,
                                       execution_duration=execution_duration,
                                       param=param,
                                       experiment_type=BURN_IO,
                                       configuration=configuration,
                                       secrets=secrets
                                       )


def network_advanced(instance_ids: List[str] = None,
                     execution_duration: str = "60",
                     command: str = "",
                     configuration: Configuration = None,
                     secrets: Secrets = None) -> SaltStackResponse:
    """
    do a customized operations on the virtual machine via Linux - TC.
    For windows, no solution as for now.

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    execution_duration : str, optional
        Lifetime of the file created. Defaults to 60 seconds.
    command : str
        the tc command, e.g.  loss 15%
    configuration : Configuration
        Chaostoolkit Configuration
    secrets : Secrets
        Chaostoolkit Secrets
    """

    logger.debug(
        "Start network_advanced: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    param = dict()
    param["duration"] = execution_duration
    param["param"] = command

    return __default_salt_experiment__(instance_ids=instance_ids,
                                       execution_duration=execution_duration,
                                       param=param,
                                       experiment_type=NETWORK_UTIL,
                                       configuration=configuration,
                                       secrets=secrets
                                       )


def network_loss(instance_ids: List[str] = None,
                 execution_duration: str = "60",
                 loss_ratio: str = "5%",
                 configuration: Configuration = None,
                 secrets: Secrets = None) -> SaltStackResponse:
    """
    do a network loss operations on the virtual machine via Linux - TC.
    For windows, no solution as for now.

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    execution_duration : str, optional
        Lifetime of the file created. Defaults to 60 seconds.
    loss_ratio : str:
        loss_ratio = "30%"
    configuration : Configuration
        Chaostoolkit Configuration
    secrets : Secrets
        Chaostoolkit Secrets
    """

    logger.debug(
        "Start network_advanced: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    param = dict()
    param["duration"] = execution_duration
    param["param"] = "loss " + loss_ratio

    return __default_salt_experiment__(instance_ids=instance_ids,
                                       execution_duration=execution_duration,
                                       param=param,
                                       experiment_type=NETWORK_UTIL,
                                       configuration=configuration,
                                       secrets=secrets
                                       )


def network_corruption(instance_ids: List[str] = None,
                       execution_duration: str = "60",
                       corruption_ratio: str = "5%",
                       configuration: Configuration = None,
                       secrets: Secrets = None) -> SaltStackResponse:
    """
    do a network loss operations on the virtual machine via Linux - TC.
    For windows, no solution as for now.

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    execution_duration : str, optional
        Lifetime of the file created. Defaults to 60 seconds.
    corruption_ratio : str:
        corruption_ratio = "30%"
    configuration : Configuration
        Chaostoolkit Configuration
    secrets : Secrets
        Chaostoolkit Secrets
    """

    logger.debug(
        "Start network_corruption: configuration='{}', "
        "instance_ids='{}'".format(configuration, instance_ids))

    param = dict()
    param["duration"] = execution_duration
    param["param"] = "corrupt " + corruption_ratio

    return __default_salt_experiment__(instance_ids=instance_ids,
                                       execution_duration=execution_duration,
                                       param=param,
                                       experiment_type=NETWORK_UTIL,
                                       configuration=configuration,
                                       secrets=secrets
                                       )


def network_latency(instance_ids: List[str] = None,
                    execution_duration: str = "60",
                    delay: str = "1000ms",
                    variance: str = "500ms",
                    ratio: str = "",
                    configuration: Configuration = None,
                    secrets: Secrets = None) -> SaltStackResponse:
    """
    Increases the response time of the virtual machine.

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    execution_duration : str, optional
        Lifetime of the file created. Defaults to 120 seconds.
    delay : str
        Added delay in ms. Defaults to 1000ms.
    variance : str
        Variance of the delay in ms. Defaults to 500ms.
    ratio: str = "5%", optional
        the specific ratio of how many Variance of the delay in ms.
        Defaults to "".
    configuration : Configuration
        Chaostoolkit Configuration
    secrets : Secrets
        Chaostoolkit Secrets
    """
    logger.debug(
        "Start network_latency: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    param = dict()
    param["duration"] = execution_duration
    param["param"] = "delay " + delay + " " + variance + " " + ratio

    return __default_salt_experiment__(instance_ids=instance_ids,
                                       execution_duration=execution_duration,
                                       param=param,
                                       experiment_type=NETWORK_UTIL,
                                       configuration=configuration,
                                       secrets=secrets
                                       )


def killall_processes(instance_ids: List[str] = None,
                      execution_duration: str = "60",
                      process_name: str = None,
                      configuration: Configuration = None,
                      signal: str = "",
                      secrets: Secrets = None) -> SaltStackResponse:
    """
    The killall utility kills processes selected by name
    refer to https://linux.die.net/man/1/killall

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    execution_duration : str, optional default to 1 second
        This is not technically not useful as the process usually is killed
        without and delay, however you can set more seconds here to let the
        thread wait for more time to extend your experiment execution in case
        you need to watch more on the observation metrics.
    process_name : str
        Name of the process to be killed
    signal : str , default to ""
        The signal of killall command, e.g. use -9 to force kill
    configuration : Configuration
        Chaostoolkit Configuration
    secrets : Secrets
        Chaostoolkit Secrets
    """
    logger.debug(
        "Start network_latency: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    param = dict()
    param["duration"] = execution_duration
    param["param"] = process_name
    param["signal"] = signal

    return __default_salt_experiment__(instance_ids=instance_ids,
                                       execution_duration=execution_duration,
                                       param=param,
                                       experiment_type=KILLALL_PROCESSES,
                                       configuration=configuration,
                                       secrets=secrets
                                       )


def kill_process(instance_ids: List[str] = None,
                 execution_duration: str = "60",
                 process: str = None,
                 configuration: Configuration = None,
                 signal: str = "",
                 secrets: Secrets = None) -> SaltStackResponse:
    """
    kill -s [signal_as_below] [processname]
    HUP INT QUIT ILL TRAP ABRT EMT FPE KILL BUS SEGV SYS PIPE ALRM TERM URG
    STOP TSTP CONT CHLD TTIN TTOU IO XCPU XFSZ VTALRM PROF WINCH INFO USR1 USR2

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    execution_duration : str, optional default to 1 second
        This is not technically not useful as the process usually is killed
        without and delay, however you can set more seconds here to let the
        thread wait for more time to extend your experiment execution in case
        you need to watch more on the observation metrics.
    process : str
        pid or process that kill command accepts
    signal : str , default to ""
        The signal of kill command, use kill -l for help
    configuration : Configuration
        Chaostoolkit Configuration
    secrets : Secrets
        Chaostoolkit Secrets
    """
    logger.debug(
        "Start network_latency: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    param = dict()
    param["duration"] = execution_duration
    param["param"] = process
    param["signal"] = signal

    return __default_salt_experiment__(instance_ids=instance_ids,
                                       execution_duration=execution_duration,
                                       param=param,
                                       experiment_type=KILL_PROCESS,
                                       configuration=configuration,
                                       secrets=secrets
                                       )


###############################################################################
# Private helper functions
###############################################################################
def __default_salt_experiment__(instance_ids: List[str] = None,
                                execution_duration: str = "60",
                                param: dict = None,
                                experiment_type: str = None,
                                configuration: Configuration = None,
                                secrets: Secrets = None
                                ) -> SaltStackResponse:
    response = dict()
    try:
        client = saltstack_api_client(secrets)
        machines = client.get_grains_get(instance_ids, 'kernel')

        jids = dict()

        if len(machines) <= 0:
            raise FailedActivity(
                "Cannot find any machines {}".format(instance_ids))

        for k, v in machines.items():
            name = k
            os_type = v
            param["instance_id"] = k
            script_content = __construct_script_content__(
                experiment_type, os_type, param)

            # Do async cmd and get jid
            logger.debug("{0} of machine: {1}".format(experiment_type, name))
            salt_method = 'cmd.run'
            jid = client.async_run_cmd(name, salt_method, script_content)
            jids[k] = jid
        logger.debug("SaltStack return jids:\n{}".format(json.dumps(jids)))
        # Wait the duration as well
        sleep(int(execution_duration))

        # Check result
        for k, v in jids.items():
            res = client.async_cmd_exit_success(v)[k]
            result = client.get_async_cmd_result(v)[k]
            if 'fail' in result:
                res = False
            response_item = "Machine {0} : {1} - Console: {2}".format(
                k, res, result)
            response[k] = response_item
        return response
    except Exception as x:
        raise FailedActivity(
            "failed issuing a execute of shell script via salt API " + str(x)
        )


def __construct_script_content__(action, os_type, parameters):

    if os_type == OS_WINDOWS:
        script_name = action+".ps1"
        # TODO in ps1
        cmd_param = '\n'.join(
            ['='.join([k, "'"+v+"'"]) for k, v in parameters.items()])
    elif os_type == OS_LINUX:
        script_name = action+".sh"
        cmd_param = '\n'.join(
            ['='.join([k, "'"+v+"'"]) for k, v in parameters.items()])
    else:
        raise FailedActivity(
            "Cannot find corresponding script for {} on OS: {}".format(
                action, os_type))

    with open(os.path.join(os.path.dirname(__file__),
                           "scripts", script_name)) as file:
        script_content = file.read()
    # merge duration
    script_content = cmd_param + "\n" + script_content
    return script_content
