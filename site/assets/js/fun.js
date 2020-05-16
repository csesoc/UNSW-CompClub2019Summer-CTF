(() => {
  let x = document.querySelector(
    ".navbar [name=mouseCoordinates] [name=mouseX]"
  );
  let y = document.querySelector(
    ".navbar [name=mouseCoordinates] [name=mouseY]"
  );

  document.body.addEventListener("mousemove", evt => {
    x.innerText = evt.clientX;
    y.innerText = evt.clientY;
  });
})();

(() => {
  var nm = document.querySelector(".navbar-menu");
  var it = document.createElement("a");
  it.classList.add("navbar-item", "has-text-grey");
  it.innerText = "toggle questions";
  it.onclick = () =>
    document.querySelector("body > div.container").classList.toggle("hide");
  nm.insertBefore(it, nm.firstChild);
})();
