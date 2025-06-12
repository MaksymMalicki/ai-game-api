extends Node2D
var spawnable = false
var isMouseOver = false
@export var isGlassOut = false
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if spawnable:
		if Input.is_action_just_pressed("click"):
			Global.is_dragging = true
			$SingleGlass.visible = true
			$SingleGlass.dragable = true
			isGlassOut = true
		if Input.is_action_pressed("click") and $SingleGlass.dragable:
			$SingleGlass.global_position = get_global_mouse_position()
			
			
		elif Input.is_action_just_released("click"):
			Global.is_dragging = false
			if $SingleGlass.onCounter:
				$SingleGlass.prevLocation = $SingleGlass.global_position
			else:
				$SingleGlass.visible = false
				isGlassOut = false
			if not isMouseOver:
				spawnable = false


func _on_area_2d_mouse_entered() -> void:
	isMouseOver = true
	if not Global.is_dragging and not isGlassOut:
		spawnable = true
		$CanvasGroup.scale = Vector2(0.14, 0.14)



func _on_area_2d_mouse_exited() -> void:
	isMouseOver = false
	if not Global.is_dragging and not isGlassOut:
		spawnable = false
	$CanvasGroup.scale = Vector2(0.131, 0.131)
