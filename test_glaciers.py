import pytest
from pytest import raises
import glaciers
import pathlib
from pathlib import Path
from glaciers import Glacier, GlacierCollection

location = ''
filepath1 = Path(location + 'sheet-A.csv')
filepath2 = Path(location + 'sheet-EE.csv')

def test_variables():
    #define variables
    glacier_id = '17363'
    name = 'Any name'
    unit = 'FG'
    lat = 30
    lon = 39.87
    code = 638

    #create a glacier object with the variables
    example = Glacier(glacier_id, name, unit, lat, lon, code)

    #assert that it outputs the correct data
    assert example.glacier_id == glacier_id
    assert example.name == name
    assert example.unit == unit
    assert example.lat == lat
    assert example.lon == lon
    assert example.code == code

def test_add_mass_balance():
    #create a collection
    collection = GlacierCollection(filepath1)
    collection.read_mass_balance_data(filepath2)

    #check for the glacier Agua Negra which has partial and total measurements for 2018 and 2019
    assert collection.glacier_classes[0].mass_balance == [-793.0, -418.0, 332.0, -7886.0, -2397.0, -13331.0]

def test_filter_code():
    #create a collection
    collection = GlacierCollection(filepath1)
    collection.read_mass_balance_data(filepath2)

    #check when code is an integer
    assert collection.filter_by_code(638) == ['AGUA NEGRA', 'BROWN SUPERIOR', 'CONCONTA NORTE', 'LAGO DEL DESIERTO I', 'LAGO DEL DESIERTO II', 'LAGO DEL DESIERTO III', 'LOS AMARILLOS', 'POTRERILLOS', 'TORTOLAS', 'AMARILLO', 'NINGCHAN GLACIER NO.1', 'VESTRE MEMURUBREEN']

    #check when code is an string with no ?
    assert collection.filter_by_code('638') == ['AGUA NEGRA', 'BROWN SUPERIOR', 'CONCONTA NORTE', 'LAGO DEL DESIERTO I', 'LAGO DEL DESIERTO II', 'LAGO DEL DESIERTO III', 'LOS AMARILLOS', 'POTRERILLOS', 'TORTOLAS', 'AMARILLO', 'NINGCHAN GLACIER NO.1', 'VESTRE MEMURUBREEN']

    #check when code is an string with one ?
    assert collection.filter_by_code('6?8') == ['AGUA NEGRA', 'BROWN SUPERIOR', 'CANITO', 'CONCONTA NORTE', 'LAGO DEL DESIERTO I', 'LAGO DEL DESIERTO II', 'LAGO DEL DESIERTO III', 'LOS AMARILLOS', 'POTRERILLOS', 'TORTOLAS', 'ADLER', 'PERS, VADRET', 'AMARILLO', 'TRONQUITOS', 'NINGCHAN GLACIER NO.1', 'RULUNG', 'HALSJOKULL', 'BLAAISEN', 'VESTRE MEMURUBREEN']

    #check when code is an string with two ?
    assert collection.filter_by_code('3??') == ['GRAN CAMPO NEVADO (GCN)', 'DRANGAJOKULL ICE CAP', 'EIRIKSJOKULL', 'EYJAFJALLAJOKULL', 'HOFSJOKUL_EYSTRI', 'HOFSJOKULL ICE CAP', 'HRUTFELL', 'LANGJOKULL ICE CAP', 'MYRDALSJOKULL ICE CAP', 'ORAEFAJOKULL', 'SNAEFELLSJOKULL', 'THRANDARJOKULL', 'TINDFJALLAJOKULL', 'TORFAJOKULL', 'TUNGNAFELLSJOKULL', 'VATNAJOKULL', 'WESTERN VATNAJOKULL ICE CAP', 'MIDTRE FOLGEFONNA', 'NORDRE FOLGEFON', 'COROPUNA']
                                            
    #check when code is an string with three ?
    assert collection.filter_by_code('???') == collection.name

def test_sort_latest():
    #create a collection
    collection = GlacierCollection(filepath1)
    collection.read_mass_balance_data(filepath2)

    #check when reverse is true
    x = collection.sort_by_latest_mass_balance(1, reverse = True)
    assert x[0].name == 'ARTESONRAJU'

    #check when reverse is false
    y = collection.sort_by_latest_mass_balance(1, reverse = False)
    assert y[0].name == 'STORSTEINSFJELLBREEN'
    
#define negative tests
def test_wrong_glacier_id_length():
    #define variables
    glacier_id = '0432'
    name = 'AGUA NEGRA'
    unit = 'AR'
    lat = 30
    lon = -69.80940
    code = 638

    #create a glacier object with the variables
    with raises(ValueError, match =("The Glacier ID should be a five digit string")):
        Glacier(glacier_id, name, unit, lat, lon, code)

def test_wrong_lat_value():
    #define variables
    glacier_id = '04392'
    name = 'AGUA NEGRA'
    unit = 'AR'
    lat = 300
    lon = -69.80940
    code = 638

    #create a glacier object with the variables
    with raises(ValueError, match =('The latitude is not within the accepted range')):
        Glacier(glacier_id, name, unit, lat, lon, code)

def test_wrong_lon_value():
    #define variables
    glacier_id = '04392'
    name = 'AGUA NEGRA'
    unit = 'AR'
    lat = 30
    lon = -639.80940
    code = 638

    #create a glacier object with the variables
    with raises(ValueError, match =('The longitude is not within the accepted range')):
        Glacier(glacier_id, name, unit, lat, lon, code)

def test_wrong_unit_length():
    #define variables
    glacier_id = '04392'
    name = 'AGUA NEGRA'
    unit = 'ARE'
    lat = 30
    lon = -63
    code = 638

    #create a glacier object with the variables
    with raises(ValueError, match =("The unit should be a two charachter string")):
        Glacier(glacier_id, name, unit, lat, lon, code)

def test_unit_format():
    #define variables
    glacier_id = '04392'
    name = 'AGUA NEGRA'
    unit = 'ar'
    lat = 30
    lon = -63
    code = 638

    #create a glacier object with the variables
    with raises(ValueError, match =("The unit should be in capital letters")):
        Glacier(glacier_id, name, unit, lat, lon, code)

def test_unit_type():
    #define variables
    glacier_id = '04392'
    name = 'AGUA NEGRA'
    unit = 18
    lat = 30
    lon = -63
    code = 638

    #create a glacier object with the variables
    with raises(TypeError, match = ("unit should be a string")):
        Glacier(glacier_id, name, unit, lat, lon, code)

def test_id_type():
    #define variables
    glacier_id = 54392
    name = 'AGUA NEGRA'
    unit = 18
    lat = 30
    lon = -63
    code = 638

    #create a glacier object with the variables
    with raises(TypeError, match = ("glacier id should be a string")):
        Glacier(glacier_id, name, unit, lat, lon, code)