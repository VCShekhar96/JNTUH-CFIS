
from PIL import Image

def inspect_rgb_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")

        width, height = img.size
        print(f"Image dimensions: {width}x{height} pixels")
        print(f"Total pixels: {width * height}")

        print("\nRGB values of every pixel:")

        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                print(
                    f"Coordinates: ({x}, {y}) -> "
                    f"Red: {r}, Green: {g}, Blue: {b}"
                )

    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    print("=== RGB Image Inspector ===")
    user_image_path = input("Enter the image path: ")
    inspect_rgb_image(user_image_path)
