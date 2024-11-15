from src.news.controllers import user_router
from src.users.controllers import news_router

all_routers = [
    user_router,
    news_router,
]
