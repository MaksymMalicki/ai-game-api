extends Node2D
var isFocused
@export var attempts = 0

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if isFocused and $TextEdit.text != "":
		if Input.is_action_just_pressed("enter"):
			var toBeSend = $TextEdit.text
			$TextEdit.text = ""
			var response = await Global.reply(toBeSend)
			attempts -= 1
			if attempts == 0 or response:
				visible = false
				await get_tree().create_timer(5.0).timeout
				Global.newClient()


func _on_text_edit_focus_entered() -> void:
	isFocused = true


func _on_text_edit_focus_exited() -> void:
	isFocused = false
