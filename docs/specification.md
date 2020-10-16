## Specification

![Screenshot](spec.png)

Description of resources:
- Connectors Deployment - the server, which receives data from users, sends it to Pravega 
and returns a result, when it is ready.
- Processors Deployment - processing all messages from Pravega. It uses trained ML model from Common PVC. 
- ML-Controller - collecting dataset, training and saving ML model to Common PVC.
- ML-Trainer - resource for parallel training.
- App-operator - controller for custom resource.

## Kafka concepts

![Screenshot](kafka_conc.png)

## Libraries and other

- Flask - server
- sk-learn - ML
- eli5 - interpreting a result
- pandas - manage data
- pyyaml - config-files

ML-pipeline:
- Tokenization - req-exps (in progress)
- Lemmatization - Word-Net (in progress)
- Vectorization - TF-IDF
- Classification - logistic regression