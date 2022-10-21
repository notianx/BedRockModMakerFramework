from xml.dom.minidom import parse, Element

from ..api.Api import *
from ..config.Configuration import nameSpace, rootBehPath, modRes, blockBehPath, templatePath

# blocks.json
blocksJsonPath = modRes + "blocks.json"
# terrain_texture.json
terrainTextureJsonPath = modRes + "textures/terrain_texture.json"


class XmlHandler:
    def __init__(self, mcBeh, rootNode: Element):
        self.__mcBeh: dict = mcBeh
        self.__rootNode: Element = rootNode
        self.deal()

    def deal(self):
        # 获取beh节点
        beh: Element = self.__rootNode.getElementsByTagName("beh")[0]
        # id配置
        ID = beh.getElementsByTagName("ID")[0].childNodes[0].data
        self.__mcBeh["minecraft:block"]["description"]["identifier"] = nameSpace + ":" + ID
        # 是否创造栏显示
        isCreateModeShow = beh.getElementsByTagName("isCreateModeShow")[0].childNodes[0].data
        self.__mcBeh["minecraft:block"]["description"]["register_to_creative_menu"] = bool(isCreateModeShow)
        # 亮度配置
        light = beh.getElementsByTagName("light")[0].childNodes[0].data
        self.__mcBeh["minecraft:block"]["components"]["minecraft:block_light_emission"]["emission"] = float(light)

    def getMcBeh(self) -> dict:
        return self.__mcBeh

    def getRootNode(self) -> Element:
        return self.__rootNode


# Block文件处理器
class BlockHandler:
    def __init__(self):

        # 获取所有要配置xml的文件
        self.xmlFiles: list = loadFiles(rootBehPath + "block", ".xml")

        # 获取原生minecraft json
        self.mcBeh: dict = loadFileWithJson(templatePath + "block/blockBeh.json")

    # 构建前进行清理
    @staticmethod
    def clear():
        deleteAllFile(blockBehPath)

        # 清空blocks.json中的内容
        json.dump({"format_version": [1, 1, 0]}, open(blocksJsonPath, 'w'), indent=2)

        # 清空terrain_texture.json中内容
        with open(terrainTextureJsonPath, encoding="utf-8") as f:
            terrainTextureJson = json.load(f)
            terrainTextureJson["texture_data"] = {}
            json.dump(terrainTextureJson, open(terrainTextureJsonPath, 'w'), indent=2)

    # 核心处理方法
    def deal(self):
        # 一切开始之前先清理
        self.clear()

        with open(blocksJsonPath, encoding="utf-8") as f:
            blockJson = json.load(f)
        with open(terrainTextureJsonPath, encoding="utf-8") as f:
            terrainTextureJson = json.load(f)

        for f in self.xmlFiles:
            with open(f, encoding="utf-8") as F:
                dom = parse(F)
                # 得到根节点
                rootNode: Element = dom.documentElement

                # 创建一个xml转换器
                xmlHandler = XmlHandler(mcBeh=self.mcBeh, rootNode=rootNode)

                # 获取配置完成的原生mc json对象
                okMcBeh = xmlHandler.getMcBeh()

                res: Element = rootNode.getElementsByTagName("res")[0]
                textures = res.getElementsByTagName("textures")[0].childNodes[0].data

                # 合成mobID
                mobID = rootNode.getElementsByTagName("beh")[0].getElementsByTagName("ID")[0].childNodes[0].data
                okId = nameSpace + ":" + mobID
                # 创建beh文件
                createJsonInPath(okMcBeh, blockBehPath + nameSpace + "_" + mobID + ".json")

                # 修改blockJson和terrainTextureJson中的内容
                blockJson[okId] = {}
                blockJson[okId]["textures"] = okId
                terrainTextureJson["texture_data"][okId] = {}
                terrainTextureJson["texture_data"][okId]["textures"] = textures

        json.dump(blockJson, open(blocksJsonPath, 'w'), indent=2)
        json.dump(terrainTextureJson, open(terrainTextureJsonPath, 'w'), indent=2)
