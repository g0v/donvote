angular.module \donvote
  ..controller \karma, ($scope, $http, stateIndicator) ->
    
    $scope.newKarma = ->
      url = if ownerapi? => ownerapi else \/api/discuss/
      url = \/api/discuss/3/karma/
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
    $scope.tend = -> $scope.data.value = it
    $scope.reset = -> $scope.data = value: 2

    $scope.reset!

    #TODO need update
