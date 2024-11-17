# Deepfake Generator

This project implements a deepfake generator using the InsightFace library to swap faces between images or video frames. The primary functionality involves using a pre-trained model for face swapping on photos and videos. The generator takes a source image or video (main) and a target image (deepfake face) and creates a new image or video with the swapped faces.

## Setup Instructions

### 1. Clone the repository

Start by cloning this repository to your local machine. Open a terminal and run:

```bash
git clone https://github.com/L0G1H/deepfake_generator.git
```

### 2. Navigate to the project folder

Change to the directory of the cloned repository:

```bash
cd deepfake_generator
```

### 3. Create and activate a virtual environment (Optional)

It's recommended to create a virtual environment to manage the dependencies. Run the following commands to set up and activate the environment:

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install dependencies

Once you are in the project folder and the virtual environment is activated, install the required dependencies using:

```bash
pip install -r requirements.txt
```

This will install all the libraries required to run the deepfake generator.

---

## Usage

### 1. **Photo Deepfake**

You can swap faces between a target image (deepfake face) and a main image (the image where the face will be replaced).

### 2. **Video Deepfake**

You can swap faces in a video by applying the face swapping process to each frame.

---

### Running the Script

1. **Launch the program**:

   After installing the dependencies, simply run the Python script:

   ```bash
   python deepfake.py
   ```

2. **Choices**: The program will prompt you to choose between the following options:
   - **'photo'**: Swap faces between a photo and a deepfake face.
   - **'video'**: Swap faces between a video and a deepfake face.
   - **'exit'**: Exit the program.

3. **Example input for photo**:

   When you choose the **'photo'** option, the program will ask for the following paths:
   ```text
   choices: 'photo', 'video', 'exit'
   enter choice > photo
   main img path > /path/to/main_image.jpg
   deepfake img path > /path/to/deepfake_face.jpg
   output img path > /path/to/output_image.jpg
   ```

4. **Example input for video**:

   When you choose the **'video'** option, the program will ask for the following paths:
   ```text
   choices: 'photo', 'video', 'exit'
   enter choice > video
   main video path > /path/to/main_video.mp4
   deepfake img path > /path/to/deepfake_face.jpg
   output video path > /path/to/output_video.mp4
   ```
