from unittest import TestCase
from PIL import Image
import os
import plxr
import adios2

class TestWriteReadPng(TestCase):

    def test_single_step(self):

        # load some image data
        img = Image.open ("{}/images/simple-3x3-1.png".format(os.path.dirname(os.path.abspath(__file__)))).convert("RGB")
        pngPixels = list(img.getdata())


        # test writing
        with adios2.open("test_simple.bp", "w") as fh:
            plxr.write_png_image (fh, img, 'test_image')

        # test reading
        with adios2.open("test_simple.bp", "r") as fh:
            rimg = plxr.read_image (fh, 'test_image', 0)
            readPixels = list(rimg.getdata())

            # Compare pixels to original
            self.assertEqual (pngPixels, readPixels)


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
        with adios2.open("test_simple.bp", "w") as fh:
            plxr.write_png_image (fh, img1, 'test_image')
            plxr.write_png_image (fh, img2, 'test_image')
            plxr.write_png_image (fh, img3, 'test_image')
            plxr.write_png_image (fh, img4, 'test_image')


        # test reading
        with adios2.open("test_simple.bp", "r") as fh:
            rimg1 = plxr.read_image (fh, 'test_image', 0)
            readPixels1 = list(rimg1.getdata())
        with adios2.open("test_simple.bp", "r") as fh:
            rimg2 = plxr.read_image (fh, 'test_image', 1)
            readPixels2 = list(rimg2.getdata())
        with adios2.open("test_simple.bp", "r") as fh:
            rimg3 = plxr.read_image (fh, 'test_image', 2)
            readPixels3 = list(rimg3.getdata())
        with adios2.open("test_simple.bp", "r") as fh:
            rimg4 = plxr.read_image (fh, 'test_image', 3)
            readPixels4 = list(rimg4.getdata())

            # Compare pixels to original
            self.assertEqual (pngPixels1, readPixels1)
            self.assertEqual (pngPixels2, readPixels2)
            self.assertEqual (pngPixels3, readPixels3)
            self.assertEqual (pngPixels4, readPixels4)

