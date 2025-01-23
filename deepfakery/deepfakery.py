#!usr/bin/python3

import numpy as np
import numpy.typing as npt
import urllib.request
import insightface
import cv2
from pathlib import Path


class DeepfakeGenerator:
    def __init__(self, model_url: str, model_path: str) -> None:
        self.model_url = model_url
        self.model_path = model_path
        self._download_model_if_needed()
        self.swapper = insightface.model_zoo.get_model(
            self.model_path, download=False, download_zip=False
        )
        self.app = insightface.app.FaceAnalysis(name="buffalo_l")
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def _download_model_if_needed(self) -> None:
        if not Path.exists(Path(self.model_path)):
            print(f"Model not found at {self.model_path}. Downloading...")

            try:
                urllib.request.urlretrieve(self.model_url, self.model_path)
                print(f"Model downloaded to {self.model_path}")
            except Exception as e:
                print(f"Failed to download the model: {e}")
                raise
        else:
            print(f"Model already exists at {self.model_path}.")

    @staticmethod
    def write_frames_to_video(
        frames: list[npt.NDArray[np.uint8]], output_path: str, fps: float
    ) -> None:
        if not frames:
            print("No frames to write.")
            return

        height, width, _ = frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        for frame in frames:
            out.write(frame)

        out.release()

    def load_face(self, img: npt.NDArray[np.uint8], multiple: bool = False) -> None:
        img_faces = self.app.get(img)

        if not img_faces:
            print("No faces detected.")
            return None

        if multiple:
            return img_faces

        if len(img_faces) != 1:
            print("Multiple faces detected, but only one was expected.")
            return None

        return img_faces[0]

    def get_deepfake_frame(
        self, main_img: npt.NDArray[np.uint8], deepfake_face: npt.NDArray[np.uint8]
    ) -> npt.NDArray[np.uint8]:
        main_faces = self.load_face(main_img, multiple=True)
        if not main_faces:
            return main_img

        res = main_img.copy()
        for main_face in main_faces:
            res = self.swapper.get(res, main_face, deepfake_face, paste_back=True)

        return res

    @staticmethod
    def extract_mp4_frames(mp4_path: str) -> tuple[list[npt.NDArray[np.uint8]], float]:
        cap = cv2.VideoCapture(mp4_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {mp4_path}")
            return [], 0

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        frames = []
        try:
            for i in range(total_frames):
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
                if i % 10 == 0:
                    print(f"Reading frames: {i + 1}/{total_frames}")
        except Exception as e:
            print(f"Error while reading frames: {e}")
            raise
        finally:
            cap.release()

        return frames, fps

    def get_video_deepfake(
        self, main_video_path: str, deepfake_img_path: str, output_path: str
    ) -> None:
        print("Loading video...")
        cap = cv2.VideoCapture(main_video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {main_video_path}")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        deepfake_img = cv2.imread(deepfake_img_path)
        if deepfake_img is None:
            print(f"Error: Failed to load image at {deepfake_img_path}")
            return

        deepfake_face = self.load_face(deepfake_img)
        if deepfake_face is None:
            print("Deepfake face could not be loaded.")
            return

        try:
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1
                print(f"Processing frame {frame_count}/{total_frames}")

                deepfake_frame = self.get_deepfake_frame(frame, deepfake_face)
                out.write(deepfake_frame)

                del deepfake_frame

                if frame_count % 10 == 0:
                    print(f"Progress: {(frame_count / total_frames) * 100:.2f}%")

        except Exception as e:
            print(f"Error during video processing: {e}")
            raise
        finally:
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            print(f"Video processing completed. Output saved to {output_path}")

    def get_photo_deepfake(
        self, main_img_path: str, deepfake_img_path: str, output_path: str
    ) -> None:
        main_img_path = Path(main_img_path).expanduser()
        deepfake_img_path = Path(deepfake_img_path).expanduser()
        output_path = Path(output_path).expanduser()

        if not Path(main_img_path).exists():
            print(f"Error: {main_img_path} does not exist.")
            return

        if not Path(deepfake_img_path).exists():
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
        if not main_faces:
            print("No faces detected in the main image.")
            return

        deepfake_face = self.load_face(deepfake_img)
        if deepfake_face is None:
            print("Deepfake face could not be loaded.")
            return

        res = main_img.copy()

        for main_face in main_faces:
            res = self.swapper.get(res, main_face, deepfake_face, paste_back=True)

        cv2.imwrite(output_path, res)
        print(f"{output_path} created.")


def main() -> None:
    model_url = "https://www.dropbox.com/scl/fi/tx59r655h4ke5414s80o3/inswapper_128.onnx?rlkey=p9ktqp27w1bxzc3s30dzb9832&st=yxc54uuw&dl=1"
    model_path = "inswapper_128.onnx"

    generator = DeepfakeGenerator(model_url, model_path)

    print("\n" * 1000)

    while True:
        print('choices: "photo", "video", "exit"')

        answer = input("enter choice > ").lower()

        if answer == "exit":
            break

        if answer == "photo":
            main_img_path = input("main img path > ")
            deepfake_img_path = input("deepfake img path > ")
            output_img_path = input("output img path > ")

            generator.get_photo_deepfake(
                main_img_path, deepfake_img_path, output_img_path
            )

        elif answer == "video":
            main_video_path = input("main video path > ")
            deepfake_img_path = input("deepfake img path > ")
            output_video_path = input("output video path > ")

            generator.get_video_deepfake(
                main_video_path, deepfake_img_path, output_video_path
            )
        else:
            print("invalid syntax")

        print()


if __name__ == "__main__":
    main()
