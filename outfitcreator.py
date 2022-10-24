
import bpy
import re   
import os 
import random
import argparse 

top_items = {
            'CASUAL': 'Wolf3D_Top_Casual',
            'CYBERPUNK': 'Wolf3D_Top_Cyberpunk',
            'OFFICE': 'Wolf3D_Top_Office'
        }

bottom_items = {
            'CASUAL': 'Wolf3D_Bottom_Casual',
            'CYBERPUNK': 'Wolf3D_Bottom_Cyberpunk',
            'OFFICE': 'Wolf3D_Bottom_Office'
        }

footwear_items = {
            'CASUAL': 'Wolf3D_Footwear_Casual',
            'CYBERPUNK': 'Wolf3D_Footwear_Cyberpunk',
            'OFFICE': 'Wolf3D_Footwear_Office'
        }
        
class Enums(bpy.types.PropertyGroup):
    
    name_string : bpy.props.StringProperty(name= "Name Your Outfit")
    
    enum_top : bpy.props.EnumProperty(
        name= "Top Style",
        description= "sample text",
        items= [('CASUAL', "Casual", ""),
                ('CYBERPUNK', "Cyberpunk", ""),
                ('OFFICE', "Office", "")
        ]
    )
    enum_bottom : bpy.props.EnumProperty(
        name= "Bottom Style",
        description= "sample text",
        items= [('CASUAL', "Casual", ""),
                ('CYBERPUNK', "Cyberpunk", ""),
                ('OFFICE', "Office", "")
        ]
    )
    enum_footwear : bpy.props.EnumProperty(
        name= "Footwear Style",
        description= "sample text",
        items= [('CASUAL', "Casual", ""),
                ('CYBERPUNK', "Cyberpunk", ""),
                ('OFFICE', "Office", "")
        ]
    )
    enum_export_format :  bpy.props.EnumProperty(
        name= "Export Format",
        description="",
        items= [('obj',"OBJ",""),
                ('fbx',"FBX",""),
                ('gltf',"GLTF",""),
                ('glb',"GLB","")]
    )
    
    
class OutfitCreatorPanel(bpy.types.Panel):
    bl_idname = "outfitcreator"
    bl_label = "Full-body Outfit Creator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout 
        
        row = layout.row()
        scene = context.scene
        mytool = scene.my_tool
        
        layout.prop(mytool, "name_string") 
        layout.label(text="Please use a blank space to separate words.")
        
        row2 = layout.row()
        layout.prop(mytool, "enum_top")   
        layout.prop(mytool, "enum_bottom")
        layout.prop(mytool, "enum_footwear")
 
        row3 = layout.row()
        layout.operator("outfitcreator.operator")
        layout.operator("generator.operator")
        
        row4 = layout.row()
        layout.label(text="Please pick a format before exporting")
        layout.prop(mytool, "enum_export_format")
         
        layout.operator("exporter.operator")
        layout.operator("batch.operator")
        
        
        

class OutfitCreatorOperator(bpy.types.Operator):
    bl_label = "Compose Outfit"
    bl_idname = "outfitcreator.operator"
    bl_description = "Composes an outfit from the chosen pieces"
    
    for item in bpy.data.objects:
            if item.name.startswith('Armature'):
                item.hide_set(True)
    
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool              
        
        for k, v in top_items.items():
            bpy.data.objects[v].hide_set(k != mytool.enum_top)
        
        for k, v in bottom_items.items():
            bpy.data.objects[v].hide_set(k != mytool.enum_bottom)
    
        for k, v in footwear_items.items():
            bpy.data.objects[v].hide_set(k != mytool.enum_footwear)
        
        return {'FINISHED'}


class GeneratorOperator(bpy.types.Operator):
    bl_idname = "generator.operator"
    bl_label = "Generate Random"
    bl_description = "Generates a random combination of all pieces"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        items = [list(top_items.values()), list(bottom_items.values()), list(footwear_items.values())]
        for item in bpy.data.objects:
            if item.name.startswith('Wolf3D'):
                item.hide_set(True)
        for item in items:
            bpy.data.objects[random.choice(item)].hide_set(False)
        return {"FINISHED"}


def export(context, format, filename):
    scene = context.scene
    mytool = scene.my_tool
    
    visible=[ob for ob in bpy.context.view_layer.objects if ob.visible_get()]
        
    for v in visible:
        v.select_set( state = True, view_layer = None)
    
    arm = bpy.data.objects['FullBody_Armature']
    arm.hide_set(False)
    arm.select_set( state = True, view_layer = None)
    body = bpy.data.objects['Wolf3D_Body']
    body.hide_set(False)
    body.select_set( state = True, view_layer = None)
    
    filepath = bpy.data.filepath
    directory = os.path.dirname(filepath)
    
    exportpath = os.path.join(directory,  "{}.{}".format(filename, format))
    if format == 'fbx':
        getattr(bpy.ops.export_scene, format)(filepath=exportpath, object_types={'ARMATURE','MESH'}, use_selection=True)
    elif format == 'obj':
        getattr(bpy.ops.export_scene, format)(filepath=exportpath, use_selection=True)
    elif format == 'glb' :
        #uses the same function as gltf
        getattr(bpy.ops.export_scene, "gltf")(filepath=exportpath, export_format='GLB', use_selection=True)
    elif format == 'gltf':
        getattr(bpy.ops.export_scene, format)(filepath=exportpath, export_format='GLTF_SEPARATE', use_selection=True)
    return exportpath


class ExporterOperator(bpy.types.Operator):
    bl_idname = "exporter.operator"
    bl_label = "Export Outfit"
    bl_description = "Exports a file of the chosen format in the .blend file location"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        def enforce_naming(string):
            #TODO: add all irregular characters
            bad_chars = [",","&","*","^","."]
            for char in bad_chars:
                if char in string: 
                    self.report({'ERROR'}, "Name contains irregular characters, please review")
            chunks = re.split(" ",string)
            new_name = "_".join(map(lambda  chunk: chunk.upper(), chunks))
            #TODO: add suffix
            return new_name
        
        filename = enforce_naming(mytool.name_string)
        if mytool.name_string == "":
            self.report({'ERROR'}, "Please, name your outfit")
            return {"FINISHED"}
 
        
        
        filename = enforce_naming(mytool.name_string)
        exportpath = export(context, mytool.enum_export_format, filename)
        self.report({'INFO'}, "Export successful at location: {}".format(exportpath))
        

        return {"FINISHED"}

class BatchOperator(bpy.types.Operator):
    bl_idname = "batch.operator"
    bl_label = "Batch Generate and Export"
    bl_description = ""

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        combinations = []
        counter = 0
                    
        for i in range(10):
            for v in top_items.values():
                bpy.data.objects[v].hide_set(True)  
            for v in bottom_items.values():
                bpy.data.objects[v].hide_set(True)  
            for v in footwear_items.values():
                bpy.data.objects[v].hide_set(True)
            
            
            for i in top_items.values():
                for j in bottom_items.values():
                    for k in footwear_items.values():
                            combinations.append((i, j, k))
            

            combination = combinations.pop(random.randrange(len(combinations)))
            
            for el in combination:
                bpy.data.objects[el].hide_set(False)
            
            filename = mytool.name_string 
            exportpath = export(context, mytool.enum_export_format, filename + 'ver-{}'.format(counter))   
            export(context, mytool.enum_export_format, filename)
            for el in combination:
                bpy.data.objects[el].hide_set(True)
            
            counter += 1
            
            self.report({'INFO'},''.join(exportpath))
            
        return {"FINISHED"}

 
def register():
    bpy.utils.register_class(Enums)
    bpy.utils.register_class(OutfitCreatorPanel)
    bpy.utils.register_class(OutfitCreatorOperator)
    bpy.utils.register_class(ExporterOperator)
    bpy.utils.register_class(GeneratorOperator)
    bpy.utils.register_class(BatchOperator)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=Enums)
  
 
def unregister():
    bpy.utils.unregister_class(Enums)
    bpy.utils.unregister_class(OutfitCreatorPanel)
    bpy.utils.unregister_class(OutfitCreatorOperator)
    bpy.utils.unregister_class(ExporterOperator)
    bpy.utils.register_class(GeneratorOperator)
    bpy.utils.unregister_class(BatchOperator)
    del bpy.types.Scene.my_tool

#TODO: loading from folder or JSON
# def load_assets():
#     for path in import_paths:
#         abspath = os.path.realpath(path)
#         bpy.ops.import_scene.obj(abspath)
 
if __name__ == "__main__":
    register()
#    load_assets()
