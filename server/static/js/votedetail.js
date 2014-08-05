// Generated by LiveScript 1.2.0
var x$;
x$ = angular.module('donvote');
x$.controller('votedetail', function($scope, $http){
  var pretainViewbox, voteChart;
  pretainViewbox = {
    target: {},
    init: function(){
      var this$ = this;
      return $(window).resize(function(){
        return this$.listener();
      });
    },
    register: function(obj){
      while (!obj.key || this.target[obj.key]) {
        obj.key = Math.random();
      }
      this.target[obj.key] = obj;
      return this.handler(obj);
    },
    worker: null,
    listener: function(){
      var this$ = this;
      if (this.worker) {
        clearTimeout(this.worker);
      }
      return this.worker = setTimeout(function(){
        var k, ref$, v;
        for (k in ref$ = this$.target) {
          v = ref$[k];
          this$.handler(v);
        }
        return this$.worker = null;
      }, 500);
    },
    handler: function(obj){
      var ref$, w, h, m, x$;
      ref$ = [$(obj.svg[0][0]).width(), $(window).height() - obj.dh, obj.m], w = ref$[0], h = ref$[1], m = ref$[2];
      $(obj.svg[0][0]).height(h);
      x$ = (obj.w = w, obj.h = h, obj);
      x$.svg[0][0].setAttribute("viewBox", (-m) + " " + (-m) + " " + (w + 2 * m) + " " + (h + 2 * m));
      x$.render();
      return x$;
    }
  };
  pretainViewbox.init();
  voteChart = {
    svg: d3.select('#vote-chart'),
    data: [],
    w: 0,
    h: 0,
    m: 20,
    dh: 250,
    name: ['Jody', 'Stanley', 'Harvey', 'Adrienne', 'Antonio', 'Laverne', 'Cesar', 'Ramon', 'Julie', 'Deanna', 'Cristen', 'Sammie'],
    color: d3.scale.category20(),
    pieChart: {
      scale: function(r){
        this.xscale = d3.scale.linear().domain([
          0, d3.max(this.data.map(function(it){
            return it.x + it.dx;
          }))
        ]).range([0, 2 * Math.PI]);
        this.yscale = d3.scale.linear().domain([
          0, d3.max(this.data.map(function(it){
            return it.count;
          }))
        ]).range([0, this.h / 2]);
        return this.mb = 10;
      },
      render: function(s){
        var ref$, r1, r2, arc, norm, x$, updateText, this$ = this;
        console.log("1>", s);
        ref$ = [30, 200], r1 = ref$[0], r2 = ref$[1];
        arc = d3.svg.arc().startAngle(function(d){
          return this$.xscale(d.x);
        }).endAngle(function(d){
          return this$.xscale(d.x + d.dx);
        }).innerRadius(function(d){
          var ref$, ref1$;
          return ((ref$ = this$.w) < (ref1$ = this$.h) ? ref$ : ref1$) / 4;
        }).outerRadius(function(d){
          var ref$, ref1$;
          return ((ref$ = this$.w) < (ref1$ = this$.h) ? ref$ : ref1$) / 2;
        });
        norm = function(d){
          return d.map(function(it){
            return it / Math.sqrt(Math.pow(d[0], 2) + Math.pow(d[1], 2));
          });
        };
        s[0].attr({
          fill: function(d, i){
            return d.color;
          },
          d: function(d, i){
            return arc({
              x: d.x,
              y: 10,
              dx: d.dx,
              dy: 100
            });
          }
        });
        x$ = this.svg.selectAll('g.path').select('path');
        x$.attr({
          transform: function(){
            return "translate(" + this$.w / 2 + " " + this$.h / 2 + ")";
          },
          fill: function(d, i){
            return d.color;
          },
          stroke: function(d, i){
            if (i === 0) {
              return "rgba(255,0,0,1)";
            }
            if (i === 1) {
              return "rgba(0,255,0,1)";
            }
            if (i === 2) {
              return "rgba(0,0,255,1)";
            }
            if (i === 3) {
              return "rgba(255,0,255,1)";
            }
          },
          "stroke-width": 1,
          d: function(d, i){
            return arc({
              x: d.x,
              y: 10,
              dx: d.dx,
              dy: 100
            });
          }
        });
        this.svg.selectAll('g.text').select('text');
        updateText = function(it){
          var x$, y$;
          x$ = it;
          y$ = x$.transition().duration(1000);
          y$.attr({
            transform: function(){
              return "translate(" + this$.w / 2 + " " + this$.h / 2 + ")";
            },
            x: function(d, i){
              return Math.sin(this$.xscale(d.x + d.dx / 2)) * r2;
            },
            y: function(d, i){
              return -Math.cos(this$.xscale(d.x + d.dx / 2)) * r2;
            },
            "text-anchor": "middle",
            "dorminant-baseline": "central"
          });
          x$.text(function(d, i){
            return d.name;
          });
          return x$;
        };
        updateText(this.svg.selectAll('g.text').select('text'));
        return updateText(this.svg.selectAll('g.text-shadow').select('text'));
      }
    },
    verticalBar: {
      scale: function(r){
        this.xscale = d3.scale.linear().domain([0, this.data.length]).range([0, this.w]);
        this.yscale = d3.scale.linear().domain([
          0, d3.max(this.data.map(function(it){
            return it.count;
          }))
        ]).range([this.h, 0]);
        return this.mb = this.w > 500 && this.data.length < 10 ? 10 : 2;
      },
      render: function(s){
        var x$, y$, updateText, this$ = this;
        s[0].attr({
          transform: "",
          d: function(d, i){
            var ref$, x, y, w, h;
            ref$ = [this$.xscale(i), this$.yscale.range()[0]], x = ref$[0], y = ref$[1];
            ref$ = [this$.xscale(i + 1) - this$.xscale(i) - this$.mb, 0], w = ref$[0], h = ref$[1];
            return "M" + x + "," + y + " L" + (x + w) + "," + y + " L" + (x + w) + "," + (y + h) + ",L" + x + "," + (y + h) + "Z";
          },
          fill: function(d, i){
            return d.color;
          }
        });
        [s[1], s[2]].map(function(it){
          var x$;
          x$ = it;
          x$.attr({
            transform: "",
            x: function(d, i){
              return (this$.xscale(i) + this$.xscale(i + 1) - this$.mb) / 2;
            },
            y: function(d, i){
              return this$.yscale.range()[0];
            },
            dy: -10,
            width: 0,
            height: 0
          });
          x$.text(function(it){
            return it.name;
          });
          return x$;
        });
        x$ = this.svg.selectAll('g.path').select('path');
        y$ = x$.transition().duration(1000);
        y$.attr({
          transform: "",
          d: function(d, i){
            var ref$, x, y, w, h;
            ref$ = [this$.xscale(i), this$.yscale(d.count)], x = ref$[0], y = ref$[1];
            ref$ = [this$.xscale(i + 1) - this$.xscale(i) - this$.mb, (ref$ = this$.yscale(0) - this$.yscale(d.count)) > 5 ? ref$ : 5], w = ref$[0], h = ref$[1];
            return "M" + x + "," + y + " L" + (x + w) + "," + y + " L" + (x + w) + "," + (y + h) + ",L" + x + "," + (y + h) + "Z";
          },
          fill: function(d, i){
            return d.color;
          }
        });
        this.svg.selectAll('g.text').select('text');
        updateText = function(it){
          var x$, y$;
          x$ = it;
          y$ = x$.transition().duration(1000);
          y$.attr({
            transform: "",
            x: function(d, i){
              return (this$.xscale(i) + this$.xscale(i + 1) - this$.mb) / 2;
            },
            y: function(d, i){
              return this$.yscale(d.count);
            },
            "text-anchor": "middle",
            "dorminant-baseline": "central"
          });
          x$.text(function(d, i){
            return d.name;
          });
          return x$;
        };
        updateText(this.svg.selectAll('g.text').select('text'));
        return updateText(this.svg.selectAll('g.text-shadow').select('text'));
      }
    },
    horizontalBar: {
      scale: function(){
        this.xscale = d3.scale.linear().domain([
          0, d3.max(this.data.map(function(it){
            return it.count;
          }))
        ]).range([0, this.w]);
        this.yscale = d3.scale.linear().domain([0, this.data.length]).range([0, this.h]);
        return this.mb = this.h > 500 && this.data.length < 10 ? 10 : 2;
      },
      render: function(s){
        var x$, y$, updateText, this$ = this;
        s[0].attr({
          transform: "",
          d: function(d, i){
            var ref$, x, y, w, h;
            ref$ = [this$.xscale.range()[0], this$.yscale(i)], x = ref$[0], y = ref$[1];
            ref$ = [0, (ref$ = this$.yscale(i + 1) - this$.yscale(i) - this$.mb) > 0 ? ref$ : 0], w = ref$[0], h = ref$[1];
            return "M" + x + "," + y + " L" + (x + w) + "," + y + " L" + (x + w) + "," + (y + h) + ",L" + x + "," + (y + h) + "Z";
          },
          fill: function(d, i){
            return d.color;
          }
        });
        [s[1], s[2]].map(function(it){
          var x$;
          x$ = it;
          x$.attr({
            transform: "",
            x: function(d, i){
              return this$.xscale.range()[0];
            },
            y: function(d, i){
              return (this$.yscale(i) + this$.yscale(i + 1) - this$.mb) / 2;
            },
            width: 0,
            height: 0
          });
          x$.text(function(it){
            return it.name;
          });
          return x$;
        });
        x$ = this.svg.selectAll('g.path').select('path');
        y$ = x$.transition().duration(1000);
        y$.attr({
          transform: "",
          d: function(d, i){
            var ref$, x, y, w, h;
            ref$ = [this$.xscale.range()[0], this$.yscale(i)], x = ref$[0], y = ref$[1];
            ref$ = [(ref$ = this$.xscale(d.count) - this$.xscale(0)) > 5 ? ref$ : 5, (ref$ = this$.yscale(i + 1) - this$.yscale(i) - this$.mb) > 2 ? ref$ : 2], w = ref$[0], h = ref$[1];
            return "M" + x + "," + y + " L" + (x + w) + "," + y + " L" + (x + w) + "," + (y + h) + ",L" + x + "," + (y + h) + "Z";
          },
          fill: function(d, i){
            return d.color;
          }
        });
        updateText = function(it){
          var x$, y$;
          x$ = it;
          y$ = x$.transition().duration(1000);
          y$.attr({
            transform: "",
            x: function(d, i){
              return 10;
            },
            y: function(d, i){
              return (this$.yscale(i) + this$.yscale(i + 1) - this$.mb) / 2;
            },
            "text-anchor": "left",
            "dominant-baseline": "central"
          });
          x$.text(function(d, i){
            return d.name;
          });
          return x$;
        };
        updateText(this.svg.selectAll('g.text').select('text'));
        return updateText(this.svg.selectAll('g.text-shadow').select('text'));
      }
    },
    use: function(choice){
      var ref$;
      if (choice) {
        this.choice = choice;
      }
      return this.type = (ref$ = this[this.choice], ref$.w = this.w, ref$.h = this.h, ref$.m = this.m, ref$.dh = this.dh, ref$.color = this.color, ref$.svg = this.svg, ref$.data = this.data, ref$);
    },
    choice: 'horizontalBar',
    render: function(){
      var s, count, this$ = this;
      this.data.sort(function(a, b){
        return a.count - b.count;
      });
      this.use();
      this.type.scale();
      s = [['path', 'path'], ['text', 'text-shadow'], ['text', 'text']].map(function(it){
        var v;
        v = this$.svg.selectAll("g." + it[1]).data(this$.data);
        v.exit().transition().duration(1000).style({
          opacity: 0
        }).remove();
        return v.enter().append('g').attr('class', it[1]).append(it[0]).attr('class', it[1]);
      });
      count = 0;
      this.svg.selectAll("g.path").select("path").each(function(d, i){
        d.x = count;
        d.dx = d.count;
        return count = count + d.count;
      });
      return this.type.render(s);
    }
  };
  pretainViewbox.register(voteChart);
  $scope.settype = function(it){
    voteChart.use(it);
    return voteChart.render();
  };
  return $http({
    url: "/api/vote/" + voteid + "/",
    method: 'GET'
  }).success(function(d){
    console.log(d);
    voteChart.data = d.plan;
    d.plan.map(function(it){
      it.count = parseInt(Math.random() * 1000);
      return it.color = voteChart.color(it.name);
    });
    return voteChart.render();
  });
});