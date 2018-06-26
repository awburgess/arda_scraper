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
        m.get('http://www.test.com', json=load_esri_geojson())
        esri_geojson = AD.acquire_esri_geojson('http://www.test.com')
    assert 'features' in esri_geojson.keys()
    assert 'type' not in esri_geojson.keys()