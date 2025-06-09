# 1. Start a new game
curl -X POST http://localhost:8000/game/start

echo "Getting details of first scientist (ID: 0)..."
curl http://localhost:8000/scientist/0

echo -e "\nGetting details of second scientist (ID: 1)..."
curl http://localhost:8000/scientist/1

echo -e "\nGetting details of third scientist (ID: 2)..."
curl http://localhost:8000/scientist/2

echo -e "\nServing drink to first scientist..."
curl -X POST "http://localhost:8000/scientist/0/serve-drink/%7B%22vol%22%3A80%2C%22sweetness%22%3A3%2C%22sourness%22%3A2%2C%22fruitness%22%3A1%2C%22herbalness%22%3A4%2C%22sparkling%22%3A1%2C%22ice%22%3A1%2C%22shaken%22%3A0%7D"

echo -e "\nServing drink to second scientist..."
curl -X POST "http://localhost:8000/scientist/1/serve-drink/%7B%22vol%22%3A60%2C%22sweetness%22%3A4%2C%22sourness%22%3A1%2C%22fruitness%22%3A3%2C%22herbalness%22%3A2%2C%22sparkling%22%3A1%2C%22ice%22%3A1%2C%22shaken%22%3A1%7D"

echo -e "\nServing drink to third scientist..."
curl -X POST "http://localhost:8000/scientist/2/serve-drink/%7B%22vol%22%3A100%2C%22sweetness%22%3A2%2C%22sourness%22%3A4%2C%22fruitness%22%3A2%2C%22herbalness%22%3A3%2C%22sparkling%22%3A0%2C%22ice%22%3A1%2C%22shaken%22%3A1%7D"

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

echo -e "\nTrying to start a new game (should fail)..."
curl -X POST http://localhost:8000/game/start

echo -e "\nTrying to get a non-existent scientist (should fail)..."
curl http://localhost:8000/scientist/999