extends Node2D
var spawnable = false
var isMouseOver = false
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if spawnable:
		if Input.is_action_just_pressed("click"):
			Global.is_dragging = true
			$IceCube.visible = true
		if Input.is_action_pressed("click"):
			$IceCube.global_position = get_global_mouse_position()
			
			
		elif Input.is_action_just_released("click"):
			Global.is_dragging = false
			$IceCube.visible = false
			#if $MintBunch.onCounter:
				#$MintBunch.prevLocation = $MintBunch.global_position
			if not isMouseOver:
				spawnable = false



func _on_area_2d_mouse_entered() -> void:
	isMouseOver = true
	if not Global.is_dragging:
		spawnable = true
		$IceMachineSprite.scale = Vector2(0.65, 0.65)


func _on_area_2d_mouse_exited() -> void:
	isMouseOver = false
	if not Global.is_dragging:
		spawnable = false
	$IceMachineSprite.scale = Vector2(0.626, 0.626)
