import taichi as ti
import os

from light_module.Model import Model

##########################################################################################################
# ToDo model setting (more models in temp_setup.txt)

def setModel(modelClass, current_dir):
    modelClass.addModel("SMPL")
    SMPLTexturePath = os.path.join(current_dir, 'light_module', 'texture', 'gray.png')
    modelClass.setTexture("SMPL", SMPLTexturePath)
    SMPLobjPath = os.path.join(current_dir, 'light_module', 'model', 'smpl_flipped_normal.obj')
    modelClass.setMesh("SMPL", SMPLobjPath, render=True)
    applyTransform_settings = (0.5, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("SMPL", applyTransform_settings)
    modelClass.setShader("SMPL", "HUMAN")

    modelClass.addModel("UPCLOTH1")
    UPCLOTH1TexturePath = os.path.join(current_dir, 'light_module', 'texture', 'clothtexture.png')
    modelClass.setTexture("UPCLOTH1", UPCLOTH1TexturePath)
    UPCLOTH1objPath = os.path.join(current_dir, 'light_module', 'model', 'tshirt_full.obj')
    modelClass.setMesh("UPCLOTH1", UPCLOTH1objPath, render=False)
    applyTransform_settings = (0.5, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("UPCLOTH1", applyTransform_settings)
    modelClass.setShader("UPCLOTH1", "ENV_LIGHT", N=3)

    modelClass.addModel("UPCLOTH2")
    UPCLOTH2TexturePath = os.path.join(current_dir, 'light_module', 'texture', 'gray.png')
    modelClass.setTexture("UPCLOTH2", UPCLOTH2TexturePath)
    UPCLOTH2objPath = os.path.join(current_dir, 'light_module', 'model', 'tshirt_full.obj')
    modelClass.setMesh("UPCLOTH2", UPCLOTH2objPath, render=False)
    applyTransform_settings = (0.5, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("UPCLOTH2", applyTransform_settings)
    modelClass.setShader("UPCLOTH2", "ENV_LIGHT", N=3)

    modelClass.addModel("UPCLOTH3")
    UPCLOTH3TexturePath = os.path.join(current_dir, 'light_module', 'texture', 'purple.png')
    modelClass.setTexture("UPCLOTH3", UPCLOTH3TexturePath)
    UPCLOTH3objPath = os.path.join(current_dir, 'light_module', 'model', 'tshirt_full.obj')
    modelClass.setMesh("UPCLOTH3", UPCLOTH3objPath, render=False)
    applyTransform_settings = (0.5, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("UPCLOTH3", applyTransform_settings)
    modelClass.setShader("UPCLOTH3", "ENV_LIGHT", N=3)

    modelClass.addModel("DOWNCLOTH1")
    DOWNCLOTH1TexturePath = os.path.join(current_dir, 'light_module', 'texture', 'clothtexture.png')
    modelClass.setTexture("DOWNCLOTH1", DOWNCLOTH1TexturePath)
    DOWNCLOTH1objPath = os.path.join(current_dir, 'light_module', 'model', 'pants_full.obj')
    modelClass.setMesh("DOWNCLOTH1", DOWNCLOTH1objPath, render=False)
    applyTransform_settings = (0.5, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("DOWNCLOTH1", applyTransform_settings)
    modelClass.setShader("DOWNCLOTH1", "ENV_LIGHT", N=3)

    modelClass.addModel("DOWNCLOTH2")
    DOWNCLOTH2TexturePath = os.path.join(current_dir, 'light_module', 'texture', 'gray.png')
    modelClass.setTexture("DOWNCLOTH2", DOWNCLOTH2TexturePath)
    DOWNCLOTH2objPath = os.path.join(current_dir, 'light_module', 'model', 'pants_full.obj')
    modelClass.setMesh("DOWNCLOTH2", DOWNCLOTH2objPath, render=False)
    applyTransform_settings = (0.5, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("DOWNCLOTH2", applyTransform_settings)
    modelClass.setShader("DOWNCLOTH2", "ENV_LIGHT", N=3)

    modelClass.addModel("DOWNCLOTH3")
    DOWNCLOTH3TexturePath = os.path.join(current_dir, 'light_module', 'texture', 'purple.png')
    modelClass.setTexture("DOWNCLOTH3", DOWNCLOTH3TexturePath)
    DOWNCLOTH3objPath = os.path.join(current_dir, 'light_module', 'model', 'pants_full.obj')
    modelClass.setMesh("DOWNCLOTH3", DOWNCLOTH3objPath, render=False)
    applyTransform_settings = (0.5, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("DOWNCLOTH3", applyTransform_settings)
    modelClass.setShader("DOWNCLOTH3", "ENV_LIGHT", N=3)

    modelClass.addModel("JACKETCLOTH1")
    JACKETCLOTH1TexturePath = os.path.join(current_dir, 'light_module', 'texture', 'clothtexture.png')
    modelClass.setTexture("JACKETCLOTH1", JACKETCLOTH1TexturePath)
    JACKETCLOTH1objPath = os.path.join(current_dir, 'light_module', 'model', 'long_shirt_full.obj')
    modelClass.setMesh("JACKETCLOTH1", JACKETCLOTH1objPath, render=False)
    applyTransform_settings = (0.5, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("JACKETCLOTH1", applyTransform_settings)
    modelClass.setShader("JACKETCLOTH1", "ENV_LIGHT", N=3)

    modelClass.addModel("JACKETCLOTH2")
    JACKETCLOTH2TexturePath = os.path.join(current_dir, 'light_module', 'texture', 'gray.png')
    modelClass.setTexture("JACKETCLOTH2", JACKETCLOTH2TexturePath)
    JACKETCLOTH2objPath = os.path.join(current_dir, 'light_module', 'model', 'long_shirt_full.obj')
    modelClass.setMesh("JACKETCLOTH2", JACKETCLOTH2objPath, render=False)
    applyTransform_settings = (0.5, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("JACKETCLOTH2", applyTransform_settings)
    modelClass.setShader("JACKETCLOTH2", "ENV_LIGHT", N=3)

    modelClass.addModel("JACKETCLOTH3")
    JACKETCLOTH3TexturePath = os.path.join(current_dir, 'light_module', 'texture', 'purple.png')
    modelClass.setTexture("JACKETCLOTH3", JACKETCLOTH3TexturePath)
    JACKETCLOTH3objPath = os.path.join(current_dir, 'light_module', 'model', 'long_shirt_full.obj')
    modelClass.setMesh("JACKETCLOTH3", JACKETCLOTH3objPath, render=False)
    applyTransform_settings = (0.5, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("JACKETCLOTH3", applyTransform_settings)
    modelClass.setShader("JACKETCLOTH3", "ENV_LIGHT", N=3)

#########################################################################################################
# ToDo Light setting


def setlighttest(lightInfo, modelClass, current_dir):
    lightInfo.addPointlight("pointLight")

    light1_posx, light1_posy, light1_posz = 1.0, 2.0, -3.5

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
    modelClass.setMesh("pointLight", light1objPath, render=False)
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
    modelClass.setMesh("multipointLight", light2objPath, render=False)
    applyTransform_settings = (0.05, (light2_posx, light2_posy, light2_posz), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("multipointLight", applyTransform_settings)
    modelClass.setShader("multipointLight", "NORMAL_NOLIGHT")

    lightInfo.addDirectlight("directLight")

    light3_posx, light3_posy, light3_posz = 0.0, 0.0, 1.0

    dir = ti.Vector([light3_posx, light3_posy, light3_posz])
    col = ti.Vector([1.0 / 255, 1.0 / 255, 1.0 / 255])
    mtl = (0.2, 0.8, 1.0, 16)
    lightInfo.setDirectInfo("directLight", dir, col, mtl)
    lightInfo.switch("directLight", boolean=True)
    lightInfo.setTaichiInfo()

    return ti.Vector([light1_posx, light1_posy, light1_posz,
                      light2_posx, light2_posy, light2_posz,
                      light3_posx, light3_posy, light3_posz])


def setlight(lightInfo, N=3):
    dir = ti.Vector([0.0, 0.0, 1.0])
    col = ti.Vector([1.0, 1.0, 1.0])
    mtl = (0.03, 0.02, 0.7, 16)

    for i in range(N):
        lightInfo.addDirectlight("Direct" + str(i))
        lightInfo.setDirectInfo("Direct" + str(i), dir, col, mtl)
        lightInfo.switch("Direct" + str(i), boolean=True)

    lightInfo.setTaichiInfo()


def updatelighttest(modelClass, lightInfo, light1_posx, light1_posy, light1_posz, light2_posx, light2_posy, light2_posz,
                    light3_posx, light3_posy, light3_posz):
    applyTransform_settings = (0.05, (light1_posx, light1_posy, light1_posz), (0.0, 0.0, 0.0))
    modelClass.updatespace("pointLight", applyTransform_settings)
    pos = ti.Vector([light1_posx, light1_posy, light1_posz])
    lightInfo.updateposition("pointLight", pos)
    applyTransform_settings = (0.05, (light2_posx, light2_posy, light2_posz), (0.0, 0.0, 0.0))
    modelClass.updatespace("multipointLight", applyTransform_settings)
    pos = ti.Vector([light2_posx, light2_posy, light2_posz])
    lightInfo.updateposition("multipointLight", pos)

    dir = ti.Vector([light3_posx, light3_posy, light3_posz])
    lightInfo.updatedirection("directLight", dir)


def updatelight(lightInfo, pred_l, pred_c, N=3):
    for i in range(N):
        dir = ti.Vector([pred_l[i * 3].item(), pred_l[i * 3 + 1].item(), pred_l[i * 3 + 2].item()])
        # col = ti.Vector([pred_c[i*3].item(), pred_c[i*3+1].item(), pred_c[i*3+2].item()])
        col = ti.Vector([1.0 / 255, 1.0 / 255, 1.0 / 255])
        lightInfo.updatedirection("Direct" + str(i), dir, N=N)
        lightInfo.updateddircolor("Direct" + str(i), col, N=N)

def updatemesh(modelClass, ui, verts):
    modelClass.updateMeshHard("SMPL", None, verts, None, MODE='VTON')
    if ui.UPcloth_selected != 3:
        for i in range(1, 4):
            if i == ui.UPcloth_selected + 1:
                Model.model["UPCLOTH" + str(i)]["mesh"].obj_render(True)
            else:
                Model.model["UPCLOTH" + str(i)]["mesh"].obj_render(False)
        modelClass.updateMeshHard("UPCLOTH" + str(ui.UPcloth_selected + 1), None, ui.upvertices, None, MODE='VTON')
    else:
        for i in range(1, 4):
            Model.model["UPCLOTH" + str(i)]["mesh"].obj_render(False)
    if ui.DOWNcloth_selected != 3:
        for i in range(1, 4):
            if i == ui.DOWNcloth_selected + 1:
                Model.model["DOWNCLOTH" + str(i)]["mesh"].obj_render(True)
            else:
                Model.model["DOWNCLOTH" + str(i)]["mesh"].obj_render(False)
        modelClass.updateMeshHard("DOWNCLOTH" + str(ui.DOWNcloth_selected + 1), None, ui.downvertices, None,
                                  MODE='VTON')
    else:
        for i in range(1, 4):
            Model.model["DOWNCLOTH" + str(i)]["mesh"].obj_render(False)
    if ui.JACKETcloth_selected != 3:
        for i in range(1, 4):
            if i == ui.JACKETcloth_selected + 1:
                Model.model["JACKETCLOTH" + str(i)]["mesh"].obj_render(True)
            else:
                Model.model["JACKETCLOTH" + str(i)]["mesh"].obj_render(False)
        modelClass.updateMeshHard("JACKETCLOTH" + str(ui.JACKETcloth_selected + 1), None, ui.jacketvertices, None,
                                  MODE='VTON')
    else:
        for i in range(1, 4):
            Model.model["JACKETCLOTH" + str(i)]["mesh"].obj_render(False)