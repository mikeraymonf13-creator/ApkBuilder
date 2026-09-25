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

    # Test tonconnect-manifest.json route
    res_tc_manifest = client.get('/tonconnect-manifest.json')
    assert res_tc_manifest.status_code == 200
    assert 'json' in res_tc_manifest.content_type
    tc_data = json.loads(res_tc_manifest.data)
    assert tc_data['name'] == 'BorderP45 TON Wallet'

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
