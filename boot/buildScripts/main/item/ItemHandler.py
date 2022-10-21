from xml.dom.minidom import Element, parse
from ..api.Api import *
from ..config.Configuration import rootBehPath, McItemBehPath, nameSpace, McItemResPath, modRes, itemTexturePath, templatePath
from ..Sql import SqlCls

class XmlHandler:
    def __init__(self, mcBeh: dict, mcRes: dict, rootNode: Element) -> None:
        self.__mcBeh: dict = mcBeh;
        self.__mcRes: dict = mcRes;
        self.__rootNode: Element = rootNode;
        self.deal();

    def deal(self):
        
        # 获取beh节点
        behNode: Element = self.__rootNode.getElementsByTagName("beh")[0]
        # ID配置
        ID = behNode.getElementsByTagName("ID")[0].childNodes[0].data;
        NAME = behNode.getElementsByTagName("name")[0].childNodes[0].data;
        SqlCls.itemList[ID] = NAME;
        
        self.__mcBeh["minecraft:item"]["description"]["identifier"] = nameSpace + ":" + ID
        # 是否创造栏显示
        isCreateModeShow = bool(behNode.getElementsByTagName("isCreateModeShow")[0].childNodes[0].data)
        self.__mcBeh["minecraft:item"]["description"]["register_to_create_menu"] = isCreateModeShow
        # 创造栏分类
        tab = behNode.getElementsByTagName("tab")[0].childNodes[0].data
        self.__mcBeh["minecraft:item"]["description"]["category"] = tab
        # 是否闪烁显示
        foil = bool(behNode.getElementsByTagName("foil")[0].childNodes[0].data)
        self.__mcBeh["minecraft:item"]["components"]["minecraft:foil"] = foil
        # 最大堆叠数
        if self.__rootNode.getAttribute("type") == "prop":
            maxSize = int(behNode.getElementsByTagName("maxSize")[0].childNodes[0].data)
            self.__mcBeh["minecraft:item"]["components"]["minecraft:max_stack_size"] = maxSize

        # 资源配置
        # resNode: Element = self.__rootNode.getElementsByTagName("res")[0]
        # ID
        self.__mcRes["minecraft:item"]["description"]["identifier"] = nameSpace + ":" + ID
        # icon
        self.__mcRes["minecraft:item"]["components"]["minecraft:icon"] = nameSpace + ":" + ID
        # 创造栏分类
        self.__mcRes["minecraft:item"]["description"]["category"] = tab
        # 创造栏是否显示
        self.__mcRes["minecraft:item"]["description"]["register_to_create_menu"] = isCreateModeShow

    def getMcBeh(self) -> dict:
        return self.__mcBeh

    def getMcRes(self) -> dict:
        return self.__mcRes

    def getRootNode(self) -> Element:
        return self.__rootNode


class ItemHandler:

    def __init__(self) -> None:
        # 获取所有要配置的xml文件
        self.files: list = loadFiles(rootBehPath + "item", ".xml")

        # 获取原生minecraft json
        self.mcBeh: dict = loadFileWithJson(templatePath + "item/itemBeh.json")
        self.mcRes: dict = loadFileWithJson(templatePath + "item/itemRes.json")

    @staticmethod
    def clear():

        # 删除所有相关物品的json文件
        deleteAllFile(McItemBehPath)
        deleteAllFile(McItemResPath)
        # 清理 itemTexture json中的内容
        with open(itemTexturePath, 'r', encoding="utf-8") as f:
            itemTexture = json.load(f)
            itemTexture["texture_data"] = {}
            json.dump(itemTexture, open(modRes + "textures/item_texture.json", 'w'), indent=2)

    def deal(self):

        # 首先清理
        self.clear()
        # itemTexture.json中 texture_data
        texture_data = {}

        for f in self.files:
            with open(f, encoding="utf-8") as F:
                dom = parse(F)
                # 得到根节点
                rootNode: Element = dom.documentElement

                xmlHandler = XmlHandler(self.mcBeh, self.mcRes, rootNode)

                okMcBeh = xmlHandler.getMcBeh()
                okMcRes = xmlHandler.getMcRes()

                beh = rootNode.getElementsByTagName("beh")[0]
                okID: str = beh.getElementsByTagName("ID")[0].childNodes[0].data

                behFileName = McItemBehPath + nameSpace + "_" + okID + ".json"
                resFileName = McItemResPath + nameSpace + "_" + okID + ".json"

                createJsonInPath(okMcBeh, behFileName)
                createJsonInPath(okMcRes, resFileName)

                res = rootNode.getElementsByTagName("res")[0]
                textures = res.getElementsByTagName("textures")[0].childNodes[0].data
                # 标记 itemTexture.json中 texture_data
                texture_data[nameSpace + ":" + okID] = {}
                texture_data[nameSpace + ":" + okID]["textures"] = textures

        # 修改 itemTexture.json中 texture_data
        with open(itemTexturePath, 'r', encoding="utf-8") as f:
            itemTexture = json.load(f)
            itemTexture["texture_data"] = texture_data
            json.dump(itemTexture, open(modRes + "textures/item_texture.json", 'w'), indent=2)
