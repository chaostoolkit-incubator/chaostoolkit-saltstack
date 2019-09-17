from unittest.mock import MagicMock, patch

from chaossaltstack.machine.probes import is_minion_online, \
    is_iproute_tc_installed
from chaoslib.exceptions import FailedActivity
import pytest


THREE_INSTANCE = ["CLIENT1", "CLIENT2", "CLIENT3"]
ONLINE_MINION = ["CLIENT1"]
OFFLINE_MINION = ["CLIENT2"]
NO_MINION = ["CLIENT3"]
ONLINE_MINIONS = ["CLIENT1", "CLIENT4"]


@patch('chaossaltstack.machine.probes.saltstack_api_client', autospec=True)
def test_is_minion_online_multiple_minions(init):
    # mock
    client = MagicMock()
    init.return_value = client
    cmd_return_value = {"CLIENT1": True,"CLIENT2": False}
    client.run_cmd.return_value = cmd_return_value
    # # do
    res = is_minion_online(instance_ids=THREE_INSTANCE)
    # # assert
    assert res["CLIENT1"] == "Online"
    assert res["CLIENT2"] == "Offline"
    assert res["CLIENT3"] == "Not a Salt Minion"


@patch('chaossaltstack.machine.probes.saltstack_api_client', autospec=True)
def test_is_minion_online_offline_single(init):
    # mock
    client = MagicMock()
    init.return_value = client
    cmd_return_value = {"CLIENT2": False}
    client.run_cmd.return_value = cmd_return_value
    # do
    res = is_minion_online(instance_ids=OFFLINE_MINION)

    assert res["CLIENT2"] == "Offline"


@patch('chaossaltstack.machine.probes.saltstack_api_client', autospec=True)
def test_is_minion_online_online_single(init):
    # mock
    client = MagicMock()
    init.return_value = client
    cmd_return_value = {"CLIENT1": True}
    client.run_cmd.return_value = cmd_return_value

    res = is_minion_online(instance_ids=ONLINE_MINION)

    assert res["CLIENT1"] == "Online"


@patch('chaossaltstack.machine.probes.saltstack_api_client', autospec=True)
def test_is_minion_online_not_minion(init):
    # mock
    client = MagicMock()
    init.return_value = client
    cmd_return_value = {"": ''}
    client.run_cmd.return_value = cmd_return_value

    res = is_minion_online(instance_ids=NO_MINION)

    assert res["CLIENT3"] == "Not a Salt Minion"


@patch('chaossaltstack.machine.probes.saltstack_api_client', autospec=True)
def test_is_minion_online_online_two(init):
    # mock
    client = MagicMock()
    init.return_value = client
    cmd_return_value = {"CLIENT1": True, "CLIENT4": True}
    client.run_cmd.return_value = cmd_return_value

    res = is_minion_online(instance_ids=ONLINE_MINIONS)

    assert res["CLIENT4"] == "Online"
    assert res["CLIENT1"] == "Online"


@patch('chaossaltstack.machine.probes.saltstack_api_client', autospec=True)
def test_is_iproute_tc_installed_multiple_minions(init):
    # mock
    client = MagicMock()
    init.return_value = client
    cmd_return_value = {'CLIENT1': 'Usage: tc xxxxx', 'CLIENT2': 'tc: command not found'}
    client.run_cmd.return_value = cmd_return_value
    # do
    res = is_iproute_tc_installed(instance_ids=THREE_INSTANCE)
    # assert
    assert res["CLIENT1"] == "Installed"
    assert res["CLIENT2"] == "Not Installed"
    assert res["CLIENT3"] == "Not a Salt Minion"


@patch('chaossaltstack.machine.probes.saltstack_api_client', autospec=True)
def test_is_iproute_tc_installed_single_not_installed(init):
    # mock
    client = MagicMock()
    init.return_value = client
    cmd_return_value = {'CLIENT1': 'Usage: tc xxxxx'}
    client.run_cmd.return_value = cmd_return_value
    # do
    res = is_iproute_tc_installed(instance_ids=ONLINE_MINION)
    # assert
    assert res["CLIENT1"] == "Installed"


@patch('chaossaltstack.machine.probes.saltstack_api_client', autospec=True)
def test_is_iproute_tc_installed_single_installed(init):
    # mock
    client = MagicMock()
    init.return_value = client
    cmd_return_value = {'CLIENT2': 'tc: command not found'}
    client.run_cmd.return_value = cmd_return_value
    # do
    res = is_iproute_tc_installed(instance_ids=OFFLINE_MINION)
    # assert
    assert res["CLIENT2"] == "Not Installed"


@patch('chaossaltstack.machine.probes.saltstack_api_client', autospec=True)
def test_is_iproute_tc_installed_two_installed(init):
    # mock
    client = MagicMock()
    init.return_value = client
    cmd_return_value = {'CLIENT1': 'Usage: tc xxxxx', 'CLIENT4': 'Usage: tc xxxxx'}
    client.run_cmd.return_value = cmd_return_value
    # do
    res = is_iproute_tc_installed(instance_ids=ONLINE_MINIONS)
    # assert
    assert res["CLIENT1"] == "Installed"
    assert res["CLIENT4"] == "Installed"


@patch('chaossaltstack.machine.probes.saltstack_api_client', autospec=True)
def test_is_iproute_tc_installed_not_minion(init):
    # mock
    client = MagicMock()
    init.return_value = client
    cmd_return_value = {'': ''}
    client.run_cmd.return_value = cmd_return_value
    # do
    res = is_iproute_tc_installed(instance_ids=NO_MINION)
    # assert
    assert res["CLIENT3"] == "Not a Salt Minion"

