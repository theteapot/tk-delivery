import unittest
import os
import subprocess
import json
import glob
import convert


def get_format(path):
    cmd = "ffprobe {path} -show_format -print_format json".format(path=path)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    return json.loads(stdout)


class TestValidate(unittest.TestCase):
    def setUp(self):
        """Sets up the environment for a test by downloading a video from
        youtube and turns it into a bunch of .png files.
        Requires runner to have youtube-dl and ffmpeg on the command line
        """
        try:
            os.mkdir("test_data/")
        except FileExistsError:
            print("test_data directory exists")

        try:
            os.mkdir("test_data/sequence")
        except FileExistsError:
            print("test_data/sequence directory exists")

        url = "https://www.youtube.com/watch?v=FUiu-cdu6mA"

        # Download a video from youtube
        subprocess.call(
            ["youtube-dl", url, "-o", "test_data/video.webm", "-f", "webm"])

        # Convert the downloaded video to an image sequence
        subprocess.call(
            [
                "ffmpeg",
                "-i",
                "test_data/video.webm",
                "-pix_fmt",
                "rgb24",
                "test_data/sequence/output_%04d.png",
            ]
        )

    def test_validate(self):
        self.assertEqual((".png", 4, "output_"),
                         convert.validate("test_data/sequence"))

    def test_sequence(self):
        convert.sequence(
            "test_data/sequence",
            "test_data/sequence_output.mp4",
            frame_rate=23.98,
            resolution="1920x1080",
            vcodec="libx264",
            crf=25,
            pix_fmt="rgba",
        )

        original_format = get_format("test_data/video.webm")
        new_format = get_format("test_data/sequence_output.mp4")

        self.assertAlmostEqual(
            float(original_format["format"]["duration"]),
            float(new_format["format"]["duration"]),
            places=1
        )

    def tearDown(self):
        try:
            os.remove("test_data/sequence_output.mp4")
        except FileNotFoundError:
            print("Could not remove test_data/sequence_output.mp4")

        try:
            os.remove("test_data/video.webm")
        except FileNotFoundError:
            print("Could not remove test_data/video.webm")

        for path in glob.glob("test_data/sequence/*"):
            try:
                os.remove(path)
            except FileNotFoundError:
                print("Could not remove {}".format(path))

        try:
            os.rmdir("test_data/sequence")
        except FileNotFoundError:
            print("Could not remove test_data/sequence")

        try:
            os.rmdir("test_data/")
        except FileNotFoundError:
            print("Could not remove test_data/")

        return


if __name__ == "__main__":
    unittest.main()
