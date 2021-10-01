import Img
from concurrent import futures
from random import shuffle
from DataGenerator import DataGenerator
import constants
from random import randint
from PIL import Image
from os import path

counter = DataGenerator().data.set_index(constants.INTERNAL_NAME)[constants.NUM_OF_ASSETS].dropna().to_dict()
full_num = []

class NFTCollection:
    
    def __init__(self, num_of_nft):
        self.unique_dnas = []
        self.unique_imgs = []

        self.df = DataGenerator().data

        fullset_list = self._get_fullset()
        missing_nft_num = num_of_nft - len(fullset_list)

        missing_nft = [self._get_random() for __ in range(missing_nft_num)]

        combined_list = fullset_list + missing_nft
        for nft in combined_list:
            img = Img.CharacterImage(name = None, asset_list = nft)
            if self._not_duplicated(img):
                self.unique_imgs.append(img)
                self.unique_dnas.append(img.dna)
                print(len(self.unique_imgs))
        
        shuffle(self.unique_imgs)
        for i,img in enumerate(self.unique_imgs):
            img.name = str(i+1).zfill(6)

    def _get_random(self):
        chosen_assets = [] # cac asset dc chon se nam trong list nay
        trait_groups = self.df[constants.ANCHOR_TRAIT].unique()
        
        for trait_group in trait_groups: #loop lan luot cac trait de chon asset
            filt = (self.df[constants.ANCHOR_TRAIT] == trait_group) & (~self.df[constants.INTERNAL_NAME].isin(full_num))
            traits = self.df[filt] #filter panda
            try:
                picked_asset = traits.sample() #list cac asset tu trait da filter
                if self._choose_asset(picked_asset):
                    asset_name = picked_asset[constants.INTERNAL_NAME].item()
                    chosen_assets.append(asset_name) #item() de return dang list, de sau nay ref vao dataframe tong ko la no se return dang dataframe
            except:
                continue
        
        self._add_to_counter(chosen_assets)
        return chosen_assets
    
    def _add_to_counter(self, assets):
        for a in assets:
            if counter.get(a) != None:
                counter[a] -= 1
                if counter[a] == 0:
                    full_num.append(a)


    def _get_fullset(self):
        fullset_collection = []
        fullset_filt = self.df[constants.FULLSET].notna()
        all_fullsets = self.df[fullset_filt][constants.FULLSET].unique()

        for trait_group in all_fullsets:
            filt = self.df[constants.FULLSET] == trait_group
            fullset = self.df[filt]
            fullset_assets = fullset[constants.INTERNAL_NAME].tolist()
            fullset_collection.append(fullset_assets)

            self._add_to_counter(fullset_assets)
        return fullset_collection


    def _not_duplicated(self, img):
        return True if img.dna not in self.unique_dnas else False


    def _choose_asset(self,series):

        percentage = float((series[constants.PERCENTAGE]))
        
        if percentage == 100:
            return True
        else:
            roll_random = randint(0,100)
            if roll_random <= percentage:
                return True
            else:
                return False

    def print_img(self, img, img_width = constants.DEFAULT_WIDTH, full_emo = False):
        "pass in img object to print"
        image_size = (img_width, round(img_width*constants.IMAGE_RATIO))
        emotions_path = img._get_paths()

        for emotion, file_paths in emotions_path.items():
            image = Image.new("RGBA", image_size)
            for f in file_paths:
                next_image = Image.open(f).convert("RGBA").resize(image_size)
                image = Image.alpha_composite(image,next_image)


            image_path = f"{path.join(constants.IMAGE_DESTINATION, img.name)}_{emotion}.png"
            image.save(image_path)
            

            if full_emo == True:
                continue
            else:
                break
            

    def print_collection(self):
        with futures.ThreadPoolExecutor() as executor:
            executor.map(self.print_img, self.unique_imgs)

    def _hash_image(self, file):
        try:
            with open(file, "rb") as f:
                bytes = f.read() #read file as bytes
                hash = md5(bytes).hexdigest()
                return hash
        except:
            print("No image to hash!")

    def export_metadata(self):
        for image in self.unique_imgs:
            print(image.image_hash)
        pass

if __name__ == "__main__":
    collection = NFTCollection(20)
    print(collection.unique_imgs[0]._get_paths())
    collection.print_collection()
    # print(collection.unique_imgs[2].emotions_dict)
    # collection.export_metadata()
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     for _ in collection.unique_imgs:
    #         executor.submit(_.print_image(full_emo=False))


