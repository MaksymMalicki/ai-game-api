extends Node2D
var spawnable = false
var isMouseOver = false

func _ready() -> void:
	pass

func _process(delta: float) -> void:
	if spawnable:
		if Input.is_action_just_pressed("click"):
			Global.is_dragging = true
			$LemonSlice.visible = true
		if Input.is_action_pressed("click"):
			$LemonSlice.global_position = get_global_mouse_position()
			
		elif Input.is_action_just_released("click"):
			Global.is_dragging = false
			$LemonSlice.visible = false
			# Increment drink values when released on counter
			if $LemonSlice/SingleArea2D.get_overlapping_areas().any(func(area): return area.is_in_group("counter")):
				Global.increment_drink_value("sourness")  # Lemon adds sourness
				Global.increment_drink_value("fruitness")  # Lemon adds fruitiness
			if not isMouseOver:
				spawnable = false

func _on_area_2d_mouse_entered() -> void:
	isMouseOver = true
	if not Global.is_dragging:
		spawnable = true
		$LemonsBowlSprite.scale = Vector2(0.65, 0.65)

func _on_area_2d_mouse_exited() -> void:
	isMouseOver = false
	if not Global.is_dragging:
		spawnable = false
	$LemonsBowlSprite.scale = Vector2(0.626, 0.626)
