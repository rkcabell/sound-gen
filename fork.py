from vpython import *
import numpy as np
import sounddevice as sd

# Shared properties
N = 3.516015  # Constant for all instances
width = 1.5
E_values = {  # Common for all instances
    "Steel": 210e9,
    "Chitin_thin": 20e9,
    "Chitin_dense": 45e9,
    "Bone_thin": 70e9,
    "Bone_dense": 114e9,
    "Hydroxyapatite": 15e9,
    "Hardwood": 13e9,
}
SAMPLE_RATE = 44100


class TuningFork:
    def __init__(self, length, height, density, shape):
        self.length = length
        self.height = height
        self.cross_section_area = width * self.height
        self.density = density
        self.shape = shape
        self.young_modulus = E_values["Steel"]
        self.sample_rate = SAMPLE_RATE
        self.moment = (1 / 12) * width * self.height**3
        self.frequency = self.calculate_frequency()
        self.area = self.height**2
        self.canvas = canvas(
            title=f"Tuning Fork - {shape.capitalize()}", width=600, height=400
        )
        self.left_prong = None
        self.right_prong = None
        self.update_prongs_shape(self.shape)
        self.setup_scene()
        self.update()

    def setup_scene(self):
        """Setup the initial scene for this fork."""

        scene = self.canvas

        self.btn_rect = button(
            text="Rectangular Prongs",
            bind=lambda: self.update_prongs_shape("rectangle"),
        )
        self.btn_cyl = button(
            text="Cylindrical Prongs", bind=lambda: self.update_prongs_shape("cylinder")
        )

        self.play_button = button(text="Play Sound", bind=self.play_sound)
        scene.append_to_caption("\n\n")

        scene.append_to_caption("N (Constant): 3.516015\n")
        scene.append_to_caption("\n\n")

        # Material selection dropdown
        scene.append_to_caption("Select Material for Young's Modulus (E): ")
        self.E_dropdown = menu(
            choices=[key for key in E_values.keys()], index=0, bind=self.set_material
        )
        scene.append_to_caption("\n\n")

        # Length slider and label
        scene.append_to_caption("Length (L) of Prongs: ")
        self.L_slider = slider(
            min=0.1, max=1.5, value=0.8, step=0.1, bind=self.update, length=220
        )
        scene.append_to_caption("\n\n")

        scene.append_to_caption("Width (W) of Prongs: " + str(width))
        scene.append_to_caption("\n\n")

        scene.append_to_caption("Height (H) of Prongs: ")
        self.H_slider = slider(
            min=0.01, max=0.1, value=0.01, step=0.01, bind=self.update, length=220
        )
        scene.append_to_caption("\n\n")

        self.area_label = wtext(text="Area (A): 0.00 m^2")
        scene.append_to_caption("\n")

        self.moment_label = wtext(text="Second Moment of Area (I): 0.00 m^4")
        scene.append_to_caption("\n")

        self.freq_label = wtext(text="Playing at frequency (f): 0.00 Hz")
        scene.append_to_caption("\n\n")

        self.update()

    def update(self):
        """
        # Calculate and update physical properties based on current settings.
        # Lvalue is passde in from L_slider.value
        # Hvalue is passde in from h_slider.value
        # Returns: text to be set to area_label.text, moment_label.txt, and frequency_label.text
        """
        self.length = self.L_slider.value
        self.height = self.H_slider.value
        self.cross_section_area = width * self.height
        self.moment = (1 / 12) * width * self.height**3
        self.frequency = self.calculate_frequency()
        self.area_label.text = f"Area (A): {self.cross_section_area:.4f} m^2"
        self.moment_label.text = f"Second Moment of Area (I): {self.moment:.6f} m^4"
        self.freq_label.text = f"Playing at frequency (f): {self.frequency:.2f} Hz"

    def calculate_frequency(self):
        """Calculate the frequency based on physical properties."""
        return (N / (2 * np.pi * self.length**2)) * np.sqrt(
            (self.young_modulus * self.moment)
            / (self.density * self.cross_section_area)
        )

    def set_material(self, material):
        """Set the material and update modulus and frequency."""
        if material in E_values:
            self.young_modulus = E_values[material]
            self.frequency = self.calculate_frequency()

    def update_prongs_shape(self, shape):
        # Handle
        cylinder(
            pos=vector(0, 0, 0),
            axis=vector(0, 1, 0),
            radius=0.05,
            length=1,
            color=color.gray(0.6),
        )

        # Update the visualization and frequency label
        if shape == "rectangle":
            print("setting prongs to rectangle")
            self.set_rectangular_prongs()
        else:
            print("setting prongs to cylinder")
            self.set_cylindrical_prongs()

    def set_rectangular_prongs(self):
        # Remove existing prongs if they exist
        if self.left_prong:
            self.left_prong.visible = False
            del self.left_prong
        if self.right_prong:
            self.right_prong.visible = False
            del self.right_prong

        # Create new prongs as attributes of this instance
        self.left_prong = box(
            canvas=self.canvas,
            pos=vector(-0.05, 1.35, 0),
            length=0.02,
            height=0.7,
            width=0.05,
            color=color.gray(0.6),
        )
        self.right_prong = box(
            canvas=self.canvas,
            pos=vector(0.05, 1.35, 0),
            length=0.02,
            height=0.7,
            width=0.05,
            color=color.gray(0.6),
        )

    def set_cylindrical_prongs(self):
        # Remove existing prongs if they exist
        if self.left_prong:
            self.left_prong.visible = False
            del self.left_prong
        if self.right_prong:
            self.right_prong.visible = False
            del self.right_prong

        # Create new cylindrical prongs
        self.left_prong = cylinder(
            canvas=self.canvas,
            pos=vector(-0.05, 1, 0),
            axis=vector(0, 1, 0),
            radius=0.03,
            length=0.7,
            color=color.gray(0.6),
        )
        self.right_prong = cylinder(
            canvas=self.canvas,
            pos=vector(0.05, 1, 0),
            axis=vector(0, 1, 0),
            radius=0.03,
            length=0.7,
            color=color.gray(0.6),
        )

    # Generate tone based on frequency
    def generate_tone(self, freq, duration=2):
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        waveform = 0.5 * np.sin(2 * np.pi * freq * t)
        return waveform

    # Play sound function
    def play_sound(self):
        # freq = frequency(N, L, E, I, P, A)
        tone = self.generate_tone(self.frequency)
        sd.play(tone, self.sample_rate)
        sd.wait()
