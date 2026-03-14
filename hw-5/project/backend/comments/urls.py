from rest_framework.routers import DefaultRouter

from .views import UserViewSet, PostViewSet, CommentViewSet, LikeViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"likes", LikeViewSet, basename="like")

urlpatterns = router.urls
