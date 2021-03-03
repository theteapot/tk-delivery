import re
import os
import subprocess


def validate(folder_path):
    """Checks files in a folder to see if they all have the same naming convention
    Returns information about what that naming convention is

    Args:
        folder_path (string): The path of the folder containing the sequence 
        to verify
    """
    check_filename = ""
    check_sequence_number = ""
    check_extension = ""

    files = os.listdir(folder_path)

    if len(files) == 0:
        raise FileNotFoundError("Selected folder has no files in it")

    # Anything after a '.' is matched, e.g. abc.png -> .png
    for file in files:
        extension = re.search(r"\.(.*)", file)
        if extension is None:
            raise FileNotFoundError(
                "Selected folder has no files with extensions")
        extension = extension.group()

        if check_extension == "":
            check_extension = extension
        elif check_extension != extension:
            raise ValueError(
                "Extension differs, expected: %s but got: %s"
                % (extension, check_extension)
            )

        # All numbers matched before the extension, e.g. abc123.png -> 123
        sequence_number_regex = r"(\d*)(?=%s)" % extension.replace(".", "\.")
        sequence_number = re.search(sequence_number_regex, file).group()

        if check_sequence_number == "":
            check_sequence_number = sequence_number
        elif len(check_sequence_number) != len(sequence_number):
            raise ValueError(
                "Sequence number length differs, expected %s but got %s"
                % (len(sequence_number), len(check_sequence_number))
            )

        # Anything left over after the sequence_number and extension are
        # removed
        filename = file.replace(sequence_number + extension, "")
        if check_filename == "":
            check_filename = filename
        elif check_filename != filename:
            raise ValueError(
                "Filenames differ, expected: %s but got: %s"
                % (filename, check_filename)
            )

    return (check_extension, len(check_sequence_number), check_filename)


def sequence(
    path,
    output_name,
    frame_rate=23.98,
    resolution="1920x1080",
    vcodec="libx264",
    crf=25,
    pix_fmt="rgba",
):

    extension, sequence_number_length, filename = validate(path)

    # TODO: add windows compatibility, formatting with %0d
    input_path = "{}/{}%0{}d{}".format(
        path, filename, sequence_number_length, extension
    )

    subprocess.call(
        [
            "ffmpeg",
            "-r",
            str(frame_rate),
            "-f",
            "image2",
            "-s",
            resolution,
            "-i",
            input_path,
            "-vcodec",
            vcodec,
            "-crf",
            str(crf),
            "-pix_fmt",
            pix_fmt,
            output_name,
            "-y",
        ]
    )

    return
