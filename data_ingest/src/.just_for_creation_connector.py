##Please don't use it or get scared due to this
import requests
import json

reqUrl = "127.0.0.1:8084/connectors/hdfs3-parquet-field3/config"

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Content-Type": "application/json" 
}

payload = json.dumps({
  "connector.class": "io.confluent.connect.hdfs3.Hdfs3SinkConnector",
  "topics.dir": "/usr/bdm",
  "confluent.topic.bootstrap.servers": "PLAINTEXT://kafka:9092",
  "flush.size": "10",
  "tasks.max": "1",
  "topics": "bique.transactions",
  "hdfs.url": "hdfs://10.4.41.51:27000",
  "rotate.interval.ms": "10000",
  "retry.backoff.ms": "5000",
  "log.dir": "/log/tr",
  "value.converter.schema.registry.url": "http://schema-registry:8081",
  "format.class": "io.confluent.connect.hdfs3.json.JsonFormat",
  "confluent.topic.replication.factor": "1",
  "value.converter.schemas.enable": "false",
  "name": "hdfs3-parquet-field3",
  "value.converter": "org.apache.kafka.connect.json.JsonConverter",
  "max.poll.interval.ms": "10000",
  "key.converter": "org.apache.kafka.connect.json.JsonConverter",
  "partitioner.class": "io.confluent.connect.hdfs.partitioner.HourlyPartitioner"
})

response = requests.request("PUT", reqUrl, data=payload,  headers=headersList)

print(response.text)