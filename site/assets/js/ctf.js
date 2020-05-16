let questions = {};
let questionsByCategory = {};
let categories = {};
let solves = [];

let me = {};

fetch("/api/auth/me", {
  method: "POST",
  credentials: "include"
})
  .then(response => response.json())
  .then(jsonData => {
    if (jsonData.status) {
      me = jsonData.data;
    }
  });

function getQuestions() {
  return fetch("/api/ctf/questions.json", {
    method: "post",
    credentials: "include"
  }).then(response => response.json());
}

function getCategories() {
  return fetch("/api/ctf/categories.json", {
    method: "post",
    credentials: "include"
  }).then(response => response.json());
}

function getSolvesAdmin() {
  return fetch("/api/ctf/adminSolves.json", {
    method: "post",
    credentials: "include"
  }).then(response => response.json());
}

function getSolves(questionId, getAll) {
  if (questionId !== undefined) {
    return fetch("/api/ctf/questionSolves.json", {
      method: "post",
      credentials: "include",
      body: JSON.stringify({
        question: questionId
      })
    }).then(response => response.json());
  }

  return fetch("/api/ctf/userSolves.json", {
    method: "post",
    credentials: "include"
  }).then(response => response.json());
}

function getLeaderboard() {
  return fetch("/api/ctf/leaderboard.json", {
    method: "post",
    credentials: "include"
  }).then(response => response.json());
}

function trySolve(questionId, flag) {
  return fetch("/api/ctf/solve", {
    method: "post",
    credentials: "include",
    body: JSON.stringify({
      question: questionId,
      flag: flag
    })
  }).then(response => response.json());
}
