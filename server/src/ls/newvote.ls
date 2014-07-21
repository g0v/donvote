angular.module \donvote
  ..controller \newvote, ($scope) ->
    $scope.vote = {planQualifiedRate: 50, planKarmaRate: 10, planKarmaCount: 10, agreeRate: 30, closeQuestionRate: 90}
    $scope.quick = {}
    $scope.custom = do
      time: false
      plan: false
      perm: false

