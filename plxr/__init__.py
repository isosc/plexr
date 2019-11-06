import numpy as np
import adios2 as ad
import io
from PIL import Image
from ast import literal_eval as make_tuple


#Given a writable opened adios file (returned by adios2.open), image data of the form used by PIL (or corresponding numpy array), and variable name, write the image to the adios file.
def write_image (ad_file, image, var_name):
    image = np.array(image)
    if not image.shape[2] == 3:
        raise TypeError("Expecting RGB Data, size of third dimension must be 3") #todo: deal with other formats

    ad_file.write("%s/__plxr_schema_type"%var_name, "__plxr:image-rgb-8")
    ad_file.write("%s/__plxr_data"%var_name, image, image.shape, (0,0,0), image.shape, end_step=True)


def write_png_image (ad_file, image, var_name):
    image = np.array(image)
    if not image.shape[2] == 3:
        raise TypeError("Expecting RGB Data, size of third dimension must be 3") #todo: deal with other formats

    image = Image.fromarray(image)

    #Write image to IO buffer as png
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    contents = np.frombuffer(buf.getvalue(), dtype=np.dtype('b'))
    #print (contents)

    #Write buffered data to adios
    ad_file.write("%s/__plxr_schema_type"%var_name, "__plxr:image-png")
    ad_file.write("%s/__plxr_data"%var_name, contents, contents.shape, (0,), contents.shape, end_step=True)

def write_image_from_matplotlib (ad_file, fig, var_name):
    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    write_image(ad_file, img, var_name)

def write_png_image_from_matplotlib (ad_file, fig, var_name):
    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    write_png_image(ad_file, img, var_name)


def get_available_image_steps (ad_file, var_name):
    ad_vars = ad_file.available_variables()
    return int(ad_vars['%s/__plxr_data'%var_name]['AvailableStepsCount'])

def read_image (ad_file, var_name,step=0):

    #Check image type
    ad_vars = ad_file.available_variables()
    schema_type = ad_vars[var_name + '/__plxr_schema_type']['Value']

    if "__plxr:image-rgb-8" in schema_type: 
        # Should allow steps to contain images of different sizes (as for image-png)
        # for now, assume steps are the same size
        shape = make_tuple(ad_vars['%s/__plxr_data'%var_name]['Shape'])
        img_data = ad_file.read("%s/__plxr_data"%var_name, start=(0,0,0), count=shape, step_start=step, step_count=1)[0] #Returns a list of one step
        return Image.fromarray(img_data)

    elif "__plxr:image-png" in schema_type:
        shapes = []
        #Loop through metadata and capture shape data
        #Can improve this later by capturing these once rather than at every read
        for ad_step in ad_file:
            ad_vars = ad_step.available_variables()
            shape = [int(ad_vars['%s/__plxr_data'%var_name]['Shape'])]
            shapes.append (shape)

        print(shapes[step])
        img_data = ad_file.read("%s/__plxr_data"%var_name, start=[0], count=shapes[step], step_start=step, step_count=1)[0] #Returns a list of one step
        buf = io.BytesIO(img_data)
        return Image.open(buf)

    else:
        print ("Unsupported schema type in read_image")
        print (schema_type)
        print ("__plxr:image-png")
        return None

def get_image_names (ad_file):
    rv = []
    ad_vars = ad_file.available_variables()
    for ad_var in ad_vars.keys():
        if ad_var.split('/')[-1].startswith('__plxr_schema_type') and 'image' in ad_vars[ad_var]['Value']:
            rv.append(ad_var[0:ad_var.rfind('/')])
    return rv


def get_raw_var_names (ad_file):
    rv = []
    ad_vars = ad_file.available_variables()
    for ad_var in ad_vars.keys():
        if not ad_var.split('/')[-1].startswith('__plxr'):
            rv.append(ad_var)
    return rv

