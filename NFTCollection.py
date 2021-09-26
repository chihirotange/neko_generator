import Img
import concurrent.futures
from random import shuffle


class NFTCollection:
    
    def __init__(self, num_of_nft):
        self.unique_dnas = []
        self.unique_imgs = []

        self.num_of_nft = num_of_nft
        while len(self.unique_imgs) < num_of_nft:
            img = Img.CharacterImage(name = None)
            if self._not_duplicated(img):
                self.unique_imgs.append(img)
                self.unique_dnas.append(img.dna)
                print(len(self.unique_imgs))
        
        shuffle(self.unique_imgs)
        for i,img in enumerate(self.unique_imgs):
            img.name = str(i+1).zfill(6)

    def _get_fullset(self):
        pass

    def _not_duplicated(self, img):
        return True if img.dna not in self.unique_dnas else False

    def print_collection(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in self.unique_imgs:
                executor.submit(_.print_image)


    def export_metadata(self):
        for image in self.unique_imgs:
            print(image.image_hash)
        
        pass

if __name__ == "__main__":
    collection = NFTCollection(20)
    # collection.unique_imgs[0]._get_paths()
    collection.unique_imgs[2].print_image(True)
    print(collection.unique_imgs[2].emotions_dict)
    # collection.export_metadata()

