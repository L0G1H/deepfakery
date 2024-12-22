# Deepfakery
This repository provides a Python class for generating deepfake images and videos by swapping faces using a pre-trained deep learning model.

## Features
- Generate deepfake images by swapping faces in a photo.
- Create deepfake videos by swapping faces in each frame of a video.
- Download and cache the deepfake model if not already available locally.
- User-friendly CLI interface for interacting with the script.

## Setup
```bash
git clone https://github.com/L0G1H/deepfakery.git
cd deepfakery
uv run deepfakery.py
```

## Usage
```bash
python deepfakery.py
```

Once the script is running, you will be presented with the following options:

- **photo**: Create a deepfake image by swapping faces in a photo.
- **video**: Create a deepfake video by swapping faces in each frame.
- **exit**: Exit the script.

### Photo Deepfake

1. Enter `photo` when prompted.
2. Provide the path to the main image (the image in which the face will be swapped).
3. Provide the path to the deepfake image (the image from which the face will be used).
4. Specify the path where the output image will be saved.

Example:
```
choices: "photo", "video", "exit"
enter choice > photo
main img path > /path/to/main/image.jpg
deepfake img path > /path/to/deepfake/face.png
output img path > /path/to/output/image.jpeg
```

### Video Deepfake
1. Enter `video` when prompted.
2. Provide the path to the main video (the video in which faces will be swapped).
3. Provide the path to the deepfake image (the image from which the face will be used).
4. Specify the path where the output video will be saved.

Example:
```
choices: "photo", "video", "exit"
enter choice > video
main video path > /path/to/main/video.mp4
deepfake img path > /path/to/deepfake/face.jpg
output video path > /path/to/output/video.mp4
```

### Exit
To exit the program, simply enter `exit` when prompted.

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
