import boto3
import cv2

if __name__ == "__main__":

    # 비교할 사진과 비교할 대상이 있는 사진의 경로를 지정한다.
    sourceFile = '../img/source.jpg'
    targetFile = '../img/target.jpg'

    # Amazon Rekognition API 사용을 위한 client를 선언한다.
    # aws_access_key_id, aws_secret_access_key 절대 공개 금지.
    client = boto3.client('rekognition', region_name='ap-northeast-2',
                          aws_access_key_id='XXXXXX', aws_secret_access_key='XXXXXX')

    # 이미지를 바이너리 파일로 연다. (Amazon Rekognition API 형태의 맞추는 것.)
    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')

    # 타켓 이미지에 경계 박스를 그려주기 위하여 opencv 라이브러리를 이용하여 이미지를 읽는다.
    a = cv2.imread(targetFile)

    # Amazon Rekognition 의 compare face API
    response = client.compare_faces(SimilarityThreshold=70,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    # 결과 중 필요한 정보 (position, confidence, similarity) 를 출력하고, position 값을 이용하여 경계 박스를 그려준다.
    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        confidence = str(faceMatch['Face']['Confidence'])
        print('The face at ' +
              str(position['Left']) + ' ' +
              str(position['Top']) + ' ' + str(position) +
              ' matches with ' + confidence + '% confidence')
        print(faceMatch['Similarity'])

        # position이 상대적인 표현이기 때문에 이미지의 크기를 곱하여 절대적인 좌표를 알아내야 한다.
        top = int(a.shape[0] * position['Top'])
        left = int(a.shape[1] * position['Left'])
        bottom = int(top + a.shape[0] * position['Height'])
        right = int(left + a.shape[1] * position['Width'])
        # confidence: probability including face in bounding box (경계 박스 안에 얼굴이 있을 확률)
        # similarity: how face is similar (얼마나 얼굴이 비슷한지에 대한 유사도)

        # 경계 박스 그려주기
        a = cv2.rectangle(img=a, pt1=(left, top), pt2=(right, bottom), color=(0, 255, 0), thickness=3)

        # 이미지 출력 및 저장
        cv2.imshow('hi', a)
        cv2.imwrite('../result.png', a)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    imageSource.close()
    imageTarget.close()

