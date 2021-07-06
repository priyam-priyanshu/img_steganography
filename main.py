from PIL import Image, ImageDraw, ImageFont
import textwrap


def msg_img(ref_image, secret_txt):
    text_to_write = secret_txt                                                  # Input Secret Message
    img = Image.open(ref_image)                                                 # Opens image (jisme encode krna hai), size ke liye
    dimension = img.size                                                        # Image ki dimesion utha li
    img.close()

    image_text = Image.new("RGB", dimension)                                    # Creating new image of same dimension and embedding the secret message
    drawer = ImageDraw.Draw(image_text)

    font = ImageFont.truetype("D:\Programming & Stuffs\ISDF\Stegenography\sources\WorkSans-Italic-VariableFont_wght.ttf", 80)
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)                          # text written
        offset += 10

    # image_text.show()                                                         # For testing purpose
    return image_text



def encoding_msg(raw_image, secret_msg):
    raw_img = Image.open(raw_image)                             # Open Image

    red_pigment = raw_img.split()[0]                              # Extracting RGB
    green_pigment = raw_img.split()[1]
    blue_pigment = raw_img.split()[2]

    x_coordinate = raw_img.size[0]
    y_coordinate = raw_img.size[1]

    msg = msg_img(raw_image, secret_msg)
    bw_msg_img = msg.convert("1")
    encoded_img = Image.new("RGB", (x_coordinate, y_coordinate))
    pixels = encoded_img.load()

    # print(msg.getpixel((178, 79)))                    # For testing purpose
    # raw_img.convert("1").show()
    # print(bw_msg_img.getpixel((180,79)))


    for i in range(x_coordinate):
        for j in range(y_coordinate):
            red_template_pix = bin(red_pigment.getpixel((i,j)))
            tencode_pix = bin(bw_msg_img.getpixel((i,j)))

            # ---------For Testing Purpose---------------
            # print(tencode_pix,tencode_pix[-1], sep="--msg--")
            # print(red_template_pix ,red_template_pix[:-1], sep="--raw--")
            # print("____")

            if tencode_pix[-1] == "1":
                red_template_pix = red_template_pix[:-1] + "1"
            else:
                red_template_pix = red_template_pix[:-1] + "0"

            pixels[i,j] = int(red_template_pix, 2), green_pigment.getpixel((i,j)), blue_pigment.getpixel((i,j))
    print("")
    encoded_img.show()
    encoded_img.save("Output\encoded_img.png")
    pass

def decode_msg(secret_msg):
    encoded_msg = Image.open(secret_msg)
    red_pigment = encoded_msg.split()[0]

    x_size = encoded_msg.size[0]
    y_size = encoded_msg.size[1]

    decoded_img = Image.new("RGB", encoded_msg.size)
    pixels = decoded_img.load()

    for i in range(x_size):
        for j in range(y_size):
            if bin(red_pigment.getpixel((i,j)))[-1] == "0":
                pixels[i,j] = (0,0,0)
            else:
                pixels[i,j] = (255,255,255)
    decoded_img.show()
    decoded_img.save("Output\decoded_img.png")
    pass


# def test():
#     sample = msg_img("sample.jpg", "This is a message").convert("1")
#     new_img = Image.new("RGB", sample.size)
#     pixels = new_img.load()
#
#     print("Loops Starts")
#     for i in range(sample.size[0]):
#         for j in range(sample.size[1]):
#             if bin(sample.getpixel((i,j)))[-1] == "0":
#                 pixels[i,j] = (0,0,0)
#             else:
#                 pixels[i,j] = (255,255,255)
#
#     new_img.show()
#     sample.show()
#     print("Loop ends")

# test()


'''
Please uncomment one of the following functions to execute the respective task.
Find your output in the Output folder
'''

#encoding_msg("sample.jpg", "Hello Mumma")
#decode_msg("Output\encoded_img.png")
