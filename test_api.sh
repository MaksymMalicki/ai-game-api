curl -X POST http://localhost:8000/game/start

echo "Getting details of first scientist (ID: 0)..."
curl http://localhost:8000/scientist/0

echo -e "\nGetting details of second scientist (ID: 1)..."
curl http://localhost:8000/scientist/1

echo -e "\nGetting details of third scientist (ID: 2)..."
curl http://localhost:8000/scientist/2

echo -e "\nServing drink to first scientist..."
curl -X POST http://localhost:8000/scientist/0/serve-drink \
  -H "Content-Type: application/json" \
  -d '{
    "vol": 80,
    "sweetness": 3,
    "sourness": 2,
    "fruitness": 1,
    "herbalness": 4,
    "sparkling": 1,
    "ice": 1,
    "shaken": 0
  }'

echo -e "\nServing drink to second scientist..."
curl -X POST http://localhost:8000/scientist/1/serve-drink \
  -H "Content-Type: application/json" \
  -d '{
    "vol": 60,
    "sweetness": 4,
    "sourness": 1,
    "fruitness": 3,
    "herbalness": 2,
    "sparkling": 1,
    "ice": 1,
    "shaken": 1
  }'

echo -e "\nServing drink to third scientist..."
curl -X POST http://localhost:8000/scientist/2/serve-drink \
  -H "Content-Type: application/json" \
  -d '{
    "vol": 100,
    "sweetness": 2,
    "sourness": 4,
    "fruitness": 2,
    "herbalness": 3,
    "sparkling": 0,
    "ice": 1,
    "shaken": 1
  }'

echo -e "\nConversation with first scientist..."
curl -X POST http://localhost:8000/scientist/0/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! How is your research going?"}'

echo -e "\nConversation with second scientist..."
curl -X POST http://localhost:8000/scientist/1/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "What are you working on these days?"}'

echo -e "\nConversation with third scientist..."
curl -X POST http://localhost:8000/scientist/2/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "How long have you been on this ship?"}'