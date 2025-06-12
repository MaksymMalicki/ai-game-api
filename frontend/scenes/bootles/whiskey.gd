extends Node2D
var movable = false
var isMouseOver = false
var isMoving = false
const startPosition = Vector2(47.0, 698.0)

func _ready() -> void:
	pass 

func _process(delta: float) -> void:
	if Input.is_action_just_pressed("click"):
		if movable:
			Global.is_dragging = true
			isMoving = true
	if Input.is_action_pressed("click") and Global.is_dragging:
		if isMoving:
			global_position = get_global_mouse_position()
		
		
	elif Input.is_action_just_released("click"):
		isMoving = false
		Global.is_dragging = false
		# Increment drink values when released on counter
		if $Area2D.get_overlapping_areas().any(func(area): return area.is_in_group("counter")):
			Global.increment_drink_value("vol")  # Whiskey increases volume
			Global.increment_drink_value("sweetness")  # Whiskey adds some sweetness
			Global.increment_drink_value("herbalness")  # Whiskey has herbal notes
		global_position = startPosition

func _on_area_2d_mouse_entered() -> void:
	isMouseOver = true
	if not Global.is_dragging:
		movable = true
		scale = Vector2(1.05, 1.05)

func _on_area_2d_mouse_exited() -> void:
	isMouseOver = false
	if not Global.is_dragging:
		movable = false
	scale = Vector2(1, 1)
