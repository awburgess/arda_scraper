"""
Unit tests for arda_scraper
"""

import pytest
import requests_mock

import arda_scraper as AD


@pytest.fixture
def load_esri_geojson() -> dict:
    """
    Load ESRI GeoJSON sample data from resources directory

    Returns:
        ESRI GeoJSON as dict
    """
    geojson = AD.Path(__file__).parent / 'resources/esri_geojson.geojson'
    with geojson.open() as infile:
        esri_geojson = AD.json.load(infile)
    return esri_geojson


def test_acquire_esri_geojson(load_esri_geojson):
    """
    Test that function handles json response

    Args:
        load_esri_geojson: Fixture for mocking ESRI Endpoint response

    """
    with requests_mock.Mocker() as m:
        m.get('http://www.test.com', json=load_esri_geojson)
        esri_geojson = AD.acquire_esri_geojson('http://www.test.com')
    assert 'features' in esri_geojson.keys()
    assert 'type' not in esri_geojson.keys()


def test_convert_esri_to_geojson_features(load_esri_geojson):
    """
    Test that the ESRI GeoJSON is appropriately converted to standard GeoJSON features

    Args:
        load_esri_geojson: Fixture for mocking ESRI GeoJSON response

    """
    standard_geojson = AD.convert_esri_to_geojson_features(load_esri_geojson)
    random_feature = standard_geojson[AD.randint(0, len(standard_geojson))]
    for key in ['geometry', 'type', 'properties']:
        assert key in random_feature.keys()


def test_get_county_bounding_boxes():
    """
    Test that county bounding boxes GeoDataFrame is created

    """
    county_gdf = AD.get_county_bounding_boxes('18')
    assert [-86.328121, 39.632177, -85.93737899999999, 39.927392] in county_gdf.values.tolist()


def test_get_state_fips():
    """
    Assert that crosswalk works as expected

    """
    in_result = AD.get_state_fips('IN')
    assert in_result == '18'
    with pytest.raises(Exception):
        AD.get_state_fips('AA')


def test_create_feature_collection(load_esri_geojson):
    """
    Assert that orchestration of collect and create feature collection works

    Args:
        load_esri_geojson: PyTest Fixture for ESRI GeoJSON

    """
    with requests_mock.Mocker() as m:
        m.get('http://www.esri.com', json=load_esri_geojson)
        geojson_feature_collection = AD.create_feature_collection(['http://www.esri.com'], 'IN')
    assert geojson_feature_collection['type'] == 'FeatureCollection'
    assert geojson_feature_collection['features'][0]['properties']['STATE'] == 'IN'

