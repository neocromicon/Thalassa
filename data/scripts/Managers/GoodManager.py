import json
import pygame

class GoodManager:
    GOODS_CONFIG = None
    
    @classmethod
    def load_goods(cls, path='data/config/Goods.json'):
        with open(path) as f:
            cls.GOODS_CONFIG = json.load(f)
            cls.textures = {
                g: pygame.image.load(f"data/img/Goods/{cls.GOODS_CONFIG['goods'][g]['texture']}")
                for g in cls.GOODS_CONFIG['goods']
            }
