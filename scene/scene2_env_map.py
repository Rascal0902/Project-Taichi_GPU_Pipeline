import taichi as ti
import os

def setModel2(modelClass, current_dir):
    modelClass.addModel("SMPL")
    SMPLTexturePath = os.path.join(current_dir, 'light_module', 'texture', 'gray.png')
    modelClass.setTexture("SMPL", SMPLTexturePath)
    SMPLobjPath = os.path.join(current_dir, 'light_module', 'model', 'SMPL_TPose.obj')
    modelClass.setMesh("SMPL", SMPLobjPath, render=True)
    applyTransform_settings = (3, (0.0, 0.0, 0.0), (0.0, 180.0, 0.0))
    modelClass.setSpaceChanger("SMPL", applyTransform_settings)
    modelClass.setShader("SMPL", "HUMAN")

    modelClass.addModel("CLOTH")
    CLOTHTexturePath = os.path.join(current_dir, 'light_module', 'texture', 'clothtexture.png')
    modelClass.setTexture("CLOTH", CLOTHTexturePath)
    CLOTHobjPath = os.path.join(current_dir, 'light_module', 'model', 'long_shirt_full.obj')
    modelClass.setMesh("CLOTH", CLOTHobjPath, render=True)
    applyTransform_settings = (3, (0.0, 0.0, 0.0), (0.0, 180.0, 0.0))
    modelClass.setSpaceChanger("CLOTH", applyTransform_settings)
    modelClass.setShader("CLOTH", "ENV_LIGHT", BACKFACE=False)

def setlighttest2(lightInfo, modelClass, current_dir):
    lightInfo.addPointlight("pointLight")

    light1_posx, light1_posy, light1_posz = 1.0, 2.0, 1.0

    pos = ti.Vector([light1_posx, light1_posy, light1_posz])
    col = ti.Vector([1.0, 1.0, 1.0])
    mtl = (0.2, 0.8, 1.0, 16)
    parm = (0.3, 0.09, 0.032)
    lightInfo.setPointInfo("pointLight", pos, col, mtl, parm)
    lightInfo.switch("pointLight", boolean=True)
    lightInfo.setTaichiInfo()

    modelClass.addModel("pointLight")
    light1TexturePath = os.path.join(current_dir, 'light_module', 'texture', 'gray.png')
    modelClass.setTexture("pointLight", light1TexturePath)
    light1objPath = os.path.join(current_dir, 'light_module', 'model', 'cube.obj')
    modelClass.setMesh("pointLight", light1objPath, render=True)
    applyTransform_settings = (0.05, (light1_posx, light1_posy, light1_posz), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("pointLight", applyTransform_settings)
    modelClass.setShader("pointLight", "NORMAL_NOLIGHT")

    lightInfo.addPointlight("multipointLight")

    light2_posx, light2_posy, light2_posz = -1.0, 2.0, 1.0

    pos = ti.Vector([light2_posx, light2_posy, light2_posz])
    col = ti.Vector([1.0, 1.0, 1.0])
    mtl = (0.2, 0.8, 1.0, 16)
    parm = (0.3, 0.09, 0.032)
    lightInfo.setPointInfo("multipointLight", pos, col, mtl, parm)
    lightInfo.switch("multipointLight", boolean=True)

    modelClass.addModel("multipointLight")
    light2TexturePath = os.path.join(current_dir, 'light_module', 'texture', 'gray.png')
    modelClass.setTexture("multipointLight", light2TexturePath)
    light2objPath = os.path.join(current_dir, 'light_module', 'model', 'cube.obj')
    modelClass.setMesh("multipointLight", light2objPath, render=True)
    applyTransform_settings = (0.05, (light2_posx, light2_posy, light2_posz), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("multipointLight", applyTransform_settings)
    modelClass.setShader("multipointLight", "NORMAL_NOLIGHT")

    lightInfo.addDirectlight("directLight")

    light3_posx, light3_posy, light3_posz = 0.0, 0.0, 1.0

    dir = ti.Vector([light3_posx, light3_posy, light3_posz])
    col = ti.Vector([1.0/255, 1.0/255, 1.0/255])
    mtl = (0.2, 0.8, 1.0, 16)
    lightInfo.setDirectInfo("directLight", dir, col, mtl)
    lightInfo.switch("directLight", boolean=True)
    lightInfo.setTaichiInfo()

    return ti.Vector([light1_posx, light1_posy, light1_posz,
                      light2_posx, light2_posy, light2_posz,
                      light3_posx, light3_posy, light3_posz])