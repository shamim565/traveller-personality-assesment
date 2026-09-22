import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def kiosk_page(live_server, page):
    page.goto(live_server.url)
    return page
