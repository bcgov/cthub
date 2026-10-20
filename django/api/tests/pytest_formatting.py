from api.utilities.formatting import format_case, format_numbers
import pandas as pd
import numpy as np
from pytest_check import check
import pytest


def error_msg(s, opt=''):
    if len(opt) != 0:
        opt = ' (' + opt + ')'
    return s + ' -- is incorrect' + opt


def test_format_numbers():

    test_df = {}
    test_series = {}
    actual = {}
    expected = {}
    message = {}

    # Test case 1
    test_series['int'] = pd.Series([1, 2, 30])
    expected['int'] = test_series['int'].astype('Int64')
    actual['int'] = format_numbers(test_series['int'])
    message['int'] = 'Case 1: Integers'

    # Test case 2
    test_series['int_nan'] = pd.Series([1, 2, 30, np.nan])
    expected['int_nan'] = test_series['int'].astype('Int64')
    actual['int_nan'] = format_numbers(test_series['int_nan'])
    message['int_nan'] = 'Case 2: Integers and np.nan'

    # Test case 3
    test_series['str'] = pd.Series(['20', '30.5', '40,000', '51.50', '1,999.9'])
    expected['str'] = pd.Series([20, 30, 40000, 52, 2000]).astype('Int64')
    actual['str'] = format_numbers(test_series['str'])
    message['str'] = 'Case 3: Strings'

    # Test case 4
    test_series['flt'] = pd.Series([10.5, 1000.000, 33.4, 21.5])
    expected['flt'] = pd.Series([10, 1000, 33, 22]).astype('Int64')
    actual['flt'] = format_numbers(test_series['flt'])
    message['flt'] = 'Case 3: Floats'

    # Test case 5
    test_series['nan'] = pd.Series([np.nan, None, pd.NA])
    expected['nan'] = pd.Series([]).astype('Int64')
    actual['nan'] = format_numbers(test_series['nan'])
    message['nan'] = 'Case 5: NAs'

    # Test 6 mix
    test_series['mix'] = pd.Series([np.nan, 10.3, '2.75', 1, 4.4, 123467678842255332])
    expected['mix'] = pd.Series([10, 3, 1, 4, 123467678842255332]).astype('Int64')
    expected['mix'].index = expected['mix'].index + 1
    actual['mix'] = format_numbers(test_series['mix'])
    message['mix'] = 'Case 6: Mix'

    # Test 7 df mix
    test_df['df_mix'] = pd.DataFrame(test_series['mix'])
    expected['df_mix'] = pd.DataFrame(
        pd.Series([pd.NA, 10, 3, 1, 4, 123467678842255332]).astype('Int64'))
    test_df['df_mix'][0] = format_numbers(test_df['df_mix'][0])
    actual['df_mix'] = test_df['df_mix']
    message['df_mix'] = 'Case 7: Mix in df'

    # Test 8 df NAs
    test_df['df_nan'] = pd.DataFrame(test_series['nan'])
    expected['df_nan'] = pd.DataFrame(
        pd.Series([pd.NA, pd.NA, pd.NA]).astype('Int64'))
    test_df['df_nan'][0] = format_numbers(test_df['df_nan'][0])
    actual['df_nan'] = test_df['df_nan']
    message['df_nan'] = 'Case 8: NANs only in df'

    for case in expected:
        with check:
            assert actual[case].equals(expected[case]) == True, error_msg(message[case])

    with pytest.raises(ValueError, match=r'Invalid or ambiguous number format'):
        format_numbers(pd.Series(['78,11']))

    with pytest.raises(ValueError, match=r'Series is empty'):
        format_numbers(pd.Series([]))

@pytest.mark.parametrize(
    'value',
    [
    '78,11',
    '2000,0000',
    '2,00',
    '2,0000',
    ]
    )
def test_ambiguous_formats_raise(value):
    with pytest.raises(
    ValueError,
    match='Invalid or ambiguous number format'
    ):
        format_numbers(pd.Series([value]))

@pytest.mark.parametrize(
    "value, expected",
    [
        ('20', 20),
        ('30.5', 30),
        ('40,000', 40000),
        ('10,500.60', 10501),
        ('13,000,000', 13000000)
    ],
    )
def test_valid_string_formats(value, expected):
    result = format_numbers(pd.Series([value]))
    assert result.iloc[0] == expected


@pytest.mark.parametrize(
    'value',
    [np.nan, None, pd.NA, '', ',']
    )
def test_missing_values_are_removed(value):
    result = format_numbers(pd.Series([value]))
    assert result.empty
    assert result.dtype == 'Int64'

@pytest.mark.parametrize(
    'input_series, case, expected',
    [
        (
            pd.Series(['hello world', 'test value']),
            'title',
            pd.Series(['Hello World', 'Test Value']),
        ),
        (
            pd.Series(['hello', 'world']),
            'upper',
            pd.Series(['HELLO', 'WORLD']),
        ),
        (
            pd.Series(['HELLO', 'WORLD']),
            'lower',
            pd.Series(['hello', 'world']),
        ),
        (
            pd.Series(['A1B 2C3', 'z1y 2D3', 'A7S6H8', '1']),
            'postal_code',
            pd.Series(['A1B2C3', 'Z1Y2D3', 'A7S6H8', '1']),
        ),
        (
            pd.Series(['  Hello  ', ' World ']),
            'skip',
            pd.Series(['Hello', 'World']),
        ),
        (
            pd.Series(['world', np.nan]),
            'skip',
            pd.Series(['world']),
        ),
        (
            pd.Series([1, 2]),
            'title',
            pd.Series(['1', '2']),
        )
    ],
)
def test_format_case(input_series, case, expected):
    actual = format_case(input_series, case=case)

    assert actual.equals(expected)

def test_format_case_error():
    with pytest.raises(ValueError, match=r'Incorrect case option'):
        format_case(pd.Series(['a', 'b']), 'lorem ipsum')

@pytest.mark.parametrize(
    'value',
    [
        'a2.5',
        '1a.9',
        'ABC.0',
        '1a.00',
        '12.5',
        '19069217904925943.7'
    ],
)
def test_format_case_ambiguous_id(value):
    with pytest.raises(ValueError, match=r'Ambiguous value'):
        format_case(pd.Series([value]), 'id')

@pytest.mark.parametrize(
    'value, expected',
    [
        pytest.param('00010', '10', id='leading zeros'),
        pytest.param('0000', '0', id='all zeros'),
        pytest.param('0', '0', id='single zero'),
        pytest.param('10', '10', id='no normalization needed'),
        pytest.param('10.0', '10', id='decimal zero'),
        pytest.param('00010.00', '10', id='leading and decimal zeros'),
        pytest.param('  00010  ', '10', id='surrounding spaces'),
        pytest.param('abc', 'abc', id='letters only'),
        pytest.param('0abc0', '0abc0', id='letters with zeroes'),
        pytest.param('0abc80', '0abc80', id='letters with digits and zeroes'),
        pytest.param('0XYZ80', '0xyz80', id='upper letters with digits and zeroes'),
        pytest.param('19069217904925943', '19069217904925943', id='large_int'),
        pytest.param('19069217904925943.0', '19069217904925943', id='large_int with .0')    ],
)
def test_format_case_id(value, expected):
    actual = format_case(
        pd.Series([value]),
        case='id',
    )

    assert actual.iloc[0] == expected

def test_format_case_id_with_missing_value():
    actual = format_case(pd.Series(['00010', pd.NA]), case='id')
    expected = pd.Series(['10'])

    assert actual.equals(expected)

@pytest.mark.parametrize(
    'case',
    [
        'title',
        'upper',
        'lower',
        'postal_code',
        'id',
        'skip'
    ],
)
@pytest.mark.parametrize(
    'value',
    [
        np.nan,
        pd.NA,
        None,
    ],
)
def test_format_case_missing_values(case, value):
    actual = format_case(
        pd.Series([value]),
        case=case,
    )

    assert actual is None