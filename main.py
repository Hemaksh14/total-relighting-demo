# Import Statements
import os, shutil
import numpy as np
from PIL import Image
# Functions: Matting, Obj_placement, harmonization
from matting.getMatting import Matting
from object_placement.placement import place
from harmonization.main import get_harmonized

#Input : Foreground Image, Background Image
#Output : Harmonized Image
def main(foreground,background):
    if not os.path.exists('input'):
        os.makedirs('input')
    #Save foreground and background images to input dir as input/foreground.png and background.png
    foreground.save('input/foreground.png')
    background.save('input/background.png')
    if not os.path.exists('matting/pretrained'):
        os.mkdir('matting/pretrained')
        shutil.copy('/content/drive/MyDrive/total-relighting-demo/SGHM-ResNet50.pth','matting/pretrained')
    # Matting
    # Input: input/foreground.png
    # Output: output_matting/fg_mask.png
    #Matting(image_path='input/foreground.png')
    Matting()
    image = Image.open('input/foreground.png')
    sghm = Image.open('output_matting/fg_mask.png')
    image = np.asarray(image)
    if len(image.shape) == 2:
        image = image[:, :, None]
    if image.shape[2] == 1:
        image = np.repeat(image, 3, axis=2)
    elif image.shape[2] == 4:
        image = image[:, :, 0:3]
    sghm = np.repeat(np.asarray(sghm)[:, :, None], 3, axis=2) / 255
    foreground_sghm =  image * sghm
    #convert array to image
    foreground_sghm = Image.fromarray(foreground_sghm.astype('uint8'), 'RGB')
    foreground_sghm.save('output_matting/foreground.png')
    #Object Placement
    # Input: output_matting/foreground.png, input/background.png, output_matting/fg_mask.png
    # Output: output_object_placement/composite_image.png output_object_placement/composite_mask.png
    #place(foreground='output_matting/foreground.png',background='input/background.png',fg_mask='output_matting/fg_mask.png')
    os.mkdir('object_placement/result')
    os.mkdir('object_placement/result/graconet')
    os.mkdir('object_placement/result/graconet/models')
    shutil.copy('/content/drive/MyDrive/total-relighting-demo/11.pth','object_placement/result/graconet/models')
    place()
    #Harmonization
    # Input: output_object_placement/composite_image.png output_object_placement/composite_mask.png
    # Output: final/harmonized_image.png
    #harmonized_image = get_harmonized(composite_img='output_object_placement/composite_image.png',mask_img='output_object_placement/composite_mask.png')
    harmonized_image = get_harmonized()
    return harmonized_image

    

