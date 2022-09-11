'''
Copyright (c) 2019 Timothy Esler
Released under the MIT license
https://github.com/timesler/facenet-pytorch/blob/master/LICENSE.md
'''
from abc import ABC, abstractmethod
from typing import Any

from io import BytesIO, StringIO
from binascii import a2b_base64
import base64
import glob
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from torchvision import transforms
import numpy as np
import pandas as pd
import wget


class BaseMLModel(ABC):
    @abstractmethod
    def cut(self, req: Any) -> Any:
        raise NotImplementedError
    def predict(self, req: Any) -> Any:
        raise NotImplementedError


class MLModel(BaseMLModel):
    """Sample ML model"""

    def __init__(self, model_path: str) -> None:
        self.mtcnn = MTCNN(image_size = 160, margin = 10).eval()
        #self.resnet = InceptionResnetV1(pretrained='vggface2').eval()
        data_url = os.environ["DATA_URL"]
        file = wget.download(data_url + "model.pt")
        self.resnet = torch.load(file)
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
        df = pd.read_csv(data_url + "id_with_no_err_vec.csv")
        self.ids = df["id"].tolist()
        self.vecs = df.drop("id", axis=1).values

    def cut(self, input_text: str) -> dict:
        input_text = BytesIO(base64.b64decode(input_text))
        img = Image.open(input_text)
        img = img.convert("RGB")
        with torch.no_grad():
            img = self.mtcnn(img, "img.png")
            #os.remove("img.png")
        is_face = True
        if str(img) == "None":
            is_face = False
        else:
            img = Image.open("img.png")
            # https://stackoverflow.com/questions/646286/how-to-write-png-image-to-string-with-the-pil
            with BytesIO() as output:
                img.save(output, format="png")
                contents = output.getvalue()
            img = base64.b64encode(contents).decode("ascii")
            
        return {"is_face": str(is_face), "img": str(img)}

    def predict(self, input_text: str) -> dict:
        img = Image.open(BytesIO(base64.b64decode(input_text)))
        img = img.convert("RGB")
        img = self.transform(img).reshape((1, 3, 160, 160))
        with torch.no_grad():
            img = self.resnet(img)
        img = img[0].detach().numpy()
        rec_actress_id = ""
        for index in np.argsort(np.square(self.vecs - img).sum(axis = 1))[:10]:
                rec_actress_id += str(self.ids[index]) + "-"
        
        # result_arr = (self.vecs * img.reshape((1, 512))).sum(axis=1)/np.linalg.norm(self.vecs, axis=1)/np.linalg.norm(img)
        # for index in np.argsort(result_arr)[::-1][:10]:
        #     rec_actress_id += str(self.ids[index]) + "-"
        return {"rec_actress_id": rec_actress_id[:-1]}
    
