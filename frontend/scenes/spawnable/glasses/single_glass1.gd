extends Node2D
var dragable = false
var toBeDiscarded = false
var toBeServed = false
var onCounter = false
var prevLocation = Vector2(0,0)
var containing = 0
const initTaste = {
	"vol": 0,
	"sweetness": 0,
	"sourness": 0,
	"fruitness": 0,
	"herbalness": 0,
	"ice": 0,
	"shaken": 0,
}

var taste = initTaste



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
				
			if toBeServed:
				taste = {
					"vol": randi() % 40,
					"sweetness": randi() % 5,
					"sourness": randi() % 5,
					"fruitness": randi() % 5,
					"herbalness": randi() % 5,
					"ice": randi() % 1,
					"shaken": randi() % 1,
				}
				Global.serveDrink(taste)
				
			if toBeDiscarded or toBeServed:
				visible = false
				prevLocation = Vector2(0,0)
				$"..".isGlassOut = false

func _on_single_area_2d_mouse_entered() -> void:
	if not Global.is_dragging:
		dragable = true
		scale = Vector2(1.5, 1.5)


func _on_single_area_2d_mouse_exited() -> void:
	if not Global.is_dragging:
		dragable = false
	scale = Vector2(1.44, 1.44)


func _on_single_area_2d_body_entered(body: Node2D) -> void:
	if body.is_in_group("glassDiscard"):
		toBeDiscarded = true
	if body.is_in_group("counter"):
		onCounter = true
	if body.is_in_group("client"):
		toBeServed = true


func _on_single_area_2d_body_exited(body: Node2D) -> void:
		if body.is_in_group("glassDiscard"):
			toBeDiscarded = false
		if body.is_in_group("counter"):
			onCounter = false
		if body.is_in_group("client"):
			toBeServed = false
