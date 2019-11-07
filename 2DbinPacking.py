from PIL import Image
import glob
import cv2
import numpy as np


format = 'RGB'
size = 4096,4096

class PackNode(object):
    """
    Creates an area which can recursively pack other areas of smaller sizes into itself.
    """
    def __init__(self, area):
        #if tuple contains two elements, assume they are width and height, and origin is (0,0)
        if len(area) == 2:
            area = (0,0,area[0],area[1])
        self.area = area

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self.area))

    def get_width(self):
        return self.area[2] - self.area[0]
    width = property(fget=get_width)

    def get_height(self):
        return self.area[3] - self.area[1]
    height = property(fget=get_height)

    def insert(self, area):
        if hasattr(self, 'child'):
            a = self.child[0].insert(area)
            if a is None: return self.child[1].insert(area)
            return a

        area = PackNode(area)
        if area.width <= self.width and area.height <= self.height:
            self.child = [None,None]
            self.child[0] = PackNode((self.area[0]+area.width, self.area[1], self.area[2], self.area[1] + area.height))
            self.child[1] = PackNode((self.area[0], self.area[1]+area.height, self.area[2], self.area[3]))
            return PackNode((self.area[0], self.area[1], self.area[0]+area.width, self.area[1]+area.height))


# Input: an array of tuples with id and image mat: [(id0, img0), (id1,img1),...]
def get_object_atlas(image_list):
    images = [(x, Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) ) for x, img in image_list]
    images = [(i.size[0]*i.size[1], id, i) for id,i in images]
    images = sorted(images)
    #images = sorted([(i.size[0]*i.size[1], id, i) for id,i in ((x,Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) for x, img in image_list))])

    tree = PackNode(size)
    image = Image.new(format, size)

    data = {}
    for area, id, img in images:
        uv = tree.insert(img.size)
        if uv is None: raise ValueError('Pack size too small.')
        image.paste(img, uv.area)
        data[id] = uv.area

    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, data

"""
if __name__ == "__main__":
    names = ["test_texture.png", "test_texture.png", "test_texture.png", "test_texture.png"]
    image_list = [ (i, cv2.imread(names[i])) for i in range(len(names))]
    atlas, data = get_object_atlas(image_list)
    print(data)
    cv2.imshow("atlas", atlas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""
