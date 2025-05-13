# Lighting Clothes

Lighting Clothes in VTON Project

## [Project Page](https://github.com/Rascal0902/Project-Taichi_GPU_Pipeline)

<p align="center">
    <img src="docs/scene4.gif">
    <br>
    <sup>environment map ball</sup>
    <br>
</p>

## News 
*2024/10/26 branch has made*

*2024/11/8 lighting demo has made*

*2024/12/24 environment map is applied*

## How to generate SSH keys and clone the project

1. Go to Settings -> SSH and GPG keys in your github page

2. Press New SSH key button 

3. Open the terminal and follow commends
   
    ```
    ssh-keygen
    cat /home/[username]/.ssh/id_rsa.pub
    ```
5. copy the key and paste the key in Add new SSH Key -> Key 

6. clone the project
   
    ```
    git clone git@github.com:medialab-ku/VTON.git
    ```
    
## How to Install Pycharm in linux

1. Go to [Download](https://www.jetbrains.com/ko-kr/pycharm/download/?section=linux) and download .tar.gz(Linux)

2. Go to Download folder and Open the terminal, follow the command below

    ```
    sudo tar -zxvf pycharm-professional-****.**.*.tar.gz
    cd pycharm-****-**-*/bin
    sh pycharm.sh
    ```
    
3. Get license in [link](https://www.jetbrains.com/ko-kr/community/education/#students)

4. put license in pycharm and open the editor

5. optional : Click Tools -> Create Desktop entry then you can make Desktop shortcut for pycharm 

# How to Run

## 0. Prerequisites

1. github repository should be cloned to your computer

## 1. Download anaconda

    sudo apt update
    sudo apt install curl -y
    curl --output anaconda.sh https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
    sha256sum anaconda.sh
    bash anaconda.sh
    sudo vi ~/.bashrc

    #Instert at buttom and press :wq
    export PATH=~/anaconda3/bin:~/anaconda3/condabin:$PATH

    source ~/.bashrc

    #check
    conda -V

## 2. Create conda environment using either terminal or pycharm

### conda
    conda env create -f environment.yaml
    conda activate vton

### conda environment export (Optional for who wants to save settings)
    conda env export > environment.yaml

### pycharm
1. Open MEDIA_learn project using pycharm, enter settings(Files->Settings, or ctrl+alt+S)
2. Click Add Interpreter, Add Local Interpreter, Conda Environment, Create new environment and set python version to 3.10
3. Open terminal(button on the bottom left), type in 'conda activate "Your_Environment_Name"', and continue the following instructions on the terminal.

## 3. Run the project

    python lighting.py