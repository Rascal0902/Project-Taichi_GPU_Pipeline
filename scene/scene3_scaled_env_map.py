import os

def setModel3(modelClass, current_dir):
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
    modelClass.setMesh("CLOTH", CLOTHobjPath, render=False)
    applyTransform_settings = (3, (0.0, 0.0, 0.0), (0.0, 180.0, 0.0))
    modelClass.setSpaceChanger("CLOTH", applyTransform_settings)
    modelClass.setShader("CLOTH", "ENV_LIGHT", N=1.4, BACKFACE=False)

