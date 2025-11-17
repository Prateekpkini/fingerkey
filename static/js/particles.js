window.onload = function () {
  const canvas = document.createElement('canvas');
  document.body.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  let particles = [];
  for (let i = 0; i < 70; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 2,
      speedX: Math.random() - 0.5,
      speedY: Math.random() - 0.5
    });
  }

  function animate() {
    ctx.fillStyle = "rgba(13, 13, 13, 0.3)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "cyan";
    for (let p of particles) {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
      p.x += p.speedX;
      p.y += p.speedY;
      if (p.x < 0 || p.x > canvas.width) p.speedX *= -1;
      if (p.y < 0 || p.y > canvas.height) p.speedY *= -1;
    }
    requestAnimationFrame(animate);
  }
  animate();
};
