import os
import json
from typing import Any

from ..config.Configuration import isShowDetail

# 得到传入的文件夹路径内的所有文件的完整路径列表
def loadFiles(dirPath, suffix=".txt"):
    files = []
    for filepath, dirName, filenames in os.walk(dirPath):
        for fileName in filenames:
            if os.path.splitext(fileName)[-1] == suffix:
                files.append(filepath + '/' + fileName)
    return files


# 通过传入的json文件路径得到一个字典对象
def loadFileWithJson(filePath: str):
    with open(filePath, encoding="utf-8") as f:
        return json.load(f)


# 删除给定目录下所有的文件
def deleteAllFile(dirPath, show=isShowDetail):
    files = os.listdir(dirPath)
    for i in files:
        f_path = os.path.join(dirPath + i)
        if os.path.isdir(f_path):
            deleteAllFile(f_path)
        else:
            os.remove(f_path)
    if show:
        print("成功删除" + dirPath + "下所有的文件")


# 在指定位置创建一个给定json对象的json文件
def createJsonInPath(jsonObj: Any, filePath: str, show=isShowDetail):
    dirPath = os.path.dirname(filePath)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    json.dump(jsonObj, open(filePath, 'w'), indent=2)
    if show:
        print("成功创建" + os.path.basename(filePath))

# 拷贝文件夹
def copyDir(src_path, targe_path, showLog = True):
    if(os.path.isdir(src_path)):
        files = os.listdir(src_path)
        for f in files:
            # 完整路径
            fullPath = os.path.join(src_path, f)
            targePath = os.path.join(targe_path, f)
            # 如果是文件夹进行递归
            if(os.path.isdir(fullPath)):
                if(not os.path.exists(targePath)):
                    os.makedirs(targePath)
                    if(showLog):
                        print("[Make dir] --> " + targePath)
                copyDir(fullPath, targe_path + '\\' + f)
            else:
                # 拷贝
                with open(fullPath, 'r', encoding="utf-8") as srcFile:
                    contents = srcFile.read()
                    with open(targePath, 'w', encoding="utf-8") as targeFile:
                        targeFile.write(contents)
                        if(showLog):
                            print("[Create file] --> " + targePath)
