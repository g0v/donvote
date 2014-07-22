angular.module \donvote
  ..controller \newvote, ($scope, $timeout, $http) ->
    $scope.clean = ->
      $scope.plan = do
        name: ""
        desc: ""
      $scope.vote = do
        name: ""
        desc: ""
        karma: []
        plan: []
        discuss: []
        startDate: new Date!
        startCountDown: 3600000
        duration: 86400000
        endCountDown: 3600000
        planCount: 2
        qualifiedRate: 25
        karmaRate: 10
        karmaCount: 10
        agreeRate: 20
        answerRate: 80
        voteRate: 75
        maxChoiceCount: 2
        rankMethod: '1'
        endByDuration: false
        disclosedBallot: false
        nullTicketRate: 40
        validVoteRate: 66
        obtainRate: 30
      $scope.quick = {}
      $scope.custom = do
        time: false
        plan: false
        perm: false
        adv: false
        disclosedBallot: 0
        endDateType: 1
    $scope.clean!
    $scope.$watch 'custom.disclosedBallot' (v) -> $scope.vote.disclosedBallot = if v => true else false
    $scope.$watch 'vote.disclosedBallot' (v) -> $scope.custom.disclosedBallot = if v => 1 else 0
    quick-time-update = (v) -> if v =>
      if v[1] =>
        $scope.vote <<< do
          startDate: new Date!
          startMethod: '2'
          endMethod: '1'
      else if v[2] =>
        $scope.vote <<< do
          startMethod: '1'
          endMethod: '1'
      else if v[3] =>
        $scope.vote <<< do
          startDate: new Date!
          startMethod: '2'
          endMethod: '2'
          endByDuration: true
          duration: 86400000
    quick-plan-update = (v) -> if v =>
      if v[1] =>
        $scope.vote.voteMethod = '1'
        $scope.vote.plan = 
          * name: \贊同
          * name: \反對
      else if v[2] =>
        $scope.vote.plan = 
          * name: \贊同
          * name: \反對
          * name: \無感
        $scope.vote.voteMethod = '1'
      else =>
        $scope.vote.voteMethod = '4'
    $scope.$watch 'quick.time', quick-time-update
    $scope.$watch 'custom.time', -> if !it => quick-time-update $scope.quick.time
    $scope.$watch 'quick.plan', quick-plan-update
    $scope.$watch 'custom.plan', -> if !it => quick-plan-update $scope.quick.plan
    $scope.newplan = (p) -> if p.name =>
      $scope.vote.plan.push {} <<< p{name, desc}
    $scope.removeplan = (p) ->
      $scope.vote.plan = $scope.vote.plan.filter -> it.name != p.name
    $scope.state = 1
    $scope.newvote = (v) ->
      $scope.state = 2
      $http do
        url: \/api/vote/
        method: \POST
        data: JSON.stringify($scope.vote)
      .success (d) ->
        $scope.clean!
        $timeout ( ->
          $scope.state = 3 
          $timeout ( -> $scope.state = 1 ), 4000
        ), 2000
      .error (e) -> console.error e
    /*$timeout ->
      $http do
        url: \/api/vote/1
        method: \GET
      .success (d) -> 
        console.log d
        $scope.custom.time = true
        $scope.custom.plan = true
        $scope.vote = d
    , 1000*/
