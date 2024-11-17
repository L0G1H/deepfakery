# Deepfake Generator

This project implements a deepfake generator using the InsightFace library to swap faces between images or video frames. The primary functionality involves using a pre-trained model for face swapping on photos and videos. The generator takes a source image or video (main) and a target image (deepfake face) and creates a new image or video with the swapped faces.

## Requirements

Before running this project, ensure the following Python packages are installed:

- `opencv-python` (cv2)
- `insightface`
- `matplotlib`
- `urllib`
- `os`

You can install the required libraries using pip:

```bash
pip install opencv-python insightface matplotlib
```

## Usage

1. **Photo Deepfake**: You can swap faces between a target image (deepfake face) and a main image (the image where the face will be replaced).

2. **Video Deepfake**: You can swap faces in a video by applying the face swapping process to each frame.

### Run the Script

1. **Launch the program**: Simply run the Python script.
   
   ```bash
   python deepfake_generator.py
   ```

2. **Choices**: The program will ask for one of the following options:
   - **'photo'**: Swap faces between a photo and a deepfake face.
   - **'video'**: Swap faces between a video and a deepfake face.
   - **'exit'**: Exit the program.

   Example input for photo:

   ```text
   choices: 'photo', 'video', 'exit'
   enter choice > photo
   main img path > /path/to/main_image.jpg
   deepfake img path > /path/to/deepfake_face.jpg
   output img path > /path/to/output_image.jpg
   ```

   Example input for video:

   ```text
   choices: 'photo', 'video', 'exit'
   enter choice > video
   main video path > /path/to/main_video.mp4
   deepfake img path > /path/to/deepfake_face.jpg
   output video path > /path/to/output_video.mp4
   ```