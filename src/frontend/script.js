let students = [];
let hall = {
    rows: 0,
    cols: 0
};

function createHall() {

    hall.rows = parseInt(document.getElementById("rows").value);
    hall.cols = parseInt(document.getElementById("cols").value);

    alert(`Hall Created: ${hall.rows} x ${hall.cols}`);
}

function addStudent() {

    const name = document.getElementById("studentName").value;
    const requirement = document.getElementById("requirement").value;

    if (name.trim() === "") {
        alert("Enter student name");
        return;
    }

    students.push({
        name: name,
        requirement: requirement
    });

    displayStudents();

    document.getElementById("studentName").value = "";
}

function displayStudents() {

    const list = document.getElementById("studentList");

    list.innerHTML = "";

    students.forEach((student, index) => {

        const li = document.createElement("li");

        li.innerHTML = `
            <strong>${student.name}</strong>
            <br>
            Requirement:
            ${student.requirement || "None"}
        `;

        list.appendChild(li);
    });
}

function generateSeating() {

    const grid = document.getElementById("hallGrid");

    grid.innerHTML = "";

    grid.style.gridTemplateColumns =
        `repeat(${hall.cols}, 1fr)`;

    // Create empty hall
    let seats = [];

    for (let r = 0; r < hall.rows; r++) {

        seats[r] = [];

        for (let c = 0; c < hall.cols; c++) {
            seats[r][c] = null;
        }
    }

    // Place students according to requirement
    students.forEach(student => {

        let placed = false;

        // FRONT ROW
        if (student.requirement === "front_row") {

            for (let c = 0; c < hall.cols; c++) {

                if (seats[0][c] === null) {

                    seats[0][c] = student;
                    placed = true;
                    break;
                }
            }
        }

        // BACK ROW
        else if (student.requirement === "back_row") {

            let lastRow = hall.rows - 1;

            for (let c = 0; c < hall.cols; c++) {

                if (seats[lastRow][c] === null) {

                    seats[lastRow][c] = student;
                    placed = true;
                    break;
                }
            }
        }

        // WHEELCHAIR (aisle seats)
        else if (student.requirement === "wheelchair") {

            for (let r = 0; r < hall.rows; r++) {

                if (seats[r][0] === null) {

                    seats[r][0] = student;
                    placed = true;
                    break;
                }

                if (seats[r][hall.cols - 1] === null) {

                    seats[r][hall.cols - 1] = student;
                    placed = true;
                    break;
                }
            }
        }

        // NORMAL / EXTRA SPACE
        if (!placed) {

            for (let r = 0; r < hall.rows; r++) {

                for (let c = 0; c < hall.cols; c++) {

                    if (seats[r][c] === null) {

                        // Extra space logic
                        if (student.requirement === "extra_space") {

                            let leftEmpty =
                                c === 0 || seats[r][c - 1] === null;

                            let rightEmpty =
                                c === hall.cols - 1 ||
                                seats[r][c + 1] === null;

                            if (!(leftEmpty && rightEmpty)) {
                                continue;
                            }
                        }

                        seats[r][c] = student;
                        placed = true;
                        break;
                    }
                }

                if (placed) break;
            }
        }
    });

    // Display seats
    for (let r = 0; r < hall.rows; r++) {

        for (let c = 0; c < hall.cols; c++) {

            const seat = document.createElement("div");

            seat.classList.add("seat");

            if (seats[r][c]) {

                const student = seats[r][c];

                seat.innerHTML = `
                    ${student.name}
                    <br>
                    <small>${student.requirement || ""}</small>
                `;

                if (student.requirement === "front_row") {
                    seat.classList.add("front-row");
                }

                if (student.requirement === "back_row") {
                    seat.classList.add("front-row");
                }

                if (student.requirement === "wheelchair") {
                    seat.classList.add("wheelchair");
                }

                if (student.requirement === "extra_space") {
                    seat.classList.add("extra-space");
                }

            } else {

                seat.innerHTML = "Empty";
                seat.classList.add("empty");
            }

            grid.appendChild(seat);
        }
    }
}