# -*- coding: utf-8 -*-
import os
import json
from time import sleep
from typing import List

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from .. import saltstack_api_client
from .constants import OS_LINUX, OS_WINDOWS
from .constants import BURN_CPU, FILL_DISK, NETWORK_UTIL, \
    BURN_IO


__all__ = ["burn_cpu", "fill_disk", "network_latency", "burn_io",
           "network_loss", "network_corruption", "network_advanced"]


def burn_cpu(instance_ids: List[str] = None,
             execution_duration: str = "60",
             configuration: Configuration = None,
             secrets: Secrets = None):
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
    """

    logger.debug(
        "Start burn_cpu: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    try:
        client = saltstack_api_client(secrets)
        machines = client.get_grains_get(instance_ids, 'kernel')

        param = dict()
        param["duration"] = execution_duration

        jids = dict()

        if len(machines) <= 0:
            FailedActivity(
                "Cannot find any machines {}".format(instance_ids))

        for k, v in machines.items():
            name = k
            os_type = v
            param["instance_id"] = k
            script_content = __construct_script_content__(
                BURN_CPU, os_type, param)

            # Do async cmd and get jid
            logger.debug("Burning CPU of machine: {}".format(name))
            salt_method = 'cmd.run'
            jid = client.async_run_cmd(name, salt_method, script_content)
            jids[k] = jid
        logger.debug(json.dumps(jids))
        # Wait the duration as well
        sleep(int(execution_duration))

        # Check result
        results = dict()
        results_overview = True
        for k, v in jids.items():
            res = client.async_cmd_exit_success(v)[k]
            result = client.get_async_cmd_result(v)[k]
            if 'fail' in result:
                res = False
            results_overview = results_overview and res
            results[k] = result
    except Exception as x:
        raise FailedActivity(
            "failed issuing a execute of shell script via salt API {}".format(
                str(x)
            ))

    if results:
        for k, v in results.items():
            logger.info(k + " - " + v)
    else:
        raise FailedActivity(
            "burn_cpu operation did not finish on time. "
        )

    if results_overview is False:
        raise FailedActivity(
            "One of experiments are failed among : {} ".format(results)
        )


def fill_disk(instance_ids: List[str] = None,
              execution_duration: str = "120",
              size: int = 1000,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    For now do not have this scenario, fill the disk with random data.

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    execution_duration : str, optional
        Lifetime of the file created. Defaults to 120 seconds.
    size : int
        Size of the file created on the disk. Defaults to 1GB.
    """

    logger.debug(
        "Start fill_disk: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    try:
        client = saltstack_api_client(secrets)
        machines = client.get_grains_get(instance_ids, 'kernel')

        param = dict()
        param["execution_duration"] = execution_duration

        jids = dict()

        if len(machines) <= 0:
            FailedActivity(
                "Cannot find any machines {}".format(instance_ids))

        for k, v in machines.items():
            name = k
            os_type = v
            param["instance_id"] = k
            script_content = __construct_script_content__(
                FILL_DISK, os_type, param)

            # Do async cmd and get jid
            logger.debug("Filling disk of machine: {}".format(name))
            salt_method = 'cmd.run'
            jid = client.async_run_cmd(name, salt_method, script_content)
            jids[k] = jid
        logger.debug(json.dumps(jids))
        # Wait the duration as well
        sleep(int(execution_duration))

        # Check result
        results = dict()
        results_overview = True
        for k, v in jids.items():
            res = client.async_cmd_exit_success(v)[k]
            result = client.get_async_cmd_result(v)[k]
            if 'fail' in result:
                res = False
            results_overview = results_overview and res
            results[k] = result
    except Exception as x:
        raise FailedActivity(
            "failed issuing a execute of shell script via salt API {}".format(
                str(x)
            ))

    if results:
        for k, v in results.items():
            logger.info(k + " - " + v)
    else:
        raise FailedActivity(
            "fill_disk operation did not finish on time. "
        )

    if results_overview is False:
        raise FailedActivity(
            "One of experiments are failed among : {} ".format(results)
        )


def burn_io(instance_ids: List[str] = None,
            execution_duration: str = "60",
            configuration: Configuration = None,
            secrets: Secrets = None):
    """
    Increases the Disk I/O operations per second of the virtual machine.

    Parameters
    ----------
    instance_ids : List[str]
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    execution_duration : str, optional
        Lifetime of the file created. Defaults to 120 seconds.
    """

    logger.debug(
        "Start burn_io: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    logger.debug(json.dumps(secrets))

    try:
        client = saltstack_api_client(secrets)
        machines = client.get_grains_get(instance_ids, 'kernel')

        param = dict()
        param["duration"] = execution_duration

        jids = dict()

        if len(machines) <= 0:
            FailedActivity(
                "Cannot find any machines {}".format(instance_ids))

        for k, v in machines.items():
            name = k
            os_type = v
            param["instance_id"] = k
            script_content = __construct_script_content__(
                BURN_IO, os_type, param)

            # Do async cmd and get jid
            logger.debug("Burning I/O of machine: {}".format(name))
            salt_method = 'cmd.run'
            jid = client.async_run_cmd(name, salt_method, script_content)
            jids[k] = jid
        logger.debug(json.dumps(jids))
        # Wait the duration as well
        sleep(int(execution_duration))

        # Check result
        results = dict()
        results_overview = True
        for k, v in jids.items():
            res = client.async_cmd_exit_success(v)[k]
            result = client.get_async_cmd_result(v)[k]
            if 'fail' in result:
                res = False
            results_overview = results_overview and res
            results[k] = result
    except Exception as x:
        raise FailedActivity(
            "failed issuing a execute of shell script via salt API {}".format(
                str(x)
            ))

    if results:
        for k, v in results.items():
            logger.info(k + " - " + v)
    else:
        raise FailedActivity(
            "burn io operation did not finish on time. "
        )

    if results_overview is False:
        raise FailedActivity(
            "One of experiments are failed among : {} ".format(results)
        )


def network_advanced(instance_ids: List[str] = None,
                     execution_duration: str = "60",
                     command: str = "",
                     configuration: Configuration = None,
                     secrets: Secrets = None):
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
    """

    logger.debug(
        "Start network_advanced: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    logger.debug(json.dumps(secrets))

    try:
        client = saltstack_api_client(secrets)
        machines = client.get_grains_get(instance_ids, 'kernel')

        param = dict()
        param["duration"] = execution_duration
        param["param"] = command

        jids = dict()

        if len(machines) <= 0:
            FailedActivity(
                "Cannot find any machines {}".format(instance_ids))

        for k, v in machines.items():
            name = k
            os_type = v
            param["instance_id"] = k
            script_content = __construct_script_content__(
                NETWORK_UTIL, os_type, param)

            # Do async cmd and get jid
            logger.debug("network_advanced of machine: {}".format(name))
            salt_method = 'cmd.run'
            jid = client.async_run_cmd(name, salt_method, script_content)
            jids[k] = jid
        logger.debug(json.dumps(jids))
        # Wait the duration as well
        sleep(int(execution_duration))

        # Check result
        results = dict()
        results_overview = True
        for k, v in jids.items():
            res = client.async_cmd_exit_success(v)[k]
            result = client.get_async_cmd_result(v)[k]
            if 'fail' in result:
                res = False
            results_overview = results_overview and res
            results[k] = result
    except Exception as x:
        raise FailedActivity(
            "failed issuing a execute of shell script via salt API {}".format(
                str(x)
            )
        )

    if results:
        for k, v in results.items():
            logger.info(k + " - " + v)
    else:
        raise FailedActivity(
            "network_advanced operation did not finish on time. "
        )
    if results_overview is False:
        raise FailedActivity(
            "One of experiments are failed among : {} ".format(results)
        )


def network_loss(instance_ids: List[str] = None,
                 execution_duration: str = "60",
                 loss_ratio: str = "5%",
                 configuration: Configuration = None,
                 secrets: Secrets = None):
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
    """

    logger.debug(
        "Start network_advanced: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    try:
        client = saltstack_api_client(secrets)
        machines = client.get_grains_get(instance_ids, 'kernel')

        param = dict()
        param["duration"] = execution_duration
        param["param"] = "loss " + loss_ratio

        jids = dict()

        if len(machines) <= 0:
            FailedActivity(
                "Cannot find any machines {}".format(instance_ids))

        for k, v in machines.items():
            name = k
            os_type = v
            param["instance_id"] = k
            script_content = __construct_script_content__(
                NETWORK_UTIL, os_type, param)

            # Do async cmd and get jid
            logger.debug("network_loss of machine: {}".format(name))
            salt_method = 'cmd.run'
            jid = client.async_run_cmd(name, salt_method, script_content)
            jids[k] = jid
        logger.debug(json.dumps(jids))
        # Wait the duration as well
        sleep(int(execution_duration))

        # Check result
        results = dict()
        results_overview = True
        for k, v in jids.items():
            res = client.async_cmd_exit_success(v)[k]
            result = client.get_async_cmd_result(v)[k]
            if 'fail' in result:
                res = False
            results_overview = results_overview and res
            results[k] = result
    except Exception as x:
        raise FailedActivity(
            "failed issuing a execute of shell script via salt API {}".format(
                str(x)
            )
        )

    if results:
        for k, v in results.items():
            logger.info(k + " - " + v)
    else:
        raise FailedActivity(
            "network_loss operation did not finish on time. "
        )
    if results_overview is False:
        raise FailedActivity(
            "One of experiments are failed among : {} ".format(results)
        )


def network_corruption(instance_ids: List[str] = None,
                       execution_duration: str = "60",
                       corruption_ratio: str = "5%",
                       configuration: Configuration = None,
                       secrets: Secrets = None):
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
    """

    logger.debug(
        "Start network_corruption: configuration='{}', "
        "instance_ids='{}'".format(configuration, instance_ids))

    try:
        client = saltstack_api_client(secrets)
        machines = client.get_grains_get(instance_ids, 'kernel')

        param = dict()
        param["duration"] = execution_duration
        param["param"] = "corrupt " + corruption_ratio

        jids = dict()

        if len(machines) <= 0:
            FailedActivity(
                "Cannot find any machines {}".format(instance_ids))

        for k, v in machines.items():
            name = k
            os_type = v
            param["instance_id"] = k
            script_content = __construct_script_content__(
                NETWORK_UTIL, os_type, param)

            # Do async cmd and get jid
            logger.debug("network_corruption of machine: {}".format(name))
            salt_method = 'cmd.run'
            jid = client.async_run_cmd(name, salt_method, script_content)
            jids[k] = jid
        logger.debug(json.dumps(jids))
        # Wait the duration as well
        sleep(int(execution_duration))

        # Check result
        results = dict()
        results_overview = True
        for k, v in jids.items():
            res = client.async_cmd_exit_success(v)[k]
            result = client.get_async_cmd_result(v)[k]
            if 'fail' in result:
                res = False
            results_overview = results_overview and res
            results[k] = result
    except Exception as x:
        raise FailedActivity(
            "failed issuing a execute of shell script via salt API {}".format(
                str(x)
            )
        )

    if results:
        for k, v in results.items():
            logger.info(k + " - " + v)
    else:
        raise FailedActivity(
            "network_corruption operation did not finish on time. "
        )

    if results_overview is False:
        raise FailedActivity(
            "One of experiments are failed among : {} ".format(results)
        )


def network_latency(instance_ids: List[str] = None,
                    execution_duration: str = "60",
                    delay: str = "1000ms",
                    variance: str = "500ms",
                    ratio: str = "",
                    configuration: Configuration = None,
                    secrets: Secrets = None):
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
    """
    logger.debug(
        "Start network_latency: configuration='{}', instance_ids='{}'".format(
            configuration, instance_ids))

    try:
        client = saltstack_api_client(secrets)
        machines = client.get_grains_get(instance_ids, 'kernel')

        param = dict()
        param["duration"] = execution_duration
        param["param"] = "delay " + delay + " " + variance + " " + ratio

        jids = dict()

        if len(machines) <= 0:
            FailedActivity(
                "Cannot find any machines {}".format(instance_ids))

        for k, v in machines.items():
            name = k
            os_type = v
            param["instance_id"] = k
            script_content = __construct_script_content__(
                NETWORK_UTIL, os_type, param)

            # Do async cmd and get jid
            logger.debug("network_latency of machine: {}".format(name))
            salt_method = 'cmd.run'
            jid = client.async_run_cmd(name, salt_method, script_content)
            jids[k] = jid
        logger.debug(json.dumps(jids))
        # Wait the duration as well
        sleep(int(execution_duration))

        # Check result
        results = dict()
        results_overview = True
        for k, v in jids.items():
            res = client.async_cmd_exit_success(v)[k]
            result = client.get_async_cmd_result(v)[k]
            if 'fail' in result:
                res = False
            results_overview = results_overview and res
            results[k] = result

    except Exception as x:
        raise FailedActivity(
            "failed issuing a execute of shell script via salt API " + str(x)
        )

    if results:
        for k, v in results.items():
            logger.info(k + " - " + v)
    else:
        raise FailedActivity(
            "network_latency operation did not finish on time. "
        )
    if results_overview is False:
        raise FailedActivity(
            "One of experiments are failed among : {} ".format(results)
        )


###############################################################################
# Private helper functions
###############################################################################
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
