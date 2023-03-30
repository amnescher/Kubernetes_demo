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
To access the MinIO cluster, you will need to create an access key and secret key. Once you have created these keys, you will need to convert them to base64 using the following command:

```echo YOUR_ACCESS_KEY | base64
```
```echo YOUR_SECRET_KEY | base64
```

After running thess command, you can copy the outputs and paste them into the minio-secret.yaml file as login credentials. This will allow you to log in to the MinIO cluster and access the necessary resources.

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
Once the MinIO service has been deployed, it is necessary to create a MinIO bucket and copy the model weights into it so that stable diffusion services can load these weights from the MinIO buckets.

To accomplish this, you must first download the model weights from [Here](https://eschercloudai-my.sharepoint.com/:f:/g/personal/a_sabet_eschercloud_ai/EiJWs38Yl4FDgyFYrQOhkg4BPoqlLKAhSXlhzBPDgwD18w?e=eyYqzU). Then, you can copy the weights into the MinIO bucket by running the following command:

```
python connect_minio.py --ip_address X.X.X.X  --access_key YOUR_ACCESS_KEY --secret_key YOUR_SECRET_KEY  --data_path path_to_directory_of_weight
```
In the above command, you will need to provide the IP address of the MinIO load balancer. To find the IP address, you can run the following command and replace the X.X.X.X with the 'EXTERNAL-IP' of the minio service:

```
kubectl get service -n ai-demo 
```
Note that path_to_directory_of_weight is the path to the model weights that you have downloaded. You should not change the name of the directory. For example:

```
python connect_minio.py --ip_address 123.143.167.231  --access_key my_minio --secret_key my_password123  --data_path /download/modelweight
```

Once the model weights are uploaded into the MinIO bucket, they will remain in the bucket as long as the MinIO microservice is operational.

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