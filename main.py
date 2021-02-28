#!/usr/bin/python3
import widgets
import convert
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(column=3, row=3)
        self.create_widgets()
        self.sequence_path = ""

        self.output_conversion_controls = {"frame_rate": "", "resolution": ""}

    def create_widgets(self):
        """Initialize all of the widgets"""

        # Conversion user input controls
        self.frame_conversion_controls = tk.Frame(self.master)
        self.frame_conversion_controls.grid(row=1, column=1)

        # Create Input Widgets
        self.widget_frame_rate = widgets.EntryWidget(
            self.frame_conversion_controls, "Frame Rate"
        )
        self.widget_frame_rate.pack()
        self.widget_resolution = widgets.EntryWidget(
            self.frame_conversion_controls, "Resolution"
        )
        self.widget_resolution.pack()
        self.widget_output_name = widgets.EntryWidget(
            self.frame_conversion_controls, "Output Name"
        )
        self.widget_output_name.pack()
        self.widget_video_codec = widgets.OptionWidget(
            self.frame_conversion_controls, "Video Codec", ["h264"]
        )
        self.widget_video_codec.pack()
        self.widget_pixel_format = widgets.OptionWidget(
            self.frame_conversion_controls, "Pixel Format", ["rgba"]
        )
        self.widget_pixel_format.pack()

        # File browser
        self.frame_directory = tk.Frame(self.master, bg="blue")
        self.frame_directory.grid(row=0, column=3)

        self.widget_directory = widgets.DirectoryWidget(
            self.frame_directory, "Select a directory"
        )
        self.widget_directory.pack()

        # Convert sequence

        self.button_convert_sequence = tk.Button(
            self,
            text="Convert button",
            command=lambda: convert.sequence(
                path=self.widget_directory.get(),
                output_name=self.widget_output_name.get(),
                frame_rate=self.widget_frame_rate.get(),
                resolution=self.widget_resolution.get(),
                vcodec=self.widget_video_codec.get(),
                pix_fmt=self.widget_pixel_format.get(),
            ),
        )
        self.button_convert_sequence.pack(side="bottom")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
