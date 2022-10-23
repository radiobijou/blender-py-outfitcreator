
import bpy
import re   
import os 
import random
import argparse 

top_items = ['Wolf3D_Top_Casual','Wolf3D_Top_Cyberpunk', 'Wolf3D_Top_Office']
bottom_items = ['Wolf3D_Bottom_Casual','Wolf3D_Bottom_Cyberpunk', 'Wolf3D_Bottom_Office']
footwear_items = ['Wolf3D_Footwear_Casual','Wolf3D_Footwear_Cyberpunk', 'Wolf3D_Footwear_Office']  
  
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
        def enforce_naming(string):
            #TODO: add all irregular characters
            bad_chars = [",","&","*","^","."]
            for char in bad_chars:
                if char in string:
                    self.report({'ERROR'}, "Name contains irregular characters, please review")
                    
            chunks = re.split(" ",string)
            new_name = "_".join(map(lambda  chunk: chunk.upper(), chunks))
            #TODO: add suffix
            #self.report({'INFO'}, new_name)
            return new_name

            #after collecting hidden, compose a parent object and name all of its components
            #bpy.context.object.name = mytool.my_string
        
        #TODO:refactor
        # top_items = [('casual','cyberpunk','office'),('Wolf3D_Top_Casual','Wolf3D_Top_Cyberpunk', 'Wolf3D_Top_Office')]
        # bottom_items = [('casual','cyberpunk','office'),('Wolf3D_Bottom_Casual','Wolf3D_Bottom_Cyberpunk', 'Wolf3D_Bottom_Office')]
        # footwear_items = [('casual','cyberpunk','office'),('Wolf3D_Footwear_Casual','Wolf3D_Footwear_Cyberpunk', 'Wolf3D_Footwear_Office')]

        # enum_items = [
        # (mytool.enum_top), (self.top_items),
        # (mytool.enum_bottom), (self.bottom_items),
        # (mytool.enum_footwear), (self.footwear_items),
        # ]      
        
        # for enum, category in enum_items:
        #     for k, v in category.items():
        #         visible = k == enum
        #         bpy.data.objects[v].hide_set(visible)


        if mytool.enum_top == 'CASUAL':
            bpy.data.objects['Wolf3D_Top_Casual'].hide_set(False)  
            bpy.data.objects['Wolf3D_Top_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Top_Office'].hide_set(True)   
            
        if mytool.enum_top == 'CYBERPUNK':
            bpy.data.objects['Wolf3D_Top_Casual'].hide_set(True)
            bpy.data.objects['Wolf3D_Top_Cyberpunk'].hide_set(False)
            bpy.data.objects['Wolf3D_Top_Office'].hide_set(True)
            
        if mytool.enum_top == 'OFFICE':
            bpy.data.objects['Wolf3D_Top_Casual'].hide_set(True)
            bpy.data.objects['Wolf3D_Top_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Top_Office'].hide_set(False)
        
        if mytool.enum_bottom == 'CASUAL':
            bpy.data.objects['Wolf3D_Bottom_Casual'].hide_set(False)  
            bpy.data.objects['Wolf3D_Bottom_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Bottom_Office'].hide_set(True)         
            
        if mytool.enum_bottom == 'CYBERPUNK':
            bpy.data.objects['Wolf3D_Bottom_Casual'].hide_set(True)  
            bpy.data.objects['Wolf3D_Bottom_Cyberpunk'].hide_set(False)
            bpy.data.objects['Wolf3D_Bottom_Office'].hide_set(True)  
            
        if mytool.enum_bottom == 'OFFICE':
            bpy.data.objects['Wolf3D_Bottom_Casual'].hide_set(True)  
            bpy.data.objects['Wolf3D_Bottom_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Bottom_Office'].hide_set(False)
        
        if mytool.enum_footwear == 'CASUAL':            
            bpy.data.objects['Wolf3D_Footwear_Casual'].hide_set(False)  
            bpy.data.objects['Wolf3D_Footwear_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Footwear_Office'].hide_set(True)       
            
        if mytool.enum_footwear == 'CYBERPUNK':
            bpy.data.objects['Wolf3D_Footwear_Casual'].hide_set(True)  
            bpy.data.objects['Wolf3D_Footwear_Cyberpunk'].hide_set(False)
            bpy.data.objects['Wolf3D_Footwear_Office'].hide_set(True)
            
        if mytool.enum_footwear == 'OFFICE':
            bpy.data.objects['Wolf3D_Footwear_Casual'].hide_set(True)  
            bpy.data.objects['Wolf3D_Footwear_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Footwear_Office'].hide_set(False)
        
        return {'FINISHED'}


class GeneratorOperator(bpy.types.Operator):
    #TODO: generate with permutations
    #Use the command line to execute
    bl_idname = "generator.operator"
    bl_label = "Generate Random"
    bl_description = "Generates a random combination of all pieces"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        items = [top_items, bottom_items, footwear_items]
        for item in bpy.data.objects:
            if item.name.startswith('Wolf3D'):
                item.hide_set(True)
        for item in items:
            bpy.data.objects[random.choice(item)].hide_set(False)
        return {"FINISHED"}

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
        format = mytool.enum_export_format
        filepath = bpy.data.filepath
        directory = os.path.dirname(filepath)
        exportpath = "{}\{}.{}".format(directory, mytool.name_string, mytool.enum_export_format)
        if mytool.enum_export_format == 'fbx':
            getattr(bpy.ops.export_scene, format)(filepath=exportpath, 
                                                                     object_types={'ARMATURE','MESH'},
                                                                     use_metadata=True)
        elif mytool.enum_export_format == 'obj':
            getattr(bpy.ops.export_scene, format)(filepath=exportpath)
        elif mytool.enum_export_format == 'glb' :
            #uses the same function as gltf 
            getattr(bpy.ops.export_scene, "gltf")(filepath=exportpath, export_format='GLB')
        elif mytool.enum_export_format == 'gltf':
            getattr(bpy.ops.export_scene, format)(filepath=exportpath, export_format='GLTF_SEPARATE')
        self.report({'INFO'}, exportpath)
        return {"FINISHED"}


 
def register():
    bpy.utils.register_class(Enums)
    bpy.utils.register_class(OutfitCreatorPanel)
    bpy.utils.register_class(OutfitCreatorOperator)
    bpy.utils.register_class(ExporterOperator)
    bpy.utils.register_class(GeneratorOperator)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=Enums)
  
 
def unregister():
    bpy.utils.unregister_class(Enums)
    bpy.utils.unregister_class(OutfitCreatorPanel)
    bpy.utils.unregister_class(OutfitCreatorOperator)
    bpy.utils.unregister_class(ExporterOperator)
    bpy.utils.register_class(GeneratorOperator)
    del bpy.types.Scene.my_tool

#TODO: loading from folder or JSON
# def load_assets():
#     for path in import_paths:
#         abspath = os.path.realpath(path)
#         bpy.ops.import_scene.obj(abspath)
 
if __name__ == "__main__":
    register()
#    load_assets()
