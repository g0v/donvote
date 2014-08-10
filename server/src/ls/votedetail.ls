angular.module \donvote
  ..controller \votedetail, ($scope, $http) ->

    pretain-viewbox = do
      target: {}
      init: ->
        $(window)resize ~> @listener!
      register: (obj) ->
        while !obj.key or @target[obj.key] => obj.key = Math.random!
        @target[obj.key] = obj
        @handler obj
      worker: null
      listener: ->
        if @worker => clearTimeout @worker
        @worker = setTimeout ~>
          for k,v of @target => @handler v
          @worker = null
        , 500
      handler: (obj)->
        [w,h,m] = [$(obj.svg.0.0)width!, $(window)height! - obj.dh, obj.m]
        $(obj.svg.0.0)height h
        obj <<< {w,h} 
          ..svg.0.0.setAttribute "viewBox", "#{-m} #{-m} #{w + 2 * m} #{h + 2 * m}"
          ..render!

    pretain-viewbox.init!


    vote-chart = do
      svg: d3.select \#vote-chart
      data: []
      w: 0, h: 0, m: 20, dh: 250
      name: <[Jody Stanley Harvey Adrienne Antonio Laverne Cesar Ramon Julie Deanna Cristen Sammie]>
      color: d3.scale.category20!

      pie-chart: do
        scale: (r) ->
          @xscale = d3.scale.linear!domain [0, d3.max(@data.map -> it.x + it.dx)] .range [0, 2 * Math.PI]
          @yscale = d3.scale.linear!domain [0, d3.max(@data.map -> it.count)] .range [0, @h/2]
          @mb = 10
        render: (s) ->
          console.log "1>", s
          [r1,r2] = [30,200]
          arc = d3.svg.arc!
            .startAngle (d) ~> @xscale d.x
            .endAngle (d) ~> @xscale d.x + d.dx
            .innerRadius (d) ~> ( @w <? @h ) / 4
            .outerRadius (d) ~> ( @w <? @h ) / 2

          norm = (d) -> d.map ->  it / Math.sqrt( d.0 ** 2 + d.1 **2 )
          s.0.attr do
            fill: (d,i) -> d.color
            d: (d,i) ~> arc {x: d.x,y: 10,dx: d.dx,dy: 100}
          @svg.selectAll \g.path .select \path
            #..transition!duration 1000
              ..attr do
                transform: ~> "translate(#{@w/2} #{@h/2})"
                fill: (d,i) -> d.color
                stroke: (d,i)-> 
                  if i == 0 => return "rgba(255,0,0,1)"
                  if i == 1 => return "rgba(0,255,0,1)"
                  if i == 2 => return "rgba(0,0,255,1)"
                  if i == 3 => return "rgba(255,0,255,1)"
                "stroke-width": 1
                d: (d,i) ~> arc {x: d.x,y: 10,dx: d.dx,dy: 100}

          @svg.selectAll \g.text .select \text
          update-text = ~>
            it
              ..transition!duration 1000
                ..attr do
                  transform: ~> "translate(#{@w/2} #{@h/2})"
                  x: (d,i) ~> Math.sin(@xscale(d.x + d.dx/2)) * ( r2 ) 
                  y: (d,i) ~> -Math.cos(@xscale(d.x + d.dx/2)) * ( r2 )
                  "text-anchor": "middle"
                  "dorminant-baseline": "central"
              ..text (d,i) -> d.name
          update-text(@svg.selectAll \g.text .select \text)
          update-text(@svg.selectAll \g.text-shadow .select \text)

      vertical-bar: do
        scale: (r) ->
          @xscale = d3.scale.linear!domain [0, @data.length] .range [0, @w]
          @yscale = d3.scale.linear!domain [0, d3.max(@data.map -> it.count)] .range [@h,0]
          @mb = if @w > 500 and @data.length < 10 => 10 else 2
        render: (s) ->
          s.0.attr do
            transform: ""
            d: (d,i) ~>
              [x,y] = [@xscale(i), @yscale.range!0]
              [w,h] = [@xscale(i + 1) - @xscale(i) - @mb, 0]
              "M#x,#y L#{x+w},#y L#{x+w},#{y+h},L#x,#{y+h}Z"
            fill: (d,i) -> d.color
          [s.1, s.2].map ~> it
            ..attr do
              transform: ""
              x: (d,i) ~> ( @xscale(i) + @xscale(i + 1) - @mb ) / 2
              y: (d,i) ~> @yscale.range!0
              dy: -10
              width: 0
              height: 0
            ..text -> it.name
          @svg.selectAll \g.path .select \path
            ..transition!duration 1000
              ..attr do
                transform: ""
                d: (d,i) ~>
                  [x,y] = [@xscale(i), @yscale(d.count)]
                  [w,h] = [@xscale(i + 1) - @xscale(i) - @mb, (@yscale(0) - @yscale(d.count)) >? 5]
                  "M#x,#y L#{x+w},#y L#{x+w},#{y+h},L#x,#{y+h}Z"
                fill: (d,i) ~> d.color

          @svg.selectAll \g.text .select \text
          update-text = ~>
            it
              ..transition!duration 1000
                ..attr do
                  transform: ""
                  x: (d,i) ~> ( @xscale(i) + @xscale(i + 1) - @mb ) / 2
                  y: (d,i) ~> @yscale d.count
                  "text-anchor": "middle"
                  "dorminant-baseline": "central"
              ..text (d,i) -> d.name
          update-text(@svg.selectAll \g.text .select \text)
          update-text(@svg.selectAll \g.text-shadow .select \text)

      horizontal-bar: do
        scale: ->
          @xscale = d3.scale.linear!domain [0, d3.max(@data.map -> it.count)] .range [0, @w]
          @yscale = d3.scale.linear!domain [0, @data.length] .range [0, @h]
          @mb = if @h > 500 and @data.length < 10 => 10 else 2
        render: (s) ->
          s.0.attr do
            transform: ""
            d: (d,i) ~>
              [x,y] = [@xscale.range!0, @yscale(i)]
              [w,h] = [0, (@yscale(i + 1) - @yscale(i) - @mb) >? 0]
              "M#x,#y L#{x+w},#y L#{x+w},#{y+h},L#x,#{y+h}Z"
            fill: (d,i) -> d.color
          [s.1, s.2].map ~> it
            ..attr do
              transform: ""
              x: (d,i) ~> @xscale.range!0
              y: (d,i) ~> ( @yscale(i) + @yscale(i + 1) - @mb ) / 2
              width: 0
              height: 0
            ..text -> it.name
          @svg.selectAll \g.path .select \path
            ..transition!duration 1000
              ..attr do
                transform: ""
                d: (d,i) ~>
                  [x,y] = [@xscale.range!0, @yscale(i)]
                  [w,h] = [((@xscale(d.count) - @xscale(0)) >? 5), (@yscale(i + 1) - @yscale(i) - @mb)>?2]
                  "M#x,#y L#{x+w},#y L#{x+w},#{y+h},L#x,#{y+h}Z"
                fill: (d,i) ~> d.color
          update-text = ~>
            it
              ..transition!duration 1000
                ..attr do
                  transform: ""
                  x: (d,i) ~> 10 #( @xscale(d.count) ) <? @w
                  y: (d,i) ~> ( @yscale(i) + @yscale(i + 1) - @mb ) / 2
                  "text-anchor": "left"
                  "dominant-baseline": "central"
              ..text (d,i) -> d.name
          update-text(@svg.selectAll \g.text .select \text)
          update-text(@svg.selectAll \g.text-shadow .select \text)
      use: (choice)->
        if choice => @choice = choice
        @type = @[@choice] <<< @{w,h,m,dh,color,svg,data}
      choice: \horizontalBar
      render: ->
        # for debug purpose
        #@data = for i from 0 til (parseInt(Math.random!*@name.length)>?5) => do
        #  name: @name[i]
        #  color: @color @name[i]
        #  count: parseInt(Math.random!*1000)
        @data.sort (a,b) -> a.count - b.count
        @use!
        @type.scale!
        s = [<[path path]> <[text text-shadow]> <[text text]>]map ~>
          v = @svg.selectAll "g.#{it.1}" .data @data
          v.exit!transition!duration 1000 .style opacity: 0 .remove!
          v.enter!append \g .attr \class, it.1
            .append it.0 .attr \class, it.1
        count = 0
        @svg.selectAll "g.path" .select "path" .each (d,i) -> 
          d <<< {x:count, dx: d.count}
          count := count + d.count
        @type.render s

    pretain-viewbox.register vote-chart
    $scope.settype = ->
      vote-chart.use it
      vote-chart.render!

    $scope.comment = do
      new: do
        submit: ->
          $http do
            url: "/api/vote/#{voteid}/discuss/"
            method: \POST
            data: JSON.stringify(@d)
          .success (d) -> console.log "success:", d
          .error (d) -> console.log "success:", d
          /*$http do
            url: "/api/vote/#{voteid}/"
            method: \PUT
            data: JSON.stringify({name: $scope.vote.name, karma: $scope.vote.karma, discuss: $scope.vote.discuss ++ [@d]})
          .success (d) -> console.log "success. ", d
          .error (d) -> console.log "failed. ", d*/
        reset: -> @d = {}
        setPoint: -> @d.point = it
        d: {}

    $scope.toggleballot = (plan) ->
      $http do
        url: "/api/vote/#{voteid}/plan/#{plan.id}/ballot/"
        method: \GET
      .success (d) ->
        if d.length =>
          $http do
            url: "/api/vote/#{voteid}/plan/#{plan.id}/ballot/"
            method: \DELETE
          .success (d) -> console.log d
          .error (d) -> console.log e
        else
          $http do
            url: "/api/vote/#{voteid}/plan/#{plan.id}/ballot/"
            method: \POST
          .success (d) -> console.log d
          .error (d) -> console.log e

    $scope.accordion = {}
    $scope.newplan = do
      d: {}
      submit: ->
        if !@d.name => return
        $http do
          url: "/api/vote/#{voteid}/plan/"
          method: \POST
          data: JSON.stringify(@d)
        .success (e) ~>
          $scope.vote.plan ++= [e]
          vote-chart.data = $scope.vote.plan
          vote-chart.render!
        .error (e) -> console.error e
    $http do
     url: "/api/vote/#{voteid}/"
     method: \GET
    .success (d) ->
      $scope.vote = d
      console.log d
      vote-chart.data = d.plan
      d.plan.map -> 
        it.count = parseInt(Math.random!*1000)
        it.color = vote-chart.color it.name
      vote-chart.render!
