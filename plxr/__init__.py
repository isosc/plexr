import numpy as np
import adios2 as ad


#Given a writable opened adios file (returned by adios2.open), image data of the form used by PIL (or corresponding numpy array), and variable name, write the image to the adios file.
def write_image (ad_file, image, var_name):
    image = np.array(image)

    if not image.shape[2] == 3:
        raise TypeError("Expecting RGB Data, size of third dimension must be 3")

    ad_file.write("%s/__plxr_schema_type"%var_name, "__plxr:image-rgb-8")
    ad_file.write("%s/__plxr_data"%var_name, image, image.shape, [0,0,0], image.shape, endl=True)

