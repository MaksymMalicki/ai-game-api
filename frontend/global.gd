extends Node2D

@export var is_dragging = false
@export var activeScientist = null
@export var baseUrl = "http://127.0.0.1:8000"

# Maximum values for drink parameters
const MAX_VALUES = {
	"vol": 100,
	"sweetness": 5,
	"sourness": 5,
	"fruitness": 5,
	"herbalness": 5,
	"sparkling": 1,
	"ice": 1,
	"shaken": 1
}

# Current drink values
var current_drink = {
	"vol": 0,
	"sweetness": 0,
	"sourness": 0,
	"fruitness": 0,
	"herbalness": 0,
	"sparkling": 0,
	"ice": 0,
	"shaken": 0
}

# Function to increment a drink parameter by 20% of its maximum value
func increment_drink_value(param: String) -> void:
	var max_value = MAX_VALUES[param]
	var increment = max_value * 0.2
	current_drink[param] = min(current_drink[param] + increment, max_value)

# Function to reset drink values
func reset_drink_values() -> void:
	for param in current_drink:
		current_drink[param] = 0

func serveDrink(taste: Dictionary) -> Array:
	var dymek := get_tree().current_scene.get_node_or_null("Dymek")
	if not dymek:
		push_error("Nie znaleziono węzła Dymek!")
	dymek.setText("")
	var http := HTTPRequest.new()
	add_child(http)

	var headers := ["Content-Type: application/json"]
	var body := JSON.stringify(taste)
	var error := http.request(baseUrl + "/scientist/"+str(activeScientist)+"/serve-drink", headers, HTTPClient.METHOD_POST, body)

	if error != OK:
		push_error("Błąd zapytania: %s" % error)
		http.queue_free()
		return []

	var result = await http.request_completed
	var response_code = result[1]
	var response_body: PackedByteArray = result[3]

	if response_code == 200:
		var response = JSON.parse_string(response_body.get_string_from_utf8())
		if response and response.has("message") and response.has("attempts_granted"):
			var message = response["message"]
			var attempts_granted = response["attempts_granted"]
			http.queue_free()
			dymek.setText(message)
			get_tree().current_scene.start_conversation(attempts_granted)
			reset_drink_values()  # Reset drink values after serving
			return [message, attempts_granted]
		else:
			push_error("Niepoprawna odpowiedź serwera: %s" % response)
	else:
		push_error("Błąd odpowiedzi HTTP: %s" % response_code)
	http.queue_free()
	return []


func reply(conversation: String) -> bool:
	print(conversation)
	var dymek := get_tree().current_scene.get_node_or_null("Dymek")
	if not dymek:
		push_error("Nie znaleziono węzła Dymek!")
	dymek.setText("")
	var http := HTTPRequest.new()
	add_child(http)

	var headers := ["Content-Type: application/json"]
	# Create a dictionary and convert it to JSON string
	var body_dict := {
		"message": conversation
	}
	var body := JSON.stringify(body_dict)
	
	var error := http.request(baseUrl + "/scientist/"+str(activeScientist)+"/conversation", headers, HTTPClient.METHOD_POST, body)
	if error != OK:
		push_error("Błąd zapytania: %s" % error)
		http.queue_free()
		return true

	var result = await http.request_completed
	var response_code = result[1]
	var response_body: PackedByteArray = result[3]

	if response_code == 200:
		var response = JSON.parse_string(response_body.get_string_from_utf8())
		if response and response.has("response") and response.has("isOver"):
			var clientResponse = response["response"]
			var isOver = response["isOver"]
			http.queue_free()
			dymek.setText(clientResponse)
			return isOver
		else:
			push_error("Niepoprawna odpowiedź serwera: %s" % response)
	else:
		push_error("Błąd odpowiedzi HTTP: %s" % response_code)
	http.queue_free()
	return true

func newClient() -> void:
	get_tree().current_scene.new_client()
