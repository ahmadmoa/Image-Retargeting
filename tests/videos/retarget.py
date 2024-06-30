import numpy as np
from cv2 import VideoCapture, VideoWriter, CAP_PROP_FPS, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT

from config.constants import DataPath
from config.plotter import Plotter
# from src.processors.Combiner import Combiner
from src.processors.Midas import Midas
from src.processors.sc.MiddleSCI import MiddleSCI
from util.Image import Image
from util.Pipeline import Pipeline
from util.Worker import Worker


import torch
print("PyTorch Version:", torch.__version__)
print("CUDA Available:", torch.cuda.is_available())
print("CUDA Version:", torch.version.cuda)
print("CUDA Device Count:", torch.cuda.device_count())
print("Current CUDA Device:", torch.cuda.current_device())
print("CUDA Device Name:", torch.cuda.get_device_name(torch.cuda.current_device()))
torch.cuda.empty_cache()  # Clear any cached memory (optional)
x = torch.rand(10, 10).cuda()
print(x)
# img = Image(f"../{DataPath.INPUT_PATH.value}/img_4.png")
# img2 = Image(f"../{DataPath.INPUT_PATH.value}/img_6.png")
#
# sc = MiddleSCI(img, 0.75, converter=Combiner)
# sc2 = MiddleSCI(img2, 0.75, converter=Combiner)

global energy, frames_count, frame_counter


def convert(obj: MiddleSCI, out: VideoWriter, *args):
    print("converted", frame_counter)
    temp = obj.convert(*args)

    # if energy is not None:
    #     temp = (temp + energy) / 2

    return obj, out, temp


def carve(obj: MiddleSCI, out: VideoWriter, *args):
    print("accumulated", frame_counter)

    args = obj.accumulate(*args)
    # print(args)
    res = obj.remove(args)

    return out, res


def accumulate(obj: MiddleSCI, out: VideoWriter, *args):
    print("accumulated", frame_counter)
    return obj, out, obj.accumulate(*args)


def remove(obj: MiddleSCI, out: VideoWriter, *args):
    print("removed", frame_counter)
    return out, obj.remove(*args)


def save(out: VideoWriter, *args):
    global frame_counter
    print("saved", frame_counter)

    img = np.array(args)[0]

    out.write(img)

    Image.save(img, f"../{DataPath.OUTPUT_PATH.value}/frames/ball/{frame_counter}.jpg")

    frame_counter += 1
    if frame_counter == frames_count:
        print("released")
        out.release()


def plot(*args):
    args = np.array(args)
    Plotter.image(args)


pipeline = Pipeline([
    Worker.make(1, convert, 2),
    Worker.make(2, carve, 3),
    # Worker.make(2, accumulate, 3),
    # Worker.make(3, remove, 4),
    Worker.make(3, save)
])

# .push((sc, img)).push((sc2, img))


def retarget_video(in_path: str, out_path: str, ratio: float):
    source = VideoCapture(in_path)

    fps = int(source.get(CAP_PROP_FPS))
    width = int(source.get(CAP_PROP_FRAME_WIDTH) * ratio)
    height = int(source.get(CAP_PROP_FRAME_HEIGHT))

    fourcc = VideoWriter().fourcc(*'mp4v')
    target = VideoWriter(out_path, fourcc, fps, (width, height))

    # print(width)

    count = 0
    global frame_counter, frames_count, energy

    frames_count = 0
    frame_counter = 0
    energy = None

    while source.isOpened():
        ret, frame = source.read()
        if not ret:
            break

        count += 1
        # if count % 3 == 0:
        #     continue

        frames_count += 1

        img = Image("", data=frame)

        sc = MiddleSCI(img, ratio, converter=Midas, prev_matrix=True)

        # energy = sc.get_matrix()

        pipeline.push((sc, target, img))

        if count == 104:
            break

    source.release()
    # print(frame_counter, frames_count)


cat = "ball"
v = 6

retarget_video(
    in_path=f"../{DataPath.INPUT_PATH.value}/videos/{cat}.mp4",
    out_path=f"../{DataPath.INPUT_PATH.value}/videos/{cat}_{v}.mp4",
    ratio=0.75
)
