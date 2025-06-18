# SPDX-License-Identifier: AGPL-3.0-or-later
# © 2025 Pushakar Gaikwad
#
# This file is part of VSE Extras.
#
# VSE Extras is free/libre software: you can redistribute it and/or modify
# it under the terms of the GNU **Affero** General Public License
# as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# VSE Extras is distributed in the hope that it will be useful,
# but **WITHOUT ANY WARRANTY**; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

bl_info = {
    "name":        "VSE Extras",
    "author":      "Pushakar Gaikwad",
    "version":     (1, 0, 2),
    "blender":     (4, 4, 0),
    "description": "Extra features and tools for the VSE",
    "category": "Sequencer",
}

import bpy




class VSE_EXTRAS_OT_SplitStrip(bpy.types.Operator):
    bl_idname = "vseextras.split_operator"
    bl_label  = "Split Strip"
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, ctx):
        remember_frame = bpy.context.scene.frame_current
        bpy.context.scene.frame_current = ctx.active_strip.frame_final_start
        bpy.ops.sequencer.delete()
        bpy.ops.sequencer.gap_remove()
        bpy.context.scene.frame_current = remember_frame
        return {'FINISHED'}
    
# Button on Sequencer header - that renders the video

def draw_render_button(self, context):
    layout = self.layout
    op = layout.operator("render.render", text="Render", icon='RENDER_ANIMATION')
    op.animation = True
    op.use_viewport = True
        
    
CLASSES = (
    VSE_EXTRAS_OT_SplitStrip,
)

addon_keymaps = []

def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
        
    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(
        name='Sequencer',
        space_type='SEQUENCE_EDITOR')

    kmi = km.keymap_items.new(VSE_EXTRAS_OT_SplitStrip.bl_idname, 'Z', 'PRESS')


    addon_keymaps.append((km, kmi))

    bpy.types.SEQUENCER_HT_header.append(draw_render_button)



def unregister():

    bpy.types.SEQUENCER_HT_header.remove(draw_render_button)

    # remove keymap items
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


    # unregister classes
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

# Allow hot‑reload via Run Script
if __name__ == "__main__":
    try:
        unregister()
    except Exception:
        pass
    register()
