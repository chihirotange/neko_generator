import pandas as pd
from DataGenerator import DataGenerator
import constants
from random import randint
from os import path
from PIL import Image
from hashlib import md5

counter = DataGenerator().data.set_index(constants.INTERNAL_NAME)[constants.NUM_OF_ASSETS].dropna().to_dict()
full_num = []

class CharacterImage:
    global counter, full_num

    def __init__(self, name, asset_list = "random", df = (DataGenerator().data)):
        "asset_list la list cac asset cau tao thanh img, gia tri mac dinh la random se tao ra asset random tu database"
        self.name = name
        self.df = df
        self.asset_list = asset_list
        self.emotions_dict = None
        self.dna = None
        self.assets = None
        self.image_path = None
        if asset_list == "random":
            self._create_random()
        else:
            self._no_random()

    def _create_random(self):
        chosen_assets = [] # cac asset dc chon se nam trong list nay
        trait_groups = self.df[constants.ANCHOR_TRAIT].unique()
        
        dna = []

        for trait_group in trait_groups: #loop lan luot cac trait de chon asset
            filt = (self.df[constants.ANCHOR_TRAIT] == trait_group) & (~self.df[constants.INTERNAL_NAME].isin(full_num))
            traits = self.df[filt] #filter panda
            try:
                picked_asset = traits.sample() #list cac asset tu trait da filter
                if self._choose_asset(picked_asset):
                    asset_name = picked_asset[constants.INTERNAL_NAME].item()
                    chosen_assets.append(asset_name) #item() de return dang list, de sau nay ref vao dataframe tong ko la no se return dang dataframe
                    dna.append(asset_name)
                    if counter.get(asset_name) != None:
                        counter[asset_name] -= 1
                        if counter[asset_name] == 0:
                            full_num.append(asset_name)
            except:
                continue

        chosen_asset_filter = self.df[constants.INTERNAL_NAME].isin(chosen_assets)

        self.assets = self.df[chosen_asset_filter] #sorted dataframe va luu vao bien moi assets cua image object
        self._true_dna(dna)


    def _no_random(self):
        filt = self.df[constants.INTERNAL_NAME].isin(self.asset_list)
        self.assets = self.df[filt]
        dna = self.assets[constants.INTERNAL_NAME].tolist()
        self._true_dna(dna)


    def _true_dna(self,dna):
        true_dna = set([d for d in dna if any(e not in d for e in constants.NOT_TRUE_DNA)])
        self.dna = true_dna

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

    def _filter_red_flags(self):
        pass


    def _get_paths(self):
        temp_df = self.assets.sort_values(by= constants.ASSET_POS)
        new_dict = {
            constants.INTERNAL_NAME: None,
            constants.ASSET_POS: None
        }

        sub_layer_assets = self.assets[constants.SUBLAYER].tolist()
        new_sublayer = [x for x in sub_layer_assets if pd.isnull(x) == False]
        sub_layer_pos = self.assets[constants.SUBLAYER_POS].tolist()
        new_sublayer_pos = [x for x in sub_layer_pos if pd.isnull(x) == False]
        
        new_dict[constants.INTERNAL_NAME] = new_sublayer
        new_dict[constants.ASSET_POS] = new_sublayer_pos

        df_to_append = pd.DataFrame(new_dict)
        temp_df = temp_df.append(df_to_append, ignore_index = True)

        temp_df.sort_values(by = constants.ASSET_POS, ascending=False, inplace=True)
        series_to_list = temp_df[constants.INTERNAL_NAME].tolist()

        for i in series_to_list:
            file_paths = [path.join(constants.IMAGE_DIR, i) + ".png" for i in series_to_list]
        
        img_paths = {}
        for emo in constants.EMOTIONS:
            emo_path = []
            for f in file_paths:
                asset = f.replace(constants.DEFAULT_EMO, emo)
                emo_path.append(asset)

            img_paths[emo] = emo_path

        return img_paths

    def print_image(self, full_emo= True, image_width = constants.DEFAULT_WIDTH):
        image_size = (image_width, round(image_width*constants.IMAGE_RATIO))
        
        emotions_dict = {}
        emotions_path = self._get_paths()

        for emotion, file_paths in emotions_path.items():
            image = Image.new("RGBA", image_size)
            for f in file_paths:
                next_image = Image.open(f).convert("RGBA").resize(image_size)
                image = Image.alpha_composite(image,next_image)


            image_path = f"{path.join(constants.IMAGE_DESTINATION, self.name)}_{emotion}.png"
            image.save(image_path)
            
            emotions_dict[emotion] = {}
            emotions_dict[emotion]["path"] = image_path
            emotions_dict[emotion]["hash"] = self._hash_image(image_path)

            if full_emo == True:
                continue
            else:
                break
            
        self.emotions_dict = emotions_dict

    def _hash_image(self, file):
        try:
            with open(file, "rb") as f:
                bytes = f.read() #read file as bytes
                hash = md5(bytes).hexdigest()
                return hash
        except:
            print("No image to hash!")