from posixpath import abspath
import bpy
import re   
import os  

#import_paths = [r"/obj/top_casual_01.obj"]  
  
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
        items= [('OBJ',".obj",""),
                ('FBX',".fbx",""),
                ('GLTF',".gltf",""),
                ('GLB',".glb","")]
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
        layout.label(text="Please pick a format before exporting")
        layout.prop(mytool, "enum_export_format")
        
        layout.operator("outfitcreator.operator")
        layout.operator("exporter.operator")
        
        

class OutfitCreatorOperator(bpy.types.Operator):
    bl_label = "Compose Outfit"
    bl_idname = "outfitcreator.operator"
    
    for item in bpy.data.objects:
            if item.name.startswith('Armature'):
                item.hide_set(True)
    
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool              
        def enforce_naming(string):
            #TODO: add all irregular characters
            bad_chars = [",","&","*","^"]
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
        
                
        
        if mytool.my_enum_top == 'CASUAL':
            bpy.data.objects['Wolf3D_Top_Casual'].hide_set(False)  
            bpy.data.objects['Wolf3D_Top_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Top_Office'].hide_set(True)   
            
        if mytool.my_enum_top == 'CYBERPUNK':
            bpy.data.objects['Wolf3D_Top_Casual'].hide_set(True)
            bpy.data.objects['Wolf3D_Top_Cyberpunk'].hide_set(False)
            bpy.data.objects['Wolf3D_Top_Office'].hide_set(True)
            
        if mytool.my_enum_top == 'OFFICE':
            bpy.data.objects['Wolf3D_Top_Casual'].hide_set(True)
            bpy.data.objects['Wolf3D_Top_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Top_Office'].hide_set(False)
        
        if mytool.my_enum_bottom == 'CASUAL':
            bpy.data.objects['Wolf3D_Bottom_Casual'].hide_set(False)  
            bpy.data.objects['Wolf3D_Bottom_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Bottom_Office'].hide_set(True)         
            
        if mytool.my_enum_bottom == 'CYBERPUNK':
            bpy.data.objects['Wolf3D_Bottom_Casual'].hide_set(True)  
            bpy.data.objects['Wolf3D_Bottom_Cyberpunk'].hide_set(False)
            bpy.data.objects['Wolf3D_Bottom_Office'].hide_set(True)  
            
        if mytool.my_enum_bottom == 'OFFICE':
            bpy.data.objects['Wolf3D_Bottom_Casual'].hide_set(True)  
            bpy.data.objects['Wolf3D_Bottom_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Bottom_Office'].hide_set(False)
        
        if mytool.my_enum_footwear == 'CASUAL':            
            bpy.data.objects['Wolf3D_Footwear_Casual'].hide_set(False)  
            bpy.data.objects['Wolf3D_Footwear_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Footwear_Office'].hide_set(True)       
            
        if mytool.my_enum_footwear == 'CYBERPUNK':
            bpy.data.objects['Wolf3D_Footwear_Casual'].hide_set(True)  
            bpy.data.objects['Wolf3D_Footwear_Cyberpunk'].hide_set(False)
            bpy.data.objects['Wolf3D_Footwear_Office'].hide_set(True)
            
        if mytool.my_enum_footwear == 'OFFICE':
            bpy.data.objects['Wolf3D_Footwear_Casual'].hide_set(True)  
            bpy.data.objects['Wolf3D_Footwear_Cyberpunk'].hide_set(True)
            bpy.data.objects['Wolf3D_Footwear_Office'].hide_set(False)
        
        return {'FINISHED'}


class ExporterOperator(bpy.types.Operator):
    bl_idname = "exporter.operator"
    bl_label = "Export Outfit"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        return {"FINISHED"}
 
 
def register():
    bpy.utils.register_class(Enums)
    bpy.utils.register_class(OutfitCreatorPanel)
    bpy.utils.register_class(OutfitCreatorOperator)
    bpy.utils.register_class(ExporterOperator)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=Enums)
 
def unregister():
    bpy.utils.unregister_class(Enums)
    bpy.utils.unregister_class(OutfitCreatorPanel)
    bpy.utils.unregister_class(OutfitCreatorOperator)
    bpy.utils.unregister_class(ExporterOperator)
    del bpy.types.Scene.my_tool

#TODO: proper loading
# def load_assets():
#     for path in import_paths:
#         abspath = os.path.realpath(path)
#         bpy.ops.import_scene.obj(abspath)
 
if __name__ == "__main__":
    register()
#    load_assets()
