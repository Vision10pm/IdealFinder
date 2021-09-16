function post() {
  var checkedInput = document.querySelectorAll("input:checked");
  var stage = document.querySelector("input[name=stage]").value;
  var clusterImgs = document.querySelectorAll(".cluster-imgs");
  var data = {};
  if (checkedInput.length == 0) {
    alert("이상형을 선택해주세요!");
  } else {
    document.querySelector(".candidate").classList.toggle("hidden");
    data["selected"] = {};
    for (let i = 0; i < checkedInput.length; i++) {
      data["selected"][checkedInput[i].dataset.id] =
        checkedInput[i].dataset.value;
      clusterImgs[checkedInput[i].dataset.name - 1].style = "";
    }
    var loadingBT = document.querySelector(".loadingBT");
    data["stage"] = stage;
    data = JSON.stringify(data).replace("\n", "");
    fetch("", {
      body: data,
      headers: {
        "Content-Type": "application/json",
      },
      method: "post",
    })
      .then((res) => res.json())
      .then((res) => {
        loadingBT.addEventListener("click", function (e) {
          ResRender(res.result, res.render);
        });
        loadingBT.classList.toggle("inact");
        loadingBT.innerHTML = "<p>다음 단계로</p>";
        return res;
      });
  }
}

function inputCheck() {
  var input = document.querySelectorAll("input.input-checkbox");
  var checkedInput = document.querySelectorAll("input.input-checkbox:checked");
  if (checkedInput.length > input.length / 2) {
    alert(`${input.length / 2}명만 골라주세요~`);
    return false;
  }
  return true;
}

function ResRender(result, renderTxt) {
  if (result == false) {
    document.querySelector("article.container").innerHTML = renderTxt;
  } else {
    document.querySelector("div.container-wrapper").innerHTML = renderTxt;
  }
}
document.addEventListener("click", function (e) {
  console.log(e.target);
  if (document.querySelector(".SelectBT").contains(e.target)) {
    post();
  }
  if (e.target.classList.contains("input-checkbox")) {
    if (e.target.classList.contains("input-checkbox")) {
      if (!inputCheck()) {
        e.target.checked = false;
      }
    }
  }
});
document.addEventListener("change", function(e) {
  if (e.target.className == "input-checkbox") {
    var totalCnt = document.querySelectorAll("input.input-checkbox").length;
    var currCnt = document.querySelectorAll("input.input-checkbox:checked").length;
    console.log(totalCnt/2-currCnt);
    document.querySelector(".avail-check").innerText = totalCnt/2-currCnt;
  } 
});

window.requestAnimFrame = (function () {
  return (
    window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    function (callback) {
      window.setTimeout(callback, 1000 / 60);
    }
  );
})();

var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
var cw = window.innerWidth;
var ch = window.innerHeight;
var fireworks = [];
var particles = [];
var hue = 120;
var limiterTotal = 50;
var limiterTick = 0;
var timerTotal = 11;
var timerTick = 0;
var mousedown = false;
var mx;
var my;

canvas.width = cw;
canvas.height = ch;

function random(min, max) {
  return Math.random() * (max - min) + min;
}

function calculateDistance(p1x, p1y, p2x, p2y) {
  var xDistance = p1x - p2x,
    yDistance = p1y - p2y;
  return Math.sqrt(Math.pow(xDistance, 2) + Math.pow(yDistance, 2));
}

function Firework(sx, sy, tx, ty) {
  this.x = sx;
  this.y = sy;
  this.sx = sx;
  this.sy = sy;
  this.tx = tx;
  this.ty = ty;
  this.distanceToTarget = calculateDistance(sx, sy, tx, ty);
  this.distanceTraveled = 0;
  this.coordinates = [];
  this.coordinateCount = 2;
  while (this.coordinateCount--) {
    this.coordinates.push([this.x, this.y]);
  }
  this.angle = Math.atan2(ty - sy, tx - sx);
  this.speed = 5;
  this.acceleration = 500;
  this.brightness = random(50, 70);
  this.targetRadius = 1;
}

Firework.prototype.update = function (index) {
  this.coordinates.pop();
  this.coordinates.unshift([this.x, this.y]);

  if (this.targetRadius < 8) {
    this.targetRadius += 0.3;
  } else {
    this.targetRadius = 1;
  }

  this.speed *= this.acceleration;

  var vx = Math.cos(this.angle) * this.speed,
    vy = Math.sin(this.angle) * this.speed;
  this.distanceTraveled = calculateDistance(
    this.sx,
    this.sy,
    this.x + vx,
    this.y + vy
  );

  if (this.distanceTraveled >= this.distanceToTarget) {
    createParticles(this.tx, this.ty);
    fireworks.splice(index, 1);
  } else {
    this.x += vx;
    this.y += vy;
  }
};

Firework.prototype.draw = function () {
  ctx.beginPath();
  ctx.moveTo(
    this.coordinates[this.coordinates.length - 1][0],
    this.coordinates[this.coordinates.length - 1][1]
  );
  ctx.lineTo(this.x, this.y);
  ctx.strokeStyle = "hsl(" + hue + ", 100%, " + this.brightness + "%)";
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(this.tx, this.ty, this.targetRadius, 0, Math.PI * 2);
  ctx.stroke();
};

function Particle(x, y) {
  this.x = x;
  this.y = y;
  this.coordinates = [];
  this.coordinateCount = 5;
  while (this.coordinateCount--) {
    this.coordinates.push([this.x, this.y]);
  }
  this.angle = random(0, Math.PI * 2);
  this.speed = random(1, 10);
  this.friction = 0.95;
  this.gravity = 1;
  this.hue = random(hue - 20, hue + 20);
  this.brightness = random(50, 80);
  this.alpha = 1;
  this.decay = random(0.015, 0.03);
}

Particle.prototype.update = function (index) {
  this.coordinates.pop();
  this.coordinates.unshift([this.x, this.y]);
  this.speed *= this.friction;
  this.x += Math.cos(this.angle) * this.speed;
  this.y += Math.sin(this.angle) * this.speed + this.gravity;
  this.alpha -= this.decay;

  if (this.alpha <= this.decay) {
    particles.splice(index, 1);
  }
};

Particle.prototype.draw = function () {
  ctx.beginPath();
  ctx.moveTo(
    this.coordinates[this.coordinates.length - 1][0],
    this.coordinates[this.coordinates.length - 1][1]
  );
  ctx.lineTo(this.x, this.y);
  ctx.strokeStyle =
    "hsla(" +
    this.hue +
    ", 100%, " +
    this.brightness +
    "%, " +
    this.alpha +
    ")";
  ctx.stroke();
};

function createParticles(x, y) {
  var particleCount = 230;
  while (particleCount--) {
    particles.push(new Particle(x, y));
  }
}

function loop() {
  requestAnimFrame(loop);
  hue += 2.3;

  ctx.globalCompositeOperation = "destination-out";
  ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
  ctx.fillRect(0, 0, cw, ch);
  ctx.globalCompositeOperation = "lighter";

  var i = fireworks.length;
  while (i--) {
    fireworks[i].draw();
    fireworks[i].update(i);
  }

  var i = particles.length;
  while (i--) {
    particles[i].draw();
    particles[i].update(i);
  }

  if (timerTick >= timerTotal) {
    if (!mousedown) {
      fireworks.push(
        new Firework(cw / 2, ch, random(0, cw), random(0, ch / 2))
      );
      timerTick = 0;
    }
  } else {
    timerTick++;
  }

  if (limiterTick >= limiterTotal) {
    if (mousedown) {
      fireworks.push(new Firework(cw / 500, ch, mx, my));
      limiterTick = 0;
    }
  } else {
    limiterTick++;
  }
}

canvas.addEventListener("mousemove", function (e) {
  mx = e.pageX - canvas.offsetLeft;
  my = e.pageY - canvas.offsetTop;
});

canvas.addEventListener("mousedown", function (e) {
  e.preventDefault();
  mousedown = true;
});

canvas.addEventListener("mouseup", function (e) {
  e.preventDefault();
  mousedown = false;
});

window.onload = loop;
