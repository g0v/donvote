angular.module \donvote
  ..controller \group.edit, <[$scope $http resInit urlpatterns]> ++ ($scope, $http, resInit, urlpatterns) ->
    $scope.group = {}
    $scope.create = ->
      $http do
        url: urlpatterns.api_create_group()
        method: \POST
        data: JSON.stringify($scope.group)
      .success (e) -> console.log e
      .error (e) -> console.error e
     
