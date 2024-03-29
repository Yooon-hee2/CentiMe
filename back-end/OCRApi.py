import io
import os
import cv2

class Coordinate:
    def __init__(self):
            self.x_pos = 0
            self.y_pos = 0


#api key setting
credential_path = "./test-e94ee409efcc.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# 이게 진짜 class
class OCRApi:
    def detect_text(self, input_image):
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        
        real_image = vision.types.Image(content=cv2.imencode('.jpg', input_image)[1].tostring())
        response = client.text_detection(
            image=real_image,
            image_context={"language_hints": ["ko"]})
        texts = response.text_annotations
        text_data_all = []
        i = 0

        if len(texts) > 0:
            for text in texts:
                text_data = []
                text_data.append(text.description)
                #print('\n"{}"'.format(text.description))
                # print(i)

                i = i + 1

                for vertex in text.bounding_poly.vertices:
                    coordinate_container = Coordinate()
                    coordinate_container.x_pos = vertex.x
                    coordinate_container.y_pos = vertex.y
                    text_data.append(coordinate_container)

                text_data_all.append(text_data)

                vertices = (['({},{})'.format(vertex.x, vertex.y)
                             for vertex in text.bounding_poly.vertices])

                # print('bounds: {}'.format(','.join(vertices)))
        else:
            print("fail to OCR")

        return text_data_all

# # 아현이랑 연결안할때 사용
# class OCRApi:
#     def detect_text(self, url):
#         from google.cloud import vision
#         client = vision.ImageAnnotatorClient()

#         image = vision.types.Image()
#         image.source.image_uri = url
#         response = client.text_detection(
#             image=image,
#             image_context={"language_hints": ["ko"]})
#         texts = response.text_annotations
#         text_data_all = []
#         i = 0

#         if len(texts) > 0:
#             for text in texts:
#                 text_data = []
#                 text_data.append(text.description)
#                 #print('\n"{}"'.format(text.description))
#                 #print(i)

#                 i = i + 1

#                 for vertex in text.bounding_poly.vertices:
#                     coordinate_container = Coordinate()
#                     coordinate_container.x_pos = vertex.x
#                     coordinate_container.y_pos = vertex.y
#                     text_data.append(coordinate_container)

#                 text_data_all.append(text_data)

#                 vertices = (['({},{})'.format(vertex.x, vertex.y)
#                              for vertex in text.bounding_poly.vertices])

#                 #print('bounds: {}'.format(','.join(vertices)))
#         else:
#             print("fail to OCR")
#             return False

#         return text_data_all