from unittest.mock import MagicMock, patch
import requests

def make_request(url):
    response = requests.get(url)
    return response.text

def test_make_request():
    # Crear un objeto MagicMock para la respuesta HTTP simulada
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = 'Hello, world!'

    # Crear un objeto MagicMock para el método de solicitud HTTP simulado
    mock_get = MagicMock()
    mock_get.return_value = mock_response

    # Aplicar el mock al módulo requests
    with patch('requests.get', mock_get):
        # Llamar a la función que hace una solicitud HTTP
        result = make_request('http://www.example.com')

    # Comprobar que la función devolvió el resultado esperado
    assert result == 'Hello, world!'
