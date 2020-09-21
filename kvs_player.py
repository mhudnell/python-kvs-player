import boto3
import cv2

STREAM_NAME = "ExampleStream"
STREAM_ARN = "arn:aws:kinesisvideo:us-east-2:686487091234:stream/ExampleStream/1600456776026"
AWS_REGION = 'us-west-2'


def hls_stream():

    kv_client = boto3.client("kinesisvideo", region_name=AWS_REGION)
    endpoint = kv_client.get_data_endpoint(
        StreamName=STREAM_NAME,
        APIName="GET_HLS_STREAMING_SESSION_URL"
    )['DataEndpoint']

    print(endpoint)

    # # Grab the HLS Stream URL from the endpoint
    kvam_client = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint, region_name=AWS_REGION)
    url = kvam_client.get_hls_streaming_session_url(
        StreamName=STREAM_NAME,
        PlaybackMode="LIVE"
    )['HLSStreamingSessionURL']

    vcap = cv2.VideoCapture(url)

    while(True):
        # Capture frame-by-frame
        ret, frame = vcap.read()

        if frame is not None:
            # Display the resulting frame
            cv2.imshow('frame', frame)

            # Press q to close the video windows before it ends if you want
            if cv2.waitKey(22) & 0xFF == ord('q'):
                break
        else:
            print("Frame is None")
            break

    # When everything done, release the capture
    vcap.release()
    cv2.destroyAllWindows()
    print("Video stop")

# def get_media_stream():
#
#     kv_client = boto3.client("kinesisvideo", region_name=AWS_REGION)
#     endpoint = kv_client.get_data_endpoint(
#         StreamName=STREAM_NAME,
#         APIName="GET_MEDIA"
#     )['DataEndpoint']
#
#     kvm_client = boto3.client('kinesis-video-media', endpoint_url=endpoint, region_name=AWS_REGION)
#     kvs_stream = kvm_client.get_media(
#                     StreamName=STREAM_NAME,
#                     StartSelector={'StartSelectorType':'NOW'}
#                 )
#
#     frame = kvs_stream['Payload'].read()
#
#     with open('/tmp/stream.avi', 'wb') as f:
#         f.write(frame)
#         vcap= cv2.VideoCapture('/tmp/stream.avi')
#
#         # display frame
#         ret, frame = vcap.read()
#         if frame is not None:
#             # Display the resulting frame
#             cv2.imshow('frame',frame)
#         else:
#             print("Frame is None")
#     print('done')


def list_available_services():
    session = boto3.Session()
    services = session.get_available_services()
    print(services)


if __name__ == '__main__':

    hls_stream()
    # get_media_stream()
    # list_available_services()
