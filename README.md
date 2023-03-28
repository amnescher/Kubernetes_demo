## Configure the Git Container Registry (GCR)

To pull microservice image from Github Container Registry, a personal access token needs to be provided to be able to pull images from GCR. Having `GIT_TOKEN`, it needs to be added to Docker authentication file using the following command:

```
docker login ghcr.io -u USERNAME --password GIT_TOKEN
```

You need to copy the entire output of the `cat ~/.docker/config.json | base64` command into the data section of `github-secret.yaml` file. This includes all of the lines of base64-encoded text that were output by the command.



Then deploy the `github-secret.yaml` file in your Kubernetes cluster by using the following command:

```
kubectl -f github-secret.yaml apply 
```
## Set up Minio service
To set the Minio login credentials, deploy the minio-secret.yaml file as follows:
```
kubectl apply -f minio-secret.yaml
```
Configure the ports of services by deploying the config-map.yaml file:
```
kubectl apply -f config-map.yaml
```
Deploy the Minio microservice:
```
kubectl apply -f minio-deployment.yaml
```
Once the Minio service is deployed, you can log in to Minio through the URL http://localhost:9090/. Make a bucket and name it "modelweights". Please download model weights  from [Here](https://eschercloudai-my.sharepoint.com/:f:/g/personal/a_sabet_eschercloud_ai/EiJWs38Yl4FDgyFYrQOhkg4BPoqlLKAhSXlhzBPDgwD18w?e=YLaybW). Upload the model weights to the following directories that you need to make in the "modelweights" Minio bucket:
```
model_weights/diff2/model_v2_768.ckpt
model_weights/diff2/x4-upscaler-ema.ckpt
model_weights/diff2/512-inpainting-ema.ckpt
model_weights/diff1/model_v1.ckpt
```
Once model weights are uploaded into Minio buckets, the model weights will live in the buckets as long as the Minio microservice is alive.

## Deploy Stable diffusion services

Deploy the Stable diffusion 1 pod and service:
```
kubectl apply -f stablediffusion1-deployment.yaml
```
Deploy the Stable diffusion 2 pod and service:
```
kubectl apply -f stablediffusion2-deployment.yaml
```

## Find the URL for the frontend of the service
To find the services, use the following command:
```
kubectl get service
```
Note the "EXTERNAL-IP" of the frontend service. Hit the "EXTERNAL-IP" of the frontend service to access the application frontend.