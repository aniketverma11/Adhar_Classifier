def prepare_image_local(image_path):
    try:
        # Loads the image into memory
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        return image
    except Exception as e:
        print(e)
        return ""

def prepare_image_web(url):
    try:
        # Loads the image into memory
        image = vision.Image()
        image.source.image_uri = url
        return image
    except Exception as e:
        print(e)
        return ""

def text_detection(url):
        response = client.text_detection(image=self.image)
        texts = response.text_annotations
        if texts:
            results = []
            for text in texts:
                results.append(self.Text_Detection(text.description, text.bounding_poly.vertices))
            return results
        return ""