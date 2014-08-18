angular.module \donvote
  ..controller \discuss, ($scope, $http, stateIndicator) ->
    
    $scope.newDiscuss = ->
      url = if ownerapi? => ownerapi else \/api/discuss/
      console.log url
      $scope.state.loading!
      $http do
        url: url
        method: \POST
        data: JSON.stringify($scope.data)
      .success (d) -> $scope.state.done!
      .error (e) -> 
        console.error e
        $scope.state.fail!

    $scope.state = stateIndicator.init!
    $scope.tend = -> $scope.data.tendency = it
    $scope.reset = -> $scope.data = tendency: 2

    $scope.reset!
