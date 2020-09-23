# -*- coding: utf-8 -*-
from collections import namedtuple


def monkey_products_return(monkeypatch):
    return PRODUCTS_JSON_DICT


def monkey_no_result(monkeypatch):
    return {}


class MockResponse:
    def json(self):
        return PRODUCTS_JSON_DICT


class MockResponseError():
    def json(self):
        raise ImportError


class TestCreateAuthorView:
    # name = None
    json_object = JsonBaseImport(URL)

    def test_get_response(self, monkeypatch):
        mock_response = MockResponse()
        monkeypatch.setattr(self.json_object, "response", mock_response)

        json_response = self.json_object.get_response()

        assert isinstance(json_response, dict)
        assert 'Result' in json_response
        assert 'ARTIGOS' in json_response['Result']
        assert 'ARTIGO' in json_response['Result']['ARTIGOS']

        product_designation = json_response['Result']['ARTIGOS']['ARTIGO'][0]['DESIGNACAO']
        assert "P.RECAU. 235/75R17.5 C/CAR. BRIDGESTONE P.FRIO P45" in product_designation

    def test_get_response_with_error(self, monkeypatch, enable_db_access):
        mock_response = MockResponseError()
        monkeypatch.setattr(self.json_object, "response", mock_response)

        json_response = self.json_object.get_response()

        assert json_response is None
