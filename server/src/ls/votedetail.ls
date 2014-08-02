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

      vertical-bar: do
        scale: (r) ->
          @xscale = d3.scale.linear!domain [0, @data.length] .range [0, @w]
          @yscale = d3.scale.linear!domain [0, d3.max(@data.map -> it.count)] .range [@h,0]
          @mb = if @w > 500 and @data.length < 10 => 10 else 2
        render: (s) ->
          s.0.attr do
            x: (d,i) ~> @xscale i
            y: (d,i) ~> @yscale.range!0
            width: (d,i) ~> @xscale(i + 1) - @xscale(i) - @mb
            height: 0
            fill: (d,i) -> d.color
          s.1
            ..attr do
              x: (d,i) ~> ( @xscale(i) + @xscale(i + 1) - @mb ) / 2
              y: (d,i) ~> @yscale.range!0
              dy: -10
              width: 0
              height: 0
            ..text -> it.name
          @svg.selectAll \g.rect .select \rect
            ..transition!duration 1000
              ..attr do
                x: (d,i) ~> @xscale i
                width: (d,i) ~> @xscale(i + 1) - @xscale(i) - @mb
                y: (d,i) ~> @yscale d.count
                height: (d,i) ~> (@yscale(0) - @yscale(d.count))>?5
                fill: (d,i) ~> d.color

          @svg.selectAll \g.text .select \text
          update-text = ~>
            it
              ..transition!duration 1000
                ..attr do
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
            x: (d,i) ~> @xscale.range!0
            y: (d,i) ~> @yscale i
            width: 0
            height: (d,i) ~> (@yscale(i + 1) - @yscale(i) - @mb) >? 0 
            fill: (d,i) -> d.color
          s.1
            ..attr do
              x: (d,i) ~> @xscale.range!0
              y: (d,i) ~> ( @yscale(i) + @yscale(i + 1) - @mb ) / 2
              width: 0
              height: 0
            ..text -> it.name
          @svg.selectAll \g.rect .select \rect
            ..transition!duration 1000
              ..attr do
                x: (d,i) ~> @xscale.range!0
                width: (d,i) ~> (@xscale(d.count) - @xscale(0)) >? 5
                y: (d,i) ~> @yscale i
                height: (d,i) ~> 
                  @yscale(i + 1) - @yscale(i) - @mb >? 2
                fill: (d,i) ~> d.color
          update-text = ~>
            it
              ..transition!duration 1000
                ..attr do
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
        s = [<[rect rect]> <[text text-shadow]> <[text text]>]map ~>
          v = @svg.selectAll "g.#{it.1}" .data @data
          v.exit!transition!duration 1000 .style opacity: 0 .remove!
          v.enter!append \g .attr \class, it.1
            .append it.0 .attr \class, it.1
        @type.render s

    pretain-viewbox.register vote-chart
    $scope.settype = ->
      vote-chart.use it
      vote-chart.render!
    $http do
     url: "/api/vote/#{voteid}/"
     method: \GET
    .success (d) ->
      console.log d
      vote-chart.data = d.plan
      d.plan.map -> 
        it.count = parseInt(Math.random!*1000)
        it.color = vote-chart.color it.name
      vote-chart.render!
