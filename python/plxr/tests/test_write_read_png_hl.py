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
            plxr.write_png_image_hl (fh, img, 'test_image', end_step=True)

        # test reading
        step = 0
        with adios2.open("test_simple.bp", "r") as fh:
            for ad_step in fh:
                self.assertEqual (step, 0)
                rimg = plxr.read_image_hl (ad_step, 'test_image')
                readPixels = list(rimg.getdata())

                # Compare pixels to original
                self.assertEqual (pngPixels, readPixels)
                step=step+1


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
        with adios2.open("test_multiple.bp", "w") as fh:
            plxr.write_png_image_hl (fh, img1, 'test_image', end_step=True)
            plxr.write_png_image_hl (fh, img2, 'test_image', end_step=True)
            plxr.write_png_image_hl (fh, img3, 'test_image', end_step=True)
            plxr.write_png_image_hl (fh, img4, 'test_image', end_step=True)


        # test reading
        readPixels = []
        with adios2.open("test_multiple.bp", "r") as fh:
            for ad_step in fh:
                rimg = plxr.read_image_hl (ad_step, 'test_image')
                readPixels.append(list(rimg.getdata()) )

            # Compare pixels to original
            self.assertEqual (pngPixels1, readPixels[0])
            self.assertEqual (pngPixels2, readPixels[1])
            self.assertEqual (pngPixels3, readPixels[2])
            self.assertEqual (pngPixels4, readPixels[3])

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


        # test writing
        with adios2.open("test_multiple.bp", "w") as fh:
            plxr.write_png_image_hl (fh, img1, 'test_image', end_step=True)
        with adios2.open("test_multiple.bp", "a") as fh:
            plxr.write_png_image_hl (fh, img2, 'test_image', end_step=True)
        with adios2.open("test_multiple.bp", "a") as fh:
            plxr.write_png_image_hl (fh, img3, 'test_image', end_step=True)
        with adios2.open("test_multiple.bp", "a") as fh:
            plxr.write_png_image_hl (fh, img4, 'test_image', end_step=True)


        # test reading
        readPixels = []
        with adios2.open("test_multiple.bp", "r") as fh:
            for ad_step in fh:
                rimg = plxr.read_image_hl (ad_step, 'test_image')
                readPixels.append(list(rimg.getdata()) )


            # Compare pixels to original
            self.assertEqual (pngPixels1, readPixels[0])
            self.assertEqual (pngPixels2, readPixels[1])
            self.assertEqual (pngPixels3, readPixels[2])
            self.assertEqual (pngPixels4, readPixels[3])


