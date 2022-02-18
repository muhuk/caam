# <pep8-80 compliant>

# caam is a Blender addon that provides a copy_and_apply_mirror Operator.
# Copyright (C) 2022  Atamert Ölçgen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bpy


bl_info = {
    "name": "caam",
    "description": "Copy and Apply Mirror operator.",
    "author": "Atamert Ölçgen",
    "version": (0, 1),
    "blender": (3, 0, 1),
    "location": "Object menu",
    "tracker_url": "https://github.com/muhuk/caam",
    "support": "COMMUNITY",
    "category": "Object"
}


def main(obj):
    modifier_name = None
    for m in obj.modifiers:
        if m.type == 'MIRROR':
            modifier_name = m.name
            print('Found mirror modifier:', modifier_name)
            bpy.ops.object.modifier_copy(modifier=modifier_name)
            bpy.ops.object.modifier_move_down(modifier=modifier_name)
            break
    if modifier_name is not None:
        for m in obj.modifiers:
            if m.type == 'MIRROR':
                bpy.ops.object.modifier_apply(modifier=m.name)
                break


class CopyAndApplyMirrorOperator(bpy.types.Operator):
    """Find the first mirror modifier, apply a copy of it and keep
       the original."""
    bl_idname = "object.copy_and_apply_mirror_operator"
    bl_label = "Copy and Apply Mirror Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context.active_object)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        CopyAndApplyMirrorOperator.bl_idname,
        text=CopyAndApplyMirrorOperator.bl_label
    )


# Register and add to the "object" menu (required to also use
# F3 search "Apply and Copy Mirror Operator" for quick access)
def register():
    bpy.utils.register_class(CopyAndApplyMirrorOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(CopyAndApplyMirrorOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
