from unittest.mock import MagicMock, patch, mock_open, call

from chaoslib.exceptions import FailedActivity
import pytest

from chaossaltstack.machine.actions import burn_cpu, burn_io, \
    network_advanced, network_corruption, network_latency, network_loss, \
    fill_disk, kill_process, killall_processes


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_burn_cpu_on_windows(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Windows"}
    client.async_run_cmd.return_value = "20190830103239148771"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True}

    # do
    burn_cpu(instance_ids=['CLIENT1'],
             execution_duration="1")

    open.assert_called_with(AnyStringWith("cpu_stress_test.ps1"))
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')
    client.async_run_cmd.assert_called_with('CLIENT1', 'cmd.run', AnyStringWith('script'))
    client.async_cmd_exit_success.assert_called_with('20190830103239148771')
    client.get_async_cmd_result.assert_called_with('20190830103239148771')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_burn_cpu_on_linux(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148771"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True}

    # do
    burn_cpu(instance_ids=['CLIENT1'],
             execution_duration="1")

    open.assert_called_with(AnyStringWith("cpu_stress_test.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')
    client.async_run_cmd.assert_called_with('CLIENT1', 'cmd.run', AnyStringWith('script'))
    client.async_cmd_exit_success.assert_called_with('20190830103239148771')
    client.get_async_cmd_result.assert_called_with('20190830103239148771')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_killall_processes_linux(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148771"
    client.get_async_cmd_result.return_value = {'CLIENT1': "experiment killall_processes -> processes <java> on <CLIENT1>: success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True}

    # do
    killall_processes(instance_ids=['CLIENT1'],
                      execution_duration="1",
                      signal="-9",
                      process_name="java")

    open.assert_called_with(AnyStringWith("killall_processes.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')
    client.async_run_cmd.assert_called_with('CLIENT1', 'cmd.run', AnyStringWith('script'))
    client.async_cmd_exit_success.assert_called_with('20190830103239148771')
    client.get_async_cmd_result.assert_called_with('20190830103239148771')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_kill_process_linux(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148771"
    client.get_async_cmd_result.return_value = {'CLIENT1': "experiment kill_process -> process <java> on <CLIENT1>: success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True}

    # do
    kill_process(instance_ids=['CLIENT1'],
                 execution_duration="1",
                 signal="-9",
                 process="java")

    open.assert_called_with(AnyStringWith("kill_process.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')
    client.async_run_cmd.assert_called_with('CLIENT1', 'cmd.run', AnyStringWith('script'))
    client.async_cmd_exit_success.assert_called_with('20190830103239148771')
    client.get_async_cmd_result.assert_called_with('20190830103239148771')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_burn_cpu_on_linux_two(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "Stressing CLIENT2 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT2> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    burn_cpu(instance_ids=['CLIENT1', 'CLIENT2'],
             execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("cpu_stress_test.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_burn_cpu_on_linux_two_error_in_script(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "experiment strees_cpu <CLIENT2> -> fail"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = burn_cpu(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("cpu_stress_test.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'success' in response['CLIENT1']
    assert 'fail' in response['CLIENT2']


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_bad_machines(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "experiment strees_cpu <CLIENT2> -> fail"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    with pytest.raises(FailedActivity, match=r"Cannot find any machines.*"):
        response = burn_cpu(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_burn_cpu_on_linux_two_error_in_execution(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "experiment strees_cpu <CLIENT2> -> failed"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': False}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = burn_cpu(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("cpu_stress_test.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'success' in response['CLIENT1']
    assert 'failed' in response['CLIENT2']

@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_burn_cpu_on_linux_wrong_os_type(init, open):
    # mock
    client = MagicMock()
    init.return_value = client
    client.get_grains_get.return_value = {'CLIENT1': "invalid"}
    # do
    with pytest.raises(FailedActivity, match=r"failed issuing a execute of shell script via salt API Cannot find corresponding script for cpu_stress_test on OS: invalid"):
        response = burn_cpu(instance_ids=['CLIENT1'], execution_duration="1")
    # assert
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_burn_io_on_linux(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148771"
    client.get_async_cmd_result.return_value = {'CLIENT1': "success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True}

    # do
    burn_io(instance_ids=['CLIENT1'],
             execution_duration="1")

    open.assert_called_with(AnyStringWith("burn_io.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')
    client.async_run_cmd.assert_called_with('CLIENT1', 'cmd.run', AnyStringWith('script'))
    client.async_cmd_exit_success.assert_called_with('20190830103239148771')
    client.get_async_cmd_result.assert_called_with('20190830103239148771')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_burn_io_on_linux_two(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "success",
                                                'CLIENT2': "success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    burn_io(instance_ids=['CLIENT1', 'CLIENT2'],
             execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("burn_io.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_burn_io_on_linux_two_error_script(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "success",
                                                'CLIENT2': "fail"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = burn_io(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("burn_io.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'fail' in response['CLIENT2']
    assert 'success' in response['CLIENT1']


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_burn_io_on_linux_two_error_execution(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "success",
                                                'CLIENT2': "success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': False, 'CLIENT2': True}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = burn_io(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("burn_io.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'success' in response['CLIENT2']
    assert 'False' in response['CLIENT1']


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_fill_disk_on_windows(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Windows"}
    client.async_run_cmd.return_value = "20190830103239148771"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True}

    # do
    fill_disk(instance_ids=['CLIENT1'], execution_duration="1")

    open.assert_called_with(AnyStringWith("fill_disk.ps1"))
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')
    client.async_run_cmd.assert_called_with('CLIENT1', 'cmd.run', AnyStringWith('script'))
    client.async_cmd_exit_success.assert_called_with('20190830103239148771')
    client.get_async_cmd_result.assert_called_with('20190830103239148771')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_fill_disk_on_linux(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148771"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True}

    # do
    fill_disk(instance_ids=['CLIENT1'], execution_duration="1")

    open.assert_called_with(AnyStringWith("fill_disk.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')
    client.async_run_cmd.assert_called_with('CLIENT1', 'cmd.run', AnyStringWith('script'))
    client.async_cmd_exit_success.assert_called_with('20190830103239148771')
    client.get_async_cmd_result.assert_called_with('20190830103239148771')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_fill_disk_on_linux_two(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "success",
                                                'CLIENT2': "success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    fill_disk(instance_ids=['CLIENT1', 'CLIENT2'],
            execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("fill_disk.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_fill_disk_on_linux_two_error_script(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "success",
                                                'CLIENT2': "fail"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = fill_disk(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("fill_disk.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'fail' in response['CLIENT2']
    assert 'success' in response['CLIENT1']


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_fill_disk_on_linux_two_error_execution(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "success",
                                                'CLIENT2': "success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': False, 'CLIENT2': True}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = fill_disk(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("fill_disk.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'success' in response['CLIENT2']
    assert 'False' in response['CLIENT1']


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_latency_on_linux(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148771"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True}

    # do
    network_latency(instance_ids=['CLIENT1'], execution_duration="1")

    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')
    client.async_run_cmd.assert_called_with('CLIENT1', 'cmd.run', AnyStringWith('script'))
    client.async_cmd_exit_success.assert_called_with('20190830103239148771')
    client.get_async_cmd_result.assert_called_with('20190830103239148771')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_latency_on_linux_two(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "Stressing CLIENT2 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT2> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    network_latency(instance_ids=['CLIENT1', 'CLIENT2'],
             execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_latency_on_linux_two_error_in_script(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "experiment strees_cpu <CLIENT2> -> fail"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = network_latency(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1", device="ens192")

    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'fail' in response['CLIENT2']
    assert 'success' in response['CLIENT1']


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_latency_on_linux_two_error_in_execution(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "experiment strees_cpu <CLIENT2> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': False}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = network_latency(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'False' in response['CLIENT2']
    assert 'success' in response['CLIENT1']


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_loss_on_linux(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148771"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True}

    # do
    network_loss(instance_ids=['CLIENT1'], execution_duration="1")

    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')
    client.async_run_cmd.assert_called_with('CLIENT1', 'cmd.run', AnyStringWith('script'))
    client.async_cmd_exit_success.assert_called_with('20190830103239148771')
    client.get_async_cmd_result.assert_called_with('20190830103239148771')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_loss_on_linux_two(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "Stressing CLIENT2 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT2> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    network_loss(instance_ids=['CLIENT1', 'CLIENT2'],
                    execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_loss_on_linux_two_error_in_script(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "experiment strees_cpu <CLIENT2> -> fail"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = network_loss(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'fail' in response['CLIENT2']
    assert 'success' in response['CLIENT1']


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_loss_on_linux_two_error_in_execution(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "experiment strees_cpu <CLIENT2> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': False}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = network_loss(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'False' in response['CLIENT2']
    assert 'success' in response['CLIENT1']


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_corruption_on_linux(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148771"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True}

    # do
    network_corruption(instance_ids=['CLIENT1'], execution_duration="1")

    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')
    client.async_run_cmd.assert_called_with('CLIENT1', 'cmd.run', AnyStringWith('script'))
    client.async_cmd_exit_success.assert_called_with('20190830103239148771')
    client.get_async_cmd_result.assert_called_with('20190830103239148771')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_corruption_on_linux_two(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "Stressing CLIENT2 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT2> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    network_corruption(instance_ids=['CLIENT1', 'CLIENT2'],
                       execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_corruption_on_linux_two_error_in_script(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "experiment strees_cpu <CLIENT2> -> fail"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = network_corruption(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'fail' in response['CLIENT2']
    assert 'success' in response['CLIENT1']

@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_corruption_on_linux_two_error_in_execution(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "experiment strees_cpu <CLIENT2> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': False}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = network_corruption(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'False' in response['CLIENT2']
    assert 'success' in response['CLIENT1']


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_advanced_on_linux(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148771"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True}

    # do
    network_advanced(instance_ids=['CLIENT1'], execution_duration="1", command="loss 5%")

    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1'], 'kernel')
    client.async_run_cmd.assert_called_with('CLIENT1', 'cmd.run', AnyStringWith('script'))
    client.async_cmd_exit_success.assert_called_with('20190830103239148771')
    client.get_async_cmd_result.assert_called_with('20190830103239148771')


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_advanced_on_linux_two(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "Stressing CLIENT2 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT2> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    network_advanced(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1", command="loss 5%")
    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_advanced_on_linux_two_error_in_script(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "experiment strees_cpu <CLIENT2> -> fail"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': True}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = network_advanced(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1", command="loss 5%")
    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'fail' in response['CLIENT2']
    assert 'success' in response['CLIENT1']


@patch("builtins.open", new_callable=mock_open, read_data="script")
@patch('chaossaltstack.machine.actions.saltstack_api_client', autospec=True)
def test_network_advanced_on_linux_two_error_in_execution(init, open):
    # mock
    client = MagicMock()
    init.return_value = client

    client.get_grains_get.return_value = {'CLIENT1': "Linux", 'CLIENT2': "Linux"}
    client.async_run_cmd.return_value = "20190830103239148772"
    client.get_async_cmd_result.return_value = {'CLIENT1': "Stressing CLIENT1 1 CPUs for 180 seconds.\nStressing 1 CPUs for 180 seconds. Done\nexperiment strees_cpu <CLIENT1> -> success",
                                                'CLIENT2': "experiment strees_cpu <CLIENT2> -> success"}
    client.async_cmd_exit_success.return_value = {'CLIENT1': True, 'CLIENT2': False}

    # do
    # with pytest.raises(FailedActivity, match=r"One of experiments are failed among.*"):
    response = network_advanced(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1", command="loss 5%")
    # assert
    open.assert_called_with(AnyStringWith("network_advanced.sh"))
    client.get_grains_get.assert_called_with(['CLIENT1', 'CLIENT2'], 'kernel')
    assert client.async_run_cmd.mock_calls == [call('CLIENT1', 'cmd.run', AnyStringWith('script')),
                                               call('CLIENT2', 'cmd.run', AnyStringWith('script'))]
    assert client.async_cmd_exit_success.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert client.get_async_cmd_result.mock_calls == [call('20190830103239148772'), call('20190830103239148772')]
    assert 'False' in response['CLIENT2']
    assert 'success' in response['CLIENT1']


def test_exception():
    # do directly to exception:
    with pytest.raises(FailedActivity, match=r"configuration is not complete.*"):
        network_advanced(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1", command="loss 5%")
    with pytest.raises(FailedActivity, match=r"configuration is not complete.*"):
        burn_cpu(instance_ids=['CLIENT1'],
                 execution_duration="1")
    with pytest.raises(FailedActivity, match=r"configuration is not complete.*"):
        burn_io(instance_ids=['CLIENT1', 'CLIENT2'],
                execution_duration="1")
    with pytest.raises(FailedActivity, match=r"configuration is not complete.*"):
        fill_disk(instance_ids=['CLIENT1'], execution_duration="1")
    with pytest.raises(FailedActivity, match=r"configuration is not complete.*"):
        network_corruption(instance_ids=['CLIENT1', 'CLIENT2'],
                           execution_duration="1")
    with pytest.raises(FailedActivity, match=r"configuration is not complete.*"):
        network_loss(instance_ids=['CLIENT1', 'CLIENT2'], execution_duration="1")
    with pytest.raises(FailedActivity, match=r"configuration is not complete.*"):
        network_latency(instance_ids=['CLIENT1'], execution_duration="1")
