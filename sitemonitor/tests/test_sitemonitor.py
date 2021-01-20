import datetime

import pytest

from main import SiteMonitor
from options import root_path

@pytest.fixture(scope="module")
def sm():
    return SiteMonitor(config=root_path / "tests/sites.yml")

def test_main_init():
    with pytest.raises(TypeError):
        SiteMonitor()

    sm = SiteMonitor(config=root_path / "tests/sites.yml")
    assert isinstance(sm, SiteMonitor) 

def test_sm(sm):
    assert all(['last_check' in x.keys() for x in sm.sites]), "Last check should be initialized"

def test_sm_needs_checking(sm):
    site = {"last_check":datetime.datetime(1970,1,1),
            "interval": 1}
    assert sm._site_needs_checking(site)
