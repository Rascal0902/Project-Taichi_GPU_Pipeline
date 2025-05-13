import os

def setModel5(modelClass, current_dir):
    modelClass.addModel("PLY")
    plyTexturePath = os.path.join(current_dir, 'light_module', 'texture', 'gray.png')
    modelClass.setTexture("PLY", plyTexturePath)
    plyPath = os.path.join(current_dir, 'light_module', 'model', 'mesh.ply')
    modelClass.setMesh("PLY", plyPath, render=True, ply=True)
    applyTransform_settings = (2, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    modelClass.setSpaceChanger("PLY", applyTransform_settings)
    modelClass.setShader("PLY", "PLY_ENV", N=1)