done = ->
fail = -> 
  console.error "[Error] ", it
  document.body.innerHTML = it
angular.module \donvote
  ..factory \Restbase, ($http) ->
    ret = do
      bind: (type, cbs={}) ->
        ret = do
          create: (d,cb,cb2) ~> @create type, d, (cb or cbs{}create.ok), (cb2 or cbs{}create.fail)
          getlist: (cb, cb2) ~> @getlist type, (cb or cbs{}getlist.ok), (cb2 or cbs{}getlist.fail)
          remove: (d,cb,cb2) ~> @remove type, d, (cb or cbs{}remove.ok), (cb2 or cbs{}remove.fail)
          update: (d,cb,cb2) ~> @update type, d, (cb or cbs{}update.ok), (cb2 or cbs{}update.fail)
          sub: do
            create: (typeB,c,d,cb,cb2) ~> 
              @sub.create type,typeB,c,d, (cb or cbs{}sub{}create.ok), (cb2 or cbs{}sub{}create.fail)
            remove: (typeB,c,d,cb,cb2) ~>
              @sub.remove type,typeB,c,d, (cb or cbs{}sub{}remove.ok), (cb2 or cbs{}sub{}remove.fail)
            update: (typeB,c,d,cb,cb2) ~>
              @sub.update type,typeB,c,d, (cb or cbs{}sub{}update.ok), (cb2 or cbs{}sub{}update.fail)
      create: (type, d, cb=done, cb2=fail) ->
        $http do
          url: "/api/#{type}/"
          method: \POST
          data: JSON.stringify(d)
        .success cb
        .error cb2
      getlist: (type, cb=done, cb2=fail) ->
        $http do
          url: "/api/#{type}/"
          method: \GET
        .success cb
        .error cb2
      remove: (type, d, cb=done, cb2=fail) ->
        $http do
          url: "/api/#{type}/#{d.id}/"
          method: \DELETE
        .success -> cb d
        .error cb2
      update: (type, d, cb=done, cb2=fail) ->
        $http do
          url: "/api/#{type}/#{d.id}/"
          method: \PUT
          data: JSON.stringify(d)
        .success cb
        .error cb2
      sub: do
        create: (typeA, typeB, c, d, cb=done, cb2=fail) ->
          c[typeB] = c[typeB] ++ [d]
          ret.update typeA, c, cb, cb2
        remove: (typeA, typeB, c, d, cb=done, cb2=fail) ->
          c[typeB] = c[typeB].filter -> it.id !=d.id
          ret.update typeA, c, ->
            ret.remove typeB, d, cb, cb2
          , cb2
        update: (typeA, typeB, c, d, cb=done, cb2=fail) ->
          ret.update typeB, d, cb, cb2
  ..controller \Ctrl.Vote, ($scope, $http, Restbase) ->
    $scope.rest = Restbase
    $scope.rest2 = Restbase.bind 'vote', do
      create: ok: (d) -> $scope.votelist ++= [d]
      remove: ok: (d) -> $scope.votelist = $scope.votelist.filter -> it.id != d.id
      sub: do
        create: 
          ok: (d) -> for v,i in $scope.votelist => if v.id==d.id => $scope.votelist[i] = d
          fail: (d) -> console.error "failed: ", d
          

    $scope.newvote = {karma: [], discuss: [], plan: []}
    $scope.newplan = {}
    $scope.newdiscuss = {}
    $scope.rest2.getlist -> $scope.votelist = it


/*angular.module \donvote
  ..controller \voteListController, ($scope, $http) ->
    $scope.votelist = []
    $scope.newvote = {karma: [], discuss: []}
    $scope.newplan = {}
    $scope.newdiscuss = {}
    $scope.addvote = ->
      $http do
        url: \/api/vote/
        method: \POST
        data: JSON.stringify($scope.newvote)
      .success (d) -> 
        window.location.reload!
        console.log d
      .error (d) -> console.log d
    $scope.fetch = ->
      $http do
        url: \/api/vote/
        method: \GET
      .success (d) -> 
        $scope.votelist = d
        for it in $scope.votelist =>
          $scope.newplan[it.id] = {}
          $scope.newdiscuss[it.id] = {}
        console.log d
      .error (d) -> console.log d

    $scope.addplan = (v) ->
      console.log $scope.newplan[v.id]
      #v.plan = v.plan ++ [d]
      console.log $scope.user
      $scope.newplan[v.id].owner_id = 1
      v.plan = v.plan ++ [$scope.newplan[v.id]]

      console.log ">>>", v
      $http do
        url: "/api/vote/#{v.id}"
        method: \PUT
        data: JSON.stringify(v)
      .success (d) -> 
        console.log d
        #window.location.reload!
      .error (d) -> 
        document.body.innerHTML = d
        console.log d

    $scope.removeplan = (u, v) ->
      u.plan = u.plan.filter -> it.id !=v.id
      $http do
        url: "/api/vote/#{u.id}"
        method: \PUT
        data: JSON.stringify(u)
      .success (d) -> console.log "done.", d
      .error (d) -> console.log "failed. ", d
      $http do
        url: "/api/plan/#{v.id}"
        method: \DELETE
      .success (d) -> console.log "deleted.", d
      .error (d) -> console.log "failed. ", d

    $scope.adddiscuss = (v) ->
      console.log $scope.newdiscuss[v.id]
      $http do
        url: \/api/discuss/
        method: \POST
        data: JSON.stringify($scope.newdiscuss[v.id])
      .success (d) -> 
        console.log d
        v.discuss = v.discuss ++ [d]
        console.log ">>>", v
        $http do
          url: "/api/vote/#{v.id}"
          method: \PUT
          data: JSON.stringify(v)
        .success (d) -> 
          console.log d
          #window.location.reload!
        .error (d) -> console.log d
      .error (d) -> console.log d
    $scope.removediscuss = (u, v) ->
      u.discuss = u.discuss.filter -> it.id !=v.id
      $http do
        url: "/api/vote/#{u.id}"
        method: \PUT
        data: JSON.stringify(u)
      .success (d) -> console.log "done.", d
      .error (d) -> console.log "failed. ", d
      $http do
        url: "/api/discuss/#{v.id}"
        method: \DELETE
      .success (d) -> console.log "deleted.", d
      .error (d) -> console.log "failed. ", d
    $scope.fetch!
    */
