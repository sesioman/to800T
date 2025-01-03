import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from digitalimage import DigitalImage
from colortransfer import ColorTransfer
from linearization import LinearExponential
from grain_rendering import grain_interface
import halo

import sys
import os


if len(sys.argv) < 3:
    raise Exception("Not enough arguments: emulation <input-path> <output-path>")

image_path = sys.argv[1].replace('\\','/')
image_name, _ = os.path.split(image_path)[1].split('.')
out_path = sys.argv[2].replace('\\','/')
out_image_name, out_format = os.path.split(out_path)[1].split('.')

# print(image_path,image_name,out_path, out_image_name, out_format)

if out_format not in ['PNG', 'png', 'TIFF', 'tiff']:
    raise Exception('Unavailable output format (Only png or tiff)')


digital_img = DigitalImage(image_path, 2)
# Halation
print('Starting halation...')
halated = halo.add_halation(np.float32(digital_img.raw))
print('Halation finished')


# import color transfer function
print('Color transfering...')
TE226_ctf = ColorTransfer.load("color_transfer_data/transfer_functions/TE226.ctf")
print('Color transfering finished')


# import linearization function
print('Applying linearization function...')
TE226_lfn = LinearExponential.load("color_transfer_data/linearization_functions/TE226.lfn")
# should take around 15s
transferred = TE226_ctf.apply(halated, TE226_lfn.apply_inv)
print('Linearization finished')
# Save

print('Saving in {}'.format(out_path))
if out_format in ['TIFF', 'tiff']:
    # Asegúrate de que transferred tenga la forma correcta
    transferred_squeezed = np.squeeze(transferred)

    # Convertir a 8 bits para Pillow
    transferred_8bit = np.clip(transferred_squeezed * 255, 0, 255).astype(np.uint8)

    # Guardar como TIFF
    Image.fromarray(transferred_8bit).save(out_path, format='TIFF')
    
else:
    Image.fromarray(np.uint8(transferred*255)).save(out_path)

print('Process exited succesfully.')