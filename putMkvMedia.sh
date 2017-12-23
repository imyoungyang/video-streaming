#!/bin/bash
# region, stream_name, mkv_file
java -Daws.accessKeyId=$1 \
-Daws.secretKey=$2 \
-Djava.library.path=./kinesis-video-native-build \
-jar ./kinesisvideo-java-demo-1.0-SNAPSHOT.jar \
$3 $4 $5
rm $5
printf "done & rm: %s\n" $5
