"""Test siteinfofetcher"""
import pytest

from siteinfofetcher import SiteFetcher

def get_dummy_site():
    return {"url":"Dummy",
            "interval":30,
            "regex":"Test.*g"}

@pytest.fixture()
def sitefetcher(httpserver):
    site = get_dummy_site()
    site['url'] = httpserver.url_for("/")
    return SiteFetcher(site)

def test_init(httpserver):
    site = get_dummy_site()
    s = SiteFetcher(site)
    assert s.regex_found == None
    assert s.latency == None
    assert s.site == site
    assert s.status_code == None

def test_site_str(sitefetcher):
    assert sitefetcher.site.get('url') in str(sitefetcher)

def test_site_dict(sitefetcher):
    d = sitefetcher.to_dict()
    assert isinstance(d, dict)
    assert {'site', 'status', 'latency', 'regex_found'} == set(d.keys())

def test_request(sitefetcher, httpserver):
    httpserver.expect_request("/").respond_with_data("Testing", content_type="text/plain")
    assert sitefetcher.get_site() == 200
    assert sitefetcher.latency != None
    assert sitefetcher.regex_found == True
