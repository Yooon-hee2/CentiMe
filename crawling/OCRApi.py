import io
import os
import cv2
import Coordinate


#api key setting
credential_path = "./test-e94ee409efcc.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

class OCRApi:
    def detect_text(self, url):
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()

        # with io.open(path, 'rb') as image_file:
        #     content = image_file.read()

        
        image = vision.types.Image()
        image.source.image_uri = url
        # image = cv2.cvtColor(cv2.UMat(vision.types.Image(content=content)), cv2.COLOR_BGR2GRAY)
        # image = cv2.imread(path)
        # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # img = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)
        # response = client.text_detection(image=image)
        response = client.text_detection(
        image=image,
        image_context={"language_hints": ["ko"]})
        texts = response.text_annotations
        text_data_all = []
        # print('Texts:')
        i = 0
        for text in texts:
                text_data = []
                text_data.append(text.description)
                print('\n"{}"'.format(text.description))
                print(i)

                i = i + 1

                for vertex in text.bounding_poly.vertices:
                    coordinate_container = Coordinate.Coordinate()
                    coordinate_container.x_pos = vertex.x
                    coordinate_container.y_pos = vertex.y
                    text_data.append(coordinate_container)

                text_data_all.append(text_data)

                vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])

                print('bounds: {}'.format(','.join(vertices)))
                
        return text_data_all


# def detect_text_uri(uri):
#     client = vision.ImageAnnotatorClient()
#     image = vision.types.Image()
#     image.source.image_uri = uri

#     response = client.text_detection(image=image)
#     texts = response.text_annotations


#     for text in texts:
#         print('\n"{}"'.format(text.description))

# detect_text_uri("http:" + "//common-unique.com/web/upload/1703/info-cl.jpg")
