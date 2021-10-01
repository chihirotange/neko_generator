import pandas as pd
from DataGenerator import DataGenerator
import constants
from os import path

class CharacterImage:

    def __init__(self, name, asset_list, df = (DataGenerator().data)):
        "asset_list la list cac asset cau tao thanh img, gia tri mac dinh la random se tao ra asset random tu database"

        self.name = name
        self.df = df
        self.emotions_dict = None
        self.image_path = None

        filt = self.df[constants.INTERNAL_NAME].isin(asset_list)
        self.assets = self.df[filt]

        dna = self.assets[constants.INTERNAL_NAME].tolist()
        self._true_dna(dna)


    def _true_dna(self,dna):
        true_dna = set([d for d in dna if any(e not in d for e in constants.NOT_TRUE_DNA)])
        self.dna = true_dna


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