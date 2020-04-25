from unittest import TestCase
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import plxr
import adios2

class TestWriteReadPng(TestCase):

    def test_single_step(self):

        # Create a mpl figure
        x = np.arange(0.0, 2, 0.01)
        y1 = np.sin(2 * np.pi * x)
        y2 = 1.2 * np.sin(4 * np.pi * x)

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

        ax1.fill_between(x, 0, y1)
        ax1.set_ylabel('between y1 and 0')

        ax2.fill_between(x, y1, 1)
        ax2.set_ylabel('between y1 and 1')

        ax3.fill_between(x, y1, y2)
        ax3.set_ylabel('between y1 and y2')
        ax3.set_xlabel('x')

#        # load some image data
#        img = Image.open ("{}/images/simple-3x3-1.png".format(os.path.dirname(os.path.abspath(__file__)))).convert("RGB")
#        pngPixels = list(img.getdata())


        # test writing
        with adios2.open("test_mpl.bp", "w") as fh:
            plxr.write_png_image_from_matplotlib (fh, fig, 'test_image')
#            plxr.write_png_image (fh, img, 'test_image')

        # test reading
        with adios2.open("test_mpl.bp", "r") as fh:
            rimg = plxr.read_image (fh, 'test_image', 0)
            readPixels = list(rimg.getdata())

            # Compare pixels to original
#            self.assertEqual (pngPixels, readPixels)

    def test_multiple_steps(self):

        # load some image data
        img1 = Image.open ("{}/images/simple-3x3-1.png".format(os.path.dirname(os.path.abspath(__file__)))).convert("RGB")
        pngPixels1 = list(img1.getdata())
        img2 = Image.open ("{}/images/simple-3x3-2.png".format(os.path.dirname(os.path.abspath(__file__)))).convert("RGB")
        pngPixels2 = list(img2.getdata())
        img3 = Image.open ("{}/images/simple-3x3-3.png".format(os.path.dirname(os.path.abspath(__file__)))).convert("RGB")
        pngPixels3 = list(img3.getdata())
        img4 = Image.open ("{}/images/simple-3x3-4.png".format(os.path.dirname(os.path.abspath(__file__)))).convert("RGB")
        pngPixels4 = list(img4.getdata())


        # test writing
        with adios2.open("test_mpl_multiple.bp", "w") as fh:
            plxr.write_png_image (fh, img1, 'test_image')
            plxr.write_png_image (fh, img2, 'test_image')
            plxr.write_png_image (fh, img3, 'test_image')
            plxr.write_png_image (fh, img4, 'test_image')


        # test reading
        with adios2.open("test_mpl_multiple.bp", "r") as fh:
            rimg1 = plxr.read_image (fh, 'test_image', 0)
            readPixels1 = list(rimg1.getdata())
        with adios2.open("test_mpl_multiple.bp", "r") as fh:
            rimg2 = plxr.read_image (fh, 'test_image', 1)
            readPixels2 = list(rimg2.getdata())
        with adios2.open("test_mpl_multiple.bp", "r") as fh:
            rimg3 = plxr.read_image (fh, 'test_image', 2)
            readPixels3 = list(rimg3.getdata())
        with adios2.open("test_mpl_multiple.bp", "r") as fh:
            rimg4 = plxr.read_image (fh, 'test_image', 3)
            readPixels4 = list(rimg4.getdata())

            # Compare pixels to original
            self.assertEqual (pngPixels1, readPixels1)
            self.assertEqual (pngPixels2, readPixels2)
            self.assertEqual (pngPixels3, readPixels3)
            self.assertEqual (pngPixels4, readPixels4)

    def test_multiple_steps_with_append(self):

        # load some image data
        img1 = Image.open ("{}/images/simple-3x3-1.png".format(os.path.dirname(os.path.abspath(__file__)))).convert("RGB")
        pngPixels1 = list(img1.getdata())
        img2 = Image.open ("{}/images/simple-3x3-2.png".format(os.path.dirname(os.path.abspath(__file__)))).convert("RGB")
        pngPixels2 = list(img2.getdata())
        img3 = Image.open ("{}/images/simple-3x3-3.png".format(os.path.dirname(os.path.abspath(__file__)))).convert("RGB")
        pngPixels3 = list(img3.getdata())
        img4 = Image.open ("{}/images/simple-3x3-4.png".format(os.path.dirname(os.path.abspath(__file__)))).convert("RGB")
        pngPixels4 = list(img4.getdata())


        # test writing using separate opens
        with adios2.open("test_mpl_multiple.bp", "w") as fh:
            plxr.write_png_image (fh, img1, 'test_image')
        with adios2.open("test_mpl_multiple.bp", "a") as fh:
            plxr.write_png_image (fh, img2, 'test_image')
        with adios2.open("test_mpl_multiple.bp", "a") as fh:
            plxr.write_png_image (fh, img3, 'test_image')
        with adios2.open("test_mpl_multiple.bp", "a") as fh:
            plxr.write_png_image (fh, img4, 'test_image')


        # test reading
        with adios2.open("test_mpl_multiple.bp", "r") as fh:
            rimg1 = plxr.read_image (fh, 'test_image', 0)
            readPixels1 = list(rimg1.getdata())
        with adios2.open("test_mpl_multiple.bp", "r") as fh:
            rimg2 = plxr.read_image (fh, 'test_image', 1)
            readPixels2 = list(rimg2.getdata())
        with adios2.open("test_mpl_multiple.bp", "r") as fh:
            rimg3 = plxr.read_image (fh, 'test_image', 2)
            readPixels3 = list(rimg3.getdata())
        with adios2.open("test_mpl_multiple.bp", "r") as fh:
            rimg4 = plxr.read_image (fh, 'test_image', 3)
            readPixels4 = list(rimg4.getdata())

            # Compare pixels to original
            self.assertEqual (pngPixels1, readPixels1)
            self.assertEqual (pngPixels2, readPixels2)
            self.assertEqual (pngPixels3, readPixels3)
            self.assertEqual (pngPixels4, readPixels4)


