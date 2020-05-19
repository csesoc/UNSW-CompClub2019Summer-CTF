Array.prototype.has = function(obj) {
  return this.indexOf(obj) > -1;
};

function openModalQuestion(questionData, srcElem) {
  let modal = document.getElementById("questionModal");
  modal.classList.toggle("solved", solves.has(questionData.id));
  modal.classList.toggle("pending", pending.has(questionData.id));
  getSolves(questionData.id).then(jsonData => {
    if (jsonData.status) {
      modal.querySelector("[name=solves]").innerText = jsonData.data;
    }
  });

  modal.querySelector("[name=answer]").value =
    questions[questionData.id].inputValue || "";
  modal.querySelector("[name=answer]").placeholder = "noice";
  modal.querySelector("[name=title]").innerText = questionData.title;
  modal.querySelector("[name=category]").innerText =
    categories[questionData.category] || "";
  modal.querySelector("[name=description]").innerHTML =
    questionData.description;

  // Open links in a new window/tab
  for (elem of modal
    .querySelector("[name=description]")
    .getElementsByTagName("a")) {
    if (!elem.target) elem.target = "_blank";
  }

  const answerSubmissionDisable = function() {
    modal.querySelector("form .input").disabled = true;
    modal.querySelector("form .button").disabled = true;
  };

  const answerSubmissionEnable = function() {
    modal.querySelector("form .input").disabled = false;
    modal.querySelector("form .button").disabled = false;
  };

  const submitEvent = function(evt) {
    evt.preventDefault();

    if (!modal.querySelector("[name=answer]").value.trim()) return;

    modal.querySelector("form").removeEventListener("submit", submitEvent);
    answerSubmissionDisable();
    modal.querySelector("form .button").classList.add("is-loading");

    let answerValue = modal.querySelector("[name=answer]").value.trim();
    trySolve(questionData.id, answerValue).then(jsonData => {
      modal.querySelector("form .button").classList.remove("is-loading");
      answerSubmissionEnable();
      modal.querySelector("form").addEventListener("submit", submitEvent);

      if (jsonData.status) {
        if (!solves.has(questionData.id)) {
          solves.push(questionData.id);
          modal.querySelector("[name=solves]").innerText =
            parseInt(modal.querySelector("[name=solves]").innerText) + 1;
          updateLeaderboard();
          }
        modal.querySelector("[name=value]").classList.add("solved");
        modal.classList.add("solved");
        srcElem.classList.add("solved");
        const form = modal.querySelector("form");
        if (!form.classList.contains("hide")) {
          form.classList.add("hide");
        }
  
      } else {
        modal.querySelector("[name=answer]").placeholder =
          answerValue + " was not right!";
        modal.querySelector("[name=answer]").value = "";
      }
    });
  };

  const form = modal.querySelector("form");
  if (!solves.has(questionData.id)) {
    if (form.classList.contains("hide")) {
      form.classList.remove("hide");
    }
    modal.querySelector("form .button").onclick = submitEvent;
  } else {
    if (!form.classList.contains("hide")) {
      form.classList.add("hide");
    }
  }

  const closeModal = function() {
    questions[questionData.id].inputValue = modal.querySelector(
      "[name=answer]"
    ).value.toString();
    modal.querySelector("[name=value]").classList.remove("solved");
    modal.classList.remove("solved");
    answerSubmissionEnable();

    modal.querySelector("form").removeEventListener("submit", submitEvent);
    modal
      .querySelector("button.cancel")
      .removeEventListener("click", cancelEvent);
    modal
      .querySelector(".modal-background")
      .removeEventListener("click", cancelEvent);
    modal.classList.remove("is-active");
  };

  const cancelEvent = closeModal;

  modal.querySelector("[name=value]").innerText = questionData.value.toString();

  modal.querySelector("form").addEventListener("submit", submitEvent);
  modal.querySelector("button.cancel").addEventListener("click", cancelEvent);
  modal
    .querySelector(".modal-background")
    .addEventListener("click", cancelEvent);
  modal.classList.add("is-active");
}

function reloadListener() {
  let modal = document.getElementById("questionModal");
  if (modal.classList.contains("active")) {
    modal
      .querySelector("button.cancel")
      .addEventListener("click", location.reload);
    modal
      .querySelector(".modal-background")
      .addEventListener("click", location.reload);
  } else {
    location.reload();
  }
}

function openModalQuestionSpecial(questionData, srcElem) {
  let modal = document.getElementById("questionModalSpecial");
  modal.classList.toggle("solved", solves.has(questionData.id));
  modal.classList.toggle("pending", pending.has(questionData.id));

  getSolves(questionData.id).then(jsonData => {
    if (jsonData.status) {
      modal.querySelector("[name=solves]").innerText = jsonData.data;
    }
  });

  getPending(questionData.id).then(jsonData => {
    if (jsonData.status) {
      modal.querySelector("[name=pending]").innerText = jsonData.data;
    }
  });

  modal.querySelector("[name=answer]").value =
    questions[questionData.id].inputValue || "";
  modal.querySelector("[name=answer]").placeholder = "noice";
  modal.querySelector("[name=title]").innerText = questionData.title;
  modal.querySelector("[name=category]").innerText =
    categories[questionData.category] || "";
  modal.querySelector("[name=description]").innerHTML =
    questionData.description;

  // Open links in a new window/tab
  for (elem of modal
    .querySelector("[name=description]")
    .getElementsByTagName("a")) {
    if (!elem.target) elem.target = "_blank";
  }

  const answerSubmissionDisable = function() {
    modal.querySelector("form .input").disabled = true;
    modal.querySelector("form .button").disabled = true;
  };

  const answerSubmissionEnable = function() {
    modal.querySelector("form .input").disabled = false;
    modal.querySelector("form .button").disabled = false;
  };

  const submitEvent = function(evt) {
    evt.preventDefault();

    if (!modal.querySelector("[name=answer]").value.trim()) return;

    modal.querySelector("form").removeEventListener("submit", submitEvent);
    answerSubmissionDisable();
    modal.querySelector("form .button").classList.add("is-loading");

    let answerValue = modal.querySelector("[name=answer]").value.trim();
    submitSpecial(questionData.id, answerValue).then(jsonData => {
      modal.querySelector("form .button").classList.remove("is-loading");
      answerSubmissionEnable();
      modal.querySelector("form").addEventListener("submit", submitEvent);

      if (jsonData.status) {
        modal.querySelector("[name=answer]").placeholder = "submission made";
        modal.querySelector("[name=answer]").value = "";
        pending.push(questionData.id);
        modal.querySelector("[name=pending]").innerText =
          parseInt(modal.querySelector("[name=pending]").innerText) + 1;
        modal.querySelector("[name=value]").classList.add("pending");
        modal.classList.add("pending");
        srcElem.classList.add("pending");
        const form = modal.querySelector("form");
        if (!form.classList.contains("hide")) {
          form.classList.add("hide");
        }
        const deleteElem = document.getElementById("delete");
        if (deleteElem.classList.contains("hide")) {
          deleteElem.classList.remove("hide");
        }
      }
    });
  };

  if (solves.has(questionData.id)) {
    const form = modal.querySelector("form");
    if (!form.classList.contains("hide")) {
      form.classList.add("hide");
    }
    const deleteElem = document.getElementById("delete");
    if (!deleteElem.classList.contains("hide")) {
      deleteElem.classList.add("hide")
    }
  } else if (pending.has(questionData.id)) {
    const form = modal.querySelector("form");
    if (!form.classList.contains("hide")) {
      form.classList.add("hide");
    }
    const deleteElem = document.getElementById("delete");
    if (deleteElem.classList.contains("hide")) {
      deleteElem.classList.remove("hide");
    }
  } else {
    const form = modal.querySelector("form");
    if (form.classList.contains("hide")) {
      form.classList.remove("hide");
    }
    const deleteElem = document.getElementById("delete");
    if (!deleteElem.classList.contains("hide")) {
      deleteElem.classList.add("hide");
    }
    modal.querySelector("form .button").onclick = submitEvent;
  }

  const closeModal = function() {
    questions[questionData.id].inputValue = modal.querySelector(
      "[name=answer]"
    ).value.toString();
    modal.querySelector("[name=value]").classList.remove("solved");
    modal.classList.remove("solved");
    modal.querySelector("[name=value]").classList.remove("pending");
    modal.classList.remove("pending");
    answerSubmissionEnable();

    modal.querySelector("form").removeEventListener("submit", submitEvent);
    modal
      .querySelector("button.cancel")
      .removeEventListener("click", cancelEvent);
    modal
      .querySelector(".modal-background")
      .removeEventListener("click", cancelEvent);
    modal.classList.remove("is-active");
  };

  const cancelEvent = closeModal;

  modal.querySelector("[name=value]").innerText = questionData.value.toString();

  modal.querySelector("form").addEventListener("submit", submitEvent);
  modal.querySelector("button.cancel").addEventListener("click", cancelEvent);
  modal
    .querySelector(".modal-background")
    .addEventListener("click", cancelEvent);
  modal.classList.add("is-active");
}

function reloadListenerSpecial() {
  let modal = document.getElementById("questionModalSpecial");
  if (modal.classList.contains("active")) {
    modal
      .querySelector("button.cancel")
      .addEventListener("click", location.reload);
    modal
      .querySelector(".modal-background")
      .addEventListener("click", location.reload);
  } else {
    location.reload();
  }
}

function dataToTile(data) {
  let tile = document.createElement("article");
  tile.classList.toggle("solved", solves.has(data.id));
  tile.classList.add("tile", "is-child", "notification", "is-3");

  let title = document.createElement("h1");
  title.classList.add("title");
  title.innerText = data.title;
  tile.appendChild(title);

  let category = document.createElement("h2");
  tile.category = category.innerText = categories[data.category] || "";
  tile.appendChild(category);

  let points = document.createElement("h3");
  tile.points = points.innerText = data.value;
  tile.appendChild(points);

  tile.addEventListener("click", function() {
    openModalQuestion(data, this);
  });

  return tile;
}

function dataToTileSpecial(data) {
  let tile = document.createElement("article");
  tile.classList.toggle("solved", solves.has(data.id));
  tile.classList.toggle("pending", pending.has(data.id));
  tile.classList.add("tile", "is-child", "notification", "is-3");

  let title = document.createElement("h1");
  title.classList.add("title");
  title.innerText = data.title;
  tile.appendChild(title);

  let category = document.createElement("h2");
  tile.category = category.innerText = categories[data.category] || "";
  tile.appendChild(category);

  let points = document.createElement("h3");
  tile.points = points.innerText = data.value;
  tile.appendChild(points);

  tile.addEventListener("click", function() {
    openModalQuestionSpecial(data, this);
  });

  return tile;
}

Promise.all([getQuestions(), getCategories(), getSolves(), getPending()]).then(
  ([questionsData, categoriesData, solvesData, pendingData]) => {
    if (categoriesData.status) {
      for (let data of categoriesData.data || []) {
        categories[data[0]] = data[1];
      }
    }

    if (solvesData.status && solvesData.data) {
      solves = solvesData.data;
    }

    if (pendingData.status && pendingData.data) {
      pending = pendingData.data;
    }

    if (questionsData.status) {
      questionsData.data.sort((o1, o2) => o1[4] - o2[4]);
      for (let data of questionsData.data || []) {
        questions[data[0]] = {
          id: data[0],
          title: data[1],
          description: data[2],
          value: data[3],
          category: data[4],
          type: data[5]
        };
        if (!questionsByCategory.hasOwnProperty(data[4])) {
          questionsByCategory[data[4]] = [];
          questionsByCategory[data[4]].push(data[0]);
        }
        if (data[5] === 0) {
          document
          .querySelector("div.tile.is-ancestor .is-parent")
          .appendChild(dataToTile(questions[data[0]]));
        } else if (data[5] === 1) {
          document
          .querySelector("div.tile.is-ancestor .is-parent")
          .appendChild(dataToTileSpecial(questions[data[0]]));
        }
        
      }

      iso = new Isotope(
        document.querySelector("div.tile.is-ancestor .is-parent"),
        {
          getSortData: {
            points: elem => elem.points,
            category: elem => elem.category
          },
          stagger: 10
        }
      );

      document
        .getElementById("filterComplete")
        .addEventListener("change", function() {
          iso.arrange({ filter: this.checked ? ":not(.solved)" : "*" });
        });

      document.getElementById("sort").addEventListener("change", function() {
        let [key, sortAsc] = this.value.split("_");
        iso.arrange({ sortBy: key, sortAscending: sortAsc == "asc" });
      });
    }
  }
);
