create_vm:
	# make nginx-build-push
	python3 '/Users/saarwintrov/devel/releai/personal-projects-1/netapp/ops/create_server.py' --create_vm

delete_vm:
	python3 '/Users/saarwintrov/devel/releai/personal-projects-1/netapp/ops/create_server.py' --delete_vm

delete_vm_disk:
	python3 '/Users/saarwintrov/devel/releai/personal-projects-1/netapp/ops/create_server.py' --delete_vm --delete_disk

nginx-build-push:
	docker build ./containers/nginx -f ./containers/nginx/Dockerfile -t nginx
	docker tag nginx wintrov/nginx:latest
	docker push wintrov/nginx:latest
