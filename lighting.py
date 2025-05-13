import taichi as ti
import subprocess
import imgui
import torch
import time
import cv2
import os

from light_module.Model import Model, Modelrender
from light_module.LightComponent import LightComponent
from light_module.imgui_coord import Util
from light_module.util import clear_folder, diffusion_preprocessing

from light_module.Gardner2019.EvalTest import Validation
from light_module.Gardner2019.util import cv2_to_PIL

from lightingsetup import setModel, setlighttest, setlight, updatelighttest, updatelight

from scene.scene1_phong import setModel1
from scene.scene2_env_map import setModel2, setlighttest2
from scene.scene3_scaled_env_map import setModel3
from scene.scene4_env_ball import setModel4
from scene.scene5_ply import setModel5


def get_frame(is_test):
    if is_test:
        img = cv2.imread('light_module/sample_images/5.jpg', cv2.IMREAD_COLOR)
        cv2.imshow('Sample', img)
        return img
    else:
        _ret, _frame = cap.read()
        _frame = cv2.flip(_frame, 1)
        cv2.imshow('Webcam', _frame)
        if not _ret:
            raise RuntimeError("Can not read frame")
        else:
            return _frame


ti.init(kernel_profiler=True, arch=ti.cuda, device_memory_GB=6)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

N = 10

Scene = 5

# Lighting setup
GardnerEval = False
DiffusionEval = False
DemoLight = True

Nocam = True
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Can not open camera.")
else:
    print("Camera is open.")

if GardnerEval:
    ckpt_path = 'light_module/Gardner2019/ckpt/checkpoint.pt'
    light_model = Validation(ckpt_path, N=N, MODE="MIX")

# taichi ui setting
window = ti.ui.Window("Lighting", (1000, 1000), fps_limit=200)
gui = window.get_gui()
canvas = window.get_canvas()
canvas.set_background_color((1, 1, 1))
scene = window.get_scene()
camera = ti.ui.Camera()
camera.position(0.0, 0.0, 10.0)

current_dir = os.path.dirname(os.path.abspath(__file__))

modelClass = Model(camera, window.get_window_shape())

if DiffusionEval:
    __frame = get_frame(Nocam)
    __Image = cv2_to_PIL(__frame)
    Image_path = os.path.join(current_dir, 'light_module', 'diffusion', 'inputs', 'cam.png')
    clear_path = os.path.join(current_dir, 'light_module', 'diffusion', 'outputs')
    clear_folder(clear_path)

    diffusion_preprocessing(Image_path, __Image)

    if os.path.exists(Image_path):
        preprocess = subprocess.Popen(['python', 'light_module/diffusion/evalTest.py'])
        preprocess.wait()

        out_path = os.path.join(clear_path, 'envmap', 'cam_ev-00.png')
        if os.path.exists(out_path):
            modelClass.initialize_env_map(current_dir, filename='cam_ev-00.png', Diffusion=True)
        else:
            print("!!!!out of memory!!!!")
            modelClass.initialize_env_map(current_dir, filename='whiteTexture.png')
    else:
        modelClass.initialize_env_map(current_dir, filename='whiteTexture.png')

else:
    modelClass.initialize_env_map(current_dir, filename='gardner3.png')

if Scene == 0:
    setModel(modelClass, current_dir)
elif Scene == 1:
    setModel1(modelClass, current_dir)
elif Scene == 2:
    setModel2(modelClass, current_dir)
elif Scene == 3:
    setModel3(modelClass, current_dir)
elif Scene == 4:
    setModel4(modelClass, current_dir)
elif Scene == 5:
    setModel5(modelClass, current_dir)

lightInfo = LightComponent()

if GardnerEval:
    setlight(lightInfo, N=N)
if DemoLight or DiffusionEval or Scene == 1 or Scene == 3 or Scene == 4:
    lightposition = setlighttest(lightInfo, modelClass, current_dir)
if Scene == 2:
    lightposition = setlighttest2(lightInfo, modelClass, current_dir)

imgui.create_context()
io = imgui.get_io()
io.fonts.add_font_default()
io.fonts.get_tex_data_as_rgba32()

width, height = window.get_window_shape()
imgui.get_io().display_size = (width, height)

###########################################################
# ToDo test environment no VTON

# imgui default setting
posx, posy, posz = 0.0, 0.0, 0.0
cam_posx, cam_posy, cam_posz = 0.0, 2.0, -10.0
size = 1
ispointchecked = False
iscoordchecked = False

# point, coordinate setup
util = Util()
temp = util.renderingtestSetup(camera, width, height)
fieldpoint = ti.Vector.field(2, dtype=ti.f32, shape=1)
fieldcoord = ti.Vector.field(2, dtype=ti.f32, shape=2)
fieldedge = ti.Vector.field(2, dtype=ti.i32, shape=1)
###########################################################

frame = get_frame(Nocam)
start_time = time.time()
step = 0.07
start = False

# running
while window.running:
    #######################################################################
    # ToDo test environment CHANGE little in VTON
    imgui.new_frame()
    with gui.sub_window("Setup Imgui", 0.7, 0, 0.3, 0.6) as g:
        g.text("Model setup")
        g.text("")
        posx = g.slider_float("posx", posx, -1.0, 1.0)
        posy = g.slider_float("posy", posy, -1.0, 1.0)
        posz = g.slider_float("posz", posz, -1.0, 1.0)
        g.text("")
        size = g.slider_float("size", size, 0.1, 10.0)
        g.text("")
        cam_posx = g.slider_float("cam_posx", cam_posx, -20.0, 20.0)
        cam_posy = g.slider_float("cam_posy", cam_posy, -20.0, 20.0)
        cam_posz = g.slider_float("cam_posz", cam_posz, -20.0, 20.0)
        g.text("")
        if DemoLight or DiffusionEval or Scene != 0:
            lightposition[0] = g.slider_float("light1_posx", lightposition[0], -5.0, 5.0)
            lightposition[1] = g.slider_float("light1_posy", lightposition[1], -5.0, 5.0)
            lightposition[2] = g.slider_float("light1_posz", lightposition[2], -5.0, 5.0)
            g.text("")
            lightposition[3] = g.slider_float("light2_posx", lightposition[3], -5.0, 5.0)
            lightposition[4] = g.slider_float("light2_posy", lightposition[4], -5.0, 5.0)
            lightposition[5] = g.slider_float("light2_posz", lightposition[5], -5.0, 5.0)
            g.text("")
            lightposition[6] = g.slider_float("light3_posx", lightposition[6], -5.0, 5.0)
            lightposition[7] = g.slider_float("light3_posy", lightposition[7], -5.0, 5.0)
            lightposition[8] = g.slider_float("light3_posz", lightposition[8], -5.0, 5.0)
            g.text("")
        ispointchecked = g.checkbox("point", ispointchecked)
        iscoordchecked = g.checkbox("coordinate", iscoordchecked)
    imgui.render()
    #######################################################################

    # Camera
    camera.track_user_inputs(window)

    #############################################
    # ToDo Camera position no VTON
    camera.position(cam_posx, cam_posy, cam_posz)
    #############################################

    camera.lookat(0.0, 0.0, 0.0)
    scene.set_camera(camera)

    if time.time() - start_time > step:
        __frame = get_frame(Nocam)
        __Image = cv2_to_PIL(__frame)
        if GardnerEval:
            _, pred_l, _, pred_c, _ = light_model.eval_param(__Image, PRINT=False)
        start = True

        cv2.waitKey(1)
        start_time = time.time()

    ############################################################################################
    # ToDo test environment little in VTON
    # update_mesh
    # NEWCUBEobjPath = os.path.join(current_dir, 'light_module', 'model', 'movecube.obj')
    # modelClass.updateMeshHard("CUBE", NEWCUBEobjPath, None, None, MODE='LIGHT')

    # update mesh setting
    if Scene == 0:
        applyTransform_settings = (size * 2, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
        modelClass.updatespace("SMPL", applyTransform_settings)

    if Scene == 4:
        applyTransform_settings = (size * 2, (posx, posy, posz), (0.0, 0.0, 0.0))
        modelClass.updatespace("SPHERE", applyTransform_settings)

    if Scene == 5:
        applyTransform_settings = (size * 2, (posx, posy, posz), (0.0, 0.0, 0.0))
        modelClass.updatespace("PLY", applyTransform_settings)
    ############################################################################################

    if start:
        if GardnerEval:
            updatelight(lightInfo, pred_l[0], pred_c[0], N)
        if DemoLight or DiffusionEval or Scene != 0:
            updatelighttest(modelClass, lightInfo, lightposition[0], lightposition[1], lightposition[2],
                            lightposition[3], lightposition[4], lightposition[5],
                            lightposition[6], lightposition[7], lightposition[8])

    cam_pos = (cam_posx, cam_posy, cam_posz)

    # Model render
    Modelrender(canvas, camera, cam_pos)

    ########################################################################################
    # ToDo test environment no VTON
    # imgui render
    if ispointchecked:
        util.displayPoint(posx, posy, posz, temp, width, height, canvas, fieldpoint, camera)
    if iscoordchecked:
        util.displayCoordinate(temp, width, height, canvas, fieldcoord, fieldedge, camera)
    ########################################################################################

    # canvas render
    canvas.scene(scene)
    imgui.render()
    window.show()

cv2.destroyAllWindows()
