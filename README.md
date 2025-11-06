## Task 1
### Backend Proxy

```python
python start_backend.py --server-ip 192.168.x.x --server-port 9000
python start_proxy.py --server-ip 192.168.x.x --server-port 8080
POST http://192.168.x.x:8080
```

### Cookie
```python
python start_sampleapp.py --server-ip 192.168.122.1 --server-port 9000 
```