
eksctl create cluster \
    --region us-east-1 \
    --name saar-demo \
    --version 1.21 \
    --region us-east-1 \
    --nodegroup-name linux-nodes\
    --node-type t3.small \
    --nodes 2
