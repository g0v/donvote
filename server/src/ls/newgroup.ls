angular.module \donvote
  ..controller \group, <[$scope $http]> ++ ($scope, $http) ->
    $scope.group = {}
    $scope.submit = ->
      console.log \ok
      $http do
        url: \/api/group/new/
        method: \POST
        data: JSON.stringify($scope.group)
      .success (e) -> console.log e
      .error (e) -> console.error e
     
