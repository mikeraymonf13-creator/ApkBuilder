import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "BorderP45")))

def test_borderp45_routes():
    from app import app
    client = app.test_client()

    # Test index route
    res = client.get('/')
    assert res.status_code == 200
    assert b'BorderP45 Portal' in res.data
    assert b'TON Transfer' in res.data
    assert b'Jetton Transfer' in res.data

    # Test sw.js route
    res_sw = client.get('/sw.js')
    assert res_sw.status_code == 200
    assert 'javascript' in res_sw.content_type

    # Test manifest.json route
    res_manifest = client.get('/manifest.json')
    assert res_manifest.status_code == 200
    assert 'json' in res_manifest.content_type

    # Test TON transfer API route
    res_ton = client.post('/api/transfer/ton', json={
        'recipient': 'EQD123',
        'amount': '10.5',
        'comment': 'Test TON transfer'
    })
    assert res_ton.status_code == 200
    data_ton = json.loads(res_ton.data)
    assert data_ton['success'] is True
    assert data_ton['recipient'] == 'EQD123'

    # Test Jetton transfer API route
    res_jetton = client.post('/api/transfer/jetton', json={
        'jetton_master': 'EQB456',
        'recipient': 'EQD123',
        'amount': '100',
        'comment': 'Test Jetton transfer'
    })
    assert res_jetton.status_code == 200
    data_jetton = json.loads(res_jetton.data)
    assert data_jetton['success'] is True
    assert data_jetton['jetton_master'] == 'EQB456'

    # Test TON Connect parse route with user endpoint URL
    test_endpoint_url = (
        "https://connect.gramwallet.io/?v=2&id=fd97f7f6ad60461e4885761d2cdc430d130c6c19854af1e8771685d0675e1f11"
        "&trace_id=01a0ca5f-f49a-73b4-b0e9-d5cfeed14928"
        "&r=%7B%22manifestUrl%22%3A%22https%3A%2F%2Ftonviewer.com%2Ftc-manifest.json%22%2C%22items%22%3A%5B%7B%22name%22%3A%22ton_addr%22%7D%2C%7B%22name%22%3A%22ton_proof%22%2C%22payload%22%3A%220d21184fedec258206e26530bd09fc347b1279f83b12e87ccbbeab6ab1286e12%22%7D%5D%7D"
        "&ret=https%3A%2F%2Ftonviewer.com%2Ftransaction%2Ff177ef98dad79d87295f17cd8e7816ab6ef715355a7e22c7477baf701b9017a6"
    )

    res_parse = client.post('/api/tonconnect/parse', json={'url': test_endpoint_url})
    assert res_parse.status_code == 200
    data_parse = json.loads(res_parse.data)
    assert data_parse['success'] is True
    assert data_parse['parsed']['version'] == '2'
    assert data_parse['parsed']['id'] == 'fd97f7f6ad60461e4885761d2cdc430d130c6c19854af1e8771685d0675e1f11'
    assert data_parse['parsed']['trace_id'] == '01a0ca5f-f49a-73b4-b0e9-d5cfeed14928'
    assert data_parse['parsed']['manifest_url'] == 'https://tonviewer.com/tc-manifest.json'
    assert len(data_parse['parsed']['items']) == 2
    assert data_parse['parsed']['items'][0]['name'] == 'ton_addr'
    assert data_parse['parsed']['items'][1]['name'] == 'ton_proof'

    # Test GET method for parse route
    res_parse_get = client.get(f'/api/tonconnect/parse?url={test_endpoint_url}')
    assert res_parse_get.status_code == 200
    data_parse_get = json.loads(res_parse_get.data)
    assert data_parse_get['success'] is True

    # Test TON Connect connect route
    res_connect = client.post('/api/tonconnect/connect', json={
        'id': 'fd97f7f6ad60461e4885761d2cdc430d130c6c19854af1e8771685d0675e1f11',
        'manifest_url': 'https://tonviewer.com/tc-manifest.json'
    })
    assert res_connect.status_code == 200
    data_connect = json.loads(res_connect.data)
    assert data_connect['success'] is True
    assert data_connect['client_id'] == 'fd97f7f6ad60461e4885761d2cdc430d130c6c19854af1e8771685d0675e1f11'
    assert 'session_id' in data_connect
