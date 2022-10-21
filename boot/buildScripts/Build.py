import os

from main.api.Api import copyDir

if(__name__) == '__main__':
    
    srcPath = os.path.dirname(__file__) + "/templates/mainProjectTemplate"
    targePath = os.path.join(os.getcwd(), "boot")
    copyDir(srcPath, targePath)
    print("\nBuild Successful")