sudo docker run --runtime nvidia -it --rm --network host \
    --volume ~/PROJECT/BKAR:/BKAR \
    --volume /tmp/argus_socket:/tmp/argus_socket \
    --device /dev/video0 \
    --device /dev/video1 \
    nvcr.io/nvidia/l4t-tensorflow:r34.1.0-tf2.8-py3