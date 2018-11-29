Array.prototype.has = function (obj) {
    return this.indexOf(obj) > -1
};

function openModalQuestion(questionData, srcElem) {
    let modal = document.getElementById('questionModal');
    modal.classList.toggle('solved', solves.has(questionData.id));

    getSolves(questionData.id)
        .then(jsonData => {
            if (jsonData.status) {
                modal.querySelector('[name=solves]').innerText = jsonData.data;
            }
        });

    modal.querySelector("[name=flag]").value = questions[questionData.id].inputValue || "";
    modal.querySelector("[name=flag]").placeholder = "FLAG{...}";
    modal.querySelector('[name=title]').innerText = questionData.title;
    modal.querySelector('[name=category]').innerText = categories[questionData.category] || "";
    modal.querySelector('[name=description]').srcdoc = "<link rel='stylesheet' href='/assets/css/iframe.sandbox.css'/>" + questionData.description; // XSS AWAY

    modal.querySelector('form .button').onclick = () => {
        modal.querySelector("[name=flag]").form.dispatchEvent(new Event('submit'))
    };

    const flagSubmissionDisable = function () {
        modal.querySelector('form .input').disabled = true;
        modal.querySelector('form .button').disabled = true;
    };

    const flagSubmissionEnable = function () {
        modal.querySelector('form .input').disabled = false;
        modal.querySelector('form .button').disabled = false;
    };

    const submitEvent = function (evt) {
        evt.preventDefault();

        if (!modal.querySelector("[name=flag]").value.trim()) return;

        modal.querySelector('form').removeEventListener('submit', submitEvent);
        flagSubmissionDisable();
        modal.querySelector('form .button').classList.add('is-loading');

        let flagValue = modal.querySelector("[name=flag]").value.trim();
        trySolve(questionData.id, flagValue)
            .then(jsonData => {
                modal.querySelector('form .button').classList.remove('is-loading');
                flagSubmissionEnable();
                modal.querySelector('form').addEventListener('submit', submitEvent);

                if (jsonData.status) {
                    modal.querySelector("[name=flag]").placeholder = "flag correct";
                    modal.querySelector("[name=flag]").value = "";
                    if (!solves.has(questionData.id)) {
                        solves.push(questionData.id);
                        modal.querySelector('[name=solves]').innerText = parseInt(modal.querySelector('[name=solves]').innerText) + 1;
                        updateLeaderboard();
                    }
                    modal.querySelector('[name=value]').classList.add('solved');
                    srcElem.classList.add('solved');
                } else {
                    modal.querySelector("[name=flag]").placeholder = flagValue + " was not right!";
                    modal.querySelector("[name=flag]").value = "";
                }
            })
    };

    const closeModal = function () {
        questions[questionData.id].inputValue = modal.querySelector("[name=flag]").value;
        modal.querySelector('[name=value]').classList.remove('solved');
        modal.classList.remove('solved');
        flagSubmissionEnable();

        modal.querySelector('form').removeEventListener('submit', submitEvent);
        modal.querySelector('button.cancel').removeEventListener('click', cancelEvent);
        modal.querySelector('.modal-background').removeEventListener('click', cancelEvent);
        modal.classList.remove('is-active');
    };

    const cancelEvent = closeModal;


    modal.querySelector('[name=value]').innerText = questionData.value;

    modal.querySelector('form').addEventListener('submit', submitEvent);
    modal.querySelector('button.cancel').addEventListener('click', cancelEvent);
    modal.querySelector('.modal-background').addEventListener('click', cancelEvent);
    modal.classList.add('is-active');
}


function dataToTile(data) {
    let tile = document.createElement('article');
    tile.classList.toggle('solved', solves.has(data.id));
    tile.classList.add("tile", "is-child", "notification", "is-3");

    let title = document.createElement('h1');
    title.classList.add("title");
    title.innerText = data.title;
    tile.appendChild(title);

    let category = document.createElement('h2');
    category.innerText = categories[data.category] || "";
    tile.appendChild(category);

    let points = document.createElement('h3');
    points.innerText = data.value;
    tile.appendChild(points);

    tile.addEventListener('click', function () {
        openModalQuestion(data, this)
    });

    return tile
}

Promise.all([getQuestions(), getCategories(), getSolves()])
    .then(([questionsData, categoriesData, solvesData]) => {
        if (categoriesData.status) {
            for (let data of categoriesData.data || []) {
                categories[data[0]] = data[1];
            }
        }

        if (solvesData.status && solvesData.data) {
            solves = solvesData.data;
        }

        if (questionsData.status) {
            for (let data of questionsData.data || []) {
                questions[data[0]] = {
                    id: data[0],
                    title: data[1],
                    description: data[2],
                    value: data[3],
                    category: data[4],
                };
                if (!questionsByCategory.hasOwnProperty(data[4])) {
                    questionsByCategory[data[4]] = [];

                    questionsByCategory[data[4]].push(data[0]);
                }
                document.querySelector('div.tile.is-ancestor .is-parent').appendChild(dataToTile(questions[data[0]]));
            }
        }
    });