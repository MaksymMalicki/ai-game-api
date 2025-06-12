extends Node2D
var dragable = false
var toBeDiscarded = false
var onCounter = false
var prevLocation = Vector2(0,0)

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if dragable:
		if Input.is_action_just_pressed("click"):
			Global.is_dragging = true
		if Input.is_action_pressed("click") and Global.is_dragging:
			global_position = get_global_mouse_position()
			
			
		elif Input.is_action_just_released("click"):
			Global.is_dragging = false
			if not onCounter:
				global_position = prevLocation
			else:
				prevLocation = global_position
				
			if toBeDiscarded:
				visible = false
				prevLocation = Vector2(0,0)
				$"..".isGlassOut = false


func _on_area_2d_mouse_entered() -> void:
	if not Global.is_dragging:
		dragable = true
		scale = Vector2(1.05, 1.05)


func _on_area_2d_mouse_exited() -> void:
	if not Global.is_dragging:
		dragable = false
	scale = Vector2(1.0, 1.0)


func _on_area_2d_body_entered(body: Node2D) -> void:
	if body.is_in_group("shakerPipe"):
		toBeDiscarded = true
	if body.is_in_group("counter"):
		onCounter = true



func _on_area_2d_body_exited(body: Node2D) -> void:
		if body.is_in_group("shakerPipe"):
			toBeDiscarded = false
		if body.is_in_group("counter"):
			onCounter = false
