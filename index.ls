angular.module \main, <[firebase]>
  ..controller \main, <[$scope $firebase $timeout $location $http render]> ++ ($scope, $firebase, $timeout, $location, $http, render) ->
    $scope <<< do
      user: null
      mlogin:
        email: ""
        password: ""
        dismiss: -> $ \#login-modal .modal \hide

    $scope.auth = new FirebaseSimpleLogin new Firebase("https://donmockup.firebaseio.com/"), (e, u) -> $scope.$apply ->
      console.log "user login:" ,u
      if e => return console.log "get user fail: ", e
      $scope.user = u

    $scope.logout = -> if $scope.user =>
      $scope.auth.logout!
      $scope <<< {email: "", password: "", user: null}

    get-access-token = ->
      console.log "get login status..."
      FB.get-login-status (res) ->
        console.log "response..."
        if res.status == "connected" =>
          console.log res
          {userID,accessToken,email} = res.auth-response{userID, accessToken, email}
          $scope.$apply ->
            $scope.user = {uid: userID, access-token: access-token}
          FB.api \me (me) -> 
            $scope.$apply -> $scope.user.email = me.email
            $scope.mlogin.dismiss!
        else => console.log "please login"

    $scope.fblogin = ->
      $scope.auth.login \facebook, rememberMe: true, scope: 'email'
      #FB.login (->
      #  get-access-token!
      #), {scope: "read_stream,email"}
    $scope.login = ->
      if !$scope.user =>
        $scope.auth.createUser $scope.mlogin.email, $scope.mlogin.password, (e,u) ->
          if e and e.code == \EMAIL_TAKEN =>
            $scope.auth.login \password, email: $scope.mlogin.email, password: $scope.mlogin.password
          else if e =>
            console.log "create user error: ", e
          else => $scope.$apply -> $scope.user = u

    $scope.mvote = do
      id: null
      obj: null
      data: null
      allballot: {}
      plans: []
      ballot: []
      planCount: (plan) ->
        @allballot[plan.id] or 0
      planById: (id) ->
        ret = @plans.filter(-> it.id == id)
        if ret.length => return ret.0.name

      setReadOnly: (v) -> @readonly = v
      toggle: (plan) ->
        if !@id or @readonly => return
        if !$scope.user => return
        planid = @plans.map -> it.id
        @metix.forEach ~> if not (it.$value in planid) => @metix.$remove it
        ret = @metix.filter ~> it.$value == plan.id
        if ret.length > 0 => ret.map ~> @metix.$remove it
        else if @metix.length < ( @obj.maxvote or 1) => @metix.$add plan.id

      new: ->
        @ <<< {name: '未命名', desc: '', maxvote: 1, plans: [], readonly: true, uid: $scope.user.uid}
        @add!
        $timeout (-> $(\#vote-modal).modal \show ), 0

      add: ->
        db = $firebase(new Firebase "https://donmockup.firebaseio.com/vote")$asArray!
        db.$loaded!then ~>
          payload = {} <<< @{name, desc, maxvote, plans, readonly}
          payload.uid = $scope.user.uid
          db.$add payload .then (ref) ~> 
            @id = ref.name!
            @load @id

      load: (id) ->
        obj = $firebase(new Firebase "https://donmockup.firebaseio.com/vote/#id")$asObject!
        obj.$loaded!then ~>
          @obj = obj
          @ <<< @obj{name, desc, maxvote, plans, readonly, uid}
          if !@plans => @plans = []
          @id = id
          $location.hash @id
        alltix = $firebase(new Firebase "https://donmockup.firebaseio.com/vote/#id/tix")$asObject!
        alltix.$loaded!then ~>
          @alltix = alltix
          update = ~>
            @allballot = {}
            @alltix.forEach (ballot) ~>
               for k,v of ballot => 
                 if !@allballot[v] => @allballot[v] = 0
                 @allballot[v]++
          update!
          @alltix.$watch update

      save: ->
        @dismiss!
        if @obj => 
          @obj <<< @{name, desc, maxvote, plans, readonly}
          @obj.uid = $scope.user.uid
          return @obj.$save!
        if !(@name) => return
        if !@obj => @add!

      dismiss: ->
        $(\#vote-modal).modal \hide

      remove: ->
        @dismiss!
        idx = $scope.votelist.datasrc.$indexFor @id
        $scope.votelist.datasrc.$remove idx
        $location.hash ""
        $scope.votelist.init!

      delplan: (plan)->
        @plans.splice @plans.indexOf(plan),1

      newplan: ->
        @plans.push {name: @newplanname, id: new Date!getTime!}
        
    prepare-metix = ->
      if !($scope.mvote.id and $scope.user and $scope.user.uid) => return
      metix = $firebase(new Firebase "https://donmockup.firebaseio.com/vote/#{$scope.mvote.id}/tix/#{$scope.user.uid}")$asArray!
      metix.$loaded!then ->
        $scope.mvote.metix = metix
        update = -> $scope.mvote.ballot = $scope.mvote.metix.map -> it.$value
        update!
        $scope.mvote.metix.$watch update
    $scope.svg = document.getElementById(\svg)
    $scope.$watch 'user', -> prepare-metix!
    $scope.$watch 'mvote.id', -> prepare-metix!

    prepare-draw = ->
      payload = ($scope.mvote.plans or []).map -> 
        {value: ($scope.mvote.allballot[it.id] or 0)} <<< it{name, id}
      render.draw payload, $scope.svg

    $scope.$watch 'mvote.allballot', prepare-draw, true
    $scope.$watch 'mvote.plans', prepare-draw, true

    resize = ->
      [h,w] = [$(window)height!, $(window)width!]
      $(svg)width w - 40
      $(svg)height h - 200
    $(window)resize resize
    resize!

    $scope.votelist = do
      init: ->
        @datasrc = $firebase(new Firebase "https://donmockup.firebaseio.com/vote" .limit 10)$asArray!
        @datasrc.$loaded!then ~> 
          if !$location.hash! => id = @datasrc[parseInt(Math.random!*@datasrc.length)].$id
          else id = $location.hash!
          $scope.mvote.load id
    $scope.votelist.init!
    FB.init do
      appId: \836557763029341
      status: true
      cookie: true
      xfbml: true
      oauth: true

    get-access-token!
