import os

# 执行脚本时是否显示细节信息
isShowDetail = False

# Mod命名空间
nameSpace = "mfjy"

# 项目beh路径
rootBehPath = "C:/Users/TianJi/Desktop/ModMakerPy/boot/beh/"
# 项目res路径
rootResPath = "C:/Users/TianJi/Desktop/ModMakerPy/boot/res/"

# modBeh路径
modBeh = "D:/MCStudioDownload/work/notian239@163.com/Cpp/AddOn/130162623aeb4f5f871e4e8265a97197" \
         "/behavior_pack_z6qLDV7H_419bb38e/"

# modRes路径
modRes = "D:/MCStudioDownload/work/notian239@163.com/Cpp/AddOn/130162623aeb4f5f871e4e8265a97197" \
         "/resource_pack_XEZHPUwg_5dc55bf0/"

# 以下路径无需修改****************************************************************************

# MC Json文件模板路径
templatePath = os.path.join(os.getcwd(), "boot\\buildScripts\\templates\\mcJsonTemplate\\")
# print(templatePath)
# item路径
McItemBehPath = modBeh + "netease_items_beh/"
# block路径
blockBehPath = modBeh + "netease_blocks/"
# entity路径
entityBehPath = modBeh + "entities/"

# item路径
McItemResPath = modRes + "netease_items_res/"
# item_texture.json路径
itemTexturePath = modRes + "textures/item_texture.json"
# entity路径
entityResPath = modRes + "entity/"
# animation_controller路径
animationControllerPath = modRes + "animation_controllers/"
