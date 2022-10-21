from enum import Enum
import bpy      

        
class Enums(bpy.types.PropertyGroup):
    
    my_string : bpy.props.StringProperty(name= "Name Your Outfit")
    
   # my_float_vector : bpy.props.FloatVectorProperty(name= "Scale", soft_min= 0, soft_max= 1000, default= (1,1,1))
    
    my_enum_top : bpy.props.EnumProperty(
        name= "Top Style",
        description= "sample text",
        items= [('OP1', "Top Style 01", ""),
                ('OP2', "Top Style 02", ""),
                ('OP3', "Top Style 03", "")
        ]
    )
    my_enum_bottom : bpy.props.EnumProperty(
        name= "Bottom Style",
        description= "sample text",
        items= [('OP1', "Bottom Style 01", ""),
                ('OP2', "Bottom Style 02", ""),
                ('OP3', "Bottom Style 03", "")
        ]
    )
    my_enum_footwear : bpy.props.EnumProperty(
        name= "Footwear Style",
        description= "sample text",
        items= [('OP1', "Footwear Style 01", ""),
                ('OP2', "Footwear Style 02", ""),
                ('OP3', "Footwear Style 03", "")
        ]
    )
    
    
class OutfitCreatorPanel(bpy.types.Panel):
    bl_idname = "OUTFITCREATOR_main_panel"
    bl_label = "Full-body Outfit Creator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout 
        layout.label(text="Create a custom outfit!")
        row = layout.row()
        scene = context.scene
        mytool = scene.my_tool
        
        layout.prop(mytool, "my_string")
        layout.prop(mytool, "my_enum_top")   
        layout.prop(mytool, "my_enum_bottom")
        layout.prop(mytool, "my_enum_footwear")
 
        layout.operator("addonname.myop_operator")
        
        

class OutfitCreatorOperator(bpy.types.Operator):
    bl_label = "Export Outfit"
    bl_idname = "addonname.myop_operator"
    
    
    
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        
        # def enforce_naming(string):
            
        
        if mytool.my_enum_top == 'OP1':
            bpy.context.object.name = mytool.my_string       
            
        if mytool.my_enum_top == 'OP2':
            bpy.context.object.name = mytool.my_string
            
        if mytool.my_enum_top == 'OP3':
            bpy.context.object.name = mytool.my_string
        
        if mytool.my_enum_bottom == 'OP1':
            bpy.context.object.name = mytool.my_string        
            
        if mytool.my_enum_bottom == 'OP2':
            bpy.context.object.name = mytool.my_string
            
        if mytool.my_enum_bottom == 'OP3':
            bpy.context.object.name = mytool.my_string
        
        if mytool.my_enum_footwear == 'OP1':         
            bpy.ops.mesh.primitive_monkey_add(size=5.0)
            bpy.context.object.name = mytool.my_string       
            
        if mytool.my_enum_footwear == 'OP2':
            bpy.ops.mesh.primitive_monkey_add(size=5.0)
            bpy.context.object.name = mytool.my_string
            
        if mytool.my_enum_footwear == 'OP3':
            bpy.ops.mesh.primitive_monkey_add(size=5.0)
            bpy.context.object.name = mytool.my_string
        
        return {'FINISHED'}
    
 
def register():
    bpy.utils.register_class(Enums)
    bpy.utils.register_class(OutfitCreatorPanel)
    bpy.utils.register_class(OutfitCreatorOperator)
    #bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= Enumerators)
 
def unregister():
    bpy.utils.unregister_class(Enums)
    bpy.utils.unregister_class(OutfitCreatorPanel)
    bpy.utils.unregister_class(OutfitCreatorOperator)
    del bpy.types.Scene.my_tool

 
 
if __name__ == "__main__":
    register()
