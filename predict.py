import os
from glob import glob
from math import ceil

from cog import BasePredictor, Input, Path
# import PIL image
from PIL import Image

from typing import List

#MODEL_PATHS = "--smpl_model_folder /smpl_data --AE_path_fname /avatarclip_data/model_VAE_16.pth --codebook_fname /avatarclip_data/codebook.pth"

# INIT_COMMANDS="""pip install git+https://github.com/voodoohop/neural_renderer.git
# mv /avatarclip_data/* /src/AvatarGen/ShapeGen/data/
# mkdir -p /src/smpl_models
# mv /smpl_data /src/smpl_models/smpl"""

class Predictor(BasePredictor):
    def setup(self):
        print("setup")
    def predict(self,
            image: Path = Input(description="Image"),
    ) -> List[Path]:


        os.system("rm -rf /src/image/* /src/video/* /src/depth/* /src/mesh/*")

        # convert image to jpeg and copy  to /src/image
        image = str(image)
        # do conversion
        im = Image.open(image)
        im = im.convert("RGB")
        im.save("/src/image/image.jpg")

        os.system("ls -l /src/image")
        os.system("xvfb-run -a python -m cProfile -o temp.dat main.py --config argument.yml")
        os.system("ls -l video")

        paths = ["video/*.mp4", "depth/*.png", "mesh/*.obj"]
        globs = [sorted(glob(path)) for path in paths]

        # flatten
        globs = [item for sublist in globs for item in sublist]

        return [Path(video_file) for video_file in globs]+ [Path("temp.dat")]
