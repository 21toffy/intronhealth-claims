#!/bin/bash

docker build -t oluwatofunmi/intron-health-service .

docker push oluwatofunmi/intron-health-service

# docker run -d -p 80:5000 oluwatofunmi/intron-health-service