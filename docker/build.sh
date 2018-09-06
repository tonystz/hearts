#!/bin/sh
docker build -t ai.registry.trendmicro.com/063/trend-hearts:practice .
docker build -t ai.registry.trendmicro.com/063/trend-hearts:rank .

echo docker run -v /pub/:/log --rm ai.registry.trendmicro.com/063/trend-hearts:practice 123 111 ws://127.0.0.1:8080

docker login ai.registry.trendmicro.com
docker push  ai.registry.trendmicro.com/063/trend-hearts:practice
docker push  ai.registry.trendmicro.com/063/trend-hearts:rank 
