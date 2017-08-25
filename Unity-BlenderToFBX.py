import bpy
import io_scene_fbx.export_fbx_bin

# Find the Blender output file
import os
outfile = os.getenv("UNITY_BLENDER_EXPORTER_OUTPUT_FILE")

# Do the conversion
print("Starting blender to FBX conversion " + outfile)

import math
from mathutils import Matrix
# -90 degrees
mtx4_x90n = Matrix.Rotation(-math.pi / 2.0, 4, 'X')

#rename bones
dot = "."
dash = "_"

try:
    bpy.context.object.pose.bones
except Exception:
    print ("no pose bones found")
else:
    for bone in bpy.context.object.pose.bones: #may need to make this a list first
        if dot in bone.name:
            bone.name = bone.name.replace(dot, dash)

try:
    bpy.context.scene.objects
except Exception:
    print ("no objects found")
else:
    for object in bpy.context.scene.objects:
        if dot in object.name:
            object.name = object.name.replace(dot, dash)
        for m in object.modifiers:
            m.show_render = m.show_viewport
            if m.type == 'SUBSURF':
                m.levels = m.render_levels

#add actions to nla editor to export without rig name prefix
try:
    bpy.context.object.animation_data.nla_tracks
except Exception:
    print ("no actions found")
else:
    for nlatrack in bpy.context.object.animation_data.nla_tracks:
        bpy.context.object.animation_data.nla_tracks.remove(nlatrack)

try:
    bpy.data.actions
except Exception:
    print ("no actions found")
else:
    for a in bpy.data.actions:
        bpy.context.object.animation_data.nla_tracks.new()
        bpy.context.object.animation_data.nla_tracks[(len(bpy.context.object.animation_data.nla_tracks)-1)].name = action.name
        bpy.context.object.animation_data.nla_tracks[(len(bpy.context.object.animation_data.nla_tracks)-1)].strips.new(action.name,0,action)
        for fcurve in bpy.data.actions[a.name].fcurves:
            b = (str(fcurve.data_path))
            splitName = b.split("\"")
            try:
                splitName[1]
            except Exception:
                print ("splitName[1] not found, no problem tho")
            else:
                if dot in splitName[1]:
                    rename = (splitName[1].replace(dot, dash))
                    name = splitName[0] + "\"" + rename + "\"" + splitName[2]
                    print (name)
                    fcurve.data_path=name #rename

print("moo")

class FakeOp:
    def report(self, tp, msg):
        print("%s: %s" % (tp, msg))

exportObjects = ['ARMATURE', 'EMPTY', 'MESH']

def defaults_unity3d():
    return {
        # These options seem to produce the same result as the old Ascii exporter in Unity3D:
        "version": 'BIN7400',
        "axis_up": 'Y',
        "axis_forward": '-Z',
        "global_matrix": Matrix.Rotation(-math.pi / 2.0, 4, 'X'),
        # Should really be True, but it can cause problems if a model is already in a scene or prefab
        # with the old transforms.
        "bake_space_transform": False,

        "use_selection": False,

        "object_types": {'ARMATURE', 'EMPTY', 'MESH', 'OTHER'},
        "use_mesh_modifiers": True,
        "use_mesh_edges": False,
        "mesh_smooth_type": 'FACE',
        "use_tspace": False,  # XXX Why? Unity is expected to support tspace import...

        "use_armature_deform_only": True,

        "use_custom_props": True,

        "bake_anim": True,
        "bake_anim_simplify_factor": 1.0,
        "bake_anim_step": 1.0,
        "bake_anim_use_nla_strips": True,
        "bake_anim_use_all_actions": False,
        "add_leaf_bones": False,  # Avoid memory/performance cost for something only useful for modelling
        "primary_bone_axis": 'Y',  # Doesn't really matter for Unity, so leave unchanged
        "secondary_bone_axis": 'X',

        "path_mode": 'AUTO',
        "embed_textures": False,
        "batch_mode": 'OFF',
    }

kwargs = defaults_unity3d()
io_scene_fbx.export_fbx_bin.save(FakeOp(), bpy.context, filepath=outfile, **kwargs)
# HQ normals are not supported in the current exporter

print("Finished blender to FBX conversion " + outfile)
