angular.module \donvote
  ..controller \discuss, ($scope, $http) ->
    console.log \asdf
    $scope.discuss = do
      new: do
        submit: ->
          url = "/api/#{window.location.pathname}discuss/".replace /\/\//g, "/"
          $http do
            url: url #"/api/vote/#{voteid}/discuss/"
            method: \POST
            data: JSON.stringify(@d)
          .success (d) -> console.log "success:", d
          .error (d) -> console.log "success:", d
        reset: -> @d = {}
        setTendency: -> @d.tendency = it
        d: {tendency: 2}

