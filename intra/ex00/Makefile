NAME=datascience

SRCS=src/docker-compose.yml

$(NAME):
	docker-compose -p $(NAME) -f $(SRCS) up -d --build

start:
	docker-compose -p $(NAME) -f $(SRCS) start

stop:
	docker-compose -p $(NAME) -f $(SRCS) stop

logs:
	docker-compose -p $(NAME) -f $(SRCS) logs

all: $(NAME)

update:
	docker-compose -p $(NAME) -f $(SRCS) up -d 

down:	
	docker-compose -p $(NAME) -f $(SRCS) down

clean:
	docker-compose -p $(NAME) -f $(SRCS) down -v


fclean:  
	docker-compose -p $(NAME) -f $(SRCS) down -v --rmi all
	docker network prune -f
	docker system prune -a --volumes

re:	fclean all

.PHONY: all up clean fclean re start stop  logs
