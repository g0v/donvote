err = -> console.error "[ERROR]", it
ok = -> console.log "[OK]", it

angular.module \donvote, <[ui.choices]>
  ..config ($httpProvider) -> $httpProvider.defaults.headers.common["X-CSRFToken"] = $.cookie \csrftoken
  ..controller \main, ($scope, $http) ->
    console.log \ok
    $scope.user = {}
    $scope.save = ->
      console.log \saving
      $http do
        url: "/user/#{$scope.id}"
        method: \PUT
        data: $scope.user{group}
      .success ok
      .error err
    $scope.init = ->
      if !$scope.id => return
      $http do
        url: "/user/#{$scope.id}/"
        method: \GET
      .success (d) -> 
        console.log "user loaded: ", d
        $scope.user = d
      .error err

    $scope.group = do
      list: []
      dict: {}
      selected: 0
      init: ->
        $http do
          url: \/group/
          method: \GET
        .success (d) ~>
          $scope.group.list = d
          d.map ~> @dict[it.id] = it
      remove: (id) ->
        console.log "removing #id"
        $scope.user.group= $scope.user.group.filter(->it!=id)
        $scope.save!
      new: ->
        console.log \ok, $scope.groupform.name.$invalid
        if $scope.groupform.name.$invalid => return
        $http do
          url: \/group/
          method: \POST
          data: {name: $scope.group.name, desc: $scope.group.desc}
        .success ~> 
          @list.push it
          @dict[it.id] = it
        .error err
      add: ->
        id = (@selected or {}).id
        console.log $scope.user.group, id
        if !id or id in $scope.user.group => return
        console.log id
        $scope.user.group.push id
        $scope.save!
        @selected = 0

    $scope.group.init!
    $scope.$watch 'id' -> $scope.init!

