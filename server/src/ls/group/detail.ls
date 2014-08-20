angular.module \donvote
  ..controller \group.detail, <[$scope $http resInit urlpatterns]> ++ ($scope, $http, resInit, urlpatterns) ->
    $scope.group = resInit.group
    $scope.urlpatterns = urlpatterns

