import sys
import numpy as np
from PIL import Image
import os

# Añadir el directorio del script al sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


import asyncio
from digitalimage import DigitalImage
from colortransfer import ColorTransfer
from linearization import LinearExponential
from grain_rendering import grain_interface
import halo

class ImageProcessor:
    
    def __init__(self):
        self.base_path = os.path.abspath(os.path.dirname(__file__))

    async def process_image(self, image_path: str, out_path: str):
        # Asegurarse de que las rutas sean absolutas
        image_path = os.path.abspath(image_path)
        out_path = os.path.abspath(out_path)
        output_dir = os.path.dirname(out_path)
        os.makedirs(output_dir, exist_ok=True)

        image_name, _ = os.path.split(image_path)[1].split('.')
        out_image_name, out_format = os.path.split(out_path)[1].split('.')

        # Validación del formato de salida
        if out_format not in ['PNG', 'png', 'TIFF', 'tiff']:
            raise Exception('Unavailable output format (Only png or tiff)')

        # Crear la instancia de DigitalImage
        digital_img = await asyncio.to_thread(DigitalImage, image_path, 2)

        # **Halation**
        print('Starting halation...')
        halated = await asyncio.to_thread(halo.add_halation, np.float32(digital_img.raw))
        print('Halation finished')

        # **Color Transfer**
        print('Color transferring...')
        transfer_function_path = os.path.join(self.base_path, "color_transfer_data/transfer_functions/TE226.ctf")
        TE226_ctf = await asyncio.to_thread(ColorTransfer.load, transfer_function_path)
        print('Color transferring finished')

        # **Linearization**
        print('Applying linearization function...')
        linearization_function_path = os.path.join(self.base_path, "color_transfer_data/linearization_functions/TE226.lfn")
        TE226_lfn = await asyncio.to_thread(LinearExponential.load, linearization_function_path)
        transferred = await asyncio.to_thread(TE226_ctf.apply, halated, TE226_lfn.apply_inv)
        print('Linearization finished')

        # **Guardado**
        print(f'Saving in {out_path}')
        if out_format in ['TIFF', 'tiff']:
            transferred_squeezed = np.squeeze(transferred)
            transferred_8bit = np.clip(transferred_squeezed * 255, 0, 255).astype(np.uint8)
            (await asyncio.to_thread(Image.fromarray, transferred_8bit)).save(out_path, format='TIFF')
        else:
            (await asyncio.to_thread(Image.fromarray, np.uint8(transferred * 255))).save(out_path)

        print('Process exited successfully.')
        return out_path


if __name__ == '__main__':

    image_path = sys.argv[1].replace('\\','/')
    image_name, _ = os.path.split(image_path)[1].split('.')
    out_path = sys.argv[2].replace('\\','/')
    out_image_name, out_format = os.path.split(out_path)[1].split('.')

    async def run():
        await ImageProcessor().process_image(image_path, out_path)
    
    asyncio.run(run())