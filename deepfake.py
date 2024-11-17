import os
import urllib.request
import insightface
import cv2


class DeepfakeGenerator:
    def __init__(self, model_url: str, model_path: str):
        self.model_url = model_url
        self.model_path = model_path
        self._download_model_if_needed()
        self.swapper = insightface.model_zoo.get_model(self.model_path, download=False, download_zip=False)
        self.app = insightface.app.FaceAnalysis(name="buffalo_l")
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def _download_model_if_needed(self):
        if not os.path.exists(self.model_path):
            print(f"Model not found at {self.model_path}. Downloading...")
            urllib.request.urlretrieve(self.model_url, self.model_path)
            print(f"Model downloaded to {self.model_path}")
        else:
            print(f"Model already exists at {self.model_path}. Using the existing model.")

    @staticmethod
    def extract_mp4_frames(mp4_path):
        cap = cv2.VideoCapture(mp4_path)
        frames = []
        fps = cap.get(cv2.CAP_PROP_FPS)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        cap.release()
        return frames, fps

    @staticmethod
    def write_frames_to_video(frames, output_path, fps) -> None:
        height, width, _ = frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        for frame in frames:
            out.write(frame)

        out.release()

    def load_face(self, img, multiple: bool = False):
        img_faces = self.app.get(img)
        if multiple:
            return img_faces
        else:
            assert len(img_faces) == 1
            return img_faces[0]

    def get_deepfake_frame(self, main_img, deepfake_face):
        main_faces = self.load_face(main_img, multiple=True)

        res = main_img.copy()
        for main_face in main_faces:
            res = self.swapper.get(res, main_face, deepfake_face, paste_back=True)

        return res

    def get_video_deepfake(self, main_video_path, deepfake_img_path, output_path):
        frames, fps = self.extract_mp4_frames(main_video_path)

        deepfake_img = cv2.imread(deepfake_img_path)
        deepfake_face = self.load_face(deepfake_img)

        deepfake_imgs = []

        for i, frame in enumerate(frames):
            print(f"{i + 1} / {len(frames)}")
            deepfake_img = self.get_deepfake_frame(frame, deepfake_face)
            deepfake_imgs.append(deepfake_img)

        self.write_frames_to_video(deepfake_imgs, output_path, fps)

    def get_photo_deepfake(self, main_img_path: str, deepfake_img_path: str, output_path: str):
        main_img_path = os.path.expanduser(main_img_path)
        deepfake_img_path = os.path.expanduser(deepfake_img_path)
        output_path = os.path.expanduser(output_path)

        if not os.path.exists(main_img_path):
            print(f"Error: {main_img_path} does not exist.")
            return
        if not os.path.exists(deepfake_img_path):
            print(f"Error: {deepfake_img_path} does not exist.")
            return

        main_img = cv2.imread(main_img_path)
        if main_img is None:
            print(f"Error: Failed to load image at {main_img_path}")
            return

        deepfake_img = cv2.imread(deepfake_img_path)
        if deepfake_img is None:
            print(f"Error: Failed to load image at {deepfake_img_path}")
            return

        main_faces = self.load_face(main_img, multiple=True)
        deepfake_face = self.load_face(deepfake_img, multiple=False)

        res = main_img.copy()

        for main_face in main_faces:
            res = self.swapper.get(res, main_face, deepfake_face, paste_back=True)

        cv2.imwrite(output_path, res)
        print(f"{output_path} created.")


def main():
    model_url = "https://www.dropbox.com/scl/fi/tx59r655h4ke5414s80o3/inswapper_128.onnx?rlkey=p9ktqp27w1bxzc3s30dzb9832&st=du2h5t6t&dl=1"
    model_path = "inswapper_128.onnx"

    generator = DeepfakeGenerator(model_url, model_path)

    while True:
        print("\n" * 10)

        print("choices: 'photo', 'video', 'exit'")

        answer = input("enter choice > ").lower()

        if "exit" == answer:
            exit()
        elif answer == "photo":
            main_img_path = input("main img path > ")
            deepfake_img_path = input("deepfake img path > ")
            output_img_path = input("output img path > ")

            generator.get_photo_deepfake(main_img_path, deepfake_img_path, output_img_path)

        elif answer == "video":
            main_video_path = input("main video path > ")
            deepfake_img_path = input("deepfake img path > ")
            output_video_path = input("output video path > ")

            generator.get_video_deepfake(main_video_path, deepfake_img_path, output_video_path)

            print(f"{output_video_path} created.")
        else:
            print("invalid syntax")

        print()


if __name__ == "__main__":
    main()
