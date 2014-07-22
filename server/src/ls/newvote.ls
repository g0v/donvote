angular.module \donvote
  ..controller \newvote, ($scope) ->
    $scope.plan = do
      name: ""
      desc: ""
    $scope.vote = do
      name: ""
      desc: ""
      startCountDown: 3600000
      duration: 86400000
      endCountDown: 3600000
      planCount: 1
      qualifiedRate: 50
      karmaRate: 10
      karmaCount: 10
      agreeRate: 30
      closeQuestionRate: 90
      voteRate: 75
      maxChoiceCount: 2
      rankMethod: 1
      endDateType: 1
      disclosedBallot: false
      nullTicketRate: 30
      validVoteRate: 75
      obtainRate: 30
    $scope.quick = {}
    $scope.custom = do
      time: false
      plan: false
      perm: false
      adv: false
      disclosedBallot: 0
      endDateType: 1

    quick-time-update = (v) -> if v =>
      if v[1] =>
        $scope.vote <<< do
          startDate: new Date!getTime! # TODO
          startMethod: {2:true}
          endMethod: {1:true}
      else if v[2] =>
        $scope.vote <<< do
          startMethod: {1:true}
          endMethod: {1:true}
      else if v[3] =>
        $scope.vote <<< do
          startDate: new Date!getTime! # TODO
          startMethod: {2:true}
          endMethod: {2:true}
          endByDuration: true
          duration: [1,0,0] # TODO
    quick-plan-update = (v) -> if v =>
      if v[1] =>
        $scope.vote.voteMethod = {1:true}
        $scope.vote.plan = 
          * name: \贊同
          * name: \反對
      else if v[2] =>
        $scope.vote.plan = 
          * name: \贊同
          * name: \反對
          * name: \無感
        $scope.vote.voteMethod = {1:true}
      else =>
        $scope.vote.voteMethod = {4:true}
    $scope.$watch 'quick.time', quick-time-update
    $scope.$watch 'custom.time', -> quick-time-update $scope.quick.time
    $scope.$watch 'quick.plan', quick-plan-update
    $scope.$watch 'custom.plan', -> quick-plan-update $scope.quick.plan
    $scope.newplan = (p) -> if p.name =>
      $scope.vote.plan.push {} <<< p{name, desc}
    $scope.removeplan = (p) ->
      $scope.vote.plan = $scope.vote.plan.filter -> it.name != p.name
    $scope.newvote = (v) ->
      console.log v
