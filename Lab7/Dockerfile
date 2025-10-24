FROM jenkins/jenkins:lts

USER root 

RUN jenkins-plugin-cli --plugins workflow-aggregator git docker-workflow


EXPOSE 8080
EXPOSE 50000