"use strict";

(function() {
  window.addEventListener("load", init);

  function init() {
    let button = document.getElementsByTagName("button");
    button.addEventListener("click", addPost);
    loadPosts();
  }

  function loadPosts() {
    
  }

  function addPost() {
    let title = document.getElementById("title-text");
    let body = document.getElementById("text-body");
    let newPost = document.createElement("div");
    newPost.classList.add("post");
    let ttl = document.createElement("h2").textContent();
  }
})();