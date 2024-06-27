import numpy as np

from config.constants import DataPath
from config.plotter import Plotter
from src.processors.Combiner import Combiner
from src.processors.sc.ImprovedSC import ImprovedSC
from src.processors.SaliencyMap import SaliencyMap
from src.processors.SobelFilter import SobelFilter
from src.processors.sc.ConnectedSC import ConnectedSC
from src.processors.sc.ForwardSC import ForwardSC
from src.processors.sc.MiddleSC import MiddleSC
from utils.Image import Image

if __name__ == '__main__':
    # name = "frames/ball/50.jpg"
    # name = "img_4.png"

    path = f"{DataPath.INPUT_PATH.value}"

    img = Image(f"{path}/moon.jpg")
    rgb = img.rgb()

    # depth = Image(f"{path}/depth.jpg")()

    energy = Combiner(img)().image()

    # Plotter.images([energy], 1, 1)

    # result = ImprovedSC(img, 0.750, converter=Combiner, feature_map=energy)()

    # backward = ConnectedSC(rgb, energy, 0.75)()
    # middle = MiddleSC(rgb, energy, 0.75)()
    # forward = ForwardSC(rgb, energy, 0.75)()

    improved = ImprovedSC(img, 0.75)()

    Plotter.images([rgb, improved], 1, 2)
