
angular.module \donvote
  ..controller \newvote, ($scope, $http) ->
    $scope.new = {}
    $scope.submit = ->
      $http do
        url: \/vote/
        method: \POST
        data: JSON.stringify($scope.new)
      .success (e) -> console.log "ok:", e
      .error (e) -> console.log "failed:", e
