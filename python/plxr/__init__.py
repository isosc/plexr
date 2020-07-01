import numpy as np
import adios2 as ad
import io
from PIL import Image
from ast import literal_eval as make_tuple


#Given a writable opened adios file (returned by adios2.open), image data of the form used by PIL (or corresponding numpy array), and variable name, write the image to the adios file.
def write_image_hl (ad_file, image, var_name, end_step=False):
    image = np.array(image)
    if not image.shape[2] == 3:
        raise TypeError("Expecting RGB Data, size of third dimension must be 3") #todo: deal with other formats

    ad_file.write("%s/__plxr_schema_type"%var_name, "__plxr:image-rgb-8")
    ad_file.write("%s/__plxr_data"%var_name, image, image.shape, (0,0,0), image.shape, end_step=end_step)


def write_png_image_hl (ad_file, image, var_name, end_step=False):
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
    ad_file.write("%s/__plxr_data"%var_name, contents, contents.shape, (0,), contents.shape, end_step=end_step)

def write_image_from_matplotlib_hl (ad_file, fig, var_name, end_step=False):
    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    write_image(ad_file, img, var_name, end_step=end_step)

def write_png_image_from_matplotlib_hl (ad_file, fig, var_name, end_step=False):
    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    write_png_image_hl(ad_file, img, var_name, end_step=end_step)


def get_available_image_steps_hl (ad_file, var_name):
    ad_vars = ad_file.available_variables()
    return int(ad_vars['%s/__plxr_data'%var_name]['AvailableStepsCount'])

def read_image_hl (ad_step, var_name):

    #Check image type
    ad_vars = ad_step.available_variables()
    schema_type = ad_step.read_string(var_name + '/__plxr_schema_type')[0]

    if "__plxr:image-rgb-8" in schema_type: 
        # Should allow steps to contain images of different sizes (as for image-png)
        # for now, assume steps are the same size
        shape = make_tuple(ad_vars['%s/__plxr_data'%var_name]['Shape'])
        #img_data = ad_step.read("%s/__plxr_data"%var_name, start=(0,0,0), count=shape, step_start=step, step_count=1)[0] #Returns a list of one step
        img_data = ad_step.read("%s/__plxr_data"%var_name, start=(0,0,0), count=shape)[0] #Returns a list of one step
        return Image.fromarray(img_data)

    elif "__plxr:image-png" in schema_type:
        shapes = []
        #Loop through metadata and capture shape data
        #Can improve this later by capturing these once rather than at every read
        ad_vars = ad_step.available_variables()
        shape = [int(ad_vars['%s/__plxr_data'%var_name]['Shape'])]

        print ("Shape is {}".format(shape))

        #print ("Reading step {}, shapes[step] is {}".format(step, shapes[step]))
        img_data = ad_step.read("%s/__plxr_data"%var_name, start=[0], count=shape)
        #img_data = ad_step.read("%s/__plxr_data"%var_name, start=[0], count=shape)[0] #Returns a list of one step
        #print (img_data)
        buf = io.BytesIO(img_data)
        return Image.open(buf)

    else:
        print ("Unsupported schema type in read_image")
        print (schema_type)
        print ("__plxr:image-png")
        return None

def get_image_names_hl (ad_file):
    rv = []
    ad_vars = ad_file.available_variables()
    for ad_var in ad_vars.keys():
        # "Value" no longer provided for strings, use read_string instead...
        #if ad_var.split('/')[-1].startswith('__plxr_schema_type') and 'image' in ad_vars[ad_var]['Value']:
        if ad_var.split('/')[-1].startswith('__plxr_schema_type') and 'image' in ad_file.read_string(ad_var, step_start=0, step_count=1)[0]:
            rv.append(ad_var[0:ad_var.rfind('/')])
    return rv


def get_raw_var_names_hl (ad_file):
    rv = []
    ad_vars = ad_file.available_variables()
    for ad_var in ad_vars.keys():
        if not ad_var.split('/')[-1].startswith('__plxr'):
            rv.append(ad_var)
    return rv



def write_image_ll (io, engine, image, var_name):
    pass


def write_png_image_ll (ad_io, ad_engine, image, var_name):
    image = np.array(image)
    if not image.shape[2] == 3:
        raise TypeError("Expecting RGB Data, size of third dimension must be 3") #todo: deal with other formats

    image = Image.fromarray(image)

    #Write image to IO buffer as png
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    contents = np.frombuffer(buf.getvalue(), dtype=np.dtype('b'))
    #print (contents)

    schema_type_str = "__plxr:image-png"
    start = (0,)

    #Write buffered data to adios
    var_schema_type = ad_io.DefineVariable("%s/__plxr_schema_type"%var_name)
        #, schema_type_str.shape, (0,), schema_type_str.shape, ad.ConstantDims)
    var_data = ad_io.DefineVariable("%s/__plxr_data"%var_name, contents, contents.shape, start, contents.shape, ad.ConstantDims)

    ad_engine.Put(var_schema_type, schema_type_str)
    ad_engine.Put(var_data, contents)
    #ad_file.write("%s/__plxr_schema_type"%var_name, "__plxr:image-png")
    #ad_file.write("%s/__plxr_data"%var_name, contents, contents.shape, (0,), contents.shape, end_step=end_step)


def write_image_from_matplotlib_ll (io, engine, fig, var_name):
    pass

def write_png_image_from_matplotlib_ll (io, engine, fig, var_name):
    pass

def get_available_image_steps_ll (io, engine, var_name):
    pass

def read_image_ll (ad_io, ad_engine, var_name):

    #Check image type
    var_type = ad_io.InquireVariable("{}/__plxr_schema_type".format(var_name) )
    #print (dir(var_type))

    print (ad_io.AvailableVariables() )

    schema_type = '                       '
    ad_engine.Get(var_type, schema_type) 
    ad_engine.PerformGets()
    print ("schema_type is ({})".format(schema_type) )


#    ad_vars = ad_step.available_variables()
#    schema_type = ad_step.read_string(var_name + '/__plxr_schema_type')[0]


    if "__plxr:image-rgb-8" in schema_type:
        # Should allow steps to contain images of different sizes (as for image-png)
        # for now, assume steps are the same size
        shape = make_tuple(ad_vars['%s/__plxr_data'%var_name]['Shape'])
        #img_data = ad_step.read("%s/__plxr_data"%var_name, start=(0,0,0), count=shape, step_start=step, step_count=1)[0] #Returns a list of one step
        img_data = ad_step.read("%s/__plxr_data"%var_name, start=(0,0,0), count=shape)[0] #Returns a list of one step
        return Image.fromarray(img_data)

    elif "__plxr:image-png" in schema_type:

        var_data = ad_io.InquireVariable("%s/__plxr_data"%var_name)
        #print(dir(var_data))
        data_size = var_data.Shape()
        data = np.zeros(data_size, dtype=np.int8)
        print (data)
        ad_engine.Get(var_data, data)
        ad_engine.PerformGets()
        buf = io.BytesIO(data)
        return Image.open(buf)
        

#        shapes = []
#        #Loop through metadata and capture shape data
#        #Can improve this later by capturing these once rather than at every read
#        ad_vars = ad_step.available_variables()
#        shape = [int(ad_vars['%s/__plxr_data'%var_name]['Shape'])]
#
#        print ("Shape is {}".format(shape))
#
#        #print ("Reading step {}, shapes[step] is {}".format(step, shapes[step]))
#        img_data = ad_step.read("%s/__plxr_data"%var_name, start=[0], count=shape)
#        #img_data = ad_step.read("%s/__plxr_data"%var_name, start=[0], count=shape)[0] #Returns a list of one step
#        #print (img_data)
#        buf = io.BytesIO(img_data)
#        return Image.open(buf)

    else:
        print ("Unsupported schema type in read_image")
        print (schema_type)
        print ("__plxr:image-png")
        return None


#    var_inTemperature = ioRead.InquireVariable("temperature2D")
#    if(var_inTemperature is False):
#        raise ValueError('var_inTemperature is False')
#
#    assert var_inTemperature is not None
#    readOffset = [2, 2]
#    readSize = [4, 4]
#
#    var_inTemperature.SetSelection([readOffset, readSize])
#    inTemperatures = np.zeros(readSize, dtype=np.int)
#    ibpStream.Get(var_inTemperature, inTemperatures, adios2.Mode.Sync)


def get_image_names_ll (io, engine):
    pass

def get_raw_var_names_ll (io, engine):
    pass


