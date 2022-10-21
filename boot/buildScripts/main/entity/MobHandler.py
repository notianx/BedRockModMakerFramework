import json
from xml.dom.minidom import parse, Element

from ..api.Api import loadFileWithJson, createJsonInPath, deleteAllFile, loadFiles
from ..config.Configuration import entityBehPath, rootBehPath, nameSpace, entityResPath, animationControllerPath, templatePath


class XmlHandler:
    def __init__(self, mcBeh, mcRes, rootNode: Element):
        self.__mcBeh: dict = mcBeh
        self.__mcRes: dict = mcRes
        self.__rootNode: Element = rootNode
        self.deal()

    def deal(self):
        # 行为配置********************************************************************************
        # 获取beh节点
        beh: Element = self.__rootNode.getElementsByTagName("beh")[0]
        # id配置
        ID = beh.getElementsByTagName("ID")[0].childNodes[0].data
        self.__mcBeh["minecraft:entity"]["description"]["identifier"] = nameSpace + ":" + ID
        self.__mcBeh["minecraft:entity"]["description"]["runtime_identifier"] = nameSpace + ":" + ID
        # family配置
        familyS = beh.getElementsByTagName("familys")[0].getElementsByTagName("family")
        for i in range(len(familyS)):
            family = familyS[i].childNodes[0].data
            self.__mcBeh["minecraft:entity"]["components"]["minecraft:type_family"]["family"].append(family)
        # 获取base节点
        base = beh.getElementsByTagName("base")[0]
        # 碰撞箱配置
        box = base.getElementsByTagName("box")[0]
        self.__mcBeh["minecraft:entity"]["components"]["minecraft:collision_box"]["width"] = \
            float(box.getElementsByTagName("width")[0].childNodes[0].data)
        self.__mcBeh["minecraft:entity"]["components"]["minecraft:collision_box"]["height"] = \
            float(box.getElementsByTagName("height")[0].childNodes[0].data)
        # 生命值配置
        health = base.getElementsByTagName("health")[0].childNodes[0].data
        self.__mcBeh["minecraft:entity"]["components"]["minecraft:health"]["value"] = float(health)
        self.__mcBeh["minecraft:entity"]["components"]["minecraft:health"]["max"] = float(health)
        # 移动配置
        move: Element = base.getElementsByTagName("move")[0]
        moveType = move.getAttribute("type")
        # 陆地
        if moveType == "land":
            self.__mcBeh["minecraft:entity"]["components"]["minecraft:movement"]["value"] = \
                float(move.getElementsByTagName("speed")[0].childNodes[0].data)
        # 水下
        elif moveType == "water":
            pass
        # 飞行
        elif moveType == "sky":
            pass
        # AI配置
        # 获取AI节点
        AI: Element = beh.getElementsByTagName("AI")[0]
        # 配置是否可以移动
        if len(AI.getElementsByTagName("canMove")) > 0:
            self.__mcBeh["minecraft:entity"]["components"]["minecraft:movement.basic"] = {}
            self.__mcBeh["minecraft:entity"]["components"]["minecraft:behavior.random_stroll"] = {
                "priority": 6,
                "speed_multiplier": 1
            }
        # 配置是否可以攀爬
        if len(AI.getElementsByTagName("canClimb")) > 0:
            self.__mcBeh["minecraft:entity"]["components"]["minecraft:can_climb"] = {}
        # 配置是否随机漫步
        if len(AI.getElementsByTagName("randomWalk")) > 0:
            self.__mcBeh["minecraft:entity"]["components"]["minecraft:can_climb"] = {}
        # 资源配置*************************************************************************************
        # 获取res节点
        res: Element = self.__rootNode.getElementsByTagName("res")[0]
        # id
        self.__mcRes["minecraft:client_entity"]["description"]["identifier"] = nameSpace + ":" + ID
        # 模型信息配置
        self.__mcRes["minecraft:client_entity"]["description"]["geometry"]["default"] = \
            res.getElementsByTagName("model")[0].childNodes[0].data
        # 材质信息配置
        material = res.getElementsByTagName("material")[0].childNodes[0].data
        if material == "default":
            pass
        # 动画信息
        animations = res.getElementsByTagName("animations")[0].getElementsByTagName("animation")
        for anim in animations:
            anim: Element = anim
            name = anim.getAttribute("name")
            text = anim.childNodes[0].data
            self.__mcRes["minecraft:client_entity"]["description"]["animations"][name] = text
        # 动画控制器配置
        # 获取动画控制器节点
        animControllerNode: Element = res.getElementsByTagName("animation_controllers")[0]
        # 合成动画控制器id
        animConID = "controller.animation." + ID
        # 打开mc原生动画控制器模板文件
        with open(templatePath + "entity/animationController.json") as f:
            # mc原生动画控制器json
            animConJson = json.load(f)
            # 设置该id的动画控制器内容
            animConJson["animation_controllers"][animConID] = {}
            # 设置默认状态
            animConJson["animation_controllers"][animConID]["initial_state"] = \
                animControllerNode.getElementsByTagName("initial_state")[0].childNodes[0].data
            # 获取所有状态节点
            states = animControllerNode.getElementsByTagName("state")
            # 遍历所有状态节点
            for state in states:
                state: Element = state
                # 状态名称
                stateName = state.getAttribute("name")
                # 获取状态中所有动画节点
                animations = state.getElementsByTagName("animations")[0].getElementsByTagName("animation")
                # 创建空的animations list
                animationsList: list = []
                for anim in animations:
                    anim: Element = anim
                    animName = anim.getAttribute("name")
                    # 将动画名添加到animations list中
                    animationsList.append(animName)
                # 获取转换条件节点
                transitions: Element = state.getElementsByTagName("transitions")[0]
                # 配置到json中
                animConJson["animation_controllers"][animConID][stateName] = {
                    "animations": [],
                    "transitions": [{}]
                }
                animConJson["animation_controllers"][animConID][stateName]["animations"] = animationsList
                animConJson["animation_controllers"][animConID][stateName]["transitions"][0][
                    transitions.getAttribute("state")] = transitions.childNodes[0].data

            # 在mod文件夹中创建该动画控制器文件
            createJsonInPath(animConJson, animationControllerPath + "controller." + ID + ".json")
            # 设置res文件中动画控制器为该控制器
            self.__mcRes["minecraft:client_entity"]["description"]["animation_controllers"][0]["default"] = animConID
            # 设置贴图文件路径
            texturePath = res.getElementsByTagName("textures")[0].childNodes[0].data
            self.__mcRes["minecraft:client_entity"]["description"]["textures"]["default"] = texturePath

    # 判断给定节点是否有某个子节点
    @staticmethod
    def isHaveNode(NodeA: Element, NodeBName: str) -> bool:
        return len(NodeA.getElementsByTagName(NodeBName)) != 0

    def getMcBeh(self) -> dict:
        return self.__mcBeh

    def getMcRes(self) -> dict:
        return self.__mcRes

    def getRootNode(self) -> Element:
        return self.__rootNode


class MobHandler:

    def __init__(self) -> None:

        # 从项目文件中获取所有mobs的xml文件
        self.xmlFiles: list = loadFiles(rootBehPath + "entity/mobs", ".xml")

        # 获取原生minecraft json模板文件
        self.mcBeh: dict = loadFileWithJson(templatePath + "entity/beh.json")
        self.mcRes: dict = loadFileWithJson(templatePath + "entity/res.json")

    def deal(self):
        # 一切开始之前先清理
        self.clear()
        # mc原生json拷贝
        mcBehJson: dict = self.mcBeh.copy()
        mcResJson: dict = self.mcRes.copy()

        # 遍历项目文件中所有mobs的xml文件
        for f in self.xmlFiles:
            with open(f, encoding="utf-8") as F:
                dom = parse(F)
                # 得到根节点
                rootNode: Element = dom.documentElement

                # 合成mobID
                mobID = rootNode.getElementsByTagName("beh")[0].getElementsByTagName("ID")[0].childNodes[0].data

                # 创建一个xml转换器
                xmlHandler = XmlHandler(mcBehJson, mcResJson, rootNode)
                # 得到处理后的原生mc json文件
                okMcBeh = xmlHandler.getMcBeh()
                okMcRes = xmlHandler.getMcRes()
                # 合成完整的文件名
                fileName = nameSpace + "_" + mobID

                # 开始在mod文件夹中创建被处理后的json文件
                createJsonInPath(okMcBeh, entityBehPath + fileName + ".json")
                createJsonInPath(okMcRes, entityResPath + fileName + ".json")

    @staticmethod
    def clear():
        # 删除所有生物相关的json文件
        deleteAllFile(entityBehPath)
        deleteAllFile(entityResPath)
        deleteAllFile(animationControllerPath)
