# order-process-api

## Project Layout Template
```
├── app/
│ ├── app.py
│ └── requirements.txt
├── tests/
│ └── test_app.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Getting Started

**Clone the repository**
```bash
git clone https://github.com/onlywe0620/order-process-api.git
cd order-process-api
```

**Build and run the application**

```bash
docker-compose up --build
```
- only run service

```bash
docker-compose up app
```
- only run test
```bash
docker-compose up test
```

## Test API with curl

### Test valid order (TWD)

```bash
curl -X POST http://localhost:8080/api/orders -H "Content-Type: application/json" -d '{
"id": "A0000001",
"name": "Melody Holiday Inn", 
"address": {
    "city": "taipei-city",
    "district": "da-an-district", 
    "street": "fuxing-south-road"
},
"price": "1000", 
"currency": "TWD"
}'
```
**return:**
```json
{
  "data": {
    "address": {
      "city": "taipei-city",
      "district": "da-an-district",
      "street": "fuxing-south-road"
    },
    "currency": "TWD",
    "id": "A0000001",
    "name": "Melody Holiday Inn",
    "price": "1000"
  },
  "message": "Valid order",
  "status_code": 200
}
```

### Test valid order (USD)

```bash
curl -X POST http://localhost:8080/api/orders -H "Content-Type: application/json" -d '{
"id": "A0000001",
"name": "Melody Holiday Inn", 
"address": {
    "city": "taipei-city",
    "district": "da-an-district", 
    "street": "fuxing-south-road"
},
"price": "20", 
"currency": "USD"
}'
```

**return:**

```json
{
  "data": {
    "address": {
      "city": "taipei-city",
      "district": "da-an-district",
      "street": "fuxing-south-road"
    },
    "currency": "TWD",
    "id": "A0000001",
    "name": "Melody Holiday Inn",
    "price": "620"
  },
  "message": "Valid order",
  "status_code": 200
}
```

### Test invalid order (json_format)

```bash
curl -X POST http://localhost:8080/api/orders -H "Content-Type: application/json" -d '{
"id": "A0000001",
"name": "Melody Holiday Inn",
"price": "1000",
"currency": "TWD"
}'
```

**return:**

```json
{
  "data": {
    "currency": "TWD",
    "id": "A0000001",
    "name": "Melody Holiday Inn",
    "price": "1000"
  },
  "message": "JSON format is incorrect",
  "status_code": 400
}
```

### Test invalid order (name)

```bash
curl -X POST http://localhost:8080/api/orders -H "Content-Type: application/json" -d '{
"id": "A0000001",
"name": "Melo2222dy Holiday Inn", 
"address": {
    "city": "taipei-city",
    "district": "da-an-district", 
    "street": "fuxing-south-road"
},
"price": "20", 
"currency": "USD"
}'
```

**return:**

```json
{
  "data": {
    "address": {
      "city": "taipei-city",
      "district": "da-an-district",
      "street": "fuxing-south-road"
    },
    "currency": "USD",
    "id": "A0000001",
    "name": "Melo2222dy Holiday Inn",
    "price": "20"
  },
  "message": "Name contains non-English characters",
  "status_code": 400
}
```

### Test invalid order (name)

```bash
curl -X POST http://localhost:8080/api/orders -H "Content-Type: application/json" -d '{
"id": "A0000001",
"name": "Melody holiday Inn", 
"address": {
    "city": "taipei-city",
    "district": "da-an-district", 
    "street": "fuxing-south-road"
},
"price": "20", 
"currency": "USD"
}'
```

**return:**

```json
{
  "data": {
    "address": {
      "city": "taipei-city",
      "district": "da-an-district",
      "street": "fuxing-south-road"
    },
    "currency": "USD",
    "id": "A0000001",
    "name": "Melody holiday Inn",
    "price": "20"
  },
  "message": "Name is not capitalized",
  "status_code": 400
}
```

### Test invalid order (curreny)

```bash
curl -X POST http://localhost:8080/api/orders -H "Content-Type: application/json" -d '{
"id": "A0000001",
"name": "Melody Holiday Inn", 
"address": {
    "city": "taipei-city",
    "district": "da-an-district", 
    "street": "fuxing-south-road"
},
"price": "20", 
"currency": "EUR"
}'
```

**return:**

```json
{
  "data": {
    "address": {
      "city": "taipei-city",
      "district": "da-an-district",
      "street": "fuxing-south-road"
    },
    "currency": "EUR",
    "id": "A0000001",
    "name": "Melody Holiday Inn",
    "price": "20"
  },
  "message": "Currency format is wrong",
  "status_code": 400
}
```

### Test invalid order (price)

```bash
curl -X POST http://localhost:8080/api/orders -H "Content-Type: application/json" -d '{
"id": "A0000001",
"name": "Melody Holiday Inn", 
"address": {
    "city": "taipei-city",
    "district": "da-an-district", 
    "street": "fuxing-south-road"
},
"price": "3000", 
"currency": "TWD"
}'
```

**return:**

```json
{
  "data": {
    "address": {
      "city": "taipei-city",
      "district": "da-an-district",
      "street": "fuxing-south-road"
    },
    "currency": "TWD",
    "id": "A0000001",
    "name": "Melody Holiday Inn",
    "price": "3000"
  },
  "message": "Price is over 2000",
  "status_code": 400
}
```

## 使用的SOLID原則
1. **單一職責原則 (Single Responsibility Principle)**: 每個類別只負責一項具體的功能，如 `FormValidation` 類別負責檢查表單格式，`FormatCheckingAndTransform` 類別負責檢查和轉換訂單格式。
2. **開放/封閉原則 (Open/Closed Principle)**: 類別設計是開放擴展的，例如可以通過繼承 `FormValidation` 或 `FormatCheckingAndTransform` 類別來新增額外的檢查邏輯，但不需要修改原本的類別。

## 使用的設計模式
1. **策略模式 (Strategy Pattern)**: `FormatCheckingAndTransform` 可以作為不同格式檢查策略的基礎，並在 `Service` 類別中進行切換。
2. **工廠模式 (Factory Pattern)**: `Response` 可以被視為一個簡單的工廠，用於創建不同類型的回應。

