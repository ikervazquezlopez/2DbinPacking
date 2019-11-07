# 2D bin packing for images

A 2D bin packing algorithm modified from http://code.activestate.com/recipes/442299/.
I modified the code to fit my requirements for my Object Based Video Compression approach.

This code will be useful for packing objects' video frames into a texture atlas.


## How to use it

In order to use this algorithm, a list of (id, opencv_img) is required. The **id** represents the identification number and **opencv_img** is an OpenCV mat. This algorithm is part of the Object Based Codec so the **id** is required to know where is each object located in the texture atlas over the video.

```python
import 2DbinPacking

image_list = [(id0, img0), (id1, img1), ...]
texture_atlas, data = get_object_atlas(image_list)

```
The output of this algorithm is a **texture_atlas** containing all the images in the list pasted into a 4K image and **data** which provides information about where are the objects located in the atlas.
