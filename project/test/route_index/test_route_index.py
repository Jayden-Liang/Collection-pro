from flask import url_for

class TestPage(object):
    def test_home_page(self, client):
        response = client.get(url_for('page.index'))
        assert response.status_code == 200
        assert b'site' in response.get_data()
    def test_info_page(self, client):
        response = client.get(url_for('page.info'))
        assert response.status_code == 200
        assert '<title>' in str(response.get_data())
