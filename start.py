import bpy

bpy.context.scene.render.engine = 'BLENDER_GAME'
bpy.ops.wm.blenderplayer_start()