"""Compiles image files from website into a pdf given a root url."""
import pymupdf
import os
import requests
from lxml import html


def main():
    """Run the program."""
    head_url = "ENTER URL HERE"
    imgdir = "images"
    output_file_name = "all-my-pics.pdf"
    image_links = get_links(head_url)
    get_images(image_links, imgdir)
    compile_images(imgdir, output_file_name)

def get_links(head_url):
    """
    Gets the image links from the head_url.
    The head_url is the location is the root where all the links are stored.
    """
    mytree = html.fromstring(requests.get(head_url).content)

    # Get all links
    links = [head_url + element.attrib["href"] for element in mytree.xpath("//a")]

    # Get all links that are images.
    file_extension = ".jpg"
    image_links = [x for x in links if file_extension in x]
    print("List of all image links:")
    for link in image_links:
        print(link)
    return image_links


def get_images(image_links, imgdir):
    """Download the images using the image_links into imgdir."""
    print("Getting images:")
    for image_url in image_links:
        image_name = image_url.split("/")[-1]
        print(image_name)
        image_path = os.path.join(imgdir, image_name)
        img_data = requests.get(image_url).content
        with open(image_path, "wb") as handler:
            handler.write(img_data)

# Most of this function is from the pymupdf documentation for compiling PDFs.
def compile_images(imgdir, output_file_name):
    """Compiles all the images from imgdir into output_file_name."""
    doc = pymupdf.open()
    imglist = os.listdir(imgdir)

    imglist.sort()

    print("Compiling images:")
    for _, f in enumerate(imglist):
        print(f)
        img = pymupdf.open(os.path.join(imgdir, f))
        rect = img[0].rect
        pdfbytes = img.convert_to_pdf()
        img.close()
        imgPDF = pymupdf.open("pdf", pdfbytes)
        page = doc.new_page(
            width=rect.width,
            height=rect.height,
        )
        page.show_pdf_page(rect, imgPDF, 0)

    print("Saving file as ", output_file_name)
    doc.save(output_file_name)


if __name__ == "__main__":
    main()
