## 💾 HTTP File Storage (aiohttp) 🐍 


## Deploy
```console
docker-compose up
```

## Use it
1. Upload:
```console
curl --location --request POST 'http://127.0.0.1:8080' \
--form 'file=@"path/to/your/file"'
```

2. Download:
```console
curl --location --request GET 'http://127.0.0.1:8080/{id}'
```

3. Delete:
```console
curl --location --request DELETE 'http://127.0.0.1:8080/{id}'
```
