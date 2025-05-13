import os

def setModel4(modelClass, current_dir):
    modelClass.addModel("SMPL")
    SMPLTexturePath = os.path.join(current_dir, 'light_module', 'texture', 'gray.png')
    modelClass.setTexture("SMPL", SMPLTexturePath)
    SMPLobjPath = os.path.join(current_dir, 'light_module', 'model', 'SMPL_TPose.obj')
    modelClass.setMesh("SMPL", SMPLobjPath, render=False)
    applyTransform_settings = (3, (0.0, 0.0, 0.0), (0.0, 180.0, 0.0))
    modelClass.setSpaceChanger("SMPL", applyTransform_settings)
    # modelClass.setShader("SMPL", "HUMAN")
    modelClass.setShader("SMPL", "ENV_LIGHT", N=1)

    modelClass.addModel("SPHERE")
    CUBETexturePath = os.path.join(current_dir, 'light_module', 'texture', 'whiteTexture.png')
    modelClass.setTexture("SPHERE", CUBETexturePath)
    CUBEobjPath = os.path.join(current_dir, 'light_module', 'model', 'sphere.obj')
    modelClass.setMesh("SPHERE", CUBEobjPath, render=True)
    applyTransform_settings = (1, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("SPHERE", applyTransform_settings)
    modelClass.setShader("SPHERE", "ENV_LIGHT", N=1)
    # modelClass.setShader("SPHERE", "NORMAL_LIGHT")