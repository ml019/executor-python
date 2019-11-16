import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.run.lambda_func import lambda_func as run_lambda_func
from tests.unit.command.test_option_generation import (
    generate_test_options_collection,
    generate_incremental_required_options_collection
)


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['!-u,--deployment-unit'] = 'unit'
ALL_VALID_OPTIONS['!-f,--function-id'] = 'function_id'
ALL_VALID_OPTIONS['-i,--input-payload'] = 'payload'
ALL_VALID_OPTIONS['-l,--include-log-tail'] = [True, False]


@mock.patch('cot.command.run.lambda_func.subprocess')
def test_input_valid(subprocess_mock):
    assert len(ALL_VALID_OPTIONS) == len(run_lambda_func.params)
    runner = CliRunner()
    # testing that's impossible to run without full set of required options
    for args, error in generate_incremental_required_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(run_lambda_func, args)
        if error:
            assert result.exit_code == 2, result.output
            assert subprocess_mock.run.call_count == 0
        else:
            assert result.exit_code == 0, result.output
            assert subprocess_mock.run.call_count == 1
            subprocess_mock.run.call_count = 0
    for args in generate_test_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(run_lambda_func, args)
        assert result.exit_code == 0, result.output
        assert subprocess_mock.run.call_count == 1
        subprocess_mock.run.call_count = 0
