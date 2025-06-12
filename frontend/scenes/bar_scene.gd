extends Node2D

@onready var sprite: Sprite2D = $Sprite2D
var lastClient = null
var textures := [
	preload("res://assets/clients/client1.png"),
	preload("res://assets/clients/client3.png"),
	preload("res://assets/clients/client6.png"),
	preload("res://assets/clients/client5.png"),
	preload("res://assets/clients/client2.png"),
	preload("res://assets/clients/client4.png"),
]
var scientist_ids: Array = []

func _ready():
	$Client.visible = false
	$Client.modulate.a = 0.0
	$Dymek.visible = false
	$Dymek.modulate.a = 0.0
	$Dymek.setText("")
	await start_game_request()
	await get_scientist()

func _process(delta: float) -> void:
	pass


func start_game_request() -> void:
	var http := HTTPRequest.new()
	add_child(http)

	var headers := ["Content-Type: application/json"]
	var body := "{}"
	var error := http.request(Global.baseUrl + "/game/start", headers, HTTPClient.METHOD_POST, body)

	if error != OK:
		push_error("Błąd zapytania: %s" % error)
		http.queue_free()
		return

	var result = await http.request_completed
	var response_code = result[1]
	var response_body: PackedByteArray = result[3]

	if response_code == 200:
		var response = JSON.parse_string(response_body.get_string_from_utf8())
		if response and response.has("scientist_ids"):
			scientist_ids = response["scientist_ids"]
			print("Odebrano scientist_ids:", scientist_ids)
		else:
			push_error("Niepoprawna odpowiedź serwera: %s" % response)
	else:
		push_error("Błąd odpowiedzi HTTP: %s" % response_code)

	http.queue_free()
func get_scientist() -> void:
	var repeat = true
	var chosen = null
	while repeat:
		chosen = randi() % min(scientist_ids.size(), textures.size())
		if chosen != lastClient:
			lastClient = chosen
			Global.activeScientist = chosen
			repeat = false
	
	var http := HTTPRequest.new()
	add_child(http)

	var headers := ["Content-Type: application/json"]
	var error := http.request(Global.baseUrl + "/scientist/"+str(Global.activeScientist), headers, HTTPClient.METHOD_GET)

	if error != OK:
		push_error("Błąd zapytania: %s" % error)
		http.queue_free()
		return

	var result = await http.request_completed
	var response_code = result[1]
	var response_body: PackedByteArray = result[3]

	if response_code == 200:
		var response = JSON.parse_string(response_body.get_string_from_utf8())
		if response and response.has("drink_hint"):
			var drink_hint = response["drink_hint"]
			print("Odebrano drink_hint:", drink_hint)
			show_scientist(drink_hint)
		else:
			push_error("Niepoprawna odpowiedź serwera: %s" % response)
	else:
		push_error("Błąd odpowiedzi HTTP: %s" % response_code)

	http.queue_free()


func show_scientist(drink_hint: String) -> void:
	var random_texture = textures[lastClient]
	$Client/ClientSprite.texture = random_texture
	$Client.visible = true
	$Dymek.setText(drink_hint)
	$Dymek.visible = true
	var fade_time = 0.5  # czas trwania fade-in w sekundach
	var steps = 30
	var wait_time = fade_time / steps

	for i in range(steps + 1):
		var alpha = float(i) / steps
		$Client.modulate.a = alpha
		$Dymek.modulate.a = alpha
		await get_tree().create_timer(wait_time).timeout

func start_conversation(attempts: int) -> void:
	$Answerbox.visible = true
	$Answerbox.attempts = attempts
	$Answerbox/TextEdit.grab_focus()
	print("starting")
	
	
func hide_scientist() -> void:
	var random_texture = textures[lastClient]
	$Client/ClientSprite.texture = random_texture
	$Client.visible = true
	$Dymek.setText("")
	$Dymek.visible = true
	var fade_time = 0.5  # czas trwania fade-in w sekundach
	var steps = 30
	var wait_time = fade_time / steps

	for i in range(steps + 1):
		var alpha = float(30 - i) / steps
		$Client.modulate.a = alpha
		$Dymek.modulate.a = alpha
		await get_tree().create_timer(wait_time).timeout
		
func new_client() -> void:
	await hide_scientist()
	await get_tree().create_timer(3.0).timeout
	await get_scientist()
