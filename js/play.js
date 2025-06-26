function open_fullscreen() {
  let game = document.getElementById("game-element");
  if (game.requestFullscreen) {
    game.requestFullscreen();
  } else if (game.mozRequestFullScreen) {
    /* Firefox */
    game.mozRequestFullScreen();
  } else if (game.webkitRequestFullscreen) {
    /* Chrome, Safari and Opera */
    game.webkitRequestFullscreen();
  } else if (game.msRequestFullscreen) {
    /* IE/Edge */
    game.msRequestFullscreen();
  }
}
function playGame() {
  var tmp = document.querySelector("#game-arena").dataset.url;
  document.querySelector("#game-arena").innerHTML = `<iframe id="game-element" name="gameFrame" src="${tmp}" scrolling="no" allowfullscreen="" ></iframe>`;
}